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

app = Flask(__name__)

# --- E-commerce Scraping Functions ---

# Function to scrape Flipkart
def scrape_flipkart(product_name):
    flipkart_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
    options1 = webdriver.ChromeOptions()
    options1.add_argument("--headless") 
    options1.add_argument('--ignore-certificate-errors')  # Ignores SSL errors
    options1.add_argument('--ignore-ssl-errors') 
    driver1 = webdriver.Chrome(options=options1)

    driver1.get(flipkart_url)
    time.sleep(3)
    search_keyword = product_name.lower().split()
    soup = BeautifulSoup(driver1.page_source, 'html.parser')
    # Find all product names 
    products = []
    prices = []
    img_links=[]
    items=soup.select("div.tUxRFH")
    if not items:
        items=soup.select("div.slAVV4")
    for item in items:
        
        product=item.select_one("div.KzDlHZ") or item.select_one("a.wjcEIp")
        price=item.select_one("div.Nx9bqj._4b5DiR") or item.select_one("div.Nx9bqj")
        product_text=product.text.strip().lower()
        price_text=price.text 
        link=item.select_one("a.CGtC98") or item.select_one("a.wjcEIp")
        href = link['href'] if link and link.has_attr('href') else None
        product_link = f"https://www.flipkart.com{href}" if href else None
        product_txt=product.text.strip()
        img_link=item.select_one("img.DByuf4")
        img=img_link.get('src') if img_link and img_link.has_attr('src') else None
        if product and price and all(word in product_text for word in search_keyword):
            img_links.append(img)
            products.append(f'<a href="{product_link}" target="_blank">{product_txt}</a>')
            prices.append(price_text)
    driver1.quit()
    pd.set_option('display.max_colwidth', None)


    if products and prices:
        # Create a dictionary where product names are keys and prices are values
        # product_price_dict = dict(zip(products, prices))
        
        # Create a Pandas DataFrame from the dictionary
        df = pd.DataFrame(zip(img_links, products, prices), columns=['Image','Product Name', 'Price'])
        df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="100">' if x else '')
        df1=df.head()
        return df1.to_html(classes='data', header="true",escape=False, index=False)  # Convert to HTML table
    else:
        return "<p>Product not found on Flipkart.</p>"
    

# Function to scrape Amazon
def scrape_amazon(product_name):
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)

    driver.get(amazon_url)
    search_keywords = product_name.lower().split()
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Identify product containers
    item_box = soup.select("div.puis-card-container.s-card-container") #puis-card-container s-card-container
    alt_item_box = soup.select("div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small")

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
                link=item.select_one("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal")
                # product_link=link.get("href") if link else None
                href = link['href'] if link and link.has_attr('href') else None
                product_link = f"https://www.amazon.in{href}" if href else None
                img_link=item.select_one("img.s-image") 
                
                img=img_link.get("src") if img_link and img_link.has_attr("src") else None



                # Check if all words in search query are in product name
                if product and price_text and product_link and all(word in product_text for word in search_keywords):
                    img_links.append(img)
                    products.append(f'<a href="{product_link}" target="_blank">{product}</a>')
                    prices.append(price_text)

            except NoSuchElementException as e:
                print(f"NoSuchElementFound: {e}")

            except AttributeError as e:
                print(f"Attribute Error: {e}")

            except Exception as e:
                print(f"Element Not Found:{e}")

    # Try Electronics Selector First
    extract_products(item_box, "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal") # electronics products names

    # If too few products, try Grocery Selector
    if len(products) < 3:
        products = []
        prices = []
        img_links=[]
        extract_products(item_box, "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal") # grocery products names
    driver.quit()
    pd.set_option('display.max_colwidth', None)

    if products and prices:
        # Create a dictionary where product names are keys and prices are values
        # product_price_dict = dict()
        
        # Create a Pandas DataFrame from the dictionary
        df = pd.DataFrame(zip(img_links,products, prices), columns=['Image','Product Name', 'Price'])
        df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="100">' if x else '')
        df1=df.head()
        return df1.to_html(classes='data', header="true",escape=False, index=False)  # Convert to HTML table
    else:
        return "<p>Product not found on Amazon.</p>"
    

# --- Groceries Scraping Functions ---

# JioMart Scraping Function
def scrape_jiomart(product_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)
    try:
        url = f"https://www.jiomart.com/search/{product_name.replace(' ','%20')}"
        driver.get(url)
        time.sleep(3)  # Initial page load
        search_keywords = product_name.lower().split()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)  # Wait for scroll to load
        # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".plp-card-details-container")))
        soup=BeautifulSoup(driver.page_source,'html.parser')
            # Extract product names and prices
        product_names = []
        prices = []
        images=[]
        try:
            # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"plp-card-details-container")))
            items=soup.select("a.plp-card-wrapper.plp_product_list")
            for item in items:
                product=item.select_one("div.plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80")
                product_text=product.text.strip() if product else None
                product_text_lower=product_text.lower()
                if product_text:
                    product_text_lower = product_text.lower()
                else:
                    continue
                price= item.select_one("span.jm-heading-xxs.jm-mb-xxs")
                price_text=price.text.strip() if price else None
                # Get product link safely
                product_link = f"https://www.jiomart.com{item.get('href', '')}"

                # Get image link safely
                img_tag = item.select_one("img.lazyautosizes.lazyloaded")
                img_link = img_tag["src"] if img_tag else "N/A"
                
                if product_text and price_text and all(word in product_text_lower for word in search_keywords):
                    product_names.append(f'<a href="{product_link}" target="_blank">{product_text}</a>')  # Make name clickable
                    prices.append(price_text)
                    images.append(img_link)
                
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")    
    finally:
        driver.quit()

    pd.set_option('display.max_colwidth', None)
    if product_names and prices:
        
        df = pd.DataFrame(zip(images,product_names, prices), columns=['Image','Product Name', 'Price'])
        df['Image'] = df['Image'].apply(lambda x: f'<img src="{x}" width="100">' if x else '')
        df1=df.head()
        return df1.to_html(classes='data', header="true",escape=False, index=False)  # Convert to HTML table
    else:
        return "<p>Product not found on JioMart.</p>"
    

# Function to scrape Zepto
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

                # print(img_link)
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
        df1=df.head()
        return df1.to_html(classes='data', header="true",escape=False, index=False)

    except Exception as e:
        driver.quit()
        return "<p>Product not found on Zepto.</p>"        
        


# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the E-commerce page
@app.route('/ecommerce', methods=['GET', 'POST'])
def ecommerce():
    flipkart_price = None
    amazon_price = None
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:
            try:
                flipkart_price = scrape_flipkart(product_name)
            except:
                flipkart_price = None
            try:
                amazon_price = scrape_amazon(product_name)
            except:
                amazon_price = None
    
    return render_template('ecommerce.html', flipkart_price=flipkart_price, amazon_price=amazon_price)

# Route for the Groceries page
@app.route('/groceries', methods=['GET', 'POST'])
def groceries():
    jiomart_price = None
    zepto_price = None
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:            
            try:
                jiomart_price = scrape_jiomart(product_name)
            except:
                jiomart_price = None
            try:
                zepto_price = scrape_zepto(product_name)
            except:
                zepto_price = None
    
    return render_template('groceries.html', jiomart_price=jiomart_price, zepto_price=zepto_price)

if __name__ == '__main__':
    app.run(debug=True)


