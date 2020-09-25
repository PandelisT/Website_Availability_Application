import unittest
import os
from website_availability import WebsiteAvailability

class TestWebsiteAvailabilityFunctions(unittest.TestCase):
    
    def test_get_ip_address(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        ip_address = website.get_ip_address()
        
        self.assertIsInstance(ip_address, str)
        
        self.assertEqual(ip_address, os.environ.get("TEST_IP_ADDRESS"))
        
    def test_get_http_status_code(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        http_status_code = website.get_http_status_code()
        
        self.assertIsInstance(http_status_code, tuple)
        
    def test_check_whois_status(self):
        website = WebsiteAvailability(os.environ.get("TEST_DOMAIN"))
        server_and_content_type = website.get_server_and_content_type()
        
        self.assertIsInstance(server_and_content_type, tuple)
