import csv
import pprint as pp

pprint = pp.PrettyPrinter()

with open('console_editions.tsv', newline='') as csv_editions:
    editions_reader = csv.reader(csv_editions, delimiter='\t')
    row_no = 0
    columns = []
    editions = []
    for row in editions_reader:
        if row_no is 0:
            for column in row:
                print(column)
                columns.append(column)
            print(columns)
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
                        row_data[current_column] = cell.split(', ')
                    elif current_column == 'edition':
                        row_data[current_column] = cell.replace('Pokemon', 'Pokémon')
                    elif current_column == 'design note':
                        row_data[current_column] = cell.replace('pokemon', 'Pokémon')
                    else:
                        row_data[current_column] = cell
                else:
                    row_data[current_column] = None
                column_no += 1
            # FIXME: properly escape for SQL; ensure right columns present
            print(f"INSERT INTO platform_editions (name, official_color, has_matte, has_transparency, has_gloss, note, image_url_filename) VALUES('{row_data['edition']}', '{row_data['color']}', {row_data['matte']}, {row_data['gloss']}, {row_data['transparency']}, {row_data['design note']}, NULL);")
        row_no += 1

with open('consoles.tsv', newline='') as csv_platforms:
    platforms_reader = csv.reader(csv_platforms, delimiter='\t')
    row_no = 0
    columns = []
    editions = []
    for row in platforms_reader:
        if row_no is 0:
            for column in row:
                columns.append(column)
            print(columns)
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
            # FIXME: properly escape for SQL; ensure right columns present
            # print(f"INSERT INTO platforms (name, platform_family, name_group, model_no, storage_capacity, disambiguation, relevance) VALUES('{row_data['name']}', 'FK', 'FK', '{row_data['model no']}', '{row_data['storage']}', '{row_data['notes']}', {row_data['relevance']});")
        row_no += 1

with open('console_families.tsv', newline='') as csv_platform_families:
    platform_families_reader = csv.reader(csv_platform_families, delimiter='\t')
    row_no = 0
    columns = []
    editions = []
    for row in platform_families_reader:
        if row_no is 0:
            for column in row:
                columns.append(column)
            print(columns)
        else:
            row_data = {}
            column_no = 0
            for cell in row:
                current_column = columns[column_no]
                if cell is not '':
                    if current_column in ['developer']:
                        row_data[current_column] = cell.title()
                    else:
                        row_data[current_column] = cell
                else:
                    row_data[current_column] = None
                column_no += 1
            # FIXME: properly escape for SQL; ensure right columns present
            # print(f"INSERT INTO platform_families (name, developer) VALUES('{row_data['name']}', '{row_data['developer']}');")
        row_no += 1
