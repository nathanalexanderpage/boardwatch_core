import csv
import pprint as pp
import psycopg2 as db
import os

from dotenv import load_dotenv

pprint = pp.PrettyPrinter()

colors = []

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

with open('console_editions.tsv', newline='') as csv_editions:
    editions_reader = csv.reader(csv_editions, delimiter='\t')
    row_no = 0
    columns = []
    editions = list()
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
                            if color not in colors:
                                colors.append(color)
                        row_data[current_column] = cell_colors
                    elif current_column == 'edition':
                        row_data[current_column] = cell.replace('Pokemon', 'Pokémon')
                    elif current_column == 'design note':
                        row_data[current_column] = cell.replace('pokemon', 'Pokémon')
                    else:
                        row_data[current_column] = cell
                else:
                    row_data[current_column] = None
                column_no += 1
            editions.append(row_data)
        row_no += 1
# pprint.pprint(editions)
# print(colors)

# visual confirmation of data to be inserted
for family in console_families:
    print(family['name'])
    for console in consoles:
        if console['console'] == family['console']:
            # print('\t' + console['name'])
            for edition in editions:
                if edition['console'] == console['console'] and edition['variation ref'] == console['desc']:
                    printable = '\t\t'
                    if edition['edition'] is not None:
                        printable += edition['edition'] + ' - '
                    if edition['color'] is not None:
                        printable += edition['color'] + ' - '
                    if edition['colors'] is not None:
                        printable += ', '.join(edition['colors'])
                    # print(printable)

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

# cur.execute("SELECT * FROM table;")
# all = (cur.fetchall())
# print(len(all[0]))

# for family in console_families:
#     print(family['name'])
#     for console in consoles:
#         if console['console'] == family['console']:
#             print('\t' + console['name'])
#             for edition in editions:
#                 if edition['console'] == console['console'] and edition['variation ref'] == console['desc']:
#                     printable = '\t\t'
#                     if edition['edition'] is not None:
#                         printable += edition['edition'] + ' - '
#                     if edition['color'] is not None:
#                         printable += edition['color'] + ' - '
#                     if edition['colors'] is not None:
#                         printable += ', '.join(edition['colors'])
#                     print(printable)

cur.execute("SELECT id FROM colors WHERE name = 'black';")
all = (cur.fetchall())
pprint.pprint(len(all))

for color in colors:
    cur.execute('INSERT INTO colors (name) VALUES(%s);', (color,))
    conn.commit()
    cur.execute('SELECT * FROM colors WHERE name = %s;', (color,))
    all = (cur.fetchall())
    pprint.pprint(all[0])

for family in console_families:
    pprint.pprint(family)
    cur.execute('INSERT INTO platform_families (name, generation, developer) VALUES(%s, %s, %s);', (family['name'], family['generation'], family['developer']))
    conn.commit()
    cur.execute('SELECT * FROM platform_families WHERE name = %s;', (family['name'],))
    all = (cur.fetchall())
    pprint.pprint(all[0])

for name_group in name_groups:
    pprint.pprint(name_group)
    cur.execute('INSERT INTO platform_name_groups (name, description) VALUES(%s, %s);', (name_group['name'], name_group['description']))
    conn.commit()
    cur.execute('SELECT * FROM platform_name_groups WHERE name = %s;', (name_group['name'],))
    all = (cur.fetchall())
    pprint.pprint(all[0])

for console in consoles:
    values = (console['name'], console['is_brand_missing'], console['model_no'], console['storage'], console['description'], console['notes'], console['relevance'])

    cur.execute('INSERT INTO platforms (name, is_brand_missing, model_no, storage_capacity, description, disambiguation, relevance) VALUES(%s, %s, %s, %s, %s, %s, %s);', values)
    conn.commit()
    cur.execute('SELECT * FROM platforms WHERE name = %s;', (console['name'],))
    all = (cur.fetchall())
    pprint.pprint(all[0])

cur.close()
conn.close()
print('-------------------- exit SQL section --------------------')
