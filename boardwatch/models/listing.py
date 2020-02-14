class Listing():
	listings = []

	def __init__(self, id, native_id, title, body, url, seller_email, seller_phone, date_posted, date_scraped):
		self.id = id
		self.native_id = native_id
		self.title = title
		self.body = body
		self.url = url
		self.seller_email = seller_email
		self.seller_phone = seller_phone
		self.date_posted = date_posted
		self.date_scraped = date_scraped
		Listing.listings.append(self)
		