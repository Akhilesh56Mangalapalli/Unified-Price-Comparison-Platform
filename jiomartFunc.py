from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jiomart_products(product_name):
    # Chrome setup
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Driver initialize
    driver = webdriver.Chrome(options=chrome_options)
    search_element = product_name.lower()
    
    try:
        # Open JioMart
        url = f"https://www.jiomart.com/search/{product_name.replace(' ', '%20')}"
        driver.get(url)
        time.sleep(3)  # Initial page load

        # Scroll to load more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for scroll to load
        search_element = product_name.lower().split()
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract product names and prices
        product_names = []
        prices = []
        images = []
        
        try:
            items = soup.select("a.plp-card-wrapper.plp_product_list")
            for item in items:
                product = item.select_one("div.plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80")
                product_text = product.text.strip() if product else None
                
                # Ensure product_text is found
                if product_text:
                    product_text_lower = product_text.lower()
                else:
                    continue  # Skip if no product text is found

                price = item.select_one("span.jm-heading-xxs.jm-mb-xxs")
                price_text = price.text.strip() if price else None

                # Get product link safely
                product_link = item.get("href", "N/A")

                # Get image link safely
                img_tag = item.select_one("img.lazyautosizes.lazyloaded")
                img_link = img_tag["src"] if img_tag else "N/A"

                # Print debugging info (remove in production)
                print(f"Product Name: {product_text}")
                print(f"Price: {price_text}")
                print(f"Image Link: {img_link}")
                print(f"Product Link: {product_link}")
                
                # Filter by search keywords
                if product_text and price_text and all(word in product_text_lower for word in search_element):
                    product_names.append(f'<a href="{product_link}" target="_blank">{product_text}</a>')  # Make name clickable
                    prices.append(price_text)
                    images.append(img_link)

            # Create DataFrame
            if product_names and prices:
                df = pd.DataFrame(zip(images, product_names, prices), columns=['Image', 'Product Name', 'Price'])
                print("\nDataFrame Output:")
                print(df.head())
            else:
                print("No products or prices found!")
        except Exception as e:
            print(f"Error extracting data: {e}")
        
    except Exception as e:
        print(f"Error in scraping: {e}")
    
    finally:
        # Close driver
        driver.quit()

# Call the function
if __name__ == "__main__":
    scrape_jiomart_products("surf excel powder")
