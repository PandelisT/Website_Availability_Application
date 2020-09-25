import requests
from bs4 import BeautifulSoup
import random
from website_availability import WebsiteAvailability


"""Scrape metadata from target URL."""
class ScrapeWebsite(WebsiteAvailability):

	def __init__(self, website_address) -> None:
		self.website_address = website_address
		
	@staticmethod
	def list_headers() -> dict:
		headers = {
	        'Access-Control-Allow-Origin': '*',
	        'Access-Control-Allow-Methods': 'GET',
	        'Access-Control-Allow-Headers': 'Content-Type',
	        'Access-Control-Max-Age': '3600',
	        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
	    }
		return headers	

	def get_response(self) -> str:
		header = ScrapeWebsite.list_headers()
		url = f"https://{self.website_address}"
		response = requests.get(url, headers=header)
		return response
	
	def get_html(self) -> str:
		r = self.get_response()
		html = BeautifulSoup(r.content, "html.parser")
		return html

	def get_title(self) -> str:
	    html = self.get_html()
	    self.title = html.title.string
	    return self.title
	
	def get_description(self) -> str:
	    html = self.get_html()
	    description = None
	    if html.find("meta", property="description"):
	        description = html.find("meta", property="description").get('content')
	    elif html.find("meta", property="og:description"):
	        description = html.find("meta", property="og:description").get('content')
	    return description
	
	def get_image(self) -> str:
	    image = None
	    html = self.get_html()
	    if html.find("meta", property="image"):
	        image = html.find("meta", property="image").get('content')
	    return image
	
	def get_site_name(self) -> str:
	    html = self.get_html()
	    return html.find("meta", property="og:site_name").get('content')
	
	def get_favicon(self) -> str:
		html = self.get_html()
		return html.find("link", attrs={"rel": "icon"}).get('href')
	    
	def return_page_metadata(self) -> None:
	    from data import Data
	    file_path = "metadata.json"
	    saved_metadata = self.all_metadata()
	    
	    new_metadata = {
	        "title": self.get_title(),
	        "description": self.get_description(),
	        "image": self.get_image(),
	        "favicon": self.get_favicon(),
	        "sitename":  self.get_site_name(),
	        }
	    
	    saved_metadata.append(new_metadata)
	    Data.save(file_path, saved_metadata) 
	    return "Added to file"
	
	def all_metadata(self):
	    from data import Data
	    file_path = "metadata.json"
	    return Data.load(file_path)