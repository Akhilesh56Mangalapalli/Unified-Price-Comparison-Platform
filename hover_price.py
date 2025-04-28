from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up undetected Chrome driver
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(options=chrome_options)

# Open the BookMyShow page
url = "https://in.bookmyshow.com/buytickets/court-state-vs-a-nobody-hyderabad/movie-hyd-ET00432575-MT/20250322"
driver.get(url)

# Wait for the showtime elements to load
wait = WebDriverWait(driver, 10)
showtime_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-7o7nez-0")))

# ActionChains for hovering
actions = ActionChains(driver)

# Store extracted data
data = []

for showtime in showtime_elements:
    actions.move_to_element(showtime).perform()  # Hover over the showtime
    time.sleep(2)  # Give time for the tooltip to appear

    try:
        # Find the tooltip containing price
        price_element = driver.find_element(By.CLASS_NAME, "tooltip-class")  # Update with actual class name
        price_text = price_element.text.strip()
        
        # Store extracted info
        data.append({
            "Showtime": showtime.text.strip(),
            "Price Details": price_text
        })
    except:
        print("Price info not found for:", showtime.text.strip())

# Print extracted data
for entry in data:
    print(entry)

# Close the browser
driver.quit()
