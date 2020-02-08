import os
import pprint
import psycopg2 as db
from dotenv import load_dotenv
from match_finder import *

load_dotenv(dotenv_path='./.env')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
cur = conn.cursor()

platform_family_configs = []

cur.execute('SELECT id, name, generation as gen FROM platform_families;')
platform_families = cur.fetchall()

for platform_family in platform_families:
	current_platform_family = {
		'id': platform_family[0],
		'type': 'platform',
		'name': platform_family[1],
		'platforms': []
	}

	cur.execute('SELECT id, name, is_brand_missing, model_no, storage_capacity FROM platforms WHERE platform_family_id = %s', (current_platform_family['id'],))
	platforms = cur.fetchall()

	# FIXME: add developer for robust matches
	for platform in platforms:
		current_platform = {
			'id': platform[0],
			'name': platform[1],
			'is_brand_missing': platform[2],
			'model_no': platform[3],
			'storage_capacity': platform[4],
			'editions': []
		}

		cur.execute('SELECT id, name, official_color FROM platform_editions WHERE platform_id = %s;', (current_platform['id'],))
		platform_editions = cur.fetchall()

		for platform_edition in platform_editions:
			current_edition = {
				'id': platform_edition[0],
				'name': platform_edition[1],
				'official_color': platform_edition[2],
				'colors': []
			}

			cur.execute('SELECT colors.id as id, colors.name as name FROM colors JOIN colors_platform_editions as cpe ON id = cpe.color_id WHERE cpe.platform_edition_id = %s;', (current_edition['id'],))
			colors = cur.fetchall()

			for color in colors:
				current_edition['colors'].append(color[1])
		
			current_platform['editions'].append(current_edition)
		current_platform_family['platforms'].append(current_platform)
	platform_family_configs.append(current_platform_family)

cur.execute('SELECT id, title, body FROM listings WHERE is_scanned = %s', (False,))
all_listings = cur.fetchall()

# for listing in all_listings:
	# print('\n\n--------------------------------\n')
	# print(listing[0])
	# print(listing[1])

platform_matchers = []

pprint.pprint(platform_family_configs)
for family_config in platform_family_configs:
	for platform_config in family_config['platforms']:
		platform_config['family_id'] = family_config['id']
		platform_config['family_name'] = family_config['name']
		platform_matchers.append(PlatformMatchFinder(platform_config))

for listing in all_listings:
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
