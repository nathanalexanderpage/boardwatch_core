import os

from boardwatch_models import Board, Listing, Platform, PlatformEdition, PlatformNameGroup, User
from dotenv import load_dotenv, find_dotenv
import psycopg2 as db

from boardwatch.common.board_site_enums import board_sites
from boardwatch.match.match import Match

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
		cur.execute("""SELECT id, native_id, title, body, price, url, date_posted, date_scraped, board_id FROM listings WHERE is_scanned = FALSE AND date_posted >= ((now() AT TIME ZONE 'utc') - interval '5 day');""")
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

	@staticmethod
	def pull_users():
		"""
		Pulls all users from db
		"""
		cur = conn.cursor()
		cur.execute("""SELECT id, username, email FROM users;""")
		raw_users = cur.fetchall()
		cur.close()

		for raw_user in raw_users:
			user = User(id=raw_user[0], username=raw_user[1], email=raw_user[2], public_id=None, password=None, created_at=None)
			user.add_to_registry()
		del raw_users

	@staticmethod
	def pull_platform_edition_watches():
		cur = conn.cursor()

		# loop through users. send e-mail notifications only for those whose settings indicate that preference.
		cur.execute("""SELECT wpe.user_id as user_id, pf.name AS platform_family, p.name AS platform, p.id AS p_id, wpe.platform_edition_id as watched_platform_edition_id, pe.name AS edition_name, pe.official_color AS official_color, x.colors AS colors FROM watchlist_platform_editions as wpe JOIN platform_editions AS pe ON pe.id = wpe.platform_edition_id JOIN platforms AS p ON pe.platform_id = p.id JOIN platform_families AS pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id JOIN generations AS gen ON gen.id = pf.generation JOIN (SELECT pe.id AS id, STRING_AGG(c.name,', ') AS colors FROM platform_editions AS pe JOIN colors_platform_editions AS cpe ON cpe.platform_edition_id = pe.id JOIN colors AS c ON c.id = cpe.color_id GROUP BY pe.id 	ORDER BY pe.id) AS x ON x.id = pe.id ORDER BY user_id, gen.id, png.name, platform_family, platform;""")
		raw_pe_watches = cur.fetchall()
		cur.close()

		pe_watches = []

		for watch in raw_pe_watches:
			pe_watches.append({
				'user_id': watch[0],
				'platform_family': watch[1],
				'platform': watch[2],
				'platform_id': watch[3],
				'watched_platform_edition_id': watch[4],
				'edition_name': watch[5],
				'official_color': watch[6],
				'colors': watch[7].split(', ')
			})

		user_pe_watches = {}

		for watch in pe_watches:
			if watch['user_id'] not in user_pe_watches:
				user_pe_watches[watch['user_id']] = {}
			if watch['platform_id'] not in user_pe_watches[watch['user_id']]:
				user_pe_watches[watch['user_id']][watch['platform_id']] = []
			user_pe_watches[watch['user_id']][watch['platform_id']].append(watch['watched_platform_edition_id'])
		
		return user_pe_watches

	@staticmethod
	def pull_platform_watches():
		cur = conn.cursor()

		# loop through users. send e-mail notifications only for those whose settings indicate that preference.
		cur.execute("""SELECT wp.user_id as user_id, p.name AS platform, p.id AS p_id, p.model_no AS model_no FROM watchlist_platforms as wp JOIN platforms AS p ON wp.platform_id = p.id JOIN platform_families AS pf ON pf.id = p.platform_family_id LEFT JOIN platform_name_groups AS png ON png.id = p.name_group_id JOIN generations AS gen ON gen.id = pf.generation;""")
		raw_platform_watches = cur.fetchall()
		cur.close()

		platform_watches = []

		for watch in raw_platform_watches:
			platform_watches.append({
				'user_id': watch[0],
				'platform': watch[1],
				'watched_platform_id': watch[2],
			})

		user_platform_watches = {}

		for watch in platform_watches:
			if watch['user_id'] not in user_platform_watches:
				user_platform_watches[watch['user_id']] = []
			user_platform_watches[watch['user_id']].append(watch['watched_platform_id'])
		
		return user_platform_watches

	@staticmethod
	def pull_platform_edition_presences():
		"""
		Returns product presences, organized in dict (keys are pe_id; values are listing_id)
		"""
		cur = conn.cursor()
		cur.execute("""SELECT listing_id, platform_edition_id, index_start, index_end, score FROM listings_platform_editions;""")
		raw_pe_presences = cur.fetchall()
		cur.close()

		pe_presences = []

		for presence in raw_pe_presences:
			pe_presences.append({
				'listing_id': presence[0],
				'platform_edition_id': presence[1],
				'index_start': presence[2],
				'index_end': presence[3],
				'score': presence[4]
			})
		del raw_pe_presences

		pe_presences_per_pe = {}

		for presence in pe_presences:
			if presence['platform_edition_id'] not in pe_presences_per_pe:
				pe_presences_per_pe[presence['platform_edition_id']] = list()
			pe_presences_per_pe[presence['platform_edition_id']].append(presence['listing_id'])

			match = Match(score=presence['score'], start=presence['index_start'], end=presence['index_end'], item=PlatformEdition.get_by_id(presence['platform_edition_id']), listing=Listing.get_by_id(presence['listing_id']))
			match.add_to_registry()
			
		print('inner Match')
		print(Match)

		del pe_presences
			
		return pe_presences_per_pe

	@staticmethod
	def pull_platform_presences():
		"""
		Returns product presences, organized in dict (keys are p_id; values are listing_id)
		"""
		cur = conn.cursor()
		cur.execute("""SELECT listing_id, platform_id, index_start, index_end, score FROM listings_platforms;""")
		raw_platform_presences = cur.fetchall()
		cur.close()

		platform_presences = []

		for presence in raw_platform_presences:
			platform_presences.append({
				'listing_id': presence[0],
				'platform_id': presence[1],
				'index_start': presence[2],
				'index_end': presence[3],
				'score': presence[4]
			})
		del raw_platform_presences

		platform_presences_per_pe = {}

		for presence in platform_presences:
			if presence['platform_id'] not in platform_presences_per_pe:
				platform_presences_per_pe[presence['platform_id']] = list()
			platform_presences_per_pe[presence['platform_id']].append(presence['listing_id'])

			match = Match(score=presence['score'], start=presence['index_start'], end=presence['index_end'], item=Platform.get_by_id(presence['platform_id']), listing=Listing.get_by_id(presence['listing_id']))
			match.add_to_registry()

		del platform_presences
		
		return platform_presences_per_pe
