import unittest
from src.website_availability import WebsiteAvailability
from src.scrape_website import ScrapeWebsite


class TestWebsiteAvailabilityFunctions(unittest.TestCase):
    def test_get_ip_address(self):
        result = WebsiteAvailability.get_ip_address("nerdypandy.com.au")
        self.assertEqual(result, "The IP address of this website is 149.28.188.138")
        
class TestScrapeWebsiteFunctions(unittest.TestCase):
    def test_get_site_name(self):
        result = ScrapeWebsite.get_site_name("nerdypandy.com.au")
        
        self.assertEqual(result, "Nerdy Pandy")
