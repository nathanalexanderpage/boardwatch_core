import os

from boardwatch_models import Listing, Platform, PlatformEdition
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from boardwatch.match.profilers import Profiler

load_dotenv(dotenv_path=find_dotenv())
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

class Match():
	registry = {}

	MATCH_SCORE_THRESHOLD = 1.5
	MATCH_SCORE_DEFAULT = 1

	MATCH_MULTIPLIER_EXACT = 5
	MATCH_MULTIPLIER_STRONG = 2
	MATCH_MULTIPLIER_WEAK = 1.5
	MATCH_MULTIPLIER_MINOR = 1.15

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
		del Match.registry[self.listing.id][self.item.__class__.__name__][self.item.id]

	def insert_into_db(self):
		conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
		cur = conn.cursor()

		try:
			if self.item.__class__.__name__ == 'PlatformEdition':
				cur.execute("""INSERT INTO listings_platform_editions (listing_id, platform_edition_id) VALUES(%s, %s) RETURNING listing_id, platform_edition_id;""", (self.listing.id, self.item.id,))
				conn.commit()
			else:
				raise Exception()
		finally:
			cur.close()

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
	def find_matches(cls):
		"""
		Find all matches inside yet unsearched listings
		"""
		# find product instances in listings
		profiler = Profiler()

		for listing in Listing.get_all():
			for edition in PlatformEdition.get_all():
				# cls.search_for_matches(listing, edition)

				searchtexts = profiler.build_string_matches(edition)

				for degree in searchtexts.keys():
					# for each listing, iterate through all searchable text segments
					for searchtext in searchtexts[degree]:
						for text in [listing.title, listing.body]:
							# evaluate if preliminary match on spot (wherever hot text within listing happens to be)
							try:
								match_index = text.index(searchtext)
								print('FOUND ' + searchtext + ' @ ' + str(match_index))
								match = Match(score=1, start=match_index, end=match_index+len(searchtext), item=edition, listing=listing)
								match.add_to_registry()
							except Exception:
								pass

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

	@classmethod
	def insert_all_to_db(cls):
		"""
		Insert all matches contained within Match class registry into database.
		"""
		for match_catalog_for_listing in cls.get_all().values():
			for product_class_matches in match_catalog_for_listing.values():
				for match in product_class_matches.values():
					try:
						match.insert_into_db()
					except Exception:
						pass

	@classmethod
	def search_for_matches(cls, listing, item):
		"""
		Finds all matches within listing text to any one product
		"""
		if type(item).__name__ == 'PlatformEdition':
			cls.search_for_platform_edition_matches(listing, item)

	@classmethod
	def search_for_platform_edition_matches(cls, listing, edn):
		platform = Platform.get_by_edition_id(edn.id)

		findings = list()
		
		if edn.name:
			f"""{edn.name}"""
			f"""{edn.name} {platform.name}"""
			f"""{platform.name} {edn.name}"""
			f"""{edn.name} {edn.official_color}"""
			f"""{edn.official_color} {edn.name}"""
		if edn.official_color:
			f"""{edn.official_color}"""
			f"""{platform.name} {edn.official_color}"""
			f"""{edn.official_color} {platform.name}"""
		if len(edn.colors) > 0:
			f"""{', '.join(edn.colors)} {platform.name}"""
			f"""{', '.join(edn.colors)} {platform.model_no} {platform.name}"""
			f"""{platform.model_no} {', '.join(edn.colors)} {platform.name}"""
			f"""{', '.join(edn.colors)} {platform.name} {platform.model_no}"""
			f"""{platform.name} {', '.join(edn.colors)}"""
			if edn.has_matte:
				f"""matte {', '.join(edn.colors)} {platform.name}"""
				f"""matte {' & '.join(edn.colors)} {platform.name}"""
			if edn.has_transparency:
				f"""transparent {', '.join(edn.colors)} {platform.name}"""
				f"""transparent {' & '.join(edn.colors)} {platform.name}"""
			if edn.has_gloss:
				f"""glossy {', '.join(edn.colors)} {platform.name}"""
				f"""glossy {' & '.join(edn.colors)} {platform.name}"""
				
		for text in [listing.title, listing.body]:
			# search progressively further in to listing title and body
			# TODO: add brand

			# organize two lists?
			# one for base search texts
			# one for corresponding lists of anti-match search protocols
