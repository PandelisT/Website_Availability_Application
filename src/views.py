import requests
import os, sys
from website_availability import WebsiteAvailability
from check_hash_and_ports import CheckHashAndPorts
from scrape_website import ScrapeWebsite
from notifications import Notifications
from colorama import Fore, init
init(autoreset=True)


class View:

	def __init__(self, website_address):
		self.website_address = website_address
	
	def get_website(self):
		isValid = True
		if self.website_address[0:8] == "https://":
			self.website_address = self.website_address[8:]
		elif self.website_address[0:7] == "http://":
			self.website_address = self.website_address[7:]
		
		try:
			response = requests.get(f"https://{self.website_address}")
			return (isValid, Fore.GREEN + "URL is valid and exists on the internet")
		except requests.ConnectionError as exception:
			isValid = False
			return (isValid, Fore.RED + "URL does not exist on the internet")
	
	def show_options(self):
	    return """\nWhat would you like to check on this website?
1. Is your website up?
2. What is the website's IP address?
3. Current HTTP status code and availability
4. Page speed/performance score using Google PageInsights
5. Domain expiry and registrar
6. Server and content type
7. SSL expiry date
8. Is the domain registered + Whois status
9. Compare MD5 hash sum
10. Port scanning with Nmap
11. Ping with Nmap
12. TCP scan with Nmap
13. Scrape website for metadata
14. Perform health check and send results to your email
15. Check bad ip score
16. Exit program\n
"""
	
class ChooseOptions(CheckHashAndPorts, ScrapeWebsite, View):
    
    def __init__(self, website_address, individual_website_response) -> None:
        self.individual_website_response = individual_website_response
        self.website_address = website_address
	
    def choose_options(self):
	    
	    website = WebsiteAvailability(self.website_address)
	    
	    website_hash_test = CheckHashAndPorts(self.website_address)
	    
	    if self.individual_website_response == "16":
	        print("*"*32)
	        print(Fore.GREEN + "Exited the program successfully")
	        print("*"*32)
	        sys.exit()
	        
	    elif self.individual_website_response == "2":
	        ip_address = website.get_ip_address()
	        return Fore.GREEN + f"The IP address of this website is {ip_address}"
	        
	    elif self.individual_website_response == "3":
	        http_status_code = website.get_http_status_code()
	        return Fore.GREEN + f"The HTTP status code is {http_status_code[0]}: {http_status_code[1]}"
	    
	    elif self.individual_website_response == "4":
	    	print("*"*50)
	    	print("Page performance is the overall performance score of your page.")
	    	print("First Meaningful Paint measures when the primary content of a page is visible.")
	    	print("Speed Index shows how quickly the contents of a page are visibly populated.")
	    	print("Time to interactive is the amount of time it takes for the page to become fully interactive.")
	    	print("*"*50)
	    	strategy = "strategy_unspecified"
	    	page_performance = website.get_pagespeed(strategy)
	    	return Fore.GREEN + f"Your page performance is {page_performance[0]}, First Meaningful Paint: {page_performance[1]}, Speed Index: {page_performance[2]},  Time To Interactive: {page_performance[3]}"
	        
	    elif self.individual_website_response == "5":
	        whois_status = website.check_whois_status()
	        return Fore.GREEN + f"Expiration date: {whois_status[0]}, Registrar: {whois_status[1]}"
	        
	    elif self.individual_website_response == "6":
	        server_and_content_type = website.get_server_and_content_type()
	        return Fore.GREEN + f"Server: {server_and_content_type[0]}, Content type: {server_and_content_type[1]}"
	        
	    elif self.individual_website_response == "7":
	        ssl_expiry = website.ssl_expiry_datetime()
	        return Fore.GREEN + f"Expiration date of SSL certificate: {ssl_expiry}"
	        
	    elif self.individual_website_response == "8":
	        domain_name_is_registered = website.is_registered()
	        if domain_name_is_registered == True:
	            return (Fore.GREEN + "Domain name is registered")
	        elif domain_name_is_registered == False:
	            return Fore.RED + "Domain name is not registered"
	            
	    elif self.individual_website_response == "9":
	        website_hash = website_hash_test.check_hash()
	        return Fore.GREEN + f"{website_hash}"
	    
	    elif self.individual_website_response == "10":
	        port_scan = website_hash_test.nmap_port_scanning()
	        return Fore.GREEN + f"{port_scan}"
	        
	    elif self.individual_website_response == "11" or self.individual_website_response == "1":
	        nmap_ping = website_hash_test.nmap_ping_scanning()
	        return Fore.GREEN + f"The website is {nmap_ping}"
	        
	    elif self.individual_website_response == "12":
	        tcp_scan = website_hash_test.nmap_tcp_scanning()
	        return Fore.GREEN + f"{tcp_scan}"
	    
	    elif self.individual_website_response == "13":
	        website_scrape = ScrapeWebsite(self.website_address)
	        json_metadata = website_scrape.return_page_metadata()
	        all_data = website_scrape.all_metadata()
	        print(f"Title: {all_data[-1]['title']}")
	        print(f"Sitename: {all_data[-1]['sitename']}")
	        print(f"Description: {all_data[-1]['description']}")
	        print(f"Image: {all_data[-1]['image']}")
	        print(f"Favicon: {all_data[-1]['favicon']}")
	        print(f"Saved metadata to metadata.json")

	    elif self.individual_website_response == "14":
	        website_health_check = website.health_check()
	        return Fore.GREEN + website_health_check["title"]
	    
	    elif self.individual_website_response == "15":
	        blacklist_score = website.check_blacklisting()
	        return Fore.GREEN + f"Your confidence score is {blacklist_score}"
	
