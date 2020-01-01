import csv
import pprint as pp
import psycopg2 as db
import os

from dotenv import load_dotenv

pprint = pp.PrettyPrinter()

colors = {}

console_families = list()
with open('console_families.tsv', newline='') as csv_platform_families:
	platform_families_reader = csv.reader(csv_platform_families, delimiter='\t')
	row_no = 0
	columns = []
	for row in platform_families_reader:
		if row_no is 0:
			for column in row:
				columns.append(column)
			# print(columns)
		else:
			row_data = {}
			column_no = 0
			for cell in row:
				current_column = columns[column_no]
				if cell is not '':
					if current_column in ['developer']:
						row_data[current_column] = cell.title()
					elif current_column in ['generation']:
						row_data[current_column] = int(cell)
					else:
						row_data[current_column] = cell
				else:
					row_data[current_column] = None
				column_no += 1
			console_families.append(row_data)
		row_no += 1
# pprint.pprint(console_families)

name_groups = list()
with open('name_groups.tsv', newline='') as csv_name_groups:
	name_groups_reader = csv.reader(csv_name_groups, delimiter='\t')
	row_no = 0
	columns = []
	for row in name_groups_reader:
		if row_no is 0:
			for column in row:
				columns.append(column)
			# print(columns)
		else:
			row_data = {}
			column_no = 0
			for cell in row:
				current_column = columns[column_no]
				if cell is not '':
					row_data[current_column] = cell
				else:
					row_data[current_column] = None
				column_no += 1
			name_groups.append(row_data)
		row_no += 1
# pprint.pprint(name_groups)

consoles = list()
with open('consoles.tsv', newline='') as csv_platforms:
	platforms_reader = csv.reader(csv_platforms, delimiter='\t')
	row_no = 0
	columns = []
	for row in platforms_reader:
		if row_no is 0:
			for column in row:
				columns.append(column)
			# print(columns)
		else:
			row_data = {}
			column_no = 0
			for cell in row:
				current_column = columns[column_no]
				if cell is not '':
					if cell == 'y' and current_column in ['is_brand_missing']:
						row_data[current_column] = True
					elif cell == 'n' and current_column in ['is_brand_missing']:
						row_data[current_column] = False
					else:
						row_data[current_column] = cell
				else:
					row_data[current_column] = None
				column_no += 1
			consoles.append(row_data)
		row_no += 1
# pprint.pprint(consoles)

console_editions = list()
with open('console_editions.tsv', newline='') as csv_editions:
	editions_reader = csv.reader(csv_editions, delimiter='\t')
	row_no = 0
	columns = []
	for row in editions_reader:
		if row_no is 0:
			for column in row:
				columns.append(column)
			# print(columns)
		else:
			row_data = {}
			column_no = 0
			for cell in row:
				current_column = columns[column_no]
				if cell is not '':
					if cell == 'y' and current_column in ['gloss', 'matte', 'transparency']:
						row_data[current_column] = True
					elif cell == 'n' and current_column in ['gloss', 'matte', 'transparency']:
						row_data[current_column] = False
					elif current_column == 'color':
						row_data[current_column] = cell.title()
					elif current_column == 'colors':
						cell_colors = cell.split(', ')
						for color in cell_colors:
							if color not in colors.keys():
								print('color')
								print(color)
								print('not in')
								print(colors.keys())
								colors[color] = None
						row_data[current_column] = cell_colors
					elif current_column == 'name':
						row_data[current_column] = cell.replace('Pokemon', 'Pokémon')
					elif current_column == 'design note':
						row_data[current_column] = cell.replace('pokemon', 'Pokémon')
					else:
						row_data[current_column] = cell
				else:
					row_data[current_column] = None
				column_no += 1
			console_editions.append(row_data)
		row_no += 1
# pprint.pprint(console_editions)

# visual confirmation of data to be inserted
for family in console_families:
	print(family['name'])
	for console in consoles:
		if console['console'] == family['console']:
			print('\t' + console['name'])
			for edition in console_editions:
				if edition['console'] == console['console'] and edition['variation ref'] == console['desc']:
					printable = '\t\t'
					if edition['name'] is not None:
						printable += edition['name'] + ' - '
					if edition['color'] is not None:
						printable += edition['color'] + ' - '
					if edition['colors'] is not None:
						printable += ', '.join(edition['colors'])
					print(printable)

# execute SQL seed statements
print('-------------------- enter SQL section --------------------')

load_dotenv(dotenv_path='../../.env')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

conn = db.connect(dbname=POSTGRESQL_DBNAME, user=POSTGRESQL_USERNAME, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT)
cur = conn.cursor()

for family in console_families:
	pprint.pprint(family)
	cur.execute('INSERT INTO platform_families (name, generation, developer) VALUES(%s, %s, %s) RETURNING id, name, generation, developer;', (family['name'], family['generation'], family['developer']))
	conn.commit()

	query_result = cur.fetchone()
	pprint.pprint(query_result)
	family['id'] = query_result[0]

for name_group in name_groups:
	pprint.pprint(name_group)
	cur.execute('INSERT INTO platform_name_groups (name, description) VALUES(%s, %s) RETURNING id, name, description;', (name_group['name'], name_group['description']))
	conn.commit()

	query_result = cur.fetchone()
	pprint.pprint(query_result)
	name_group['id'] = query_result[0]

for console in consoles:
	console['name_group_id'] = None
	for name_group in name_groups:
		if name_group['name'] in console['name']:
			console['name_group_id'] = name_group['id']

	console['platform_family_id'] = None
	for family in console_families:
		if family['console'] == console['console']:
			console['platform_family_id'] = family['id']

	values = (console['name'], console['platform_family_id'], console['name_group_id'], console['is_brand_missing'], console['model_no'], console['storage'], console['description'], console['notes'], console['relevance'])

	cur.execute('INSERT INTO platforms (name, platform_family_id, name_group_id, is_brand_missing, model_no, storage_capacity, description, disambiguation, relevance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, name, name_group_id, is_brand_missing, model_no, storage_capacity, description, disambiguation, relevance;', values)
	conn.commit()

	query_result = cur.fetchone()
	pprint.pprint(query_result)
	console['id'] = query_result[0]

for color in colors.keys():
	cur.execute('INSERT INTO colors (name) VALUES(%s) RETURNING id, name;', (color,))
	conn.commit()

	query_result = cur.fetchone()
	pprint.pprint(query_result)
	colors[color] = query_result[0]

for edition in console_editions:
	for console in consoles:
		if edition['console'] == console['console'] and edition['variation ref'] == console['desc']:
			edition['platform_id'] = console['id']

	values = (edition['name'], edition['platform_id'], edition['color'], edition['matte'], edition['transparency'], edition['gloss'], edition['design note'], edition['image_url'])

	cur.execute('INSERT INTO platform_editions (name, platform_id, official_color, has_matte, has_transparency, has_gloss, note, image_url) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, name, platform_id, official_color, has_matte, has_transparency, has_gloss, note, image_url;', values)
	conn.commit()

	query_result = cur.fetchone()
	edition['id'] = query_result[0]

	for color in colors.keys():
		if color in edition['colors']:
			cur.execute('INSERT INTO colors_platform_editions (platform_edition_id, color_id) VALUES(%s, %s)', (edition['id'], colors[color]))
	conn.commit()

cur.close()
conn.close()
print('-------------------- exit SQL section --------------------')
pprint.pprint(console_editions)
