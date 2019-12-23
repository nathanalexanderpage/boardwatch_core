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
            pprint.pprint(row_data)
        row_no += 1

with open('consoles.tsv', newline='') as csv_consoles:
    consoles_reader = csv.reader(csv_consoles, delimiter='\t')
    row_no = 0
    columns = []
    editions = []
    for row in consoles_reader:
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
            pprint.pprint(row_data)
            # print("INSERT INTO platforms (name, platform_family, name_group, model_no, storage_capacity, description, disambiguation, relevance) VALUES('GameCube', 'FK', 'FK', 'DOL-001', 'pink', 'Nintendo''s ______th home console, debuted in', 'the original GameCube', 10);")
        row_no += 1
