from selenium import webdriver
from config.config import Config
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.json_reader import load_json

def test_e2e():
    data = load_json("testdata/data.json")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.get(Config.URL)

    home = HomePage(driver)
    products = ProductsPage(driver)
    cart = CartPage(driver)

    temp = home.get_temperature()
    category = home.choose_category(temp)
    heading = products.get_product_page_name()
    assert category in heading

    items, expected_total = products.add_min_max_products()

    cart.open_cart()

    cart_items = cart.get_cart_items()
    assert len(cart_items) == 2

    for item in items:
        assert item in cart_items

    assert cart.get_total() == expected_total

    cart.checkout()
    cart.complete_payment(data)

    status = cart.get_payment_status()
    assert status == "success"  

    driver.quit()