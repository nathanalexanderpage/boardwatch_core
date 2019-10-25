class MatchFinder():
	"""parent match finder class -- mostly for rules inheritance; not to be used to find actual matches"""

	# class variables
	MATCH_SCORE_THRESHOLD = 2

	def __init__(self, want, config):
		self.want = want
		self.config = config
		self.def_self_attr(self)

	def def_self_attr(self):
		self.type = 'generic'
		self.attr = 'this is a catch-all function for the parent class; usually, this is where child classes define instance attributes that are specific to each child class'

	def assess_match(self, result):
		match_score = 0.9
		title_compare = result['title'].lower()
		for match_keyword_strong in self.want['match_strong']:
			if match_keyword_strong.lower() in title_compare:
				match_score *= 1.5
				break
		for match_keyword_weak in self.want['match_weak']:
			if match_keyword_weak.lower() in title_compare:
				match_score *= 1.2
				break
		return match_score

class ConsoleMatchFinder(MatchFinder):
	"""for finding consoles"""
	
	def def_self_attr(self):
		self.avoid = {
			'anywhere': [
				'I will'
			],
			'before': {
				'space_separated_yes': [
					'for',
					'broken',
					'buying'
				]
			}
		}
		self.name_group_members = list(filter(lambda console: console['name_group'] == self.want['name_group'], consoles))

	def assess_match(self, result):
		print('this is where a match score will be calculated for consoles once the child class is filled out. for now, use parent class MatchFinder.')

if __name__ == '__main__':
	print('running ' + __file__)

	import pprint
	from console_data_resource import *
	
	pp = pprint.PrettyPrinter(indent=2)
	
	result = {
		'datetime': '2019-10-16 20:08',
		'neighborhood': '(Bryant)',
		'price': 0,
		'title': 'playstation 4 pro',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-playstation-4-pro/6999023452.html'
	}

	config = {
		'price_point': 100
	}

	pp.pprint(consoles)
	matcher = MatchFinder(ps4)
	print(matcher.assess_match(result))
	# matches = [x for x in lst if fulfills_some_condition(x)]
