
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def scrape_amazon(product_name):
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)

    driver.get(amazon_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all product names 
    product_names  = soup.find_all("h2",class_="a-size-medium a-spacing-none a-color-base a-text-normal")  # Select product elements using Flipkart's CSS class
    #Nx9bqj _4b5DiR --price class
   
    prices_element  = soup.find_all("span",class_=["a-price-whole"])

    # price_element = soup.select_one(".a-price .a-offscreen")
    driver.quit() 

    products = []
    for product_name in product_names:
        product = product_name.text.strip()  # Extract and clean the price text
        products.append(product)


    prices = []
    for price_element in prices_element:
        price = price_element.text.strip()  # Extract and clean the price text
        prices.append(price)


    if products and prices:
        # Create a dictionary where product names are keys and prices are values
        product_price_dict = dict(zip(products, prices))
        
        # Create a Pandas DataFrame from the dictionary
        df = pd.DataFrame(list(product_price_dict.items()), columns=['Product Name', 'Price'])
        
        return df
    else:
        return {"Product not found": "Price not available"}, None
        

df = scrape_amazon("samsung galaxy s24 ultra")
print(df)
pd.set_option('display.max_colwidth', None)
if df is not None:
    print("\nProduct-Price DataFrame:")
    print(df.head())
