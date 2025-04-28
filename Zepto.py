# Function to scrape Zepto
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
def scrape_zepto(product_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # service = Service('path/to/chromedriver')
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = f"https://www.zepto.com/search?query={product_name}"  # Update with the correct Zepto search URL
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        
        products = []
        quantity=[]
        prices = []
        search_element=product_name.lower().split()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        items = driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-card"]')  # Limit to top 5 products
        for item in items:
            # Extract product name
            name_element = item.find_element(By.CSS_SELECTOR, '[data-testid="product-card-name"]')
            name = name_element.text.strip() if name_element else "N/A"
            name_text=name.lower()
            qaun=item.find_element(By.CSS_SELECTOR,'[data-testid="product-card-quantity"]')
            q=qaun.text.strip() if qaun else "N/A"
            # Extract price
            price_element = item.find_element(By.CSS_SELECTOR, '[data-testid="product-card-price"]')
            price = price_element.text.strip() if price_element else "N/A"
            print(name)
            if name != "N/A" and price != "N/A" and q != "N/A" and all(word in name_text for word in search_element):
                products.append(name)
                prices.append(price)
                quantity.append(q)
        
        driver.quit()
        
        if not products:
            return None
        
        df = pd.DataFrame({'Product Name': products,'Quantity':quantity, 'Price': prices})
        # return df.to_html(classes='data', index=True)
        print(df)
    except Exception as e:
        print(f"Error scraping Zepto with Selenium: {e}")
        driver.quit()
        return None
    
scrape_zepto("heritage curd")