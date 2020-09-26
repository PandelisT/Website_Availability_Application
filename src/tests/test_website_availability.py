import unittest
import os
import datetime
from website_availability import WebsiteAvailability

class TestWebsiteAvailabilityFunctions(unittest.TestCase):
    
    website = WebsiteAvailability("nerdypandy.com.au")
    
    def test_get_ip_address(self):
        website = WebsiteAvailability("nerdypandy.com.au") # os.environ.get("TEST_DOMAIN")
        ip_address = website.get_ip_address()
        self.assertIsInstance(ip_address, str)
        self.assertEqual(ip_address, "149.28.188.138" ) # os.environ.get("TEST_IP_ADDRESS")
        
    def test_get_http_status_code(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        http_status_code = website.get_http_status_code()
        self.assertIsInstance(http_status_code, tuple)
        self.assertTrue(len(http_status_code)==2)
        self.assertTrue(type(http_status_code[0]) is int and type(http_status_code[1]) is str)
        
    def test_get_server_and_content_type(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        server_and_content_type = website.get_server_and_content_type()
        
        self.assertIsInstance(server_and_content_type, tuple)
        self.assertTrue(len(server_and_content_type)==2)
        self.assertTrue(type(server_and_content_type[0]) and type(server_and_content_type[1]) is str)
        
    def test_check_whois_status(self):
        website = WebsiteAvailability("sydneyhearingclinic.com.au")
        whois_status = website.check_whois_status()
        self.assertIsInstance(whois_status, tuple)
        self.assertTrue(len(whois_status)==2)
    
    # def test_get_pagespeed(self):
    #     website = WebsiteAvailability("nerdypandy.com.au")
    #     strategy = "strategy_unspecified"
    #     page_performance = website.get_pagespeed(strategy)
    #     self.assertIsInstance(page_performance, tuple)
    #     self.assertTrue(len(page_performance)==4)
    #     self.assertTrue(type(page_performance[0]) is float and type(page_performance[1]) and type(page_performance[2]) and type(page_performance[3]) is str)
        
    def test_is_registered(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        domain_name_is_registered = website.is_registered()
        self.assertIsInstance(domain_name_is_registered, bool)
        
    def test_ssl_expiry_datetime(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        ssl_expiry = website.ssl_expiry_datetime()
        self.assertIsInstance(ssl_expiry, datetime.datetime)
    
    # def test_health_check(self):
    #     website = WebsiteAvailability("nerdypandy.com.au")
    #     website_health_check = website.health_check()
    #     self.assertIsInstance(website_health_check, tuple)
    #     self.assertTrue(len(website_health_check)==3)
    #     self.assertTrue(type(website_health_check[0]) is float and type(website_health_check[1]) is int and type(website_health_check[2] is int) )

    # def test_check_blacklisting(self):
    #     website = WebsiteAvailability("nerdypandy.com.au")
    #     blacklist_score = website.check_blacklisting()
    #     self.assertIsInstance(blacklist_score, int)