#!/home/pratyaksh/Desktop/testing/bin/python3
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
import logging

# Define the absolute path to the CSV file
base_dir = '/home/pratyaksh/Desktop/testing'
data_filename = os.path.join(base_dir, 'data.csv')
log_filename = os.path.join(base_dir, 'script.log')

logging.basicConfig(filename=log_filename, level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

load_dotenv()
def write_to_csv(data, filename=data_filename):
    """Write data to a CSV file. Each inner list of data is a row."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def read_from_csv(filename=data_filename):
    """Read data from a CSV file and return as a list of lists. Handles file not existing."""
    if not os.path.exists(filename):
        return []  # Return an empty list if the file doesn't exist
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        return list(reader)

def load_driver():
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
    return driver
# driver.get("https://www.rentvst.com/arlington-valuxuryapartments/virginia-square-towers/conventional/")

def main():
    print("Script started")
    driver = load_driver()
    try:  
        time.sleep(5)
        # Wait for the cookie popup reject button to be clickable
        reject_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pc_banner_reject_all"))
        )

        # Click the reject button to dismiss the cookie popup
        reject_button.click()
        logging.debug("Cookie popup dismissed.")

        # Scroll down to the bottom of the page to ensure all elements are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.debug("Scrolled to the bottom of the page.")

        # Wait for the tab to be clickable after dismissing the popup
        tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "fp-tab-2"))
        )
        tab.click()
        logging.debug("Clicked on the tab.")

    # Wait for the element to be clickable or visible
        primary_action_link = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".active .primary-action"))
        )

        # Click on the 'a' tag
        primary_action_link.click()
        logging.debug("Clicked on the primary action link.")

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
            logging.debug(f"Unit: {unit}, Rent: {rent}, SqFt: {sq_ft}, Available: {availability}")

        old_data = read_from_csv()
        logging.debug(f"Old data: {old_data}")
        logging.debug(f"New data: {data[0]}")
        if old_data != data:
            logging.debug("Data has changed. Updating the local file...")
            send_push_notification(os.getenv('USER_KEY'), "New apt Available", f"Unit {data[0][0]} Sq Ft: {data[0][2]} Available: {data[0][3]}")

            write_to_csv(data)  # Update the CSV file with new data
        else:
            logging.debug("Data is up to date. No update needed.")
        # Pause before closing the browser
        logging.debug("Script complete, exiting..")
    except Exception as e:
        # Handle any exceptions that occur during the process
        logging.error("Failed to complete the script:", exc_info=True)
    finally:
        # Close the driver after completion
        driver.quit()
        logging.debug("Driver closed.")

if __name__ == '__main__':
    main()