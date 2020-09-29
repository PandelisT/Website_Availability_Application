import socket
import os
import requests
import whois
import json
import datetime
import logging
import ssl


class WebsiteAvailability:
    def __init__(self, website_address: str) -> None:
        self.website_address = website_address

    def get_ip_address(self) -> str:
        # Returns IP address of website address
        try:
            ip_address = socket.gethostbyname(f"{self.website_address}")
            return ip_address
        except Exception:
            return "Unable to get IP Address"

    def get_http_status_code(self) -> tuple:
        # Returns HTTP status of website address
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
            return (0, "No Internet")

    def check_whois_status(self) -> tuple:
        # Returns expiration date of domain and registrar
        try:
            domain = whois.whois(f"{self.website_address}")
            return (domain.expiration_date, domain.registrar)
        except Exception:
            return ("Expiration date unavailable", "Domain registrar unavailable")

    def get_pagespeed(self, strategy: str) -> tuple:
        # Returns performance score and other metrics using the Google PageSpeed API
        try:
            Google_API_Key = os.environ.get("GOOGLE_API")
            base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
            response_url = f"{base_url}https://{self.website_address}&key={Google_API_Key}&strategy={strategy}"
            response = requests.get(response_url)
            json_data = response.json()
            score = json_data["lighthouseResult"]["categories"]["performance"]["score"]
            first_meaningful_paint = json_data["lighthouseResult"]["audits"]["first-meaningful-paint"]["displayValue"]
            speed_index = json_data["lighthouseResult"]["audits"]["speed-index"]["displayValue"]
            time_to_interactive = json_data["lighthouseResult"]["audits"]["interactive"]["displayValue"]
            return (score*100, first_meaningful_paint, speed_index, time_to_interactive)
        except KeyError:
            print("Unable to connect to Google Page Insights API.")
            return (0, "0", "0", "0")

    def is_registered(self) -> bool:
        # Returns True or False if the domain name is registered
        try:
            w = whois.whois(self.website_address)
            return bool(w.domain_name)
        except Exception:
            return False

    def get_server_and_content_type(self) -> tuple:
        # Returns server and content type of website
        try:
            resp = requests.head(f"https://{self.website_address}")
            server = resp.headers["server"]
            content_type = resp.headers["content-type"]
            return (server, content_type)
        except Exception:
            return ("Unavailable", "Unavailable")

    def ssl_expiry_datetime(self) -> datetime.datetime:
        # Returns SSL expiry date
        try:
            logger = logging.getLogger("SSLVerify")
            ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
            context = ssl.create_default_context()
            conn = context.wrap_socket(socket.socket(socket.AF_INET), 
                                       server_hostname=self.website_address)
            logger.debug(f"Connect to {self.website_address}")
            conn.connect((self.website_address, 443))
            ssl_info = conn.getpeercert()
            return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        except Exception:
            return datetime.datetime.now()

    def health_check(self) -> tuple:
        # Returns health check metrics
        try:
            strategy = "strategy_unspecified"
            page_performance = self.get_pagespeed(strategy)
            http_status = self.get_http_status_code()
            blacklisting_score = self.check_blacklisting()
            return (page_performance[0], http_status[0], blacklisting_score)
        except Exception:
            print("Unable to perform health check")
            return (0, 0, 0)

    def check_blacklisting(self) -> int:
        # Returns blacklisting score using the Signals Auth0 API"
        try:
            headers = {"x-auth-token": os.environ.get("SIGNALS_API")}
            base_url = "https://signals.api.auth0.com/v2.0/ip/"
            response_url = f"{base_url}{self.get_ip_address()}"
            response = requests.get(response_url, headers=headers)
            r = json.loads(response.text)
            return r['fullip']['baddomain']['score']
        except Exception:
            print("""Unable to check blacklisting. Possible error with Signals API if value is 1.""")
            return 1
