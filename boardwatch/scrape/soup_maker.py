import pprint

from boardwatch_models import Listing
from bs4 import BeautifulSoup
import requests

from boardwatch.scrape import scraper

class SoupMaker():
	def __init__(self):
		self.finished = False
		self.error = {
			'has_error': False,
			'error_message': None
		}
		self.def_self_attr()
	
	def __str__(self):
		string = '<SoupMaker Object (Generic)>'
		if self.url and len(self.url) > 0:
			string = string + ' ' + self.url
		return string

	def def_self_attr(self):
		self.site = None
		self.url = None

	def build_search_url(self):
		if self.url:
			return self.url
		else:
			return None

	def set_url(self, url):
		self.url = url

	def set_site(self, site):
		self.site = site

	def mark_finished(self):
		self.finished = True

	def request_get(self):
		return requests.get(self.build_search_url())

	def request_response(self):
		print('requesting response... from ' + self.build_search_url())
		return requests.get(self.build_search_url())

	def parse_search_response(self, soup):
		return soup

	def process_response(self, response):
		print(response)
		if response.status_code >= 200 & response.status_code < 300:
			print('good status code.')
			soup = self.get_soup(response.content)
			return self.parse_search_response(soup)
		else:
			raise Exception('Site connection was unsuccessful. Check error message for details.')

	def get_soup(self, html_response):
		return BeautifulSoup(html_response, 'html.parser')

	def make_soup(self):
		if not self.build_search_url():
			print('No scrape URL.')
			raise Exception('No URL to use in scraping. Terminating program.')
		else:
			print('scraping...')
			return self.process_response(self.request_response())

class CraigslistSoupMaker(SoupMaker):
	def def_self_attr(self):
		self.site = 'Craigslist'
		self.url_base = 'https://seattle.craigslist.org/'
		self.url_search_base = 'search/'
		self.url_search_extensions = {
			'video_games': 'vga/'
		}
	
	def build_search_url(self):
		print('building search URL...')
		print(self.url_base + self.url_search_base + self.url_search_extensions['video_games'])
		return self.url_base + self.url_search_base + self.url_search_extensions['video_games']

	def parse_search_response(self, soup):
		results = soup.find(id='sortable-results').ul.find_all('li')
		
		results_data = []
		for result in results:
			result_data = scraper.CraigslistResultScraper(result)
			# listing = Listing(id=None, native_id=result_data.data['id'], title=result_data.data['title'], body=result_data.data['body'], url=result_data.data['url'], seller_email=result_data.data['seller_email'], seller_phone=result_data.data['seller_phone'], date_posted=result_data.data['datetime'], date_scraped=None)
			results_data.append(result_data.data)
		# print(results_data)
		return results_data

class CraigslistPostSoupMaker(SoupMaker):
	def def_self_attr(self):
		self.site = 'Craigslist'
		self.url = None

	def parse_search_response(self, soup):
		return soup.find(class_='body')
	
if __name__ == '__main__':
	print('running ' + __file__)

	import pprint
	pp = pprint.PrettyPrinter(indent=2)

	# cl_scraper = CraigslistSoupMaker()
	# test_response = cl_scraper.request_get().content
	# test_parsed_results = cl_scraper.parse_search_response(test_response)
	# pp.pprint(test_parsed_results)

	single_post_scraper = SoupMaker()
	no_img_url = 'https://seattle.craigslist.org/see/vgm/d/woodinville-game-boy-and-games/7011448918.html'
	single_img_url = 'https://seattle.craigslist.org/see/vgm/d/seattle-3ds-fire-emblem-echoes-limited/6992105694.html'
	multi_img_url = 'https://seattle.craigslist.org/see/vgm/d/seattle-nintendo-switch-lot/7011771234.html'
	single_post_scraper.set_url(single_img_url)
	data = single_post_scraper.make_soup()
