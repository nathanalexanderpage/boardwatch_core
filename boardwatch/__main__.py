import os
import pathlib
import pprint
import sys

from boardwatch_models import Board
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from common.board_site_enums import board_sites
from match.matchers import Prepper
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

cur.execute('SELECT id, name FROM boards;')
boards = cur.fetchall()

for site in board_sites:
	for board in boards:
		if site['name'] == board[1] and site['is_supported'] == True:
			Board(board[0], site['name'], site['url'], site['is_supported'])

for board in Board.boards:
	print(dir(board))

	listing_pop_maker = ListingPopulatorMaker(board)

	populator = listing_pop_maker.make_listing_populator()
	populator.populate()
