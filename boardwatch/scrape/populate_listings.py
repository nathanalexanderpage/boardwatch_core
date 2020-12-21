import os
import pprint

from boardwatch_models import Board, Listing
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from .scraper import CraigslistPostScraper
from .soup_maker import CraigslistPostSoupMaker, CraigslistSoupMaker
from boardwatch.common import board_site_enums

pp = pprint.PrettyPrinter(indent=2)

load_dotenv(dotenv_path=find_dotenv())
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

class ListingPopulator():
	def populate(self):
		print('Trying to execute for unconfigured board site')

class CraigslistListingPopulator(ListingPopulator):
	def populate(self):
		print('making scraper')
		cl_results_scraper = CraigslistSoupMaker()
		print('making soup')
		results = cl_results_scraper.make_soup()

		# pp.pprint(results)

		conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
		cur = conn.cursor()

		for board in [board for board in board_site_enums.board_sites if board['is_supported'] == True]:
			cur.execute('SELECT id FROM boards WHERE name = %s', (board['name'],))
			board_id = cur.fetchone()

			for result in results:
				cur.execute("""SELECT id, native_id, title FROM listings WHERE native_id = %s""", (result['id'],))
				existing_post_id = cur.fetchone()
				if existing_post_id is None:
					post_soup_maker = CraigslistPostSoupMaker()
					post_soup_maker.set_url(result['url'])
					post_soup = post_soup_maker.make_soup()
					post_data = CraigslistPostScraper(post_soup)

					listing = Listing(id=None, native_id=result['id'], title=result['title_massaged'], body=post_data.data['body'], price=None, url=result['url'], date_posted=result['datetime'], date_scraped=None)

					# TODO: move me to listing instance method
					cur.execute("""INSERT INTO listings (board_id, native_id, url, title, body, price, date_posted) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id, title;""", (board_id, listing.native_id, listing.url, listing.title, listing.body, listing.price, listing.date_posted))
					conn.commit()
					temp = cur.fetchone()
					print(temp)
				else:
					print('dupe listing; skipping')
					print(existing_post_id)
		cur.close()
