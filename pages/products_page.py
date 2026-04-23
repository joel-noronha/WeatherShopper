import re
from locators.locators import Locators

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
    
    def get_product_page_name(self):
        heading_text = self.driver.find_element(*Locators.PRODUCT_PAGE_HEADING).text
        return heading_text

    def add_min_max_products(self):
        products = self.driver.find_elements(*Locators.PRODUCTS)

        product_map = {}
        prices = []

        for product in products:
            name = product.find_element(*Locators.NAME).text
            price_text = product.find_element(*Locators.PRICE).text
            price = int(re.search(r'\d+', price_text).group())

            button = product.find_element(*Locators.ADD_BUTTON)

            product_map[price] = {"name": name, "button": button}
            prices.append(price)

        min_price = min(prices)
        max_price = max(prices)

        product_map[min_price]["button"].click()
        product_map[max_price]["button"].click()

        return (
            [product_map[min_price]["name"], product_map[max_price]["name"]],
            min_price + max_price
        )