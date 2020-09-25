import unittest
import os
from src.website_availability import WebsiteAvailability

class TestWebsiteAvailabilityFunctions(unittest.TestCase):
    
    def test_get_ip_address(self):
        website = WebsiteAvailability("nerdypandy.com.au") # os.environ.get("TEST_DOMAIN")
        ip_address = website.get_ip_address()
        
        self.assertIsInstance(ip_address, str)
        
        self.assertEqual(ip_address, "149.28.188.138" ) # os.environ.get("TEST_IP_ADDRESS")
        
    def test_get_http_status_code(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        http_status_code = website.get_http_status_code()
        
        self.assertIsInstance(http_status_code, tuple)
        
    def test_check_whois_status(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        server_and_content_type = website.get_server_and_content_type()
        
        self.assertIsInstance(server_and_content_type, tuple)
