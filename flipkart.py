import requests
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

from bs4 import BeautifulSoup
import time

def scrape_flipkart(product_name):
    flipkart_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
    options1 = webdriver.ChromeOptions()
    options1.add_argument("--headless")
    options1.add_argument('--ignore-certificate-errors')  # Ignores SSL errors
    options1.add_argument('--ignore-ssl-errors')  # Ignores SSL handshake errors
    options1.add_argument('--disable-web-security')   
    driver1 = webdriver.Chrome(options=options1)

    driver1.get(flipkart_url)
    search_element=product_name.lower().split()
    soup = BeautifulSoup(driver1.page_source, 'html.parser')
    # Find all product names 
    products = []
    prices = []
    links=[]
    items=soup.select("div.tUxRFH")
    if not items:
        items=soup.select("div.slAVV4")
    for item in items:
        product=item.select_one("div.KzDlHZ") or item.select_one("a.wjcEIp")
        price=item.select_one("div.Nx9bqj._4b5DiR") or item.select_one("div.Nx9bqj")
        product_text=product.text.strip().lower()
        price_text=price.text
        link1=item.select_one("a.CGtC98") or item.select_one("a.wjcEIp")
        href = link1['href'] if link1 and link1.has_attr('href') else None
        product_link = f"https://www.flipkart.com{href}" if href else None
        # link = item.select_one("img.DByuf4")
        # if not link:
            # print("wrong css selector")
        # img_link = link.get('src') if link and link.has_attr('src') else None
        # print(item.prettify())
        # product_link=link['href']
        # print(product_text+" "+price_text)
        if product_text and price_text:
            if product_text[-3:]=="...":
                driver1.get(product_link)
                time.sleep(1.5)
                try:
                    full_name = driver1.find_element(By.CLASS_NAME, "VU-ZEz").text.strip().lower()
                except Exception:
                    full_name = product_text 
            else:
                full_name = product_text
            
            if all(word in full_name for word in search_element):
            # print(product.text.strip())
                products.append(product.text.strip())
                prices.append(price_text)
                # links.append(img_link)
        

    driver1.quit()
    pd.set_option('display.max_colwidth', None)


    
    # product_price_dict = zip(products, prices)
    
    # Create a Pandas DataFrame from the dictionary
    df = pd.DataFrame(zip(products, prices), columns=['Product Name', 'Price'])
    if df.empty:
        print("df is empty")
    else:print(df.head())
    

scrape_flipkart("lg 6-in-1 ac")