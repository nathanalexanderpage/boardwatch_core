class Match():
	registry = {}

	def __init__(self, score, start, end, item, listing):
		"""
		Create a new match object.
		"""
		self.score = score
		self.start = start
		self.end = end
		self.item = item
		self.listing = listing

	def add_to_registry(self):
		if self.listing.id not in Match.registry:
			Match.registry[self.listing.id] = dict()
		if self.item.__class__.__name__ not in Match.registry[self.listing.id]:
			Match.registry[self.listing.id][self.item.__class__.__name__] = dict()
		Match.registry[self.listing.id][self.item.__class__.__name__][self.item.id] = self

	def remove_from_registry(self):
		print('REMOVING')
		print(self)
		print(Match.registry[self.listing.id][self.item.__class__.__name__][self.item.id])
		del Match.registry[self.listing.id][self.item.__class__.__name__][self.item.id]

	def is_overlapping(self, other_match):
		if (
			other_match.start <= self.start and other_match.end > self.start
		) or (
			other_match.start < self.end and other_match.end >= self.end
		):
			return True
		return False

	@classmethod
	def get_all(cls):
		"""
		Returns registry of all matches (a dict sorted by listing ID).
		"""
		return cls.registry

	@classmethod
	def remove_competing_matches(cls):
		"""
		Examine all matches to eliminate those which correspond to the same listing text segment.
		"""
		# FIXME: at present, will rudimentarily delete former PlatformEdition match if scores are equal. In the future, if the highest score for PlatformEdition is a tie, neither PlatformEdition should be reported and it should fall to the Platform.
		for listing_matches_per_product_class in cls.registry.values():
			for product_matches in listing_matches_per_product_class.values():
				for match_key in list(product_matches):
					match = product_matches.get(match_key)
					if match:
						for product_class in ['Platform', 'PlatformEdition', 'Game']:
							if cls.registry[match.listing.id].get(product_class):
								for contrasted_match_item_key in list(cls.registry[match.listing.id][product_class]):
									contrasted_match = cls.registry[match.listing.id][product_class][contrasted_match_item_key]
									if match is not contrasted_match and match.is_overlapping(contrasted_match) and contrasted_match.score <= match.score:
										contrasted_match.remove_from_registry()
