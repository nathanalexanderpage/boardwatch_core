import os
import pathlib
import pprint
import sys
import re

from boardwatch_models import Board, Listing, Platform, PlatformEdition, PlatformNameGroup, User
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from common.board_site_enums import board_sites
from data.puller import DataPuller
from boardwatch.mail.mail_sender import Mailer
from boardwatch.match.match import Match
from boardwatch.match.preppers import Prepper
from boardwatch.scrape.populate_listings import ListingPopulator
from boardwatch.scrape.listing_pop_maker import ListingPopulatorMaker

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

# gather new listings
for board in Board.get_all():
	populator = ListingPopulatorMaker.make_listing_populator(board)
	populator.populate()

# pull all database listings newer than 1 day old
DataPuller.pull_listings()

# find all product matches within listing; ensure no two matchings using same text within each posting; insert remaining matches to db
Match.find_matches()
Match.remove_competing_matches()
Match.insert_all_to_db()
Match.clear_registry()

# pull platform edition watches from db
user_pe_watches = DataPuller.pull_platform_edition_watches()

print('user_pe_watches')
pp.pprint(user_pe_watches)

# pull platform edition presences from db
pe_presences_per_pe = DataPuller.pull_platform_edition_presences()

print('pe_presences_per_pe')
pp.pprint(pe_presences_per_pe)

# pull platform edition watches from db
user_platform_watches = DataPuller.pull_platform_watches()

print('user_platform_watches')
pp.pprint(user_platform_watches)

# pull platform presences from db
platform_presences_per_platform = DataPuller.pull_platform_presences()

print('platform_presences_per_platform')
pp.pprint(platform_presences_per_platform)

# calibrate Mailer class to platform edition presences
Mailer.calibrate_pe_presences(pe_presences_per_pe)
Mailer.calibrate_platform_presences(platform_presences_per_platform)
del pe_presences_per_pe, platform_presences_per_platform

# pull all users from db
DataPuller.pull_users()

pprint.pprint(Match.get_all())

# iterate through user_pe_watches, sending e-mail notification for each user
for user_id in user_pe_watches:
	user = User.get_by_id(user_id)
	mailer = Mailer(user=user, platforms=user_platform_watches.get(user.id), platform_editions=user_pe_watches.get(user.id), games=None, accessories=None)
	is_user_mail_html_compatible = True
	mailer.send_mail(is_user_mail_html_compatible)
del user_pe_watches

cur.close()
