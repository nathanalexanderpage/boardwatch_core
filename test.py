from match_finder import *
import pprint
from scraper import *

pp = pprint.PrettyPrinter(indent=2)

example_want1 = {
	'item': 'PlayStation 4',
	'type': 'console',
	'company': 'Sony',
	'match_strong': [
		'PS4',
		'PlayStation 4',
		'PlayStation4',
		'Play Station 4',
		'PS 4'
	],
	'match_weak': [
		'PlayStation',
		'Play Station',
		'PS'
	]
}


cl_scraper = CraigslistScraper()
test_response = cl_scraper.search('video_games').content
test_parsed_results = cl_scraper.parse_search_response(test_response)
pp.pprint(test_parsed_results)
pp.pprint(example_want1)
matcher = MatchFinder(example_want1)
matches = []
for result in test_parsed_results:
	if matcher.assess_match(result) > 1:
		matches.append(result)

pp.pprint(matches)
