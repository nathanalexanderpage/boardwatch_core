import os

from boardwatch_models import Board, Listing, Platform, PlatformEdition, PlatformNameGroup
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
        cur = conn.cursor()

        cur.execute("""SELECT id, name, description FROM platform_name_groups;""")
        raw_platform_name_groups = cur.fetchall()

        for raw_png in raw_platform_name_groups:
            png = PlatformNameGroup(id=raw_png[0], name=raw_png[1], description=raw_png[2])
            png.add_to_registry()

        cur.close()

    def pull_platforms(self):
        cur = conn.cursor()

        cur.execute("""SELECT p.id, p.name, p.is_brand_missing, p.platform_family_id, pf.name as platform_family_name, p.model_no, p.storage_capacity, p.description, p.disambiguation, p.relevance FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups as png ON png.id = p.name_group_id;""")
        raw_ps = cur.fetchall()
        
        for raw_p in raw_ps:
            p = Platform(id=raw_p[0], name=raw_p[1], is_brand_missing_from_name=raw_p[2], platform_family_id=raw_p[3], platform_family_name=raw_p[4], model_no=raw_p[5], storage_capacity=raw_p[6], description=raw_p[7], disambiguation=raw_p[8], relevance=raw_p[9])
            p.add_to_registry()

        cur.close()

    def pull_platform_editions(self):
        pass

    def pull_games(self):
        pass
