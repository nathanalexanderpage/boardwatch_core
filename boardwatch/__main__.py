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
DataPuller.pull_boards()
DataPuller.pull_platform_name_groups()
DataPuller.pull_platforms()
DataPuller.pull_platform_editions()

# platform families
# FIXME: pfs missing

profiler = Profiler()

# gather new listings
for board in Board.get_all():
	populator = ListingPopulatorMaker.make_listing_populator(board)
	populator.populate()

# pull all database listings newer than 1 day old
DataPuller.pull_listings()

# find product instances in listings
for listing in Listing.get_all():
	for edition in PlatformEdition.get_all():
		searchtexts = profiler.build_string_matches(edition)
		# pp.pprint(searchtexts)

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
					except Exception as e:
						# print(e)
						continue
pp.pprint(Match.get_all())
# ensure matches are checked against each other (no more than one product match record per text segment in listing)
Match.remove_competing_matches()

# insert db record to indicate match between listing and each found product
# cur.execute("""INSERT INTO listings_platform_editions (listing_id, platform_edition_id) VALUES(%s, %s);""", (listing.id, edition.id,))

# loop through users. send e-mail notifications only for those whose settings indicate that preference.
cur.execute("""SELECT wpe.user_id as user_id, pf.name AS platform_family, p.name AS platform, p.id AS p_id, wpe.platform_edition_id as watched_platform_edition_id, pe.name AS edition_name, pe.official_color AS official_color, x.colors AS colors FROM watchlist_platform_editions as wpe JOIN platform_editions AS pe ON pe.id = wpe.platform_edition_id JOIN platforms AS p ON pe.platform_id = p.id JOIN platform_families AS pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id JOIN generations AS gen ON gen.id = pf.generation JOIN (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors FROM platform_editions AS pe JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id JOIN colors AS c ON c.id = cpe.color_id GROUP BY pe.id 	ORDER BY pe.id) AS x ON x.id = pe.id ORDER BY user_id, gen.id, png.name, platform_family, platform;""")
raw_pe_watches = cur.fetchall()

pe_watches = []

for watch in raw_pe_watches:
	pe_watches.append({
		'user_id': watch[0],
		'platform_family': watch[1],
		'platform': watch[2],
		'platform_id': watch[3],
		'watched_platform_edition_id': watch[4],
		'edition_name': watch[5],
		'official_color': watch[6],
		'colors': watch[7].split(', ')
	})

user_watches = {}

for watch in pe_watches:
	pp.pprint(watch)
	if watch['user_id'] not in user_watches:
		user_watches[watch['user_id']] = {}
	if watch['platform_id'] not in user_watches[watch['user_id']]:
		user_watches[watch['user_id']][watch['platform_id']] = []
	user_watches[watch['user_id']][watch['platform_id']].append(watch['watched_platform_edition_id'])

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
pp.pprint(Match.get_all())

# iterate through user_watches, composing e-mail notification for each user

cur.close()
