from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from website_availability import WebsiteAvailability
import os
import requests
import json


class Notifications(WebsiteAvailability):

    def __init__(self, receiver: str) -> None:
        self.receiver = receiver

    def send_email_status(self):
        # try:
        # website = WebsiteAvailability(self.website_address)
        # website_health_check = website.health_check()
        url = 'https://api.sendgrid.com/v3/mail/send'
        headers = { 
        "Authorization" : f"Bearer {os.environ.get('SENDGRID_API_KEY')}",
        "Content-Type" : "application/json" 
        } 
        payload = {"personalizations": 
            [{"to": [{"email": f"{os.environ.get('TEST_EMAIL')}"}]}],
            "from": {"email": f"{os.environ.get('TEST_EMAIL')}"},
            "subject": "Health Check Status Report",
            "content": [{"type": "text/plain", "value": "test"}]}
        message = requests.post(url, data=json.dumps(payload), headers=headers)
        print(message.text)
        return "Success!"
        # except Exception:
        #     return "Error"


# send_website = Notifications("pandeli@nerdypandy.com")
# send_it = send_website.send_email_status()

#{page_performance[0]}, HTTP Status: {http_status[0]}, Blacklisting score is: {blacklisting_score}"}
