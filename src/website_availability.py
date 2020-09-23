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
		return f"Your confidence score is {r['fullip']['baddomain']['score']}"