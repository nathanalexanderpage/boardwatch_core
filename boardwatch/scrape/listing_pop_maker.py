from boardwatch_models import Board

from boardwatch.scrape.populate_listings import ListingPopulator, CraigslistListingPopulator

class ListingPopulatorMaker():
	def __init__(self):
		pass

	@staticmethod
	def make_listing_populator(board):
		if board.name == 'Craigslist':
			return CraigslistListingPopulator()
		else:
			return ListingPopulator()
