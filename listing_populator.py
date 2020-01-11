import os
import psycopg2 as db
from dotenv import load_dotenv
from soup_maker import *

import pprint
pp = pprint.PrettyPrinter(indent=2)

cl_results_scraper = CraigslistSoupMaker()
results = cl_results_scraper.scrape()

pp.pprint(results)

load_dotenv(dotenv_path='../../.env')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
cur = conn.cursor()

boards = ['Craigslist']

for board in boards:
	cur.execute('SELECT id FROM boards WHERE name = %s', (board,))
	board_id = cur.fetchone()

	for result in results:
		post_data = CraigslistResultScraper(result)
		cur.execute('INSERT INTO listings (board_id, native_id, url, title, body, seller_email, seller_phone, date_posted) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (board_id, result['id'], result['url'], result['title_massaged'], result['body'], result['seller_email'], result['seller_phone'], result['datetime']))
