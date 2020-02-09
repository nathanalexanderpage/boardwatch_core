import sys
import pathlib
path_to_parent = str(pathlib.Path(__file__).resolve().parents[1].absolute())
sys.path.append(path_to_parent)

import boardwatch

from boardwatch.common import board_site_enums
from boardwatch.scrape.populate_listings import ListingPopulator
from boardwatch.mail.mail_sender import Mailer

print('imports work')
