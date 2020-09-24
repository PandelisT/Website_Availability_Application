import socket
import os
import sys
import time
import requests
import whois
import json
import urllib
import hashlib
import urllib3
import random
from urllib.request import urlopen
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
	    
	def get_http_status_code(self) -> tuple:
	        try:
	            response = requests.get(f"https://{self.website_address}")
	            status = response.status_code

	            if status == 200:
	                return (status, "Available")
	            elif status >= 500:
	            	return (status, "Server error")
	            elif status >= 400:
	            	return (status, "User error")
	            elif status >= 300:
	            	return (status, "Redirection")
	            else:
	               return (status, "Unavailable")
	            
	        except Exception:
	        	print("No Internet")
	            
	def check_whois_status(self) -> tuple:
	    domain = whois.whois(f"{self.website_address}")
	    return (domain.expiration_date, domain.registrar)
	
	def get_pagespeed(self, strategy: str) -> float:
		Google_API_Key = os.environ.get("GOOGLE_API")
		base_url= "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
		response_url = f"{base_url}https://{self.website_address}&key={Google_API_Key}&strategy={strategy}"
		response = requests.get(response_url)
		json_data = response.json()
		lighthouseResult = json_data["lighthouseResult"]
		categories = lighthouseResult["categories"]
		performance = categories["performance"]
		score = performance["score"]
		return score*100
		
	def is_registered(self) -> bool:
	  try:
	      w = whois.whois(self.website_address)
	      return bool(w.domain_name)
	  except Exception:
	        return False

	def get_server_and_content_type(self) -> tuple:
	 	resp = requests.head(f"https://{self.website_address}")
	 	server = resp.headers['server']
	 	content_type = resp.headers['content-type']
	 	return (server, content_type)
	 	
	def ssl_expiry_datetime(self) -> datetime.datetime:
		logger = logging.getLogger("SSLVerify")
		ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
		context = ssl.create_default_context()
		conn = context.wrap_socket(
	        socket.socket(socket.AF_INET),
	        server_hostname=self.website_address)
		logger.debug(f"Connect to {self.website_address}")
		conn.connect((self.website_address, 443))
		ssl_info = conn.getpeercert()
		return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
		
	def health_check(self):
		if self.website_address.get_http_status_code() == (200, "Available"):
			return "Your site is healthy!"
		else:
			return "There's something wrong with your site"
			
	def check_blacklisting(self) -> str:
		headers = { "x-auth-token": os.environ.get("SIGNALS_API")}
		base_url= "https://signals.api.auth0.com/v2.0/ip/"
		response_url = f"{base_url}{self.get_ip_address()}"
		response = requests.get(response_url, headers=headers)
		r = json.loads(response.text)
		print("As a rule of thumb, the more negative a value, the higher risk the IP. A zero value is neutral (good).")
		return r['fullip']['baddomain']['score']
