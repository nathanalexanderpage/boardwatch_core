class MatchFinder():
	def __init__(self, want):
		self.type = 'all-purpose'
		self.want = want

	def assess_match(self, result):
		match_score = 0.9
		for match_keyword_strong in self.want['match_strong']:
			if match_keyword_strong.lower() in result['title']:
				match_score *= 1.5
				break
		for match_keyword_weak in self.want['match_weak']:
			if match_keyword_weak.lower() in result['title']:
				match_score *= 1.2
				break
		return match_score

class ConsoleMatchFinder(MatchFinder):
	def __init__(self):
		self.type = 'console'

	def assess_match(self, result):
		print('this is where a match score will be calculated for consoles once the child class is filled out. for now, use parent class MatchFinder.')

if __name__ == '__main__':
	print('running ' + __file__)

	example_wants = []
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
	example_wants.append(example_want1)

	import pprint
	pp = pprint.PrettyPrinter(indent=2)
	
	result = {
		'datetime': '2019-10-16 20:08',
		'neighborhood': '(Bryant)',
		'price': 0,
		'title': 'playstation 4 pro',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-playstation-4-pro/6999023452.html'
	}

	pp.pprint(example_want1)
	matcher = MatchFinder(example_want1)
	print(matcher.assess_match(result))
	# matches = [x for x in lst if fulfills_some_condition(x)]
