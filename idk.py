from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
def scrape_zepto(product_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = f"https://www.zepto.com/search?query={product_name.replace(' ', '+')}"
        driver.get(url)
        search_keywords = product_name.lower().split()

        # Scroll to load lazy-loaded items
        for scroll in range(3):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="product-card"]'))
        )

        products = []
        quantities = []
        prices = []
        images = []

        cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-card"]')

        for card in cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, '[data-testid="product-card-name"]').text.strip()
                name_text = name.lower()

                quantity = card.find_element(By.CSS_SELECTOR, '[data-testid="product-card-quantity"]').text.strip()
                price = card.find_element(By.CSS_SELECTOR, '[data-testid="product-card-price"]').text.strip()
                
                try:
                    
                    product_link = card.get_attribute("href")
                    
                except:
                    product_link = "N/A"
                img_tag=card.find_element(By.CSS_SELECTOR,'[data-testid="product-card-image"]')
                img_link = img_tag.get_attribute("src") if img_tag else "N/A"

                print(img_link)
                if name and price and all(word in name_text for word in search_keywords):
                    products.append(f'<a href="{product_link}" target="_blank">{name}</a>')
                    quantities.append(quantity)
                    prices.append(price)
                    images.append(img_link)

            except Exception as inner_e:
                print(f"Skipping card due to error: {inner_e}")

        driver.quit()

        if not products:
            print("No products found.")
            return None

        df = pd.DataFrame(zip(images, products, quantities, prices), columns=['Image','Product', 'Quantity', 'Price'])
        df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="100">' if x else '')
        print(df.head())
        return df

    except Exception as e:
        driver.quit()
        print(f"An error occurred: {e}")
scrape_zepto("tomato")