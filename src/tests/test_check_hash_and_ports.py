import unittest
import os
from website_availability import WebsiteAvailability
from scrape_website import ScrapeWebsite
from check_hash_and_ports import CheckHashAndPorts

class TestCheckHashAndPortsFunctions(unittest.TestCase):
    
    def test_get_site_name(self):
        website_hash_test = CheckHashAndPorts("nerdypandy.com.au")
        website_hash = website_hash_test.check_hash()
        self.assertIsInstance(website_hash, str)

    def test_nmap_port_scanning(self):
        website_hash_test = CheckHashAndPorts("nerdypandy.com.au")
        port_scan = website_hash_test.nmap_port_scanning()
        self.assertIsInstance(port_scan, str)
    
    def test_nmap_ping_scanning(self):
        website_hash_test = CheckHashAndPorts("nerdypandy.com.au")
        nmap_ping = website_hash_test.nmap_ping_scanning()
        self.assertIsInstance(nmap_ping, str)
        self.assertEqual(nmap_ping, "up" or "down")
        