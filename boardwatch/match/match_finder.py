import pprint

class MatchFinder():
	"""parent match finder class -- mostly for rules inheritance; not to be used to find actual matches"""

	def __init__(self, want, config={}):
		self.want = want
		self.config = config
		self.want

		self.MATCH_SCORE_THRESHOLD = 1.5
		self.MATCH_SCORE_DEFAULT = 1

		self.MATCH_MULTIPLIER_EXACT = 5
		self.MATCH_MULTIPLIER_STRONG = 2
		self.MATCH_MULTIPLIER_WEAK = 1.5
		self.MATCH_MULTIPLIER_MINOR = 1.15

		self.type = 'generic'
		self.attr = 'this is a catch-all function for the parent class; usually, this is where child classes define instance attributes that are specific to each child class'

		self.build_string_matches()

	def __str__(self):
		return 'MatchFinder parent class instance. To be used for testing purposes only.'

	def build_string_matches(self):
		print('use child class\'s')

	def check_if_weed_out(self, title_compare):
		for check in self.antimatch_factors['anywhere']:
			if check in title_compare: return True
		return False

	def check_if_negative_matches(self, title_compare, positive_match_string):
		print('CHECKING if \'' + positive_match_string + '\' truly matches with \'' + title_compare + '\'')
		if self.check_if_weed_out(title_compare): return True
		if title_compare.find(positive_match_string) > 0:
			for check in self.antimatch_factors['before']['space_separated_yes']:
				print('CHECKING IF \'' + check.lower() + ' ' + positive_match_string + '\' in \'' + title_compare + '\'')
				if check.lower() + ' ' + positive_match_string in title_compare: return True
			for check in self.antimatch_factors['before']['space_separated_no']:
				print('CHECKING IF \'' + check.lower() + positive_match_string + '\' in \'' + title_compare + '\'')
				if check.lower() + positive_match_string in title_compare: return True
		if title_compare.find(positive_match_string) + len(positive_match_string) < len(title_compare) - 1:
			for check in self.antimatch_factors['after']['space_separated_yes']:
				print('CHECKING IF \'' + positive_match_string + ' ' + check.lower() + '\' in \'' + title_compare + '\'')
				if positive_match_string + ' ' + check.lower() in title_compare: return True
			for check in self.antimatch_factors['after']['space_separated_no']:
				print('CHECKING IF \'' + positive_match_string + check.lower() + '\' in \'' + title_compare + '\'')
				if positive_match_string + check.lower() in title_compare: return True
		print(positive_match_string)
		return False

	def match_score_calculate(self, result):
		stop_matching_positive = False
		match_score = 1
		title_compare = result['title'].lower()
		# positive match multipliers
		for match_string_exact in self.match_factors['positive']['exact']:
			if match_string_exact.lower() == title_compare:
				stop_matching_positive = True
				match_score *= self.MATCH_MULTIPLIER_EXACT
				break
		for match_string_strong in self.match_factors['positive']['strong']:
			if stop_matching_positive:
				break
			if match_string_strong.lower() in title_compare:
				if not self.check_if_negative_matches(title_compare, match_string_strong.lower()):
					match_score *= self.MATCH_MULTIPLIER_STRONG
		for match_string_weak in self.match_factors['positive']['weak']:
			if stop_matching_positive:
				break
			if match_string_weak.lower() in title_compare:
				print('FOUND: ' + match_string_weak)
				if not self.check_if_negative_matches(title_compare, match_string_weak.lower()):
					match_score *= self.MATCH_MULTIPLIER_WEAK
		for match_string_weak in self.match_factors['positive']['minor']:
			if stop_matching_positive:
				break
			if match_string_weak.lower() in title_compare:
				stop_matching_positive = True
				match_score *= self.MATCH_MULTIPLIER_MINOR
				break

		print(str(match_score))
		return match_score
	
	def assess_match(self, result):
		if self.match_score_calculate(result) >= self.MATCH_SCORE_THRESHOLD:
			return True
		else:
			return False

	def assess_meta_price_point(self, result):
		"""determine if match is at or below user's specified price point"""
		print('assessing price point...')
		if self.config['price_point'] == None:
			return True
		elif result['price'] > self.config['price_point']:
			return False
		else:
			return True

