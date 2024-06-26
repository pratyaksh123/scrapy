from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from pushover import send_push_notification

import time
import csv
import os

load_dotenv()
def write_to_csv(data, filename='data.csv'):
    """Write data to a CSV file. Each inner list of data is a row."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def read_from_csv(filename='data.csv'):
    """Read data from a CSV file and return as a list of lists. Handles file not existing."""
    if not os.path.exists(filename):
        return []  # Return an empty list if the file doesn't exist
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        return list(reader)


# Set up Chrome options for headless execution
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')  # Set window size
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(r'/usr/bin/chromedriver',chrome_options=options)
options.add_argument('--disable-dev-shm-usage')
driver.get("https://www.rentrt.com/arlington-vaapartments/randolph-towers/conventional/")
# driver.get("https://www.rentvst.com/arlington-valuxuryapartments/virginia-square-towers/conventional/")

# Wait for the element to be clickable and then click it
try:  
    time.sleep(5)
    # Wait for the cookie popup reject button to be clickable
    reject_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pc_banner_reject_all"))
    )

    # Click the reject button to dismiss the cookie popup
    reject_button.click()
    print("Cookie popup dismissed.")

    # Scroll down to the bottom of the page to ensure all elements are loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolled to the bottom of the page.")

    # Wait for the tab to be clickable after dismissing the popup
    tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "fp-tab-2"))
    )
    tab.click()
    print("Clicked on the tab.")

# Wait for the element to be clickable or visible
    primary_action_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".active .primary-action"))
    )

    # Click on the 'a' tag
    primary_action_link.click()
    print("Clicked on the primary action link.")

     # Wait for the modal to become visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "modal-container"))
    )
    
    # Ensure the availability table is loaded
    availability_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.check-availability-table"))
    )

    # Fetch all rows in the availability table
    data = []
    rows = availability_table.find_elements(By.CSS_SELECTOR, "div.unit-row.js-unit-row")
    for row in rows:
        unit = row.find_element(By.CSS_SELECTOR, "div.unit-col.unit").text
        rent = row.find_element(By.CSS_SELECTOR, "div.unit-col.rent").text
        sq_ft = row.find_element(By.CSS_SELECTOR, "div.unit-col.sqft").text
        availability = row.find_element(By.CSS_SELECTOR, "div.unit-col.availability").text
        data.append([unit, rent, sq_ft, availability])
        print(f"Unit: {unit}, Rent: {rent}, SqFt: {sq_ft}, Available: {availability}")

    old_data = read_from_csv()
    print("Old data:", old_data)
    print("New data:", data)
    if old_data != data:
        print("Data has changed. Updating the local file...")
        send_push_notification(os.getenv('USER_KEY'), "New apt Available", "The data has changed on the website.")

        write_to_csv(data)  # Update the CSV file with new data
    else:
        print("Data is up to date. No update needed.")
    # Pause before closing the browser
    print("Script complete, exiting..")
except Exception as e:
    # Handle any exceptions that occur during the process
    print("An error occurred:", e)

finally:
    # Close the driver after completion
    driver.quit()
    print("Driver closed.")