from boardwatch.models.board import Board
from boardwatch.scrape.populate_listings import ListingPopulator, CraigslistListingPopulator

class ListingPopulatorMaker():
	def __init__(self, board):
		self.board = board


	def make_listing_populator(self):
		if self.board.name == 'Craigslist':
			return CraigslistListingPopulator()
		else:
			return ListingPopulator()
