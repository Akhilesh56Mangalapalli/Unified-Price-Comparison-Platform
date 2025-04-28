from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotVisibleException,ElementNotSelectableException,StaleElementReferenceException
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import json
import random
import pandas as pd

# chrome_options = Options()
chrome_options = uc.ChromeOptions()
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
]
chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Attempt to bypass bot detection
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # 1=allow, 2=block
    "profile.default_content_setting_values.geolocation": 2     # 1=allow, 2=block
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the Driver
driver = uc.Chrome(options=chrome_options)
# driver2 = uc.Chrome(options=chrome_options)
driver.maximize_window()
actions = ActionChains(driver)
def search_movie_on_bookmyshow():
    try:
        url = "https://in.bookmyshow.com/buytickets/court-state-vs-a-nobody-hyderabad/movie-hyd-ET00432575-MT/20250412"
        driver.get(url)
        time.sleep(5)
        venues = driver.find_elements(By.CSS_SELECTOR,"sc-e8nk8f-3.iFKUFD")
        for venue in venues:
            wait = WebDriverWait(driver, 10)
            elements = wait.until(EC.presence_of_all_element_located((By.CSS_SELECTOR, 'sc-1vhizuf-0.dqVIoM')))

    # Hover over the element
            for element in elements:
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()

        # Wait for the tooltip to appear
                tooltip = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'sc-1vhizuf-5.iPJvdd')))

        # Scrape tooltip text
                print("Tooltip text:", tooltip.text)

# Optional: Pause if you want to keep it hovered for 5 seconds
        time.sleep(5)
    except Exception as e:
        print(e)
    except TimeoutException:
        print("Timeout Exception")
    except StaleElementReferenceException:
        print("Stale Element Reference Exception")
    except NoSuchElementException:
        print("No Such Element Exception")
    
    finally:
        driver.quit()

search_movie_on_bookmyshow()