import pprint

from boardwatch_models import Platform, PlatformEdition

pp = pprint.PrettyPrinter()

class Profiler():
	"""profile used for finding a match for a product within a listing"""

	MATCH_SCORE_THRESHOLD = 1.5
	MATCH_SCORE_DEFAULT = 1

	MATCH_MULTIPLIER_EXACT = 5
	MATCH_MULTIPLIER_STRONG = 2
	MATCH_MULTIPLIER_WEAK = 1.5
	MATCH_MULTIPLIER_MINOR = 1.15

	def __init__(self):
		pass

	def build_string_matches(self, item):
		# print('building item match profile for ' + str(item) + '...')
		match_strings = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}

		if type(item).__name__ == 'Platform':
			print('making match strings for ' + str(item))

		if type(item).__name__ == 'PlatformEdition':
			platform = Platform.get_by_edition_id(item.id)
			is_platform_family_namesake = True if item.name == platform.platform_family_name else False
			# FIXME: add developer, alternate_names for robust matches
			# positive exact matches
			if platform.model_no:
				match_strings['exact'].append(platform.model_no)

			if item.official_color and item.name:
				if not is_platform_family_namesake:
					match_strings['exact'].append(item.official_color + ' ' + item.name + ' ' +platform.platform_family_name)

				match_strings['exact'].append(item.official_color + ' ' + item.name + ' ' + item.name)
				match_strings['exact'].append(item.name + ' ' + item.official_color + ' ' + item.name)
				match_strings['exact'].append(item.name + ' ' + item.name + ' ' + item.official_color)
				match_strings['exact'].append(item.official_color + ' ' + item.name)
				match_strings['exact'].append(item.name + ' ' + item.official_color)

			elif item.name:
				match_strings['exact'].append(item.name + ' ' + item.name)

			# positive strong matches
			# FIXME: check that platform name isn't the generic name contained within other similar platform names like "3DS" is in "New 3DS", "3DS XL", "New 3DS XL", etc.
			if not is_platform_family_namesake and item.name:
				match_strings['strong'].append(item.name)
			for color in item.colors:
				if item.name and not is_platform_family_namesake:
					match_strings['strong'].append(item.name + ' ' + platform.platform_family_name)

				if item.name:
					match_strings['strong'].append(item.name + ' ' + item.name)

					if not item.official_color or color != item.official_color.lower():
						match_strings['strong'].append(color + ' ' + item.name)

			if item.official_color and item.name:
				match_strings['strong'].append(item.official_color + ' ' + item.name)
			if item.official_color and not is_platform_family_namesake:
				match_strings['strong'].append(item.official_color + ' ' + platform.platform_family_name)
			
			# positive weak matches
			for color in item.colors:
				if item.name and not is_platform_family_namesake:
					match_strings['weak'].append(color + ' ' + platform.platform_family_name)

			# positive minor matches
			if not is_platform_family_namesake:
				match_strings['minor'].append(platform.platform_family_name)

			# negative matches
			antimatch_strings = {
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

		else:
			raise Exception()
		
		return match_strings

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
