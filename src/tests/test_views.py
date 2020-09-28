import unittest
import os
from colorama import Fore
from colorama import init
init(autoreset=True)
from views import View
from website_availability import WebsiteAvailability

class TestViewsFunctions(unittest.TestCase):
    
    def test_get_website(self):
        website = View("sdfgsdfhsfh")
        result = website.get_website()
        self.assertFalse(result[0])

        website = View(os.environ.get("TEST_DOMAIN"))
        result = website.get_website()
        self.assertTrue(result[0])

        website_address = f"https://{os.environ.get('TEST_DOMAIN')}"
        website = View(website_address)
        result = website.get_website()
        self.assertTrue(result[0])

        website_address = f"http://{os.environ.get('TEST_DOMAIN')}"
        website = View(website_address)
        result = website.get_website()
        self.assertTrue(result[0])
