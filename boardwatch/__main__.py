import os
import pathlib
import pprint
import sys
import re

from boardwatch_models import Board, Listing, Platform, PlatformEdition, PlatformNameGroup
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from common.board_site_enums import board_sites
from data.puller import DataPuller
from match.match import Match
from match.preppers import Prepper
from match.profilers import Profiler
from scrape.populate_listings import ListingPopulator
from scrape.listing_pop_maker import ListingPopulatorMaker

pp = pprint.PrettyPrinter()

load_dotenv(dotenv_path=find_dotenv())
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
cur = conn.cursor()

# pull all product data from db
data_puller = DataPuller()
data_puller.pull_boards()
data_puller.pull_platform_name_groups()

# platform families
# FIXME: pfs missing

# platforms
cur.execute("""SELECT p.id, p.name, p.is_brand_missing, p.platform_family_id, pf.name as platform_family_name, p.model_no, p.storage_capacity, p.description, p.disambiguation, p.relevance FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups as png ON png.id = p.name_group_id;""")
raw_ps = cur.fetchall()
for raw_p in raw_ps:
	p = Platform(id=raw_p[0], name=raw_p[1], is_brand_missing_from_name=raw_p[2], platform_family_id=raw_p[3], platform_family_name=raw_p[4], model_no=raw_p[5], storage_capacity=raw_p[6], description=raw_p[7], disambiguation=raw_p[8], relevance=raw_p[9])
	p.add_to_registry()

# platform editions
cur.execute("""SELECT pe.id AS id, pe.name AS name, pe.official_color AS official_color, pe.has_matte AS has_matte, pe.has_transparency AS has_transparency, pe.has_gloss AS has_gloss, pe.note AS note, pe.image_url AS image_url, x.colors, p.id AS platform_id FROM platforms AS p JOIN platform_editions AS pe ON pe.platform_id = p.id JOIN (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors FROM platform_editions AS pe JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id JOIN colors AS c ON c.id = cpe.color_id GROUP BY pe.id ORDER BY pe.id) AS x ON x.id = pe.id ORDER BY p.id, name, official_color;
""")
raw_platform_editions = cur.fetchall()
for raw_pe in raw_platform_editions:
	pe = PlatformEdition(id=raw_pe[0], name=raw_pe[1], official_color=raw_pe[2], has_matte=raw_pe[3], has_transparency=raw_pe[4], has_gloss=raw_pe[5], note=raw_pe[6], image_url=raw_pe[7])

	for color in raw_pe[8].split(', '):
		pe.colors.append(color)

	# put edition to platform
	p_id = raw_pe[9]
	pp.pprint(Platform.get_all())
	Platform.get_by_id(p_id).add_edition(pe)

profiler = Profiler()

for board in Board.get_all():
	populator = ListingPopulatorMaker(board).make_listing_populator()
	populator.populate()
	# pull all new listings
	# for listing in Listing.listings:
	test_listing = Listing(id=0, native_id=0, title='TEST LISTING SNES console', body='TEST LISTING\nused SNS-101 console, good condition purple Super Nintendo Entertainment System', url='https://www.domain.tld/page', seller_email=None, seller_phone=None, date_posted=None, date_scraped=None)
	for listing in [test_listing]:
		print(listing)

		# for each listing, iterate through all products
		for platform in Platform.get_all():
			print(platform.name)
			# print(platform.editions)
			if platform.name == 'Super Nintendo Entertainment System':
				# print('\n\n\n------------SNES-----------\n\n\n')
				for edition in platform.editions:
					searchtexts = profiler.build_string_matches(platform)
					pp.pprint(searchtexts)

					for degree in searchtexts.keys():
						
						# for each listing, iterate through all searchable text segments
						for searchtext in searchtexts[degree]:
							for text in [listing.title, listing.body]:
								# evaluate if preliminary match on spot (wherever hot text within listing happens to be)
								try:
									match_index = text.index(searchtext)
									print('FOUND ' + searchtext + ' @ ' + str(match_index))
									Match(score=1, start=match_index, end=match_index+len(searchtext), item=current_p, listing=listing)
								except Exception as e:
									# print(e)
									continue

					continue
					
					# if preliminary match, look in product's name group to check if matched item text isn't suited better for a different product with similar name

					# insert db record to indicate match between listing and each found product
					for match in Match.matches:
						if match.type == 'platform':
							cur.execute("""INSERT INTO listings_platform_editions (listing_id, platform_edition_id) VALUES(%s, %s);""", (listing.id, edition.id,))
						else:
							pass

# loop through users. send e-mail notifications only for those whose settings indicate that preference.
cur.execute("""SELECT wpe.user_id as user_id, pf.name AS platform_family, p.name AS platform, wpe.platform_edition_id as watched_platform_edition_id, pe.name AS edition_name, pe.official_color AS official_color, x.colors AS colors FROM watchlist_platform_editions as wpe JOIN platform_editions AS pe ON pe.id = wpe.platform_edition_id JOIN platforms AS p ON pe.platform_id = p.id JOIN platform_families AS pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id JOIN generations AS gen ON gen.id = pf.generation JOIN (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors FROM platform_editions AS pe JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id JOIN colors AS c ON c.id = cpe.color_id GROUP BY pe.id ORDER BY pe.id) AS x ON x.id = pe.id ORDER BY user_id, gen.id, png.name, platform_family, platform;""")
raw_pe_watches = cur.fetchall()

pe_watches = []

for watch in raw_pe_watches:
	pe_watches.append({
		'user_id': watch[0],
		'platform_family':  watch[1],
		'platform': watch[2],
		'watched_platform_edition_id': watch[3],
		'edition_name': watch[4],
		'official_color': watch[5],
		'colors': watch[6].split(', ')
	})

user_watches = {}

for watch in pe_watches:
	if watch['user_id'] not in user_watches:
		user_watches[watch['user_id']] = {}
	if watch['platform'] not in user_watches[watch['user_id']]:
		user_watches[watch['user_id']][watch['platform']] = []
	user_watches[watch['user_id']][watch['platform']].append(watch['watched_platform_edition_id'])

pp.pprint(user_watches)

# grab product presences, organize in respective lookup dicts
cur.execute("""SELECT listing_id, platform_edition_id FROM listings_platform_editions;""")
raw_pe_presences = cur.fetchall()

pe_presences = []
pe_presences_per_pe = {}

for presence in raw_pe_presences:
	pe_presences.append({
		'listing_id': presence[0],
		'platform_edition_id': presence[1]
	})

for presence in pe_presences:
	if presence['platform_edition_id'] not in pe_presences_per_pe:
		pe_presences_per_pe[presence['platform_edition_id']] = presence['listing_id']

pp.pprint(pe_presences_per_pe)

# iterate through user_watches, composing e-mail notification for each user

cur.close()
