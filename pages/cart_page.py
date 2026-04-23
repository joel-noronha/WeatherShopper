import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import Locators


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_cart(self):
        self.driver.find_element(*Locators.CART_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(Locators.CART_ROWS))

    def get_cart_items(self):
        cart_product_names = []
        cart_items = self.driver.find_elements(*Locators.CART_ROWS)
        for item in cart_items:
            name = item.find_element(*Locators.ITEM_NAME).text
            cart_product_names.append(name)
        return cart_product_names
        

    def get_total(self):
        total = self.driver.find_element(*Locators.TOTAL).text
        return int(re.search(r'\d+', total).group())

    def checkout(self):
        self.driver.find_element(*Locators.CHECKOUT_BTN).click()
    
    def complete_payment(self):
        self.driver.switch_to.frame(
            self.driver.find_element(*Locators.FRAME)
        )

        self.wait.until(EC.visibility_of_element_located(Locators.EMAIL))
        self.driver.find_element(*Locators.EMAIL).send_keys("test@test.com")
        for digit in "4242424242424242":
            self.driver.find_element(*Locators.CARD).send_keys(digit)
            time.sleep(0.1)
        
        for date in "12/26":
            self.driver.find_element(*Locators.EXPIRY).send_keys(date)
        
        self.driver.find_element(*Locators.CVC).send_keys("123")
        self.driver.find_element(*Locators.ZIP).send_keys("12345")

        self.driver.find_element(*Locators.SUBMIT).click()
        self.driver.switch_to.default_content()

    def get_payment_status(self):
        try:
            self.wait.until(EC.visibility_of_element_located(Locators.SUCCESS))
            return "success"
        except:
            return "failed"