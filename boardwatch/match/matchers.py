import os
import pprint
import psycopg2 as db
from dotenv import load_dotenv
from .profilers import *
from boardwatch.models.listing import Listing
from boardwatch.models.platform_edition import PlatformEdition
from boardwatch.models.platform import Platform
from boardwatch.models.platform_family import PlatformFamily

load_dotenv(dotenv_path='../../.env')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
cur = conn.cursor()

class Prepper():
	def go():
		Prepper.construct_items()
		Prepper.prep_listings()
		Prepper.prep_items()
		Prepper.find_matches()

	def construct_items():
		cur.execute('SELECT id, name, generation as gen FROM platform_families;')
		platform_families = cur.fetchall()

		for platform_family in platform_families:
			current_platform_family = PlatformFamily(platform_family[0], platform_family[1])

			cur.execute('SELECT id, name, is_brand_missing, model_no, storage_capacity, description, disambiguation, relevance FROM platforms WHERE platform_family_id = %s', (current_platform_family.id,))
			platforms = cur.fetchall()

			# FIXME: add developer for robust matches
			for platform in platforms:
				current_platform = Platform(platform[0], platform[1], platform[2], platform[3], platform[4], platform[5], platform[6], platform[7])

				current_platform_family.platforms.append(current_platform)

				cur.execute('SELECT id, name, official_color, has_matte, has_transparency, has_gloss, note, image_url FROM platform_editions WHERE platform_id = %s;', (current_platform.id,))
				platform_editions = cur.fetchall()

				for platform_edition in platform_editions:
					current_edition = PlatformEdition(platform_edition[0], platform_edition[1], platform_edition[2], platform_edition[3], platform_edition[4], platform_edition[5], platform_edition[6], platform_edition[7])

					current_platform.editions.append(current_edition)

					cur.execute('SELECT colors.id as id, colors.name as name FROM colors JOIN colors_platform_editions as cpe ON id = cpe.color_id WHERE cpe.platform_edition_id = %s;', (current_edition.id,))
					colors = cur.fetchall()

					for color in colors:
						current_edition.colors.append(color[1])
				
	def prep_items():
		for family in PlatformFamily.platform_families:
			# print(family.platforms[0])
			for platform in family.platforms:
				platform.make_match_strings(family)
			# 	for edition in platform.editions:
			# 		edition.make_match_strings(platform, family)

	def prep_listings():
		cur.execute('SELECT id, native_id, title, body, url, seller_email, seller_phone, date_posted, date_scraped FROM listings WHERE is_scanned = %s', (False,))
		all_raw_listings = cur.fetchall()

		for listing in all_raw_listings:
			new_listing = Listing(listing[0], listing[1], listing[2], listing[3], listing[4], listing[5], listing[6], listing[7], listing[8])
			print('\n\n--------------------------------\n')
			print(new_listing.title)

	def find_matches():
		for listing in Listing.listings:
			PlatformFamily.assess_all_matches(listing)





			for matcher in platform_matchers:
				matcher.match_scores_calculate(listing)
				for match in matcher.want['matches']:
					print('inserting record...')
					try:
						if match['edition_id']:
							cur.execute('INSERT INTO listings_platform_editions (listing_id, platform_edition_id) VALUES(%s, %s) RETURNING listing_id, platform_edition_id', (match['listing_id'], match['edition_id']))
						else:
							cur.execute('INSERT INTO listings_platforms (listing_id, platform_id) VALUES(%s, %s) RETURNING listing_id, platform_id', (match['listing_id'], matcher.want['id']))
						conn.commit()
						insert_response = cur.fetchone()
					except Exception as error:
						print('error during insert.')
						print(error)
						conn.commit()
