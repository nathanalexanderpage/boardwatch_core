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
		if self.item.listing.id not in Match.registry:
			Match.registry[self.item.listing.id] = dict()
		if self.item.__class__ not in Match.registry[self.item.listing.id]:
			Match.registry[self.item.listing.id][self.item.__class__] = list()
		Match.registry[self.item.listing.id][self.item.__class__].append(self)

	def remove_competing_matches(self):
		"""
		Examine all matches to eliminate those which correspond to the same text.
		"""
		pass

	@classmethod
	def get_all(cls):
		"""
		Returns registry of all matches.
		"""
		return cls.registry
