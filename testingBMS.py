from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# Set up Selenium
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(options=chrome_options)

# Open BookMyShow URL
url = "https://in.bookmyshow.com/buytickets/court-state-vs-a-nobody-hyderabad/movie-hyd-ET00432575-MT/20250322"
driver.get(url)


element = driver.find_element(By.XPATH,'//*[@id="super-container"]/div[1]/div[4]/div/div/section[2]/div/div[1]/section/div/div/div[1]/div[2]/div[1]/div[1]/div/div[1]')
ActionChains(driver).move_to_element(element).perform()
time.sleep(30)
# price = driver.find_element_by_xpath("//xpath_to_price").text
# print(price)
# Wait for page to load
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-7o7nez-0.iueRmY")))

# Parse with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract venues using CSS selector
# venues = soup.select("div.sc-e8nk8f-3.iFKUFD")  # Adjust the selector accordingly
# x=0
# for i in venues:
#     # print(i.select_one("div.sc-7o7nez-0.iueRmY").text.strip())
#     j=i.select_one("div.sc-1vhizuf-0.dqVIoM")
#     print()
#     print(j.text.strip())
#     x+=1
#     print("venue level: "+ str(x))
    
    # for k in j:
    #     print(k.text.strip())
# show_times = soup.select("div.sc-1vhizuf-0.dqVIoM")


# Store extracted data
# data = []

# for venue in venues:
#     try:
#         # Extract venue name
        # venue_name = venue.select_one("div.sc-7o7nez-0.iueRmY").text.strip()  # Use CSS selector for venue name
        # print(venue_name+"  ")
        
        # show_timings = venue.select_one("div.sc-1vhizuf-0.dqVIoM").text.strip()  # Use CSS selector for time slots
        # print(show_timings)

        

        
        # data.append({"Venue": venue_name, "Show Timings": show_timings})  # Store extracted data in a dictionary
        # print(data)
    # except AttributeError:
    #     print("Exception ochindi")
    #     continue

# Convert to DataFrame
# df = pd.DataFrame(data)
# print(df)

# # Save as CSV
# df.to_csv("bookmyshow_showtimes.csv", index=False)

# Close driver
driver.quit()
