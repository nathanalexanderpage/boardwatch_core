# import os
# import psycopg2 as db
# from dotenv import load_dotenv

# load_dotenv(dotenv_path='../../.env')
# POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
# POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
# POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
# POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
# POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

class Board():
	boards = []

	def __init__(self, id, name, url, is_scraping_supported, listings=[]):
		self.id = id
		self.name = name
		self.url = url
		self.is_scraping_supported = is_scraping_supported
		self.listings = listings
		Board.boards.append(self)

	def summary(self):
		print('id: ' + str(self.id))
		print('name: ' + self.name)
		print('url: ' + self.url)
		print('is_scraping_supported: ' + str(self.is_scraping_supported))

	def insert_listings_into_db(self):
		conn = db.connect()
		for listing in self.listings:
			break
