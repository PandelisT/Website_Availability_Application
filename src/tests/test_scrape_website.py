import unittest
import os
from src.website_availability import WebsiteAvailability
from src.scrape_website import ScrapeWebsite

class TestScrapeWebsiteFunctions(unittest.TestCase):
    def test_get_site_name(self):
        website = ScrapeWebsite("sydneyhearingclinic.com.au")
        result = website.get_site_name()
        self.assertIsInstance(result, str)