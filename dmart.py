from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Function to scrape DMart using Selenium
def scrape_dmart(product_name):
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('path/to/chromedriver')  # Update with the path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = f"https://www.dmart.in/search?search_term={product_name}"
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (adjust as needed)
        
        products = []  
        prices = []
        # Find elements using Selenium (update selectors based on DMart's structure)
        items = driver.find_elements(By.CSS_SELECTOR, '.vertical-card_card-vertical__Q8seS')[:5]  # Hypothetical selector
        for item in items:
            name = item.find_element(By.CSS_SELECTOR, 'div.vertical-card_title__pMGg9')  # Hypothetical selector
            price = item.find_element(By.CSS_SELECTOR, 'span.product-price')  # Hypothetical selector
            if name and price:
                products.append(name.text.strip())
                prices.append(price.text.strip())
        
        driver.quit()
        
        if not products:
            return None
        
        df = pd.DataFrame({'Product Name': products, 'Price': prices})
        return df.to_html(classes='data', index=True)
    except Exception as e:
        print(f"Error scraping DMart with Selenium: {e}")
        driver.quit()
        return None