from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Chrome setup
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Driver initialize
driver = webdriver.Chrome(options=chrome_options)

# Open JioMart
url = "https://www.jiomart.com/"
driver.get(url)
time.sleep(3)  # Initial page load

# Search for "onions"
search_box = driver.find_element(By.CSS_SELECTOR, ".aa-Input.search_input")
search_box.send_keys("paneer")
search_box.send_keys(Keys.ENTER)

# Wait for search results to load
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80"))
    )
    print("Search results loaded successfully!")
except Exception as e:
    print(f"Error waiting for results: {e}")
    driver.quit()
    exit()

# Scroll to load more products
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # Wait for scroll to load

# Extract product names
product_names = []
prices_list=[]
prices=driver.find_elements(By.CLASS_NAME,"plp-card-details-price-wrapper")
products = driver.find_elements(By.CSS_SELECTOR, ".plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80")
for price in prices:
    try:
        name = price.text.strip()
        if name:  # Avoid empty strings
            prices_list.append(name)
    except Exception as e:
        print(f"Error extracting product: {e}")


for product in products:
    try:
        name = product.text.strip()
        if name:  # Avoid empty strings
            product_names.append(name)
    except Exception as e:
        print(f"Error extracting product: {e}")

# Print product names
# for i, name in enumerate(product_names, 1):
#     print(f"{i}. {name}")

# Close driver
driver.quit()

# Optional: Create DataFrame
if product_names and prices_list:
    df = pd.DataFrame({"Product name":product_names,"Price value": prices_list})
    print("\nDataFrame Output:")
    print(df)
# if product_names:
#     df = pd.DataFrame({"Product Name": product_names})
#     print("\nDataFrame Output:")
#     print(df.head())
    # df.to_csv("jiomart_onions.csv", index=False)
    # print("Data saved to jiomart_onions.csv")
else:
    print("No products found!")