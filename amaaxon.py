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


def scrape_amazon(product_name):
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)

    driver.get(amazon_url)
    search_keywords = product_name.lower().split()  # Convert search term into words

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Identify product containers
    # item_box = soup.select("div.a-section.a-spacing-small.a-spacing-top-small")
    item_box = soup.select("div.puisg-row")
    alt_item_box = soup.select("div.a-section.a-spacing-base") #or soup.select("div.a-section a-spacing-base")

    if len(item_box) < 3:
        item_box = alt_item_box  # Fallback selector

    products = []
    prices = []
    img_links=[]
    def extract_products(item_box, css_selector):
        for item in item_box:
            try:
                product_names = item.select_one(css_selector)
                product = product_names.text.strip() if product_names else None
                product_text = product.lower() if product else ""

                price = item.select_one("span.a-offscreen")
                price_text = price.text.strip() if price else None
                link=item.select_one("img.s-image")
                if not link:
                    print("links not fetched")
                img_link=link.get('src') if link and link.has_attr('src') else None
                print(img_link)

                # Check if all words in search query are in product name
                if product and price_text and img_link and all(word in product_text for word in search_keywords):
                    # products.append(f'<a href="{product_link}" target="_blank">{product}</a>')
                    products.append(product)
                    prices.append(price_text)
                    img_links.append(img_link)

            except NoSuchElementException as e:
                print(f"NoSuchElementFound: {e}")

            except AttributeError as e:
                print(f"Attribute Error: {e}")

            except Exception as e:
                print(f"Element Not Found:{e}")

    # Try Electronics Selector First
    extract_products(item_box, "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal")

    # If too few products, try Grocery Selector
    if len(products) < 3:
        products = []
        prices = []
        img_links=[]
        extract_products(item_box, "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal")

    # product_price_dict = zip(products, prices)
    # df = pd.DataFrame(list(product_price_dict.items()), columns=['Product Name', 'Price'])
    df = pd.DataFrame(zip(products, prices, img_links), columns=['Product Name', 'Price', 'Product_link'])

    pd.set_option('display.max_colwidth', None)
    print(df.head())

    
scrape_amazon("samsung s24 ultra")