import unittest
import os
from website_availability import WebsiteAvailability
from scrape_website import ScrapeWebsite

class TestScrapeWebsiteFunctions(unittest.TestCase):
    
    def test_get_site_name(self):
        website = ScrapeWebsite("nerdypandy.com.au")
        result = website.get_site_name()
        self.assertIsInstance(result, str)
        
    def test_get_title(self):
        website = ScrapeWebsite("nerdypandy.com.au")
        result = website.get_title()
        self.assertIsInstance(result, str)

    def test_get_description(self):
        website = ScrapeWebsite("nerdypandy.com.au")
        result = website.get_description()
        self.assertIsInstance(result, str)

    def test_get_image(self):
        website = ScrapeWebsite("nerdypandy.com.au")
        result = website.get_image()
        self.assertIsInstance(result, str)
        
    def test_favicon(self):
        website = ScrapeWebsite("nerdypandy.com.au")
        result = website.get_favicon()
        self.assertIsInstance(result, str)

