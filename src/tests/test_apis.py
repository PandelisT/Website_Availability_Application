import unittest
import os
import json
import requests
from website_availability import WebsiteAvailability
from scrape_website import ScrapeWebsite
from check_hash_and_ports import CheckHashAndPorts


class TestAPIs(unittest.TestCase):
    
    def test_google_page_insights_api(self):
        error = False
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        strategy="strategy_unspecified"

        try:
            page_performance = website.get_pagespeed(strategy)
        except:
            error = True

        self.assertFalse(error)
        self.assertIsInstance(page_performance[0], float)
    
    def test_signals_ip_api(self):
        error = False
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        try:
            blacklist_score = website.check_blacklisting()
        except:
            error = True

        self.assertFalse(error)
        self.assertIsInstance(blacklist_score, int)
        
    def test_Sendgrid_api(self):
        error  = False
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {"Authorization": f"{os.environ.get('SENDGRID_API')}",
                       "Content-Type": "application/json"}
            payload = {"personalizations": 
                       [{"to": [{"email": f"{os.environ.get('TEST_EMAIL')}"}]}],
                        "from": {"email": f"{os.environ.get('TEST_EMAIL')}"},
                        "subject": "Test",
                        "content": [{"type": "text/plain", "value": "Testing API"}]}
            message = requests.post(url, data=json.dumps(payload), headers=headers)
        except:
            error = True
        
        self.assertFalse(error)
