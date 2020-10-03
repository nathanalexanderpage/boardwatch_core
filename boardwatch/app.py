import sys
import pathlib
path_to_root = str(pathlib.Path(__file__).resolve().parents[1].absolute())
sys.path.append(path_to_root)

from common import board_site_enums
from scrape.populate_listings import ListingPopulator
from mail.mail_sender import Mailer

print('imports work')
