from boardwatch.models.platform_edition import PlatformEdition

score_dict = {
	'exact': 5,
	'strong': 3,
	'weak': 2,
	'minor': 1.4
}

class Platform():
	platforms = []

	def __init__(self, id, name, is_brand_missing_from_name, model_no, storage_capacity, description, disambiguation, relevance, editions=[]):
		self.id = id
		self.name = name
		self.is_brand_missing_from_name = is_brand_missing_from_name
		self.model_no = model_no
		self.storage_capacity = storage_capacity
		self.description = description
		self.disambiguation = disambiguation
		self.relevance = relevance
		self.editions = []

		self.match_strings = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}

		Platform.platforms.append(self)

	def make_match_strings(self, platform_family):
		if self.model_no:
			print(self.model_no)
			self.match_strings['exact'].append(self.model_no)
			print('added')

	def assess_matches(self, listing):
		self.find_string_matches(listing.title)
		self.find_string_matches(listing.body)
		for edition in self.editions:
			edition.assess_matches(listing)

	def find_string_matches(self, text):
		match_score = 1
		for degree in self.match_strings.keys():
			for string in self.match_strings[degree]:
				if string in text:
					match_score *= score_dict[degree]
		if (match_score != 1):
			print(match_score)
