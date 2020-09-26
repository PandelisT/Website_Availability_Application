# import requests
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from website_availability import WebsiteAvailability
# import os

# class Notifications(WebsiteAvailability):
    
#     def __init__(self, sender: str, receiver: str) -> None:
#         self.sender = sender
#         self.receiver = receiver
    
#     def send_email_status(self):
        
#         message = Mail(
#             from_email=f"{self.sender}",
#             to_emails=f"{self.receiver}",
#             subject=f"Health status of your website: {self.website_address.get_http_status_code()}",
#             html_content='<strong>For more information contact: 0400 000 000</strong>')
#         try:
#             sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
#             response = sg.send(message)
#             return "Sent successfully"
#         except:
#             return "Error"
            
