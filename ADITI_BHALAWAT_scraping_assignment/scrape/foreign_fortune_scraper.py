from scrape.scraper_base import ScraperBase
import json

class ScraperValidator:
    @staticmethod
    def validate_product_info(product_info):
        errors = []

        # Sale price should be less than or equal to original price
        if product_info.get("sale_prices") and product_info.get("price") and product_info["sale_prices"][0] > product_info["price"]:
            errors.append("Sale price is greater than the original price.")

        # Mandatory fields: title, product_id
        mandatory_fields = ["title", "product_id"]
        for field in mandatory_fields:
            if not product_info.get(field):
                errors.append(f"{field} is a mandatory field and is missing.")

        # Validate each model
        for model in product_info.get("models", []):
            if not model.get("variants"):
                errors.append(f"Model '{model.get('color', 'N/A')}' is missing variant information.")
            else:
                for variant in model["variants"]:
                    # Each variant should have an image and a price
                    if not variant.get("image"):
                        errors.append(f"Variant '{variant.get('size', 'N/A')}' in model '{model.get('color', 'N/A')}' is missing images.")
                    if not variant.get("price"):
                        errors.append(f"Variant '{variant.get('size', 'N/A')}' in model '{model.get('color', 'N/A')}' is missing price.")

        return errors

class ForeignFortuneScraper(ScraperBase):
    BASE_URL = "https://foreignfortune.com"

    def __init__(self):
        super().__init__(self.BASE_URL)

    def scrape(self):
        super().scrape()
        menu_links = self.extract_menu_links()

        all_product_data = {}

        for link in menu_links:
            products_links = self.visit_and_parse(link)

            for product_link in products_links:
                product_data = self.extract_product_data(product_link)
                validation_errors = ScraperValidator.validate_product_info(product_data)

                if not validation_errors:
                    all_product_data[product_link] = product_data
                else:
                    print(f"Validation errors for product {product_link}:")
                    for error in validation_errors:
                        print(f"- {error}")

        if all_product_data:
            with open('output/foreign_fortune_data.json', 'w') as json_file:
                json.dump(all_product_data, json_file, indent=2)

    def visit_and_parse(self, link):
        product_links = []
        super().__init__(link)
        super().scrape()
        soup = self.soup
        max_page = self.extract_pagination_max_page(soup)
        product_links.extend(self.extract_product_links(soup))

        for i in range(2, max_page + 1):
            paginated_link = f"{link}?page={i}"
            super().__init__(paginated_link)
            super().scrape()
            next_page_soup = self.soup
            product_links.extend(self.extract_product_links(next_page_soup))

        return product_links

    def extract_menu_links(self):
        mobile_nav = self.soup.find('ul', class_='mobile-nav')
        return [f"{self.BASE_URL}{a['href']}" for a in mobile_nav.find_all('a', class_='mobile-nav__link')]

    def extract_product_links(self, soup):
        product_links = []
        parent_div = soup.find('div', class_='grid grid--uniform grid--view-items')

        if not parent_div:
            return product_links

        for product_card in parent_div.find_all('div', class_='grid-view-item product-card'):
            product_link = f"{self.BASE_URL}{product_card.select_one('.grid-view-item__link')['href']}"
            product_links.append(product_link)

        return product_links

    def extract_pagination_max_page(self, soup):
        pagination_text = soup.find('li', class_='pagination__text')
        if pagination_text:
            text_content = pagination_text.get_text(strip=True)
            return int(text_content.split()[-1])
        return 1

    def extract_image_links(self, photo_wrappers):
        return [f"{self.BASE_URL}{wrapper.find('div', class_='product-single__photo')['data-zoom'][2:]}" for wrapper in photo_wrappers]

    def extract_product_data(self, link):
        super().__init__(link)
        super().scrape()

        photo_wrappers = self.soup.find_all('div', class_='product-single__photo-wrapper')
        image_links = self.extract_image_links(photo_wrappers)

        product_price_element = self.soup.select_one('#ProductPrice-product-template')
        original_price = float(product_price_element.text.strip().replace('$', '').replace(',', '')) if product_price_element else None

        sale_price = float(self.soup.select_one('#ProductPrice-product-template').text.strip().replace('$', '').replace(',', '')) if self.soup.select_one('.product-price__sale-label-product-template') else None

        script_tag = self.soup.find('script', {'id': 'ProductJson-product-template'})
        script_content = script_tag.contents[0]
        product_data = json.loads(script_content)

        product_title = product_data['title']
        product_description = product_data['description']
        product_id = product_data['id']
        product_variants = product_data['variants']

        product_info = {
            "brand": "Foreign Fortune Collection",
            "description": product_description,
            "image": image_links[0] if image_links else None,
            "images": image_links,
            "models": [],
            "price": original_price,
            "prices": [original_price] if original_price else [],
            "sale_prices": [sale_price] if sale_price else [],
            "title": product_title,
            "url": link,
            "product_id": product_id
        }

        color_models = {}

        for variant in product_variants:
            variant_title = variant['title']
            variant_price = variant['price'] / 100
            variant_id = variant['id']

            variant_parts = variant_title.split("/")

            size = variant_parts[0].strip() if len(variant_parts) >= 1 else "N/A"
            color = variant_parts[1].strip() if len(variant_parts) >= 2 else "N/A"

            variant_info = {
                "id": variant_id,
                "image": image_links[0],
                "price": variant_price,
                "size": size
            }

            if color in color_models:
                color_models[color]["variants"].append(variant_info)
            else:
                color_models[color] = {
                    "color": color,
                    "variants": [variant_info]
                }

        product_info["models"] = list(color_models.values())

        return product_info