import unittest
import os
import datetime
from website_availability import WebsiteAvailability

class TestWebsiteAvailabilityFunctions(unittest.TestCase):
    
    website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
    
    def test_get_ip_address(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        ip_address = website.get_ip_address()
        self.assertIsInstance(ip_address, str)
        self.assertEqual(ip_address, os.environ.get("TEST_IP_ADDRESS"))
        
    def test_get_http_status_code(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        http_status_code = website.get_http_status_code()
        self.assertIsInstance(http_status_code, tuple)
        self.assertTrue(len(http_status_code)==2)
        self.assertTrue(type(http_status_code[0]) is int and type(http_status_code[1]) is str)
        
    def test_get_server_and_content_type(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        server_and_content_type = website.get_server_and_content_type()
        self.assertIsInstance(server_and_content_type, tuple)
        self.assertTrue(len(server_and_content_type)==2)
        self.assertTrue(type(server_and_content_type[0]) and type(server_and_content_type[1]) is str)
        
    def test_check_whois_status(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        whois_status = website.check_whois_status()
        self.assertIsInstance(whois_status, tuple)
        self.assertTrue(len(whois_status)==2)
    
    def test_get_pagespeed(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        strategy = "strategy_unspecified"
        page_performance = website.get_pagespeed(strategy)
        self.assertIsInstance(page_performance, tuple)
        self.assertTrue(len(page_performance)==4)
        self.assertTrue(type(page_performance[0]) is float and type(page_performance[1]) and type(page_performance[2]) and type(page_performance[3]) is str)
        
    def test_is_registered(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        domain_name_is_registered = website.is_registered()
        self.assertIsInstance(domain_name_is_registered, bool)
        
    def test_ssl_expiry_datetime(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        ssl_expiry = website.ssl_expiry_datetime()
        self.assertIsInstance(ssl_expiry, datetime.datetime)
    
    def test_health_check(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        website_health_check = website.health_check()
        self.assertIsInstance(website_health_check, tuple)
        self.assertTrue(len(website_health_check)==3)
        self.assertTrue(type(website_health_check[0]) is float and type(website_health_check[1]) is int and type(website_health_check[2] is int) )

    def test_check_blacklisting(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        blacklist_score = website.check_blacklisting()
        self.assertIsInstance(blacklist_score, int)
