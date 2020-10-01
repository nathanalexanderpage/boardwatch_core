import pprint

class Profiler():
	"""profile used for finding a match for a product within a listing"""

	profiles = []

	def __init__(self, want, **kwargs):
		self.want = want

		self.MATCH_SCORE_THRESHOLD = 1.5
		self.MATCH_SCORE_DEFAULT = 1

		self.MATCH_MULTIPLIER_EXACT = 5
		self.MATCH_MULTIPLIER_STRONG = 2
		self.MATCH_MULTIPLIER_WEAK = 1.5
		self.MATCH_MULTIPLIER_MINOR = 1.15

		# positive matches
		self.match_strings = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}

		# negative matches
		self.antimatch_strings = {
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

		# conditional execution based on class name
		if type(want).__name__ == 'Platform':
			self.type = 'platform'
			self.attr = 'used to determine whether or not a block of text contains mention of a given gaming platform'
			self.antimatch_strings['anywhere'].extend([
				'I will',
				'wanted:',
				'no console',
				'box only',
				'repair',
				'broken',
				'busted',
				'defective'
			])
			self.antimatch_strings['before']['space_separated_yes'].extend([
				'for',
				'for the',
				'buying',
				'your',
				'looking for',
				'looking for a',
				'no',
				'compatible with'
			])
			# self.antimatch_strings['before']['space_separated_no'].extend([])
			self.antimatch_strings['after']['space_separated_yes'].extend([
				'compatible',
				'for parts',
				'for pieces',
				'accessory',
				'accessories',
				'controller',
				'control',
				'pad'
			])
			self.antimatch_strings['after']['space_separated_no'].extend([
				'-compatible'
			])

			# FIXME: More complicated language logic TBD

			# self.seek_modifiers = {
			# 	'anywhere': [
			# 		'Limited Edition'
			# 	],
			# 	'before': {
			# 		'space_separated_yes': [
			# 			'+',
			# 			'&',
			# 			',',
			# 			';',
			# 			'.',
			# 			'!',
			# 			'and',
			# 			'plus',
			# 			'with',
			# 			'also'
			# 		],
			# 		'space_separated_no': []
			# 	},
			# 	'after': {
			# 		'space_separated_yes': [
			# 			'with',
			# 			'plus'
			# 		],
			# 		'space_separated_no': []
			# 	}
			# }

			self.name_group_members = kwargs['name_group_members']
			
		else:
			raise Exception('Wanted item is of type ' + type(want) + ', which has not been configured for profile creation in code.')

		self.build_string_matches()
		Profiler.profiles.append(self)

	def __str__(self):
		return 'Profiler instance for finding ' + self.want.name
			
	def build_string_matches(self):
		print('building item match profile...')

		if type(self.want).__name__ == 'Platform':
			is_platform_family_namesake = True if self.want.name == self.want.platform_family_name else False

			for edition in self.want.editions:
				edition['match_strings'] = {
				'exact': [],
				'strong': [],
				'weak': [],
				'minor': []
			}
			pprint.pprint(self.want)

			# FIXME: add developer, alternate_names for robust matches
			# positive exact matches
			if self.want.model_no:
				self.match_strings['exact'].append(self.want.model_no)

			for edition in self.want.editions:
				if edition.official_color and edition.name:
					if not is_platform_family_namesake:
						edition['match_strings']['exact'].append(edition.official_color + ' ' + edition.name + ' ' + self.want.platform_family_name)

					edition['match_strings']['exact'].append(edition.official_color + ' ' + edition.name + ' ' + self.want.name)
					edition['match_strings']['exact'].append(edition.name + ' ' + edition.official_color + ' ' + self.want.name)
					edition['match_strings']['exact'].append(edition.name + ' ' + self.want.name + ' ' + edition.official_color)
					edition['match_strings']['exact'].append(edition.official_color + ' ' + self.want.name + ' ' + edition.name)

				elif edition.name:
					edition['match_strings']['exact'].append(edition.name + ' ' + self.want.name)
					edition['match_strings']['exact'].append(self.want.name + ' ' + edition.name)

				elif edition.official_color:
					edition['match_strings']['exact'].append(edition.official_color + ' ' + self.want.name)
					edition['match_strings']['exact'].append(self.want.name + ' ' + edition.official_color)

			# positive strong matches
			# FIXME: check that platform name isn't the generic name contained within other similar platform names like "3DS" is in "New 3DS", "3DS XL", "New 3DS XL", etc.
			if not is_platform_family_namesake:
				self.match_strings['strong'].append(self.want.name)
			for edition in self.want.editions:
				for color in edition.colors:
					if edition.name and not is_platform_family_namesake:
						edition['match_strings']['strong'].append(edition.name + ' ' + self.want.platform_family_name)

					if edition.name:
						edition['match_strings']['strong'].append(edition.name + ' ' + self.want.name)

					if not edition.official_color or color != edition.official_color.lower():
						edition['match_strings']['strong'].append(color + ' ' + self.want.name)

				if edition.official_color:
					edition['match_strings']['strong'].append(edition.official_color + ' ' + self.want.name)
				if edition.official_color and not is_platform_family_namesake:
					edition['match_strings']['strong'].append(edition.official_color + ' ' + self.want.platform_family_name)
			
			# positive weak matches
			for edition in self.want.editions:
				for color in edition.colors:
					if edition.name and not is_platform_family_namesake:
						edition['match_strings']['weak'].append(color + ' ' + self.want.platform_family_name)

			# positive minor matches
			if not is_platform_family_namesake:
				self.match_strings['minor'].append(self.want.platform_family_name)

			# negative matches
			self.antimatch_strings = {
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

			pprint.pprint(self.want)
		
		else:
			raise Exception()

	def check_if_weed_out(self, title_compare):
		for check in self.antimatch_strings['anywhere']:
			if check in title_compare: return True
		return False

	def check_if_negative_matches(self, title_compare, positive_match_string):
		print('CHECKING if \'' + positive_match_string + '\' truly matches with \'' + title_compare + '\'')
		if self.check_if_weed_out(title_compare): return True
		if title_compare.find(positive_match_string) > 0:
			for check in self.antimatch_strings['before']['space_separated_yes']:
				print('CHECKING IF \'' + check.lower() + ' ' + positive_match_string + '\' in \'' + title_compare + '\'')
				if check.lower() + ' ' + positive_match_string in title_compare: return True
			for check in self.antimatch_strings['before']['space_separated_no']:
				print('CHECKING IF \'' + check.lower() + positive_match_string + '\' in \'' + title_compare + '\'')
				if check.lower() + positive_match_string in title_compare: return True
		if title_compare.find(positive_match_string) + len(positive_match_string) < len(title_compare) - 1:
			for check in self.antimatch_strings['after']['space_separated_yes']:
				print('CHECKING IF \'' + positive_match_string + ' ' + check.lower() + '\' in \'' + title_compare + '\'')
				if positive_match_string + ' ' + check.lower() in title_compare: return True
			for check in self.antimatch_strings['after']['space_separated_no']:
				print('CHECKING IF \'' + positive_match_string + check.lower() + '\' in \'' + title_compare + '\'')
				if positive_match_string + check.lower() in title_compare: return True
		print(positive_match_string)
		return False

	def match_score_calculate(self, result):
		stop_matching_positive = False
		match_score = 1
		title_compare = result['title'].lower()
		# positive match multipliers
		for match_string_exact in self.match_strings['positive']['exact']:
			if match_string_exact.lower() == title_compare:
				stop_matching_positive = True
				match_score *= self.MATCH_MULTIPLIER_EXACT
				break
		for match_string_strong in self.match_strings['positive']['strong']:
			if stop_matching_positive:
				break
			if match_string_strong.lower() in title_compare:
				if not self.check_if_negative_matches(title_compare, match_string_strong.lower()):
					match_score *= self.MATCH_MULTIPLIER_STRONG
		for match_string_weak in self.match_strings['positive']['weak']:
			if stop_matching_positive:
				break
			if match_string_weak.lower() in title_compare:
				print('FOUND: ' + match_string_weak)
				if not self.check_if_negative_matches(title_compare, match_string_weak.lower()):
					match_score *= self.MATCH_MULTIPLIER_WEAK
		for match_string_weak in self.match_strings['positive']['minor']:
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

	# FIXME: account for possibility of platforms of different consoles with same names (PS2 slim, PS4 slim)
	# FIXME: make sure platform names within the same family are distinguished between when generating matches. make sure a potential match with one is not any of the others
	# FIXME: (efficiency) when preventing false matches for sibling consoles, ensure absence of foil strings using intra-string position instead of 'not in [entire str]'
	def match_scores_calculate(self, result):
		title_compare = result[1].lower()
		body_compare = result[2].lower()

		self.want['matches'] = []
		for edition in self.want.editions:
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
			for match_string_exact in self.match_strings['exact']:
				if match_string_exact.lower() == title_compare:
					stop_matching_positive = True
					match_score *= self.MATCH_MULTIPLIER_EXACT
					break
			if not stop_matching_positive:
				for match_string_strong in self.match_strings['strong']:
					if match_string_strong.lower() in title_compare:
						if not self.check_if_negative_matches(title_compare, match_string_strong.lower()):
							match_score *= self.MATCH_MULTIPLIER_STRONG
				for match_string_weak in self.match_strings['weak']:
					if match_string_weak.lower() in title_compare:
						print('FOUND: ' + match_string_weak)
						if not self.check_if_negative_matches(title_compare, match_string_weak.lower()):
							match_score *= self.MATCH_MULTIPLIER_WEAK
				for match_string_weak in self.match_strings['minor']:
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
