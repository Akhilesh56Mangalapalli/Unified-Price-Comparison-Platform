from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def solve_skyscanner_captcha(driver):
    try:
        # Check for CAPTCHA iframe and switch to it if present
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='captcha']"))
            )
            driver.switch_to.frame(iframe)
        except:
            pass  # No iframe, proceed normally

        # Locate CAPTCHA slider using a more flexible CSS selector
        slider = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class*='captcha'] button, .slider-button"))
        )
        
        # Simulate click, hold, move, and release for slider interaction
        actions = ActionChains(driver)
        actions.click_and_hold(slider).pause(1)
        
        # Adjust movement based on your observations (e.g., 200px horizontally)
        actions.move_by_offset(200, 0).pause(2)
        actions.release().perform()

        # Wait for confirmation (adjust condition as needed)
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".captcha-container"))
        )
        
        # Switch back to default content if iframe was used
        driver.switch_to.default_content()
        return True

    except Exception as e:
        print(f"CAPTCHA Error: {str(e)}")
        driver.switch_to.default_content()
        return False

def scrape_skyscanner():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://www.skyscanner.com")
        
        # Trigger CAPTCHA if necessary (e.g., by performing searches)
        # ...
        
        if not solve_skyscanner_captcha(driver):
            raise Exception("CAPTCHA resolution failed")
        
        # Continue with scraping
        # ...

    finally:
        driver.quit()

# Execute the scraper
scrape_skyscanner()