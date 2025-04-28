from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import undetected_chromedriver as uc
from fake_useragent import UserAgent




def scrape_skyscrape(origin,destination,date):
    skyscanner_url = f'https://www.skyscanner.co.in/transport/flights/HYD/BOM/20250208/'
    # options1 = webdriver.ChromeOptions()
    ua = UserAgent()
    random_ua = ua.random 
    # options1.add_argument("--headless")  # Run Chrome in headless mode (no browser UI)
    options = uc.ChromeOptions()

    # options.add_argument("--headless")  # Run in headless mode if needed
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random_ua}")
    
    # Initialize the Chrome driver with options
    driver = uc.Chrome(options=options)
    driver.get(skyscanner_url)
    # WebDriverWait(driver,100).until(By.CSS_SELECTOR,'')
    
    
    # # Parse the page with BeautifulSoup
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)
   

    # # Find all product names 
    # product_names  = soup.find_all("div",class_="KzDlHZ")  # Select product elements using Flipkart's CSS class
    # #Nx9bqj _4b5DiR --price class
    # prices_element  = soup.find_all("div",class_="Nx9bqj _4b5DiR")

    

    # driver.quit()  

    # products = []
    # for product_name in product_names:
    #     product = product_name.text.strip()  # Extract and clean the price text
    #     products.append(product)
    

    # prices = []
    # for price_element in prices_element:
    #     price = price_element.text.strip()  # Extract and clean the price text
    #     prices.append(price)
    
    

    # if products and prices:
    #     # Create a dictionary where product names are keys and prices are values
    #     product_price_dict = dict(zip(products, prices))
        
    #     # Create a Pandas DataFrame from the dictionary
    #     df = pd.DataFrame(list(product_price_dict.items()), columns=['Product Name', 'Price'])
        
    #     return df
    # else:
    #     return {"Product not found": "Price not available"}, None




scrape_skyscrape("HYD","BOM",20250205)





# # Print the DataFrame of products and prices
# pd.set_option('display.max_colwidth', None)
# if df is not None:
#     print("\nProduct-Price DataFrame:")
#     print(df.head())
