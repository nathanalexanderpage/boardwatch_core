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

	@staticmethod
	def pull_boards():
		cur = conn.cursor()
		cur.execute("""SELECT id, name FROM boards;""")
		raw_boards = cur.fetchall()

		for site in board_sites:
			for board in raw_boards:
				if site['name'] == board[1] and site['is_supported'] == True:
					Board(board[0], site['name'], site['url'], site['is_supported'])

		cur.close()

	@staticmethod
	def pull_listings():
		cur = conn.cursor()
		cur.execute("""SELECT id, native_id, title, body, price, url, date_posted, date_scraped, board_id FROM listings WHERE is_scanned = FALSE AND date_posted >= ((now() AT TIME ZONE 'utc') - interval '1 day');""")
		raw_listings = cur.fetchall()

		for raw_l in raw_listings:
			listing = Listing(id=raw_l[0], native_id=raw_l[1], title=raw_l[2], body=raw_l[3], price=raw_l[4], url=raw_l[5], date_posted=raw_l[6], date_scraped=raw_l[7])
			listing.add_to_registry()

		cur.close()

	@staticmethod
	def pull_platform_name_groups():
		cur = conn.cursor()
		cur.execute("""SELECT id, name, description FROM platform_name_groups;""")
		raw_platform_name_groups = cur.fetchall()

		for raw_png in raw_platform_name_groups:
			png = PlatformNameGroup(id=raw_png[0], name=raw_png[1], description=raw_png[2])
			png.add_to_registry()

		cur.close()

	@staticmethod
	def pull_platforms():
		cur = conn.cursor()
		cur.execute("""SELECT p.id, p.name, p.is_brand_missing, p.platform_family_id, pf.name as platform_family_name, p.model_no, p.storage_capacity, p.description, p.disambiguation, p.relevance FROM platforms as p JOIN platform_families as pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups as png ON png.id = p.name_group_id;""")
		raw_ps = cur.fetchall()

		for raw_p in raw_ps:
			p = Platform(id=raw_p[0], name=raw_p[1], is_brand_missing_from_name=raw_p[2], platform_family_id=raw_p[3], platform_family_name=raw_p[4], model_no=raw_p[5], storage_capacity=raw_p[6], description=raw_p[7], disambiguation=raw_p[8], relevance=raw_p[9])
			p.add_to_registry()

		cur.close()

	@staticmethod
	def pull_platform_editions():
		cur = conn.cursor()
		cur.execute("""SELECT pe.id AS id, pe.name AS name, pe.official_color AS official_color, pe.has_matte AS has_matte, pe.has_transparency AS has_transparency, pe.has_gloss AS has_gloss, pe.note AS note, pe.image_url AS image_url, x.colors, p.id AS platform_id FROM platforms AS p JOIN platform_editions AS pe ON pe.platform_id = p.id JOIN (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors FROM platform_editions AS pe JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id JOIN colors AS c ON c.id = cpe.color_id GROUP BY pe.id ORDER BY pe.id) AS x ON x.id = pe.id ORDER BY p.id, name, official_color;
		""")
		raw_platform_editions = cur.fetchall()

		for raw_pe in raw_platform_editions:
			pe = PlatformEdition(id=raw_pe[0], name=raw_pe[1], official_color=raw_pe[2], has_matte=raw_pe[3], has_transparency=raw_pe[4], has_gloss=raw_pe[5], note=raw_pe[6], image_url=raw_pe[7])

			for color in raw_pe[8].split(', '):
				pe.colors.append(color)

			# put edition to platform
			p_id = raw_pe[9]
			Platform.get_by_id(p_id).add_edition(pe)

			pe.add_to_registry()

		cur.close()

	@staticmethod
	def pull_games():
		pass
