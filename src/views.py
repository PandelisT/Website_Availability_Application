import requests
import os
import sys
import json
from website_availability import WebsiteAvailability
from check_hash_and_ports import CheckHashAndPorts
from scrape_website import ScrapeWebsite
from colorama import Fore
from colorama import init
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
            requests.get(f"https://{self.website_address}")
            return (isValid, Fore.GREEN + "URL is valid")
        except requests.ConnectionError:
            isValid = False
            return (isValid, Fore.RED + "URL is not valid")

    def show_options(self):
        return """\nWhat would you like to check on this website?
1. Is your website up?
2. What is the website's IP address?
3. Current HTTP status code and availability
4. Page performance using Google Page Speed Insights
5. Domain expiry and registrar
6. Server and content type
7. SSL expiry date
8. Is the domain registered?
9. Compare MD5 hash sum
10. Port scanning with Nmap
11. Ping with Nmap
12. Scrape website for metadata
13. Perform health check
14. Check bad ip score
15. Exit program\n
"""


class ChooseOptions(CheckHashAndPorts, ScrapeWebsite, View):

    def __init__(self, website_address, individual_website_response) -> None:
        self.individual_website_response = individual_website_response
        self.website_address = website_address

    def choose_options(self):

        website = WebsiteAvailability(self.website_address)

        website_hash_test = CheckHashAndPorts(self.website_address)

        if self.individual_website_response == "15":
            print("*"*32)
            print(Fore.GREEN + "Exited the program successfully")
            print("*"*32)
            sys.exit()

        elif self.individual_website_response == "2":
            try:
                ip_address = website.get_ip_address()
                return Fore.GREEN + f"The IP address of this website is {ip_address}"
            except Exception:
                return "Unable to get IP address"

        elif self.individual_website_response == "3":
            try:
                http_status_code = website.get_http_status_code()
                return Fore.GREEN + f"The HTTP status code is {http_status_code[0]}: {http_status_code[1]}"
            except Exception:
                return "Unable to get HTTP status code"
                
        elif self.individual_website_response == "4":
            print("*"*50)
            print("Page performance is the overall performance score.")
            print("First Meaningful Paint measures when the primary content is visible.")
            print("Speed Index shows how quickly the page is populated.")
            print("Time to interactive is time it takes to become fully interactive.")
            print("*"*50)
            try: 
                strategy = "strategy_unspecified"
                page_performance = website.get_pagespeed(strategy)
                return Fore.GREEN + f"Your page performance is {page_performance[0]}, First Meaningful Paint: {page_performance[1]}, Speed Index: {page_performance[2]},  Time To Interactive: {page_performance[3]}"
            except Exception:
                return "Unable to get data"
                
        elif self.individual_website_response == "5":
            try:
                whois_status = website.check_whois_status()
                return Fore.GREEN + f"Expiration date: {whois_status[0]}, Registrar: {whois_status[1]}"
            except Exception:
                return "Unable to get Expiration date or registrar"

        elif self.individual_website_response == "6":
            try:
                server_and_content_type = website.get_server_and_content_type()
                return Fore.GREEN + f"Server: {server_and_content_type[0]}, Content type: {server_and_content_type[1]}"
            except Exception:
                return "Unable to get server and content type"
                
        elif self.individual_website_response == "7":
            try:
                ssl_expiry = website.ssl_expiry_datetime()
                return Fore.GREEN + f"Expiration date of SSL certificate: {ssl_expiry}"
            except Exception:
                return "Unable to get expiration dat of SSL"

        elif self.individual_website_response == "8":
            try:
                domain_name_is_registered = website.is_registered()
                if domain_name_is_registered is True:
                    return (Fore.GREEN + "Domain name is registered")
                elif domain_name_is_registered is False:
                    return Fore.RED + "Domain name is not registered"
            except Exception:
                return "Cannot find if domain is registered"

        elif self.individual_website_response == "9":
            try:
                website_hash = website_hash_test.check_hash()
                return Fore.GREEN + f"{website_hash}"
            except Exception:
                return "Cannot get MD5 sum"

        elif self.individual_website_response == "10":
            try:
                port_scan = website_hash_test.nmap_port_scanning()
                return Fore.GREEN + f"{port_scan}"
            except:
                return "Unable to do port scan"

        elif self.individual_website_response == "11" or self.individual_website_response == "1":
            try:
                nmap_ping = website_hash_test.nmap_ping_scanning()
                return Fore.GREEN + f"The website is {nmap_ping}"
            except Exception:
                return "Unable to ping website"

        elif self.individual_website_response == "12":
            try:
                website_scrape = ScrapeWebsite(self.website_address)
                json_metadata = website_scrape.return_page_metadata()
                all_data = website_scrape.all_metadata()
                print(Fore.GREEN + f"Title: {all_data[-1]['title']}")
                print(Fore.GREEN + f"Sitename: {all_data[-1]['sitename']}")
                print(Fore.GREEN + f"Description: {all_data[-1]['description']}")
                print(Fore.GREEN + f"Image: {all_data[-1]['image']}")
                print(Fore.GREEN + f"Favicon: {all_data[-1]['favicon']}")
                return Fore.GREEN + "Saved metadata to metadata.json"
            except Exception:
                return "Unable to retrieve metadata"

        elif self.individual_website_response == "13":
            try:
                print("Performing health check. Please be patient.")
                website_health_check = website.health_check()
                url = "https://api.sendgrid.com/v3/mail/send"
                headers = {"Authorization": f"{os.environ.get('SENDGRID_API')}",
                           "Content-Type": "application/json"}
                payload = {"personalizations": 
                           [{"to": [{"email": f"{os.environ.get('TEST_EMAIL')}"}]}],
                           "from": {"email": f"{os.environ.get('TEST_EMAIL')}"},
                           "subject": "Health Check Status Report",
                           "content": [{"type": "text/plain", "value": f"Your page performance is: {website_health_check[0]}, HTTP Status: {website_health_check[1]}, Blacklisting score is: {website_health_check[2]}"}]}
                message = requests.post(url, data=json.dumps(payload), headers=headers)
                return Fore.GREEN + f"Your page performance is: {website_health_check[0]}, HTTP Status: {website_health_check[1]}, Blacklisting score is: {website_health_check[2]}"
            except Exception:
                return "Unable to perform health check"
                
        elif self.individual_website_response == "14":
            try:
                blacklist_score = website.check_blacklisting()
                return Fore.GREEN + f"Your confidence score is {blacklist_score}"
            except Exception:
                return "Unable to get blacklist score"
        
        else:
            return Fore.RED + "That wasn't an option, try again."
