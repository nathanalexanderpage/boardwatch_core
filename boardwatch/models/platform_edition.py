class PlatformEdition():
	def __init__(self, id, name, official_color, has_matte, has_transparency, has_gloss, note, image_url, colors=[]):
		self.id = id
		self.name = name
		self.official_color = official_color
		self.colors = colors
		self.has_matte = has_matte
		self.has_transparency = has_transparency
		self.has_gloss = has_gloss
		self.note = note
		self.image_url = image_url
