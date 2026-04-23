import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import Locators

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_temperature(self):
        try:
            temp = self.wait.until(EC.visibility_of_element_located(Locators.TEMPERATURE)).text
            temp_value = int(re.search(r'\d+', temp).group())
            if temp_value < -50 or temp_value > 100:
                raise AssertionError(f"Invalid temperature from UI: {temp}")
            return temp_value
        except TimeoutException:
            raise AssertionError("Temperature not displayed on homepage")

    

    def choose_category(self, temp):
        if temp <= 25:
            self.driver.find_element(*Locators.BUY_MOISTURIZER).click()
            return "Moisturizers"
        else:
            self.driver.find_element(*Locators.BUY_SUNSCREEN).click()
            return "Sunscreens"