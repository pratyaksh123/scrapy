from dotenv import load_dotenv
import os
import http.client
import urllib.parse

# Load environment variables from .env file
load_dotenv()

def send_push_notification(user_key, message, title="Alert", retry=60, expire=3600, url=None, url_title=None, priority=2, sound=None):
    app_token = os.getenv('PUSHOVER_API_TOKEN')
    if not app_token:
        raise ValueError("PUSHOVER_API_TOKEN is not set. Please check your .env file.")

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    data = {
        "token": app_token,
        "user": user_key,
        "message": message,
        "title": title,
        "priority": priority,
        "retry": retry,  # Time between retries in seconds
        "expire": expire  # How long to continue retrying in seconds
    }
    if url:
        data["url"] = url
    if url_title:
        data["url_title"] = url_title
    if sound:
        data["sound"] = sound

    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode(data), {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    print(response.status, response.reason, response.read().decode())
