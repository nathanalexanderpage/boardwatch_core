from match_finder import *
import pprint
from scraper import *
from console_data_resource import *

pp = pprint.PrettyPrinter(indent=2)

cl_scraper = CraigslistScraper()
test_response = cl_scraper.search('video_games').content
test_parsed_results = cl_scraper.parse_search_response(test_response)
pp.pprint(test_parsed_results)
pp.pprint(ps4)
matcher = ConsoleMatchFinder(ps4, {})
matches = []
for result in test_parsed_results:
	pprint.pprint(result['title'])
	if matcher.assess_match(result) >= matcher.MATCH_SCORE_THRESHOLD:
		matches.append(result)

for match in matches:
	print(match['title'])
	print(match['price'])