import os
import psycopg2 as db
from dotenv import load_dotenv
from .scraper import CraigslistPostScraper
from .soup_maker import CraigslistPostSoupMaker, CraigslistSoupMaker
from boardwatch.common import board_site_enums

import pprint
pp = pprint.PrettyPrinter(indent=2)

class ListingPopulator():
	def populate(self):
		cl_results_scraper = CraigslistSoupMaker()
		results = cl_results_scraper.make_soup()

		# pp.pprint(results)

		load_dotenv(dotenv_path='../../.env')
		POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
		POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
		POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
		POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
		POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

		conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
		cur = conn.cursor()

		for board in [board for board in board_site_enums.board_sites if board['is_supported'] == True]:
			cur.execute('SELECT id FROM boards WHERE name = %s', (board['name'],))
			board_id = cur.fetchone()

			for result in results:
				cur.execute('SELECT id, native_id, title FROM listings WHERE native_id = %s', (result['id'],))
				existing_post_id = cur.fetchone()
				if existing_post_id is None:
					post_soup_maker = CraigslistPostSoupMaker()
					post_soup_maker.set_url(result['url'])
					post_soup = post_soup_maker.make_soup()
					post_data = CraigslistPostScraper(post_soup)

					# print('printing post_data:')
					# print(post_data.data)

					cur.execute('INSERT INTO listings (board_id, native_id, url, title, body, seller_email, seller_phone, date_posted) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, title', (board_id, result['id'], result['url'], result['title_massaged'], post_data.data['body'], post_data.data['seller_email'], post_data.data['seller_phone'], result['datetime']))
					conn.commit()
					insert_response = cur.fetchone()
				else:
					print('listing already in database; skipping')
					print(existing_post_id)
