import socket
import os
import time
import requests
import whois
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
import urllib
from bs4 import BeautifulSoup
import csv
from time import sleep
import hashlib
import urllib3
import random
from urllib.request import urlopen
import nmap3
import datetime
import logging
import ssl
from bs4 import BeautifulSoup



class WebsiteAvailability:
	def __init__(self, website_address: str) -> None:
		self.website_address = website_address
		
	def get_ip_address(self) -> str:
		ip_address = socket.gethostbyname(f"{self.website_address}")
		return ip_address
	    
	def get_ping(self) -> str:
	    return os.system(f"ping {self.website_address}")
	    
	def get_http_status_code(self) -> str:
	        try:
	            response = requests.get(f"https://{self.website_address}")
	            status = response.status_code

	            if status == 200:
	                return "200: Available"
	            else:
	               return "Unavailable"
	            time.sleep(1)
	            
	        except Exception:
	            return "No Internet"
	            
	def check_whois_status(self) -> str:
	    domain = whois.whois(f"{self.website_address}")
	    return f"Expiration date: {domain.expiration_date}, Registrar: {domain.registrar}"
	
	def get_pagespeed(self, strategy: str) -> float:
		API_Key = "AIzaSyBUh1J0UqOPodBk5K-xnKUeLdlt1KTRQxc"
		base_url= "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
		response_url = f"{base_url}https://{self.website_address}&key={API_Key}&strategy=strategy_unspecified"
		response = requests.get(response_url)
		json_data = response.json()
		lighthouseResult = json_data["lighthouseResult"]
		categories = lighthouseResult["categories"]
		performance = categories["performance"]
		score = performance["score"]
		return (score*100)
		
	def is_registered(self) -> bool:
	  try:
	      w = whois.whois(self.website_address)
	      print("DOMAIN REGISTRAR: ", w.registrar)
	      print("WHOIS SERVER: ", w.whois_server)
	      print("Domain Creation Date: ",w.creation_date)
	      print("Expiration Date: ", w.expiration_date)
	      return bool(w.domain_name)
	  except Exception:
	        return False

	def get_server_and_content_type(self) -> str:
	 	resp = requests.head(f"https://{self.website_address}")
	 	server = resp.headers['server']
	 	content_type = resp.headers['content-type']
	 	return f"Server: {server}, Content type: {content_type}"
	 	
	def ssl_expiry_datetime(self) -> datetime.datetime:
		logger = logging.getLogger('SSLVerify')
		ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
		
		context = ssl.create_default_context()
		conn = context.wrap_socket(
	        socket.socket(socket.AF_INET),
	        server_hostname=self.website_address,
	    )
	
		logger.debug(f'Connect to {self.website_address}')
		conn.connect((self.website_address, 443))
		ssl_info = conn.getpeercert()
		return f"Expiration date of SSL certificate: {datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)}"
		
	
	def health_check(self):
		if self.website_address.get_http_status_code() == "200: Available" and self.website_address.get_pagespeed("strategy_unspecified") > 70:
			return "Your site is healthy!"
		else:
			return "There's something wrong with your site"


# website_1 = WebsiteAvailability(website_address)
# test = website_1.ssl_expiry_datetime()
# print(website_1.get_pagespeed("mobile"))


class CheckHashAndPorts(WebsiteAvailability):
	def __init__(self, website_address: str) -> None:
		self.website_address = website_address
		
	"""Comparing MD5 Hash sum"""
	def check_hash(self) -> str:
		url = f"https://{self.website_address}"
		response = urlopen(url).read()
		currentHash = hashlib.sha224(response).hexdigest()
		
		tries = 0
		while tries <3:
		    try:
		        response = urlopen(url).read()
		        currentHash = hashlib.sha224(response).hexdigest()
		        time.sleep(5)
		        response = urlopen(url).read()
		        newHash = hashlib.sha224(response).hexdigest()
		
		        if newHash == currentHash:
		        	print("Same hash!")
		        	tries += 1
		        	continue
		        else:
		            response = urlopen(url).read()
		            currentHash = hashlib.sha224(response).hexdigest()
		            print("Something isn't right!")
		            time.sleep(5)
		            tries += 1
		
		    except Exception:
		    	print("error")
		    	
		return "Completed"
		
	"""Nmap analysis of ports, pinging and tcp scan"""
	def nmap_port_scanning(self) -> str:
		nmap = nmap3.Nmap()
		results = nmap.scan_top_ports(f"{self.website_address}")
		ip_address = self.website_address.get_ip_address()
			
		for port in results[ip_address]:
			if port['state'] == "open":
				print(f"Port {port['portid']}: {port['state']}")
				
	def nmap_ping_scanning(self) -> str:
		nmap = nmap3.NmapScanTechniques()
		ip_address = self.website_address.get_ip_address()
		result = nmap.nmap_ping_scan(ip_address)
		return result[0]['state']
		
	def nmap_tcp_scanning(self) -> str:
		nmap = nmap3.NmapScanTechniques()
		ip_address = self.website_address.get_ip_address()
		result = nmap.nmap_tcp_scan(ip_address)
		return result

# website_3 = CheckHashAndPorts(WebsiteAvailability(website_address))

# print('results are:')
# print(website_3.nmap_ping_scanning())
# print(website_3.nmap_tcp_scanning())

