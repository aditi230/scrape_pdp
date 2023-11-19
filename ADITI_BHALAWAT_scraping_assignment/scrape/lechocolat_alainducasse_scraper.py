from scrape.scraper_base import ScraperBase
import json


class LeChocolatAlainDucasseScraper(ScraperBase):
    def __init__(self):
        super().__init__('https://www.lechocolat-alainducasse.com/uk/')

    def scrape(self):
        super().scrape()
        site_menu = self.soup.find("ul", class_="siteMenu js-menu")
        menu_links = self.extract_menu_links(site_menu)

        # Initialize a dictionary to store data for each link
        all_data = {}

        # Visit and parse each link
        for link in menu_links:
            products_data = self.visit_and_parse(link)
            all_data[link] = products_data

        # Write the data to a JSON file
        with open("output/lechocolat_data.json", "w") as json_file:
            json.dump(all_data, json_file, indent=2)

        print("Data has been successfully written to 'lechocolat_data.json'.")

    def extract_menu_links(self, menu_item):
        links = set()
        for li in menu_item.find_all("li", class_="siteMenuItem"):
            a_tag = li.find("a", class_="siteMenuItem__link")
            link = a_tag.get("href")
            if link:
                links.add(link)
        return links

    def visit_and_parse(self, link):
        super().__init__(link)
        super().scrape()
        # Select the section containing the product list
        product_list_section = self.soup.find('section', {'id': 'js-product-list', 'class': 'products__list'})

        # Initialize a list to store product data
        products_data = []

        # Iterate through each div with the specified format
        for product_div in product_list_section.find_all('div', class_='productMiniature js-product-miniature'):
            # Extract product details
            product_name = self.get_text_or_default(product_div.select_one('.productMiniature__name h2.productMiniature__title'))
            product_subtitle = self.get_text_or_default(product_div.select_one('.productMiniature__name h2.productMiniature__title small'))
            product_weight = self.get_text_or_default(product_div.select_one('.productMiniature__subtitle .productMiniature__weight'))
            product_price = self.get_text_or_default(product_div.select_one('.productMiniature__prices .productMiniature__price'))
            product_image_url = product_div.select_one('.productMiniature__thumbnails img')['src']

            # Extract data from the script tag
            script_tag = product_div.select_one('.product-data-ga4')
            script_data = json.loads(script_tag.text) if script_tag else {}

            # Create a dictionary for the current product
            product_data = {
                "Product Name": product_name,
                "Product Subtitle": product_subtitle,
                "Product Weight": product_weight,
                "Product Price": product_price,
                "Product Image URL": product_image_url,
                **script_data
            }

            # Append the product data to the list
            products_data.append(product_data)

        return products_data

    def get_text_or_default(self, element, default="N/A"):
        return element.get_text(strip=True) if element else default
