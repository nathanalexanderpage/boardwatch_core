import os
import psycopg2 as db
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
cur = conn.cursor()

cur.execute('SELECT title, body FROM listings WHERE is_scanned = %s', (False,))
listings = cur.fetchall()

for listing in listings:
    print('\n--------------------------------\n')
    print(listing[0])
    print(listing[1])