class PlatformMatchFinder(MatchFinder):
	"""for finding consoles"""

	def __init__(self, want, name_group_members=[], config={}):
		super().__init__(want)
		self.type = 'platform'
		self.attr = 'used to determine whether or not a block of text contains mention of a given gaming platform'
		self.antimatch_factors = {
			'anywhere': [
				'I will',
				'wanted:',
				'no console',
				'box only',
				'repair',
				'broken',
				'busted',
				'defective'
			],
			'before': {
				'space_separated_yes': [
					'for',
					'for the',
					'buying',
					'your',
					'looking for',
					'looking for a',
					'no'
				],
				'space_separated_no': []
			},
			'after': {
				'space_separated_yes': [
					'compatible'
					'for parts',
					'for pieces',
					'accessory',
					'accessories',
					'controller',
					'control',
					'pad'
				],
				'space_separated_no': [
					'-compatible'
				]
			}
		}
		self.seek_modifiers = {
			'anywhere': [
				'Limited Edition'
			],
			'before': {
				'space_separated_yes': [
					'+',
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
		self.name_group_members = name_group_members

	def __str__(self):
		return 'MatchFinder instance for finding ' + self.want['name']
	
	def build_string_matches(self):
		print('building item match profile...')

		is_platform_family_namesake = True if self.want['name'] == self.want['family_name'] else False

		self.want['match_strings'] = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}

		for edition in self.want['editions']:
			edition['match_strings'] = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}
		pprint.pprint(self.want)

		# FIXME: add developer, alternate_names for robust matches
		# positive exact matches
		if self.want['model_no']:
			self.want['match_strings']['exact'].append(self.want['model_no'])

		for edition in self.want['editions']:
			if edition['official_color'] and edition['name']:
				if not is_platform_family_namesake:
					edition['match_strings']['exact'].append(edition['official_color'] + ' ' + edition['name'] + ' ' + self.want['family_name'])

				edition['match_strings']['exact'].append(edition['official_color'] + ' ' + edition['name'] + ' ' + self.want['name'])
				edition['match_strings']['exact'].append(edition['name'] + ' ' + edition['official_color'] + ' ' + self.want['name'])
				edition['match_strings']['exact'].append(edition['name'] + ' ' + self.want['name'] + ' ' + edition['official_color'])
				edition['match_strings']['exact'].append(edition['official_color'] + ' ' + self.want['name'] + ' ' + edition['name'])

			elif edition['name']:
				edition['match_strings']['exact'].append(edition['name'] + ' ' + self.want['name'])
				edition['match_strings']['exact'].append(self.want['name'] + ' ' + edition['name'])

			elif edition['official_color']:
				edition['match_strings']['exact'].append(edition['official_color'] + ' ' + self.want['name'])
				edition['match_strings']['exact'].append(self.want['name'] + ' ' + edition['official_color'])

		# ORIGINAL
		# for edition in self.want['editions']:
		# 	pos_exact_edition = []
		# 	pos_exact_edition.append(self.want['name'])
		# 	pos_exact_edition.append(self.want['developer'] + ' ' + self.want['name'])
		# 	if self.want['abbreviation_official']:
		# 		pos_exact_edition.append(self.want['abbreviation_official'])
		# 		pos_exact_edition.append(self.want['developer'] + ' ' + self.want['abbreviation_official'])
		# 	for name in self.want['names_other']:
		# 		pos_exact_edition.append(name)
		# 		pos_exact_edition.append(self.want['developer'] + ' ' + name)
		# 	for platform in self.want['platforms']:
		# 		if platform['model_no']:
		# 			pos_exact_edition.append(platform['model_no'])
		# 		if platform['storage_capacity'] and self.want['abbreviation_official']:
		# 			pos_exact_edition.append(self.want['abbreviation_official'] + ' ' + platform['storage_capacity'])
		# 		if platform['name']:
		# 			pos_exact_edition.append(self.want['name'] + ' ' + platform['name'])
		# 			pos_exact_edition.append(self.want['developer'] + ' ' + self.want['name'] + ' ' + platform['name'])
		# 			if platform['storage_capacity']:
		# 				pos_exact_edition.append(self.want['name'] + ' ' + platform['name'] + ' ' + platform['storage_capacity'])
		# 				pos_exact_edition.append(self.want['developer'] + ' ' + self.want['name'] + ' ' + platform['name'] + ' ' + platform['storage_capacity'])
		# 				if self.want['abbreviation_official']:
		# 					pos_exact_edition.append(self.want['abbreviation_official'] + ' ' + platform['name'] + ' ' + platform['storage_capacity'])
		# 					pos_exact_edition.append(self.want['developer'] + ' ' + self.want['abbreviation_official'] + ' ' + platform['name'] + ' ' + platform['storage_capacity'])
		# 			if self.want['abbreviation_official']:
		# 				pos_exact_edition.append(self.want['abbreviation_official'] + ' ' + platform['name'])
		# 				pos_exact_edition.append(self.want['developer'] + ' ' + self.want['abbreviation_official'] + ' ' + platform['name'])
		# 	self.match_factors['edition']['positive']['exact'] = pos_exact_edition

		# positive strong matches
		# FIXME: check that platform name isn't the generic name contained within other similar platform names like "3DS" is in "New 3DS", "3DS XL", "New 3DS XL", etc.
		if not is_platform_family_namesake:
			self.want['match_strings']['strong'].append(self.want['name'])
		for edition in self.want['editions']:
			for color in edition['colors']:
				if edition['name'] and not is_platform_family_namesake:
					edition['match_strings']['strong'].append(edition['name'] + ' ' + self.want['family_name'])

				if edition['name']:
					edition['match_strings']['strong'].append(edition['name'] + ' ' + self.want['name'])

				if not edition['official_color'] or color != edition['official_color'].lower():
					edition['match_strings']['strong'].append(color + ' ' + self.want['name'])

			if edition['official_color']:
				edition['match_strings']['strong'].append(edition['official_color'] + ' ' + self.want['name'])
			if edition['official_color'] and not is_platform_family_namesake:
				edition['match_strings']['strong'].append(edition['official_color'] + ' ' + self.want['family_name'])
		
		# ORIGINAL
		# pos_strong.append(self.want['developer'] + ' ' + self.want['name'] + ' console')
		# pos_strong.append(self.want['developer'] + ' ' + self.want['name'] + ' system')
		# if self.want['abbreviation_official']:
		# 	pos_strong.append(self.want['developer'] + ' ' + self.want['abbreviation_official'] + ' console')
		# 	pos_strong.append(self.want['developer'] + ' ' + self.want['abbreviation_official'] + ' system')
		# for name in self.want['names_other']:
		# 	pos_strong.append(self.want['developer'] + ' ' + name + ' console')
		# 	pos_strong.append(self.want['developer'] + ' ' + name + ' system')
		# for platform in self.want['platforms']:
		# 	if platform['name']:
		# 		pos_strong.append(self.want['name'] + ' ' + platform['name'])
		# 	if platform['storage_capacity']:
		# 		pos_strong.append(self.want['name'] + ' ' + platform['storage_capacity'])
		# 	for edn in platform['editions']:
		# 		if edn['name']:
		# 			# if ':' in edn['name']:
		# 			# 	split_edition_name = edn['name'].split(':')
		# 			pos_strong.append(self.want['name'] + ' ' + edn['name'])
		# 			pos_strong.append(edn['name'] + ' ' + self.want['name'])
		# 			for color in edn['colors']:
		# 				pos_strong.append(self.want['name'] + ' ' + edn['name'] + ' ' + color)
		# 				pos_strong.append(color + ' ' + self.want['name'])
		# 				if platform['name']:
		# 					pos_strong.append(self.want['name'] + ' ' + platform['name'] + ' ' + edn['name'] + ' ' + color)
		# 		for color in edn['colors']:
		# 			pos_strong.append(self.want['name'] + ' ' + color)
		# 			pos_strong.append(color + ' ' + self.want['name'])
		# self.match_factors['positive']['strong'] = pos_strong

		# positive weak matches
		for edition in self.want['editions']:
			for color in edition['colors']:
				if edition['name'] and not is_platform_family_namesake:
					edition['match_strings']['weak'].append(color + ' ' + self.want['family_name'])

		# ORIGINAL
		# pos_weak.append(self.want['name'])
		# if self.want['abbreviation_official']:
		# 	pos_weak.append(self.want['abbreviation_official'])
		# for name in self.want['names_other']:
		# 	pos_weak.append(name)

		# positive minor matches
		if not is_platform_family_namesake:
			self.want['match_strings']['minor'].append(self.want['family_name'])

		# pos_minor.append(self.want['developer'])

		# negative matches
		antimatch_factors = {
			'anywhere': [],
			'before': {
				'space_separated_yes': [],
				'space_separated_no': []
			},
			'after': {
				'space_separated_yes': [],
				'space_separated_no': []
			}
		}

		# for system in self.name_group_members:
		# 	# if system['name'] not in self.want['name']:
		# 	# 	antimatch_factors['anywhere'].append(system['name'])
		# 	if self.want['name'] in system['name']:
		# 		if system['name_prefix']:
		# 			antimatch_factors['before']['space_separated_yes'].append(system['name_prefix'])
		# 			antimatch_factors['before']['space_separated_no'].append(system['name_prefix'])
		# 		if system['name_suffix']:
		# 			antimatch_factors['after']['space_separated_yes'].append(system['name_suffix'])
		# 			antimatch_factors['after']['space_separated_no'].append(system['name_suffix'])


		# for neg_match in antimatch_factors['anywhere']:
		# 	self.antimatch_factors['anywhere'].append(neg_match)
		# for neg_match in antimatch_factors['before']['space_separated_yes']:
		# 	self.antimatch_factors['before']['space_separated_yes'].append(neg_match)
		# for neg_match in antimatch_factors['before']['space_separated_no']:
		# 	self.antimatch_factors['before']['space_separated_no'].append(neg_match)
		# for neg_match in antimatch_factors['after']['space_separated_yes']:
		# 	self.antimatch_factors['after']['space_separated_yes'].append(neg_match)
		# for neg_match in antimatch_factors['after']['space_separated_no']:
		# 	self.antimatch_factors['after']['space_separated_no'].append(neg_match)

		pprint.pprint(self.want)
		
	def parentheses_judger(self, comp_title):
		pass
		if self.want['abbreviation_official']:
			antimatch_factors.append('(' + self.want['abbreviation_official'] + ')')
		antimatch_factors.append('(' + self.want['name'] + ')')
		antimatch_factors.append('(' + self.want['name_group'] + ')')
		for name in self.want['names_other']:
			antimatch_factors.append('(' + self.want['name_group'] + ')')

	# FIXME: account for possibility of platforms of different consoles with same names (PS2 slim, PS4 slim)
	# FIXME: (efficiency) when preventing false matches for sibling consoles, ensure absence of foil strings using intra-string position instead of 'not in [entire str]'
	def match_scores_calculate(self, result):
		title_compare = result[1].lower()
		body_compare = result[2].lower()

		self.want['matches'] = []
		for edition in self.want['editions']:
			stop_matching_positive = False
			match_score = 1

			# positive match multipliers
			for match_string_exact in edition['match_strings']['exact']:
				if match_string_exact.lower() in title_compare or match_string_exact.lower() in body_compare:
					stop_matching_positive = True
					match_score *= self.MATCH_MULTIPLIER_EXACT
					break
			if not stop_matching_positive:
				for match_string_strong in edition['match_strings']['strong']:
					if match_string_strong.lower() in title_compare or match_string_strong.lower() in body_compare:
						# if not self.check_if_negative_matches(title_compare, match_string_strong.lower()):
							match_score *= self.MATCH_MULTIPLIER_STRONG
				for match_string_weak in edition['match_strings']['weak']:
					if match_string_weak.lower() in title_compare or match_string_weak.lower() in body_compare:
						# if not self.check_if_negative_matches(title_compare, match_string_weak.lower()):
							match_score *= self.MATCH_MULTIPLIER_WEAK
				for match_string_weak in edition['match_strings']['minor']:
					if not stop_matching_positive and (match_string_weak.lower() in title_compare or match_string_weak.lower() in body_compare):
						stop_matching_positive = True
						match_score *= self.MATCH_MULTIPLIER_MINOR
						break

			if match_score > self.MATCH_SCORE_THRESHOLD:
				self.want['matches'].append({
					'edition_id': edition['id'],
					'listing_id': result[0]
				})

		if len(self.want['matches']) == 0:
			stop_matching_positive = False
			match_score = 1

			# positive match multipliers
			for match_string_exact in self.want['match_strings']['exact']:
				if match_string_exact.lower() == title_compare:
					stop_matching_positive = True
					match_score *= self.MATCH_MULTIPLIER_EXACT
					break
			if not stop_matching_positive:
				for match_string_strong in self.want['match_strings']['strong']:
					if match_string_strong.lower() in title_compare:
						if not self.check_if_negative_matches(title_compare, match_string_strong.lower()):
							match_score *= self.MATCH_MULTIPLIER_STRONG
				for match_string_weak in self.want['match_strings']['weak']:
					if match_string_weak.lower() in title_compare:
						print('FOUND: ' + match_string_weak)
						if not self.check_if_negative_matches(title_compare, match_string_weak.lower()):
							match_score *= self.MATCH_MULTIPLIER_WEAK
				for match_string_weak in self.want['match_strings']['minor']:
					if match_string_weak.lower() in title_compare:
						stop_matching_positive = True
						match_score *= self.MATCH_MULTIPLIER_MINOR
						break
		if match_score > self.MATCH_SCORE_THRESHOLD:
			self.want['matches'].append({
				'edition_id': None,
				'listing_id': result[0]
			})

		print(str(match_score))
		return match_score

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
	matcher = PlatformMatchFinder(wii, {})
	pp.pprint(matcher.match_factors)
	pp.pprint(matcher.antimatch_factors)
	match_score = matcher.match_score_calculate(result)
	print(match_score)
	# matches = [x for x in lst if fulfills_some_condition(x)]
