import os
import pathlib
import psycopg2 as db
import sys
from dotenv import load_dotenv

path_to_root = str(pathlib.Path(__file__).resolve().parents[2].absolute())
sys.path.append(path_to_root)

import boardwatch
