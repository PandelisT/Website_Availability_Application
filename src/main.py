import sys
import time
import requests
from colorama import Fore, init
init(autoreset=True)

from website_availability import WebsiteAvailability
from check_hash_and_ports import CheckHashAndPorts
from scrape_website import ScrapeWebsite
from notifications import Notifications
import functions as f


if "--help" in sys.argv:
    f.instructions()
    time.sleep(10)
else:
    pass
    
print(72*"*")
print(Fore.GREEN + "Welcome to the Website Availability Python Terminal Application (WAPTA)!")
print(72*"*")


while True:
	website_address = input("Which website would you like to check? ")
	
	if website_address[0:8] == "https://":
		website_address = website_address[8:]
	elif website_address[0:7] == "http://":
		website_address = website_address[7:]
	
	try:
		response = requests.get(f"https://{website_address}")
		print("*"*40)
		print(Fore.GREEN + "URL is valid and exists on the internet")
		print("*"*40)
		break
	except requests.ConnectionError as exception:
		print("*"*40)
		print(Fore.RED + "URL does not exist on the internet")
		print("*"*40)

while True: 
	
	individual_website_response = input("""\nWhat would you like to check on this website?
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
""")
			
	if individual_website_response == "16":
		print("*"*32)
		print(Fore.GREEN + "Exited the program successfully")
		print("*"*32)
		sys.exit()
	
	elif individual_website_response == "2":
		website = WebsiteAvailability(website_address)
		ip_address = website.get_ip_address()
		print(Fore.GREEN + f"The IP address of this website is {ip_address}")
		continue	
		
	elif individual_website_response == "3":
		website = WebsiteAvailability(website_address)
		http_status_code = website.get_http_status_code()
		print(Fore.GREEN + f"The HTTP status code is {http_status_code}")
		continue
	
	elif individual_website_response == "4":
	    strategy = "strategy_unspecified"
	    website = WebsiteAvailability(website_address)
	    page_speed = website.get_pagespeed(strategy)
	    print(Fore.GREEN + f"Your page speed is {page_speed}")
	    continue
	    
	elif individual_website_response == "5":
	    website = WebsiteAvailability(website_address)
	    whois_status = website.check_whois_status()
	    print(Fore.GREEN + f"{whois_status}")
	    continue
	    
	elif individual_website_response == "6":
	    website = WebsiteAvailability(website_address)
	    server_and_content_type = website.get_server_and_content_type()
	    print(Fore.GREEN + f"{server_and_content_type}") 
	    continue
	
	elif individual_website_response == "7":
		website = WebsiteAvailability(website_address)
		ssl_expiry = website.ssl_expiry_datetime()
		print(Fore.GREEN + f"Expiration date of SSL certificate: {ssl_expiry}") 
		continue
	
	elif individual_website_response == "8":
		website = WebsiteAvailability(website_address)
		domain_name_is_registered = website.is_registered()
		if domain_name_is_registered == True:
			print(Fore.GREEN + "Domain name is registered")
		elif domain_name_is_registered == False:
			print(Fore.RED + "Domain name is not registered")
		
	elif individual_website_response == "9":
	    website = CheckHashAndPorts(website_address)
	    website_hash = website.check_hash()
	    print(Fore.GREEN + f"{website_hash}")
	    continue
	
	elif individual_website_response == "10":
	    website = CheckHashAndPorts(website_address)
	    port_scan = website.nmap_port_scanning()
	    print(Fore.GREEN + f"{port_scan}")
	    continue
	
	elif individual_website_response == "11" or individual_website_response == "1":
	    website = CheckHashAndPorts(website_address)
	    nmap_ping = website.nmap_ping_scanning()
	    print(Fore.GREEN + f"{nmap_ping}")
	    continue
	    
	elif individual_website_response == "12":
	    website = CheckHashAndPorts(website_address)
	    tcp_scan = website.nmap_tcp_scanning()
	    print(Fore.GREEN + f"{tcp_scan}")
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
		print(Fore.GREEN + website_health_check["title"])
		continue
	
	elif individual_website_response == "15":
		website = WebsiteAvailability(website_address)
		blacklist_score = website.check_blacklisting()
		print(Fore.GREEN + f"{blacklist_score}")
		continue
	