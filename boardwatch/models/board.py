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

    def __init__(self, id, name, url, listings=[]):
        self.id = id
        self.name = name
        self.url = url
        self.listings = listings
        self.is_scraping_supported
		boards.append(self)

    def insert_listings_into_db(self)
		for listing in self.listings:
			# conn = db.connect()
