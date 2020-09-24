import unittest
from website_availability import WebsiteAvailability
from scrape_website import ScrapeWebsite


class TestWebsiteAvailabilityFunctions(unittest.TestCase):
    
    def test_get_ip_address(self):
        website = WebsiteAvailability("nerdypandy.com.au") #Environemnt variables for domains
        ip_address = website.get_ip_address()
        self.assertEqual(ip_address, "149.28.188.138") #Environemnt variables for domains
        
    def test_get_http_status_code(self):
        website = WebsiteAvailability("nerdypandy.com.au")
        http_status_code = website.get_http_status_code()
        self.assertEqual(http_status_code, "200: Available" or "Unavailable" or "No Internet")
        
class TestScrapeWebsiteFunctions(unittest.TestCase):
    def test_get_site_name(self):
        website = ScrapeWebsite("nerdypandy.com.au")
        result = website.get_site_name()
        self.assertEqual(result, "Nerdy Pandy") # test that it is a string
