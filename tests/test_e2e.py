from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time

def test_browser_launch():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://weathershopper.pythonanywhere.com/")
    heading = driver.find_element(By.XPATH, '//h2[text()="Current temperature"]')
    assert heading.is_displayed()

    
    temp_element = wait.until(
        EC.visibility_of_element_located((By.ID, "temperature"))
    )

    assert temp_element.is_displayed()

    temp_text = temp_element.text
    value = int(re.search(r'\d+', temp_text).group())
    print("Temp:",value)
    
    if value <= 25:
        print("Buy moisturizers")
        driver.find_element(By.XPATH,'//button[text()="Buy moisturizers"]').click()
        category = "Moisturizers"
    elif value > 25:
        print("Buy sunscreens")
        driver.find_element(By.XPATH,'//button[text()="Buy sunscreens"]').click()
        category = "Sunscreens"
    heading_text = driver.find_element(By.TAG_NAME, "h2").text
    print("Heading text:",heading_text)
    assert category in heading_text

    products = driver.find_elements(By.CLASS_NAME, "text-center")
    prices = []
    product_map = {}

    for product in products:
        name = product.find_element(By.XPATH, './/p[contains(@class,"font-weight-bold")]').text
        price_text = product.find_element(By.XPATH, ".//p[contains(text(),'Price')]").text
        price = int(re.search(r'\d+', price_text).group())

        add_btn = product.find_element(By.TAG_NAME, "button")

        prices.append(price)
        product_map[price] = {
            "name": name,
            "button": add_btn
        }
    
    min_price = min(prices) 
    max_price = max(prices)
    expected_total = min_price + max_price
    print("Expected total in cart:", expected_total)

    print(min_price, max_price)


    product_map[min_price]["button"].click()
    product_map[max_price]["button"].click()

    cart_items_added = [
        product_map[min_price]["name"],
        product_map[max_price]["name"]
    ]

    print("Items added:", cart_items_added)

    driver.find_element(By.CSS_SELECTOR, ".thin-text.nav-link").click()
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "table")))

    cart_items = driver.find_elements(By.XPATH, "//table/tbody/tr") 

    cart_product_names = []
    for item in cart_items:
        name = item.find_element(By.XPATH, "./td[1]").text
        cart_product_names.append(name)

    print("Cart items:", cart_product_names)
    print("Cart count:",len(cart_items))

    assert len(cart_items) == 2
    for expected_item in cart_items_added:
        assert expected_item in cart_product_names, f"{expected_item} not found in cart"

    total_value = driver.find_element(By.ID, "total").text
    print(total_value)
    total_inCart = int(re.search(r'\d+', total_value).group())

    assert (expected_total == total_inCart)
    
    driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

    driver.switch_to.frame(driver.find_element(By.CLASS_NAME, "stripe_checkout_app"))
    wait.until(EC.visibility_of_element_located((By.ID, "email")))
    
    driver.find_element(By.ID, "email").send_keys("test@test.com") 
    driver.find_element(By.ID, "email").send_keys(Keys.TAB)

    card_number_field = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='card_number']"))
    )
    card_number_field.click()
    for digit in "4242424242424242":
        card_number_field.send_keys(digit)
        time.sleep(0.1)
    
    
    expiry_field = driver.find_element(By.XPATH, "//input[@id='cc-exp']")
    expiry_field.click()
    for date in "12/26":
        expiry_field.send_keys(date)
    
    
    cvc_field = driver.find_element(By.XPATH, "//input[@id='cc-csc']")
    cvc_field.click()
    cvc_field.send_keys("123")
    
    cvc_field.send_keys(Keys.TAB)
    postal_field = driver.find_element(By.XPATH, "//input[@id='billing-zip']")
    postal_field.click()
    postal_field.send_keys("12345")   
    driver.find_element(By.ID, "submitButton").click()
    driver.switch_to.default_content()
    confirmation = wait.until(EC.presence_of_element_located((By.XPATH,"//h2[text()='PAYMENT SUCCESS']")))
    print("Confirmation page reached:", confirmation.text)
    assert confirmation.is_displayed()
    driver.quit()
    
    