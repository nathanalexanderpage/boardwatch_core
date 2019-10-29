from console_data_resource import *

class MatchFinder():
	"""parent match finder class -- mostly for rules inheritance; not to be used to find actual matches"""

	def __init__(self, want, config):
		self.want = want
		self.config = config
		self.match_factors = {
			'positive': {
				'exact': [],
				'strong': [],
				'weak': [],
				'minor': []
			},
			'negative': {
				'strong': [],
				'weak': [],
				'minor': []
			}
		}
		self.MATCH_SCORE_THRESHOLD = 1.5
		self.MATCH_SCORE_DEFAULT = 1

		self.MATCH_MULTIPLIER_EXACT = 5
		self.MATCH_MULTIPLIER_STRONG = 2
		self.MATCH_MULTIPLIER_WEAK = 1.5
		self.MATCH_MULTIPLIER_MINOR = 1.15

		self.def_self_attr()
		self.build_string_matches()

	def __str__(self):
		return 'MatchFinder parent class instance. To be used for testing purposes only.'

	def def_self_attr(self):
		self.type = 'generic'
		self.attr = 'this is a catch-all function for the parent class; usually, this is where child classes define instance attributes that are specific to each child class'

	def build_string_matches(self):
		print('use child class\'s')

	def assess_match(self, result):
		stop_matching = False
		match_score = 1
		title_compare = result['title'].lower()
		for match_string_exact in self.match_factors['positive']['exact']:
			if match_string_exact.lower() == title_compare:
				stop_matching = True
				match_score *= self.MATCH_MULTIPLIER_EXACT
				break
		for match_string_strong in self.match_factors['positive']['strong']:
			if stop_matching:
				break
			if match_string_strong.lower() in title_compare:
				match_score *= self.MATCH_MULTIPLIER_STRONG
				break
		for match_string_weak in self.match_factors['positive']['weak']:
			if stop_matching:
				break
			if match_string_weak.lower() in title_compare:
				match_score *= self.MATCH_MULTIPLIER_WEAK
				break
		print(str(match_score))
		return match_score

	def assess_meta_price_point(self, result):
		"""determine if match is at or below user's specified price point"""
		print('assessing price point...')
		if self.config['price_point'] == None:
			return True
		elif result['price'] > self.config['price_point']:
			return False
		else:
			return True

class ConsoleMatchFinder(MatchFinder):
	"""for finding consoles"""

	def __str__(self):
		return 'MatchFinder instance for finding ' + self.want['developer'] + ' ' + self.want['name']

	match_factors = {
		'positive': {},
		'negative': {}
	}
	
	def def_self_attr(self):
		self.avoid = {
			'anywhere': [
				'I will',
				'wanted:',
				'no console',
				'box only',
				'repairs',
				'broken',
				'busted'
			],
			'before': {
				'space_separated_yes': [
					'for',
					'for the',
					'buying',
					'your'
				],
				'space_separated_no': []
			},
			'after': {
				'space_separated_yes': [
					'for parts',
					'for pieces',
					'accessory',
					'accessories',
					'controller',
					'control',
					'pad',

				],
				'space_separated_no': []
			}
		}
		self.seek_modifiers = {
			'anywhere': [],
			'before': {
				'space_separated_yes': [],
				'space_separated_no': []
			},
			'after': {
				'space_separated_yes': [
					'with',
					'plus'
				],
				'space_separated_no': []
			}
		}
		self.conjunctions = {
			'before_or_after': {
				'positive': [
					'&',
					',',
					';',
					'.',
					'!',
					'and',
					'plus',
					'with',
					'also'
				],
				'negative': []
			},
			'before': {
				'positive': [],
				'negative': [
					'no'
				]
			},
			'after': {
				'positive': [],
				'negative': []
			}
		}
		self.name_group_members = list(filter(lambda console: console['name_group'] == self.want['name_group'], consoles))

	def build_string_matches(self):
		print('building item match profile...')

		# positive exact matches
		pos_exact = []
		pos_exact.append(self.want['name'])
		pos_exact.append(self.want['developer'] + ' ' + self.want['name'])
		if self.want['abbreviation_official']:
			pos_exact.append(self.want['abbreviation_official'])
			pos_exact.append(self.want['developer'] + ' ' + self.want['abbreviation_official'])
		for name in self.want['names_other']:
			pos_exact.append(name)
			pos_exact.append(self.want['developer'] + ' ' + name)
		for vtn in self.want['variations']:
			if vtn['model_no']:
				pos_exact.append(vtn['model_no'])
			if vtn['name']:
				pos_exact.append(self.want['name'] + ' ' + vtn['name'])
				pos_exact.append(self.want['developer'] + ' ' + self.want['name'] + ' ' + vtn['name'])
				if vtn['storage_capacity']:
					pos_exact.append(self.want['name'] + ' ' + vtn['name'] + ' ' + vtn['storage_capacity'])
					pos_exact.append(self.want['developer'] + ' ' + self.want['name'] + ' ' + vtn['name'] + ' ' + vtn['storage_capacity'])
					if self.want['abbreviation_official']:
						pos_exact.append(self.want['abbreviation_official'] + ' ' + vtn['name'] + ' ' + vtn['storage_capacity'])
				if self.want['abbreviation_official']:
					pos_exact.append(self.want['abbreviation_official'] + ' ' + vtn['name'])
					pos_exact.append(self.want['developer'] + ' ' + self.want['abbreviation_official'] + ' ' + vtn['name'])
		self.match_factors['positive']['exact'] = pos_exact

		# positive strong matches
		pos_strong = []
		pos_strong.append(self.want['developer'] + ' ' + self.want['name'] + ' console')
		if self.want['abbreviation_official']:
			pos_strong.append(self.want['developer'] + ' ' + self.want['abbreviation_official'] + ' console')
		for name in self.want['names_other']:
			pos_strong.append(self.want['developer'] + ' ' + name + ' console')
		for vtn in self.want['variations']:
			if vtn['model_no']:
				pos_strong.append(vtn['model_no'])
			if vtn['name']:
				pos_strong.append(self.want['name'] + ' ' + vtn['name'])
			if vtn['storage_capacity']:
				pos_strong.append(self.want['name'] + ' ' + vtn['storage_capacity'])
			for edn in vtn['editions']:
				if edn['name']:
					# if ':' in edn['name']:
					# 	split_edition_name = edn['name'].split(':')
					pos_strong.append(self.want['name'] + ' ' + edn['name'])
					pos_strong.append(edn['name'] + ' ' + self.want['name'])
				for color in edn['colors']:
					pos_strong.append(self.want['name'] + ' ' + color)
					pos_strong.append(color + ' ' + self.want['name'])

		self.match_factors['positive']['strong'] = pos_strong

		# positive weak matches
		pos_weak = []

		pos_weak.append(self.want['name'])
		pos_weak.append(self.want['abbreviation_official'])
		for name in self.want['names_other']:
			pos_weak.append(name)

		self.match_factors['positive']['weak'] = pos_weak

		# positive minor matches
		pos_minor = []

		pos_minor.append(self.want['developer'])

		self.match_factors['positive']['minor'] = pos_minor

		# negative strong matches
		neg_strong = []

		for name in self.name_group_members:
			neg_strong.append(name)

		self.match_factors['negative']['strong'] = neg_strong

if __name__ == '__main__':
	print('running ' + __file__)

	import pprint
	
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
	matcher = ConsoleMatchFinder(ps4, {})
	pp.pprint(matcher.match_factors)
	match_score = matcher.assess_match(result)
	print(match_score)
	# matches = [x for x in lst if fulfills_some_condition(x)]
