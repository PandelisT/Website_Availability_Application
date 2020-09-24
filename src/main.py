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
from views import View
from views import ChooseOptions

if "--help" in sys.argv:
    f.instructions()
    time.sleep(10)
else:
    pass

"""Welcome Message"""
print(72*"*")
print(Fore.GREEN + "Welcome to the Website Availability Python Terminal Application (WAPTA)!")
print(72*"*")

"""Loop to check user input"""	
while True:
		website_address = input("Which website would you like to check? ")
		get_new_website = View(website_address)
		new_website = get_new_website.get_website()
		print("*"*40)
		print(new_website[1])
		print("*"*40)
		
		if new_website[0] == True:
			break
		elif new_website[0] == False:
			continue
		
"""Looping through options"""
while True: 
	get_new_website = View(website_address)	
	options = get_new_website.show_options()
	individual_website_response = input(options)
	option = ChooseOptions(website_address, individual_website_response)
	print(option.choose_options())
	time.sleep(3)