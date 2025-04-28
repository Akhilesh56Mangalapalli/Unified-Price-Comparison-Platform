from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import json
import random
import pandas as pd

# chrome_options = Options()
chrome_options = uc.ChromeOptions()
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
]
chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Attempt to bypass bot detection
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # 1=allow, 2=block
    "profile.default_content_setting_values.geolocation": 2     # 1=allow, 2=block
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the Driver
driver = uc.Chrome(options=chrome_options)
# driver2 = uc.Chrome(options=chrome_options)
driver.maximize_window()
actions = ActionChains(driver)
def search_movie_on_bookmyshow(movie_name,city):
    try:
        url = f"https://in.bookmyshow.com/explore/home/{city}"
        driver.get(url)

        # this is included in the url
        # city = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//img[@alt='HYD']")))
        # actions.move_to_element(city).click().perform()

        search_trigger= WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"//span[@id='4'][@class='bwc__sc-1nbn7v6-8 hbuyht']")))
        actions.move_to_element(search_trigger).click().perform()

        # actions.click(search_trigger)
        # search_trigger.click() # Clear any existing text
        input_field= WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[placeholder='Search for Movies, Events, Plays, Sports and Activities']")))
        # actions.move_to_element(input_field).click().perform()
        actions.move_to_element(input_field).move_by_offset(5, 5).pause(0.2).move_by_offset(-5, -5).click().perform()

        for char in movie_name:
            input_field.send_keys(char)
            time.sleep(random.uniform(0.3,0.7))  # Adjust delay as needed

        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_field
        )
        script = """
        arguments[0].dispatchEvent(new KeyboardEvent('keydown', {'key': 'a', bubbles: true}));
        arguments[0].dispatchEvent(new KeyboardEvent('keyup', {'key': 'a', bubbles: true}));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """
        driver.execute_script(script, input_field)

        
        suggestions_list = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li[class='bwc__sc-1iyhybo-9 fMpEag'] div[class='bwc__sc-3t17w7-15 ddrnsU']"))
            )

        # Use arrow keys to select the first suggestion and press Enter
        # actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.ENTER).perform()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//div[@class='sc-qswwm9-8 goilWl']//button[@class='sc-8f9mtj-0 sc-8f9mtj-1 sc-1vmod7e-0 bGKFux']"))).click()
        # driver2=driver.get(driver.current_url)
        # soup = BeautifulSoup(driver2, 'html.parser')
        # theater_names  = soup.find_all("div",class_="sc-7o7nez-0 iueRmY")
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        # container=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-e8nk8f-3 iFKUFD")))
         # Wait for new content to load

        theater_names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-7o7nez-0.iueRmY")))
        # theater_names=driver.find_elements(By.CLASS_NAME,"sc-7o7nez-0 iueRmY")
        # print(theater_names)
        
        theaters = []
        for theater_name in theater_names:
            theater = theater_name.text.strip()  # Extract and clean the price text
            # print(theater)
            theaters.append(theater) 
        for i in theaters:print(i)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        venues = soup.select("div.sc-e8nk8f-3.iFKUFD")
        data = []

        for venue in venues:
            try:
#               # Extract venue name
                venue_name = venue.select_one("div.sc-7o7nez-0.iueRmY").text.strip()  # Use CSS selector for venue name
        # print(venue_name+"  ")
        # Extract show timings   .sc-1vhizuf-2.bzAAyo
        # show_timings = venue.select("div.sc-1vhizuf-0.dqVIoM")
        
                show_timings = venue.select_one("div.sc-1vhizuf-0.dqVIoM").text.strip()  # Use CSS selector for time slots
        # print(show_timings)

        # print(venue_name+" "+str(showtimes))
                data.append({"Venue": venue_name, "Show Timings": show_timings})  # Store extracted data in a dictionary
        # print(data)
            except AttributeError:
                print("Exception ochindi")
                continue

# Convert to DataFrame
        df = pd.DataFrame(data)
        print(df)



#sc-1la7659-1 cMmsIX

           
             


       

            
                
        

        
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # finally:
    #     driver.quit()

# Run the function
movie_name = "court"
region="hyderabad"
search_movie_on_bookmyshow(movie_name,region)
# if not results:
#     print("No results or an error occurred.")