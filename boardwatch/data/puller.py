import os

from boardwatch_models import Board, Listing, Platform, PlatformEdition
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from boardwatch.common.board_site_enums import board_sites

load_dotenv(dotenv_path=find_dotenv())
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)

class DataPuller():
    def __init__(self):
        pass

    def pull_boards(self):
        cur = conn.cursor()

        cur.execute("""SELECT id, name FROM boards;""")
        boards = cur.fetchall()

        for site in board_sites:
            for board in boards:
                if site['name'] == board[1] and site['is_supported'] == True:
                    Board(board[0], site['name'], site['url'], site['is_supported'])

        cur.close()

    def pull_listings(self):
        pass

    def pull_platform_name_groups(self):
        pass

    def pull_platforms(self):
        pass

    def pull_platform_editions(self):
        pass

    def pull_games(self):
        pass
