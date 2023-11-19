from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import json

class TraderJoesScraper:

    def __init__(self):
        self.product_data = {}

    def scrape_product_page(self, driver):
        """
        Extracts product information from the Trader Joe's page and stores it in a dictionary.
        """
        products_text = driver.find_element(By.CLASS_NAME, "ProductList_productList__list__3-dGs").text
        product_entries = products_text.split("ADD TO LIST\n")

        for product_entry in product_entries:
            details = product_entry.strip().split('\n')

            if len(details) >= 3:
                self.product_data[details[1]] = {
                    "name":details[1],
                    "category": details[0],
                    "price": details[2].split('/')[0].replace("$", ""),
                    "quantity": details[2].split('/')[1]
                }
            else:
                print(f"Skipping invalid product entry: {product_entry}")

    def scrape_all_products(self, driver):
        """
        Logic for clicking the next page button and calling the scrape_product_page function when appropriate.
        """
        next_button_selector = ".Pagination_pagination__arrow__3TJf0.Pagination_pagination__arrow_side_right__9YUGr"

        while True:
            try:
                driver.execute_script("window.scrollTo(0, 3500);")

                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector))
                )

                self.scrape_product_page(driver)

                action = ActionChains(driver)
                action.move_to_element(next_button).pause(1).click().perform()

            except TimeoutException:
                self.scrape_product_page(driver)
                break

            except Exception as e:
                print(f"Error: {e}")
                break

    def scrape_and_store_data(self):
        """
        Orchestrates the process of scraping data from the Trader Joe's website and returns the data in the product_data dictionary.
        """
        self.product_data.clear()

        options = Options()
        options.page_load_strategy = 'normal'
        options.add_argument('--headless=new')

        driver = webdriver.Chrome(options=options)

        driver.set_window_size(880, 1080)
        driver.get("https://www.traderjoes.com/home/products/category/food-8")
        self.scrape_all_products(driver)
        driver.quit()
        return self.product_data

    def write_json_file(self):
        """
        Expects the dictionary format to be product name: (category, price, quantity) then converts the dictionary to a .json.
        """
        with open('output/trader_joes_data.json', 'w', encoding='utf-8') as file_output:
            json.dump(self.product_data, file_output, indent=2)

    def scrape(self):
        self.scrape_and_store_data()
        self.write_json_file()
