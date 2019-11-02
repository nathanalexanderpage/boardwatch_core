import requests
from result_parser import *
from bs4 import BeautifulSoup

class Scraper():
	def __init__(self):
		self.finished = False
		self.error = {
			'has_error': False,
			'error_message': None
		}
		self.def_self_attr()
	
	def __str__(self):
		string = '<Scraper Object (Generic)>'
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
		print('requesting response...')
		return requests.get(self.build_search_url())

	def process_response(self, response):
		print(response)
		if response.status_code >= 200 & response.status_code < 300:
			print('good status code.')
			soup = self.get_soup(response.content)
			return self.parse_search_response(soup)
		else:
			raise Exception('Site connection was unsuccessful in some way. Check error message for details.')

	def get_soup(self, html_response):
		return BeautifulSoup(html_response, 'html.parser')

	def scrape(self):
		if not self.build_search_url():
			print('No scrape URL.')
			raise Exception('No URL to use in scraping. Terminating program.')
		else:
			print('scraping...')
			return self.process_response(self.request_response())

class CraigslistScraper(Scraper):
	def def_self_attr(self):
		self.site = 'craigslist'
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
			result_data = CraigslistResultScraper(result)
			results_data.append(result_data.data)
		print(results_data)
		return results_data

class CraigslistPostScraper(Scraper):
	def def_self_attr(self):
		self.site = None
		self.url = None

	def parse_search_response(self, soup):
		mapbox = soup.find(id='map')
		map_longitude = mapbox['data-longitude']
		print(map_longitude)
		map_latitude = mapbox['data-latitude']
		print(map_latitude)
		map_data_accuracy_score = mapbox['data-accuracy']
		print(map_data_accuracy_score)
		pix = soup.find_all(class_='thumb')
		pics = []
		for pic in pix:
			pics.append(pic['href'])
		print(pics)
		attrs = soup.find(class_='attrgroup').find_all('span')
		condition = None
		manufacturer = None
		model = None
		for attr in attrs:
			if attr.name == 'span':
				if 'condition:' in attr.text:
					condition = attr.find('b').text.strip()
					print(condition)
				if 'make / manufacturer:' in attr.text:
					manufacturer = attr.find('b').text.strip()
					print(manufacturer)
				if 'model name / number:' in attr.text:
					model = attr.find('b').text.strip()
					print(model)
		posting_body = soup.find(id='postingbody')
		qr_code_text = posting_body.find(class_='print-information print-qrcode-container').text
		post_text = posting_body.text[len(qr_code_text):].strip()
		print(post_text)
		post_info_tags = soup.find_all(class_='postinginfo')
		post_id = None
		for tag in post_info_tags:
			if tag.name == 'p':
				if 'post id:' in tag.text:
					post_id = tag.text[len('post id:'):].strip()
		print(post_id)
		return post_id
	
if __name__ == '__main__':
	print('running ' + __file__)

	import pprint
	pp = pprint.PrettyPrinter(indent=2)

	# cl_scraper = CraigslistScraper()
	# test_response = cl_scraper.request_get().content
	# test_parsed_results = cl_scraper.parse_search_response(test_response)
	# pp.pprint(test_parsed_results)

	single_post_scraper = CraigslistPostScraper()
	single_post_scraper.set_url('https://seattle.craigslist.org/see/vgm/d/seattle-3ds-fire-emblem-echoes-limited/6992105694.html')
	data = single_post_scraper.scrape()
