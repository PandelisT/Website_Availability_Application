import sys
import time
import requests

from website_availability import WebsiteAvailability
from check_hash_and_ports import CheckHashAndPorts
from scrape_website import ScrapeWebsite
from notifications import Notifications
from functions import instructions


if "--help" in sys.argv:
    instructions()
    time.sleep(10)
else:
    pass
    
print(70*"*")
print("Welcome to the Website Availability Python Terminal Application (WAPTA)!")
print(70*"*")

website_address = input("Which website would you like to check? ")


try:
	if website_address[0:8] == "https://":
		website_address = website_address[8:]
	elif website_address[0:7] == "http://":
		website_address = website_address[7:]
		response = requests.get(f"https://{website_address}")
	print("*"*40)
	print("URL is valid and exists on the internet")
	print("*"*40)
except requests.ConnectionError as exception:
	print("*"*40)
	print("URL does not exist on the internet")
	print("*"*40)
	
while True: 
	
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
	
	# elif individual_website_response == "1":
	# 	website = WebsiteAvailability(website_address)
	# 	ip_address = website.get_ping()
	# 	print(f"The IP address of this website is {ip_address}")
	# 	continue
	
	elif individual_website_response == "2":
		website = WebsiteAvailability(website_address)
		ip_address = website.get_ip_address()
		print(f"The IP address of this website is {ip_address}")
		continue	
		
	elif individual_website_response == "3":
		website = WebsiteAvailability(website_address)
		http_status_code = website.get_http_status_code()
		print(f"The HTTP status code is {http_status_code}")
		continue
	
	elif individual_website_response == "4":
	    strategy = "strategy_unspecified"
	    website = WebsiteAvailability(website_address)
	    page_speed = website.get_pagespeed(strategy)
	    print(f"Your page speed is {page_speed}")
	    continue
	    
	elif individual_website_response == "5":
	    website = WebsiteAvailability(website_address)
	    whois_status = website.check_whois_status()
	    print(f"{whois_status}")
	    continue
	    
	elif individual_website_response == "6":
	    website = WebsiteAvailability(website_address)
	    server_and_content_type = website.get_server_and_content_type()
	    print(f"{server_and_content_type}") 
	    continue
	
	elif individual_website_response == "7":
		website = WebsiteAvailability(website_address)
		ssl_expiry = website.ssl_expiry_datetime()
		print(f"{ssl_expiry}") 
		continue
	
	elif individual_website_response == "8":
		website = WebsiteAvailability(website_address)
		website_is_registered = website.is_registered()
		print(f"{website_is_registered}")
		
	elif individual_website_response == "9":
	    website = CheckHashAndPorts(website_address)
	    website_hash = website.check_hash()
	    print(f"{website_hash}")
	    continue
	
	elif individual_website_response == "10":
	    website = CheckHashAndPorts(website_address)
	    port_scan = website.nmap_port_scanning()
	    print(f"{port_scan}")
	    continue
	
	elif individual_website_response == "11":
	    website = CheckHashAndPorts(website_address)
	    nmap_ping = website.nmap_ping_scanning()
	    print(f"{nmap_ping}")
	    continue
	    
	elif individual_website_response == "12":
	    website = CheckHashAndPorts(website_address)
	    tcp_scan = website.nmap_tcp_scanning()
	    print(f"{tcp_scan}")
	    continue
	
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
	    continue
	    
	elif individual_website_response == "14":
		website = WebsiteAvailability(website_address)
		website_health_check = website.health_check()
		print(website_health_check["title"])
		continue
	
	elif individual_website_response == "15":
		website = WebsiteAvailability(website_address)
		blacklist_score = website.check_blacklisting()
		print(blacklist_score)
		continue
	