import os
import pathlib
import psycopg2 as db
import sys
from dotenv import load_dotenv

path_to_root = str(pathlib.Path(__file__).resolve().parents[2].absolute())
sys.path.append(path_to_root)

import boardwatch

load_dotenv(dotenv_path='../../.env')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_DBNAME = os.getenv('POSTGRESQL_DBNAME')

