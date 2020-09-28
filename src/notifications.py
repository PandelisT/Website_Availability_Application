from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from website_availability import WebsiteAvailability
import os


class Notifications(WebsiteAvailability):

    def __init__(self, sender: str, receiver: str) -> None:
        self.sender = sender
        self.receiver = receiver

    def send_email_status(self):
        try:
            website = WebsiteAvailability(self.website_address)
            website_health_check = website.health_check()
            message = Mail(
                from_email=f"{self.sender}",
                to_emails=f"{self.receiver}",
                subject=f"Health check for {self.website_address}",
                html_content=f"Your page performance is: {website_health_check[0]}, HTTP Status: {website_health_check[1]}, Blacklisting score is: {website_health_check[2]}")
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            if response.status_code == 200:
                return "Sent successfully"
        except Exception:
            return "Error"
