import socket
import os
import sys
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
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		ip_address = self.get_ip_address()
		return os.system(f"ping {ip_address}")
	    
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
		if self.website_address.get_http_status_code() == "200: Available":
			return "Your site is healthy!"
		else:
			return "There's something wrong with your site"
			
	def check_blacklisting(self):
		ip_address = self.get_ip_address()
		headers = { "x-auth-token": "3843809f-9481-4a92-bc6c-49b6a0222fe7" }
		base_url= "https://signals.api.auth0.com/v2.0/ip/"
		response_url = f"{base_url}{ip_address}"
		response = requests.get(response_url, headers=headers)
		r = json.loads(response.text)
		print("As a rule of thumb, the more negative a value, the higher risk the IP. A zero value is neutral (good).")
		return f"Your confidence score is r['fullip']['baddomain']['score']"

class CheckHashAndPorts(WebsiteAvailability):

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
		ip_address = self.get_ip_address()
		
			
		for port in results[ip_address]:
			if port['state'] == "open":
				print(f"Port {port['portid']}: {port['state']}")
		
		return "Completed"
				
	def nmap_ping_scanning(self) -> str:
		nmap = nmap3.NmapScanTechniques()
		ip_address = self.get_ip_address()
		result = nmap.nmap_ping_scan(ip_address)
		return result[0]['state']
		
	def nmap_tcp_scanning(self) -> str:
		nmap = nmap3.NmapScanTechniques()
		ip_address = self.get_ip_address()
		result = nmap.nmap_tcp_scan(ip_address)
		return result

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
	    """Scrape target URL for metadata and save to json."""
	    from data import Data
	    file_path = "metadata.json"
	    saved_metadata = self.all_metadata()
	    
	    title = self.get_title()
	    description = self.get_description()
	    image = self.get_image()
	    favicon = self.get_favicon()
	    sitename = self.get_site_name()
	    
	    new_metadata = {
	        'title': title,
	        'description': description,
	        'image': image,
	        'favicon': favicon,
	        'sitename':  sitename,
	        }
	    
	    saved_metadata.append(new_metadata)
	    
	    return Data.save(file_path, saved_metadata) 
	
	def all_metadata(self):
	    from data import Data
	    file_path = "metadata.json"
	    return Data.load(file_path)

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
            

def instructions():
    print("""
Here are the steps to run this application:

1. Run the **./main.py** file in the terminal to start the application.
2. Use the log in details in the **username.py** file to successfully log in and access the application. If you input the incorrect combination three times you will be exited from the application.
3. Press the ENTER key after any input in the terminal to access the option you chose.
4. Make sure your input is as accurate as possible according to the prompts.
5. If you accidentally exit the program, any actions you did during the previous run will remain.
6. To run the program again simply follow Step 1. above. 
""") 

if "--help" in sys.argv:
    instructions()
    time.sleep(10)
else:
    pass

    
print("Welcome to the Website Availability Python Terminal Application (WAPTA)!")
response = input(
"""Would you like to test an individual website or multiple websites?
1. Single website
2. All websites\n
Please choose 1 or 2\n"""
)

website_address = input("Which website would you like to check? ")

while True: 
	if response == "1":
		try:
			response = requests.get(f"https://{website_address}")
			print("*"*40)
			print("URL is valid and exists on the internet")
			print("*"*40)
		except requests.ConnectionError as exception:
			print("*"*40)
			print("URL does not exist on the internet")
			print("*"*40)
			break
		
		individual_website_response = input("""\nWhat would you like to check on this website?
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
15. Check bad ip score
16. Exit program\n
""")
		
		if individual_website_response == "16":
			print("*"*30)
			print("Exited the program successfully")
			print("*"*30)
			sys.exit()
		
	elif response == "2":
		pass
	
	if individual_website_response == "1":
		website = WebsiteAvailability(website_address)
		ip_address = website.get_ping()
		print(f"The IP address of this website is {ip_address}")	
	
	if individual_website_response == "2":
		website = WebsiteAvailability(website_address)
		ip_address = website.get_ip_address()
		print(f"The IP address of this website is {ip_address}")
		
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
		website = WebsiteAvailability(website_address)
		ssl_expiry = website.ssl_expiry_datetime()
		print("Please be patient as this test may take a minute or so...")
		print(f"{ssl_expiry}") 
		
	elif individual_website_response == "8":
		website = WebsiteAvailability(website_address)
		website_is_registered = website.is_registered()
		print(f"{website_is_registered}")
		
	elif individual_website_response == "9":
	    website = CheckHashAndPorts(website_address)
	    website_hash = website.check_hash()
	    print(f"{website_hash}")
	
	elif individual_website_response == "10":
	    website = CheckHashAndPorts(website_address)
	    port_scan = website.nmap_port_scanning()
	    print(f"{port_scan}")
	
	elif individual_website_response == "11":
	    website = CheckHashAndPorts(website_address)
	    nmap_ping = website.nmap_ping_scanning()
	    print(f"{nmap_ping}")
		
	elif individual_website_response == "12":
	    website = CheckHashAndPorts(website_address)
	    tcp_scan = website.nmap_tcp_scanning()
	    print(f"{tcp_scan}")
		
	elif individual_website_response == "13":
	    website = ScrapeWebsite(website_address)
	    json_metadata = website.return_page_metadata()
	    all_data = website.all_metadata()
	    print(f"Title: {all_data[-1]['title']}")
	    print(f"Sitename: {all_data[-1]['sitename']}")
	    print(f"Description: {all_data[-1]['description']}")
	    print(f"Image: {all_data[-1]['image']}")
	    print(f"Favicon: {all_data[-1]['favicon']}")
	    print(f"Saved metadata to metadata.json")
	    
	elif individual_website_response == "14":
		website = WebsiteAvailability(website_address)
		website_health_check = website.health_check()
		print(website_health_check["title"])
		
	elif individual_website_response == "15":
		website = WebsiteAvailability(website_address)
		blacklist_score = website.check_blacklisting()
		print(blacklist_score)
		