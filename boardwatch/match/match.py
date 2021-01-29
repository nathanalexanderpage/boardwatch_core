import os

from boardwatch_models import Listing, Platform, PlatformEdition
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db
import pprint

from boardwatch.match.profilers import Profiler

load_dotenv(dotenv_path=find_dotenv())
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

class Match():
	registry = dict()

	MATCH_SCORE_THRESHOLD = 1.5
	MATCH_SCORE_DEFAULT = 1

	MATCH_MULTIPLIERS = {
		'exact': 5,
		'strong': 2,
		'weak': 1.5,
		'minor': 1.15
	}

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

	@classmethod
	def clear_registry(cls):
		cls.registry = dict()

	def insert_into_db(self):
		conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
		cur = conn.cursor()

		try:
			if self.item.__class__.__name__ == 'PlatformEdition':
				cur.execute("""INSERT INTO listings_platform_editions (listing_id, platform_edition_id, index_start, index_end, score) VALUES(%s, %s, %s, %s, %s) RETURNING listing_id, platform_edition_id;""", (self.listing.id, self.item.id, self.start, self.end, self.score))
				conn.commit()
				query_result = cur.fetchone()
				pprint.pprint(query_result)
			elif self.item.__class__.__name__ == 'Platform':
				print('\t\t\t\t INSERTING ' + str(self.item))
				cur.execute("""INSERT INTO listings_platforms (listing_id, platform_id, index_start, index_end, score) VALUES(%s, %s, %s, %s, %s) RETURNING listing_id, platform_id;""", (self.listing.id, self.item.id, self.start, self.end, self.score))
				conn.commit()
				query_result = cur.fetchone()
				print('\t\tquery_result = ' + str(query_result))
			else:
				raise Exception()
		except Exception as error:
			print(error)
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
	def get_by_info(cls, listing, item):
		"""
		Returns single match based on lookup criteria.
		"""
		return cls.registry[listing.id][item.__class__.__name__][item.id]

	@classmethod
	def find_matches(cls):
		"""
		Find all matches inside yet unsearched listings
		"""
		# find product instances in listings
		profiler = Profiler()

		for listing in Listing.get_all():
			for edition in PlatformEdition.get_all():
				cls.search_for_matches(listing, edition)
			for platform in Platform.get_all():
				cls.search_for_matches(listing, platform)

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

		pprint.pprint('cls.get_all()')
		pprint.pprint(cls.get_all())

		for match_catalog_for_listing in cls.get_all().values():
			for product_class_matches in match_catalog_for_listing.values():
				for match in product_class_matches.values():
					print(match.item)
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
		elif type(item).__name__ == 'Platform':
			cls.search_for_platform_matches(listing, item)
		else:
			raise Exception()

	@classmethod
	def search_for_platform_edition_matches(cls, listing, edn):
		platform = Platform.get_by_edition_id(edn.id)

		hottexts = {
			'exact': list(),
			'strong': list(),
			'weak': list(),
			'minor': list()
		}

		if len(edn.colors) > 0 and platform.name and not edn.name:
			hottexts['strong'].append(f"""{', '.join(edn.colors)} {platform.name}""")
			hottexts['strong'].append(f"""{platform.name} {', '.join(edn.colors)}""")
		if len(edn.colors) > 0 and platform.name and edn.name:
			hottexts['weak'].append(f"""{', '.join(edn.colors)} {platform.name}""")
			hottexts['weak'].append(f"""{platform.name} {', '.join(edn.colors)}""")
			hottexts['exact'].append(f"""{edn.name} {platform.name} {', '.join(edn.colors)}""")
			hottexts['exact'].append(f"""{edn.name} {', '.join(edn.colors)} {platform.name}""")
			hottexts['exact'].append(f"""{platform.name} {edn.name} {', '.join(edn.colors)}""")
			hottexts['exact'].append(f"""{platform.name} {', '.join(edn.colors)} {edn.name}""")
			hottexts['exact'].append(f"""{', '.join(edn.colors)} {edn.name} {platform.name}""")
			hottexts['exact'].append(f"""{', '.join(edn.colors)} {platform.name} {edn.name}""")
		if len(edn.colors) > 0 and platform.name and edn.has_matte:
			hottexts['strong'].append(f"""matte {', '.join(edn.colors)} {platform.name}""")
			hottexts['strong'].append(f"""matte {' & '.join(edn.colors)} {platform.name}""")
		if len(edn.colors) > 0 and platform.name and edn.has_transparency:
			hottexts['strong'].append(f"""transparent {', '.join(edn.colors)} {platform.name}""")
			hottexts['strong'].append(f"""transparent {' & '.join(edn.colors)} {platform.name}""")
		if len(edn.colors) > 0 and platform.name and edn.has_gloss:
			hottexts['strong'].append(f"""glossy {', '.join(edn.colors)} {platform.name}""")
			hottexts['strong'].append(f"""glossy {' & '.join(edn.colors)} {platform.name}""")
		if len(edn.colors) > 0 and platform.name and platform.model_no:
			hottexts['exact'].append(f"""{', '.join(edn.colors)} {platform.model_no} {platform.name}""")
			hottexts['exact'].append(f"""{platform.model_no} {', '.join(edn.colors)} {platform.name}""")
			hottexts['exact'].append(f"""{', '.join(edn.colors)} {platform.name} {platform.model_no}""")
		if edn.name and edn.official_color:
			hottexts['strong'].append(f"""{edn.name} {edn.official_color}""")
			hottexts['strong'].append(f"""{edn.official_color} {edn.name}""")
		if edn.name and platform.name:
			hottexts['strong'].append(f"""{edn.name} {platform.name}""")
			hottexts['strong'].append(f"""{platform.name} {edn.name}""")
		if edn.official_color and platform.name:
			hottexts['strong'].append(f"""{platform.name} {edn.official_color}""")
			hottexts['strong'].append(f"""{edn.official_color} {platform.name}""")
		if edn.name and (not edn.official_color and not platform.model_no):
			hottexts['strong'].append(f"""{edn.name}""")
		if edn.name and (edn.official_color or platform.model_no):
			hottexts['weak'].append(f"""{edn.name}""")
		if edn.official_color and edn.official_color not in edn.colors:
			hottexts['minor'].append(f"""{edn.official_color}""")

		pprint.pprint(hottexts)
		
		# TODO: split up function so components are testable
		
		for degree in hottexts.keys():
			for hottext in hottexts[degree]:
				for text in [listing.title, listing.body]:
					search_start_index = 0
					while search_start_index < len(text):
						# print(edn.id, search_start_index, len(text))
						# TODO: add brand

						# organize two lists?
						# one for base search texts
						# one for corresponding lists of anti-match search protocols
						try:
							match_index = text[search_start_index:].index(hottext)
							# print('FOUND ' + hottext + ' @ ' + str(match_index + search_start_index))
							# print(text[search_start_index+match_index:search_start_index+match_index+len(hottext)])
							match = Match(score=cls.MATCH_MULTIPLIERS[degree], start=match_index+search_start_index, end=search_start_index+match_index+len(hottext), item=edn, listing=listing)

							if match.score > cls.MATCH_SCORE_THRESHOLD:
								match.add_to_registry()

							search_start_index = match_index + search_start_index + 1
						except Exception:
							search_start_index = len(text)

	@classmethod
	def search_for_platform_matches(cls, listing, platform):
		hottexts = {
			'exact': list(),
			'strong': list(),
			'weak': list(),
			'minor': list()
		}
		
		storage_capacity = None
		storage_capacity_low = None
		storage_capacity_high = None

		index_hyphen = None

		if platform.storage_capacity:
			try:
				index_hyphen = platform.storage_capacity.index('-')
				storage_capacity_low = platform.storage_capacity[:index_hyphen]
				storage_capacity_high = platform.storage_capacity[index_hyphen+1:]
			except Exception:
				storage_capacity = platform.storage_capacity

		if platform.name:
			hottexts['strong'].append(f"""{platform.name}""")
		if platform.model_no:
			hottexts['exact'].append(f"""{platform.model_no}""")
		if storage_capacity and storage_capacity != 'n/a' and platform.name:
			hottexts['exact'].append(f"""{storage_capacity} {platform.name}""")
			hottexts['exact'].append(f"""{platform.name} {storage_capacity}""")
		if storage_capacity_low and platform.name:
			hottexts['exact'].append(f"""{storage_capacity_low} {platform.name}""")
			hottexts['exact'].append(f"""{platform.name} {storage_capacity_low}""")
		if storage_capacity_high and platform.name:
			hottexts['exact'].append(f"""{storage_capacity_high} {platform.name}""")
			hottexts['exact'].append(f"""{platform.name} {storage_capacity_high}""")

		pprint.pprint(hottexts)
		
		# TODO: split up function so components are testable
		
		for degree in hottexts.keys():
			for hottext in hottexts[degree]:
				for text in [listing.title, listing.body]:
					search_start_index = 0
					while search_start_index < len(text):
						# print(platform.id, search_start_index, len(text))
						# TODO: add brand

						# organize two lists?
						# one for base search texts
						# one for corresponding lists of anti-match search protocols
						try:
							# print(hottext + '  in  ' + text[search_start_index::] + '  ?')
							match_index = text[search_start_index:].index(hottext)
							print('FOUND ' + hottext + ' @ ' + str(match_index + search_start_index))
							print(text[search_start_index+match_index:search_start_index+match_index+len(hottext)])
							match = Match(score=cls.MATCH_MULTIPLIERS[degree], start=match_index+search_start_index, end=search_start_index+match_index+len(hottext), item=platform, listing=listing)

							if match.score > cls.MATCH_SCORE_THRESHOLD:
								match.add_to_registry()

							search_start_index = match_index + search_start_index + 1
						except Exception:
							search_start_index = len(text)
