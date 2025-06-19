import cloudscraper
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def send_push_notification(message: str):
    data = {
        "token": os.getenv("PUSHOVER_API_TOKEN"),
        "user": os.getenv("PUSHOVER_USER_KEY"),
        "message": message,
        "title": "Rental Alert",
        "priority": 1
    }

    r = requests.post("https://api.pushover.net/1/messages.json", data=data)
    print("Pushover response:", r.status_code, r.text)


def main():
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    raw_html = scraper.get("https://www.rentrt.com/arlington-vaapartments/randolph-towers/conventional/").text

    bs4 = BeautifulSoup(raw_html, "html.parser")
    primary_actions = bs4.find_all("button", {"class": "primary-action"})

    # button 1 , 3 we have to target
    studio_button = primary_actions[0]
    single_bed_button = primary_actions[2]

    if studio_button.text != "Get Notified":
        send_push_notification("Studio Apartment is available!")
    if single_bed_button.text != "Get Notified":
        send_push_notification("Studio Apartment is available!")

if __name__ == "__main__":
    main()