"""Scrape metadata from target URL."""
class ScrapeWebsite(WebsiteAvailability):

	def __init__(self, website_address):
		self.website_address = website_address
		
	@staticmethod
	def list_headers():
		headers = {
	        'Access-Control-Allow-Origin': '*',
	        'Access-Control-Allow-Methods': 'GET',
	        'Access-Control-Allow-Headers': 'Content-Type',
	        'Access-Control-Max-Age': '3600',
	        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
	    }
		return headers	

	def get_response(self):
		header = ScrapeWebsite.list_headers()
		url = f"https://{self.website_address}"
		response = requests.get(url, headers=header)
		return response
	
	def get_html(self):
		r = self.get_response()
		html = BeautifulSoup(r.content, 'html.parser')
		return html

	def get_title(self):
	    """Scrape page title."""
	    html = self.get_html()
	    self.title = html.title.string
	    return self.title
	
	def get_description(self):
	    """Scrape page description."""
	    html = self.get_html()
	    description = None
	    if html.find("meta", property="description"):
	        description = html.find("meta", property="description").get('content')
	    elif html.find("meta", property="og:description"):
	        description = html.find("meta", property="og:description").get('content')
	    return description
	
	def get_image(self):
	    """Scrape share image."""
	    image = None
	    html = self.get_html()
	    if html.find("meta", property="image"):
	        image = html.find("meta", property="image").get('content')
	    return image
	
	def get_site_name(self):
	    """Scrape site name."""
	    html = self.get_html()
	    return html.find("meta", property="og:site_name").get('content')
	
	def get_favicon(self):
		html = self.get_html()
		"""Scrape favicon."""
		return html.find("link", attrs={"rel": "icon"}).get('href')
	    
	def return_page_metadata(self) -> dict:
	    """Scrape target URL for metadata."""
	    
	    metadata = {
	        'title': self.get_title(),
	        'description': self.get_description(),
	        'image': self.get_image(),
	        'favicon': self.get_favicon(),
	        'sitename': self.get_site_name(),
	        'url': self.website_address
	        }
	    return metadata
	
# website_3 = ScrapeWebsite("nerdypandy.com.au")
# print(website_3.return_page_metadata())

class Notifications(WebsiteAvailability):
    
    def __init__(self, sender: str, receiver: str, sender_number, receiver_number) -> str:
        self.sender = sender
        self.receiver = receiver
        self.sender_number = sender_number
        self.receiver_number = receiver_number
    
    def send_email_status(self):
        
        message = Mail(
            from_email=f"{self.sender}",
            to_emails=f"{self.receiver}",
            subject=f"Health status of your website: {self.website_address.get_http_status_code()}",
            html_content='<strong>For more information contact: 0400 000 000</strong>')
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            return "Sent successfully"
        except:
            return "Error"
            
# notification = Notifications("pandeli@nerdypandy.com","pandeli@nerdypandy.com")
# print(notification.send_email_status())

print("Welcome to the Website Availability Python Terminal Application (WAPTA)!")
response = input(
"""Would you like to test an individual website or all your websites?
1. Single website
2. All websites\n
Please choose 1 or 2\n""")

if response == "1":
	website_address = input("Which website would you like to check? ")
	
	individual_website_response = input("""What would you like to check on this website?
	1. Is your website up?
	2. IP address
	3. Current HTTP status code and availability
	4. Page speed using Google PageInsights
	5. Domain expiry and registrar
	6. Server and content type
	7. SSL expiry date
	8. Is the domain registered? and Whois status
	9. Compare MD5 hash sum
	10. Port scanning with Nmap
	11. Ping with Nmap
	12. TCP scan with Nmap
	13. Scrape website for metadata
	14. Perform health check and send results to your email
	""")
	
elif response == "2":
	pass


if individual_website_response == "2":
	website = WebsiteAvailability(website_address)
	ip_address = website.get_ip_address()
	print(f"The IP address of this websie is {ip_address}")
elif individual_website_response == "3":
	website = WebsiteAvailability(website_address)
	http_status_code = website.get_http_status_code()
	print(f"The HTTP status code is {http_status_code}")
elif individual_website_response == "4":
    strategy = "strategy_unspecified"
    website = WebsiteAvailability(website_address)
    page_speed = website.get_pagespeed(strategy)
    print("Please be patient as this test may take a minute or so...")
    print(f"Your page speed is {page_speed}")
elif individual_website_response == "5":
    website = WebsiteAvailability(website_address)
    whois_status = website.check_whois_status()
    print("Please be patient as this test may take a minute or so...")
    print(f"{whois_status}")
    
elif individual_website_response == "6":
    website = WebsiteAvailability(website_address)
    server_and_content_type = website.get_server_and_content_type()
    print("Please be patient as this test may take a minute or so...")
    print(f"{whois_status}") 
	
elif individual_website_response == "7":
	pass
elif individual_website_response == "8":
	website = WebsiteAvailability(website_address)
	website_is_registered = website.is_registered()
	print(f"{website_is_registered}")
elif individual_website_response == "9":
	pass
elif individual_website_response == "10":
	pass
elif individual_website_response == "11":
	pass
elif individual_website_response == "12":
	pass
elif individual_website_response == "13":
	pass
elif individual_website_response == "14":
	pass