import unittest
import os
from website_availability import WebsiteAvailability
from scrape_website import ScrapeWebsite
from check_hash_and_ports import CheckHashAndPorts

class TestAPIs(unittest.TestCase):
    
    def test_google_page_insights_api(self):
        error = False
        website = WebsiteAvailability("nerdypandy.com.au")
        strategy="strategy_unspecified"
        
        try:
            page_performance = website.get_pagespeed(strategy)
        except:
            error = True
        
        self.assertFalse(error)
        self.assertIsInstance(page_performance[0], float)
        
    
    def test_signals_ip_api(self):
        error = False
        website = WebsiteAvailability("nerdypandy.com.au")
        try:
            blacklist_score = website.check_blacklisting()
        except:
            error = True
        
        self.assertFalse(error)
        self.assertIsInstance(blacklist_score, int)
