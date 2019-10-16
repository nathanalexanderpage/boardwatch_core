import requests
from bs4 import BeautifulSoup

class Scraper():
	def __init__(self):
		self.finished = False
		self.error = {
			'has_error': False,
			'error_message': None
		}

	def mark_finished(self):
		self.finished = True

	def request_get(self, url):
		return requests.get(url)

class CraigslistScraper(Scraper):
	def __init__(self):
		self.finished = False
		self.site = 'craigslist'
		self.url_base = 'https://seattle.craigslist.org/'
		self.url_search_base = 'search/'
		self.url_search_extensions = {
			'video_games': 'vga/'
		}
	
	def build_search_url(self, section):
		return self.url_base + self.url_search_base + self.url_search_extensions[section]

	def search(self, section):
		search_url = self.build_search_url(section)
		return self.request_get(search_url)

	def parse_search_response(self, html_response):
		soup = BeautifulSoup(html_response, 'html.parser')
		soup = soup.find(id='sortable-results')
		print(soup.prettify())

if __name__ == '__main__':
	cl_scraper = CraigslistScraper()
	cl_scraper.parse_search_response(cl_scraper.search('video_games').content)
