import re

class FakeResult():
	def __init__(self, title):
		self.data = {}
		self.data['datetime'] = '2019-10-28 00:53'
		self.data['neighborhood'] = '(Kirkland/Kingsgate/Northgate/Greenlake)',
		self.data['price'] = 4
		self.data['url'] = 'https://seattle.craigslist.org/see/vgm/d/kirkland-sega-game-gear-handheld-system/6988310659.html'
		title_tag_cleaned = re.sub(',', ', ', title).strip()
		title_tag_cleaned = re.sub(' {2,}', ' ', title_tag_cleaned)
		self.data['title'] = title_tag_cleaned
		duplicate_remove_chars = [
			'\\?'
			'\\*'
			'!',
			'-',
			',',
			'~',
			'&'
		]
		for char in duplicate_remove_chars:
			str_to_replace_command = char + '{2,}'
			title_tag_cleaned = re.sub(str_to_replace_command, char, title_tag_cleaned)
		self.data['title_massaged'] = title_tag_cleaned
