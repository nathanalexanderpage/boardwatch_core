import pprint
import requests
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=2)

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
		results = soup.find(id='sortable-results').ul.find_all('li')
		results_data = []
		for result in results:
			print(result.prettify())
			result_data = {}
			title_tag = result.find(class_='result-title')
			result_data["title"] = title_tag.text.lower()
			result_data["url"] = title_tag['href']
			result_data["datetime"] = result.p.time['datetime']
			result_data["price"] = result.find(class_='result-price').text
			result_data["neighborhood"] = result.find(class_='result-hood').text
			results_data.append(result_data)
		return results_data

if __name__ == '__main__':
	cl_scraper = CraigslistScraper()
	test_response = cl_scraper.search('video_games').content
	test_parsed_results = cl_scraper.parse_search_response(test_response)
	pp.pprint(test_parsed_results)