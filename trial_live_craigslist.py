import pprint
from console_data_resource import *
from match_finder import *
from soup_maker import *

pp = pprint.PrettyPrinter(indent=2)

console_to_test = ps4

cl_results_scraper = CraigslistSoupMaker()
test_parsed_results = cl_results_scraper.scrape()

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
