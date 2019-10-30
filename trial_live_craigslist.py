import pprint
from console_data_resource import *
from match_finder import *
from scraper import *

pp = pprint.PrettyPrinter(indent=2)

console_to_test = ps1

cl_scraper = CraigslistScraper()
test_response = cl_scraper.search('video_games').content
test_parsed_results = cl_scraper.parse_search_response(test_response)
pp.pprint(test_parsed_results)
pp.pprint(console_to_test)
matcher = ConsoleMatchFinder(console_to_test, {})
matches = []
for result in test_parsed_results:
	pprint.pprint(result['title'])
	if matcher.assess_match(result):
		matches.append(result)
# matches = [result for result in test_parsed_results if matcher.assess_match(result)]

for match in matches:
	print(match['title'])
