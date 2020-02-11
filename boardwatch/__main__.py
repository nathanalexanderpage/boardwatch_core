import sys
import pathlib
path_to_root = str(pathlib.Path(__file__).resolve().parents[1].absolute())
sys.path.append(path_to_root)
import boardwatch.common.board_site_enums as site_enums
from boardwatch.scrape.populate_listings import ListingPopulator
from boardwatch.match.matchers import dsfjdaisjfdnvwieuncoi

populator = ListingPopulator()
populator.populate()
