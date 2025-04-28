from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import json
import random
import pandas as pd

# 2Captcha API Key (uncomment and add if needed later)
# CAPTCHA_API_KEY = "your_2captcha_api_key"

def solve_skyscanner_captcha(driver):
    try:
        # Wait for the parent section with the unique identifier to appear
        parent_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section[@class='App_App__captcha__NTllM']"))
        )
        print(parent_section)
        # Look for iframes on the page
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(iframes)
        if not iframes:
            print("No iframes found on the page.")
            return False

        # Try switching to each iframe to find the CAPTCHA button
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                print("switched to iframe")
                
                # Wait for the CAPTCHA button within the iframe
                captcha_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='button']"))
                )
                
                # Simulate the press and hold action
                actions = ActionChains(driver)
                actions.click_and_hold(captcha_element).perform()
                time.sleep(10)  # Hold for 10 seconds, adjust if necessary
                actions.release().perform()
                
                # Wait for the CAPTCHA to be solved or for the page to proceed
                # Check if the CAPTCHA element is no longer visible or if the page changes
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element(captcha_element)
                )
                
                # Switch back to the default content
                driver.switch_to.default_content()
                return True  # CAPTCHA solved
            except Exception as e:
                print(f"Error in iframe {iframe}: {e}")
                # Switch back to default content if an error occurs in this iframe
                driver.switch_to.default_content()
                continue

        print("CAPTCHA button not found in any iframe.")
        return False

    except Exception as e:
        print(f"Failed to solve CAPTCHA: {e}")
        # Ensure we switch back to default content in case of exception
        driver.switch_to.default_content()
        return False

def scrape_skyscanner():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    ]
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode if needed
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Attempt to bypass bot detection
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = "https://www.skyscanner.co.in/transport/flights/HYD/BOM/20250221/"
        driver.get(url)
        time.sleep(10)
        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, ".App_App__headline__OGFkN"))
        )

        # Solve the CAPTCHA
        if not solve_skyscanner_captcha(driver):
            print("CAPTCHA solving failed, exiting.")
            return None

        # Now scrape flight information
        # flights = []
        # flight_elements = driver.find_elements(By.CLASS_NAME, "day-view")  # Adjust class name if different
        # for flight in flight_elements:
        #     # Extract price and flight details - this is highly dependent on Skyscanner's HTML structure
        #     try:
        #         price = flight.find_element(By.CLASS_NAME, "price").text
        #         airline = flight.find_element(By.CLASS_NAME, "airline-name").text
        #         duration = flight.find_element(By.CLASS_NAME, "duration").text
        #         flights.append({
        #             "price": price,
        #             "airline": airline,
        #             "duration": duration
        #         })
        #     except:
        #         # Skip flights where we can't find all details
        #         continue

        # return flights

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()

# Run the scraper
# results = 
scrape_skyscanner()
# if results:
#     # Convert the list of dictionaries to a pandas DataFrame
#     df = pd.DataFrame(results)
#     print(df)
#     # Optionally, save to CSV
#     df.to_csv('skyscanner_flights.csv', index=False)
# else:
#     print("No results or an error occurred.")