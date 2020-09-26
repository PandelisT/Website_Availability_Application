import hashlib
from urllib.request import urlopen
import nmap3
from website_availability import WebsiteAvailability


class CheckHashAndPorts(WebsiteAvailability):

	"""Comparing MD5 Hash sum"""
	def check_hash(self) -> str:
		url = f"https://{self.website_address}"
		response = urlopen(url).read()
		newHash = hashlib.sha224(response).hexdigest()

		from data import Data
		file_path = "hash.json"
		saved_hashes = self.all_hashes()
		for website_hash in saved_hashes:
			if website_hash['title'] == self.website_address:
				if website_hash['hash'] == newHash:
					return "Same hash!"
				else:
					return "Website may be hacked!"
			if website_hash['title'] != self.website_address:
				pass

		new_hash = {"title": self.website_address, "hash": newHash}
		saved_hashes.append(new_hash)
		Data.save(file_path, saved_hashes)
		return "Added to file"

	    	
	def all_hashes(self):
	    from data import Data
	    file_path = "hash.json"
	    return Data.load(file_path)
	
	"""Nmap analysis of ports, pinging and tcp scan"""
	def nmap_port_scanning(self) -> str:
		nmap = nmap3.Nmap()
		results = nmap.scan_top_ports(f"{self.website_address}")
		ip_address = self.get_ip_address()
		for port in results[ip_address]:
			if port['state'] == "open":
				print(f"Port {port['portid']}: {port['state']}")
		return "Completed"
				
	def nmap_ping_scanning(self) -> str:
		nmap = nmap3.NmapScanTechniques()
		ip_address = self.get_ip_address()
		result = nmap.nmap_ping_scan(ip_address)
		return result[0]['state']

