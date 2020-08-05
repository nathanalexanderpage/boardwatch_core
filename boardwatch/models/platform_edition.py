score_dict = {
	'exact': 5,
	'strong': 3,
	'weak': 2,
	'minor': 1.4
}

class PlatformEdition():
	editions = []

	def __init__(self, id, name, official_color, has_matte, has_transparency, has_gloss, note, image_url, colors=[]):
		self.id = id
		self.colors = colors
		self.has_matte = has_matte
		self.has_transparency = has_transparency
		self.has_gloss = has_gloss
		self.image_url = image_url
		self.name = name
		self.note = note
		self.official_color = official_color

		self.match_strings = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}

		self.match_string_call_count = 0

		PlatformEdition.editions.append(self)

	def make_match_strings(self, platform, platform_family):
		# exact
		if self.official_color and self.name:
			self.match_strings['exact'].append(self.official_color + ' ' + self.name + ' ' + platform_family.name)
			self.match_strings['exact'].append(self.official_color + ' ' + self.name + ' ' + platform.name)
			self.match_strings['exact'].append(self.name + ' ' + platform.name + ' ' + self.official_color)
			self.match_strings['exact'].append(self.official_color + ' ' + platform.name + ' ' + self.name)

		elif self.name:
			self.match_string_call_count += 1
			print('made match strings ' + str(self.match_string_call_count) + ' times')
			self.match_strings['exact'].append(self.name + ' ' + platform.name)
			# self.match_strings['exact'].append(platform.name + ' ' + self.name)

		elif self.official_color:
			self.match_strings['exact'].append(self.official_color + ' ' + platform.name)
			self.match_strings['exact'].append(platform.name + ' ' + self.official_color)

		# TODO: strong, weak, minor

	def assess_matches(self, listing):
		self.find_string_matches(listing.title)
		self.find_string_matches(listing.body)

	def find_string_matches(self, text):
		match_score = 1
		print(self.match_strings)
		for degree in self.match_strings.keys():
			for string in self.match_strings[degree]:
				print('checking for "' + string + '" in "' + text + '"...')
				if string in text:
					match_score *= score_dict[degree]
		if match_score != 1:
			print(match_score)
		