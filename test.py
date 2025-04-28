# # from selenium import webdriver
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
# from selenium.webdriver.support import expected_conditions as ec

# browser=uc.Chrome()
# browser.get('https://www.skyscanner.co.in/transport/flights/HYD/BOM/20250208/')
# hold='#root > div > div:nth-child(2) > div.flightBody > div.overlay > div > div > div.makeFlex.hrtlCenter.right > button'
# WebDriverWait(browser,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,hold))).click()
# browser.clickAndHold((By.CSS_SELECTOR,hold))
#root > div > div:nth-child(2) > div.flightBody > div.overlay > div > div > div.makeFlex.hrtlCenter.right > button
import random
from selenium import webdriver
from fake_useragent import UserAgent

# Define your list of proxies
proxies = [
    "http://157.254.53.50:80",
    "http://32.223.6.94:80",
    "http://50.202.75.26:80",
    "http://50.232.104.86:80",
    "http://50.175.212.66:80",
    "http://50.217.226.47:80",
    "http://50.239.72.16:80",
    "http://50.221.74.130:80",
    "http://189.202.188.149:80",
    "http://50.174.7.152:80",
    "http://103.152.112.120:80",
    "http://194.182.178.90:3128"
]

def get_driver():
    # Pick a random proxy from the list
    proxy = random.choice(proxies)
    
    # Create a random user-agent
    ua = UserAgent()
    random_ua = ua.random

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={random_ua}")
    options.add_argument(f"--proxy-server={proxy}")
    # Exclude the "enable-automation" switch and disable the automation extension.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Optionally, disable some blink features that can reveal automation
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    return driver

# Use the driver
driver = get_driver()
driver.get("https://www.skyscanner.co.in/transport/flights/HYD/BOM/20250208/")  # This site can show you your current IP and user-agent
time.sleep(100)