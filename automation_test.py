from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

DEMO_URL = "https://demoblaze.com/"
USERNAME = "ajay_885"
PASSWORD = "Subwaysurf0"
PRODUCT_CATEGORY = "Laptops"
PRODUCT_NAME = "MacBook Pro"
WAIT_TIMEOUT = 15

def safe_accept_alert(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        text = alert.text
        print("Alert found and accepting:", text)
        alert.accept()
        return text
    except Exception:
        return None

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    try:
        driver.get(DEMO_URL)
        print("Opened Demoblaze home page")
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login2")))
        login_btn.click()
        print("Login modal opened")
        wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))

        driver.find_element(By.ID, "loginusername").clear()
        driver.find_element(By.ID, "loginusername").send_keys(USERNAME)
        driver.find_element(By.ID, "loginpassword").clear()
        driver.find_element(By.ID, "loginpassword").send_keys(PASSWORD)

        driver.find_element(By.XPATH, "//button[text()='Log in']").click()
        print("Login submitted, waiting for success or alert...")

        alert_text = safe_accept_alert(driver, timeout=5)
        if alert_text:
            print("Login alert handled; continuing without being logged in.")
        else:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, "nameofuser")))
                name_element = driver.find_element(By.ID, "nameofuser")
                print("Login successful. Displayed user:", name_element.text)
            except Exception:
                print("No login confirmation found; proceeding anyway.")

        time.sleep(1)

        cat_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, PRODUCT_CATEGORY)))
        cat_link.click()
        print(f"Clicked category: {PRODUCT_CATEGORY}")
        product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, PRODUCT_NAME)))
        product_link.click()
        print(f"Opened product page: {PRODUCT_NAME}")

        add_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart")))
        add_btn.click()
        print("Clicked 'Add to cart' - waiting for confirmation alert...")

        add_alert_text = safe_accept_alert(driver, timeout=5)
        if add_alert_text:
            print("Add-to-cart alert accepted:", add_alert_text)
        else:
            print("No add-to-cart alert found; continuing.")

        cart_btn = wait.until(EC.element_to_be_clickable((By.ID, "cartur")))
        cart_btn.click()
        print("Navigated to cart page, verifying item presence...")

        wait.until(EC.presence_of_element_located((By.XPATH, "//tr/td[2]")))
        cart_items = driver.find_elements(By.XPATH, "//tr/td[2]")

        cart_product_names = [elem.text.strip() for elem in cart_items if elem.text.strip() != ""]
        print("Cart product names found:", cart_product_names)

        if any(PRODUCT_NAME in name for name in cart_product_names):
            print("✅ Test Passed: Product found in cart ->", PRODUCT_NAME)
        else:
            print("❌ Test Failed: Product NOT found in cart. Cart contents:", cart_product_names)


    except Exception as e:
        print("ERROR during test execution:", repr(e))
        raise
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
