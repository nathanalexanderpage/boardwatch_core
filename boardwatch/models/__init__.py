import os
import pathlib
import psycopg2 as db
import sys
from dotenv import load_dotenv

path_to_root = str(pathlib.Path(__file__).resolve().parents[2].absolute())
sys.path.append(path_to_root)

from boardwatch.models.board import Board
from boardwatch.models.board_maker import BoardMaker
from boardwatch.models.game import Game
from boardwatch.models.listing import Listing
from boardwatch.models.platform import Platform
from boardwatch.models.platform_edition import PlatformEdition
