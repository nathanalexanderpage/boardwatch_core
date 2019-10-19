class MatchFinder():
	def __init__(self, want, config):
		self.type = 'generic'
		self.want = want
		self.disambig = disambig_items

	def def_self_attr(self):


	def assess_match(self, result):
		match_score = 0.9
		for match_keyword_strong in self.want['match_strong']:
			if match_keyword_strong.lower() in result['title']:
				match_score *= 1.5
				break
		for match_keyword_weak in self.want['match_weak']:
			if match_keyword_weak.lower() in result['title']:
				match_score *= 1.2
				break
		return match_score

class ConsoleMatchFinder(MatchFinder):
	def __init__(self):
		self.type = 'console'
		self.avoid = {
			'before': {
				'space_separated_yes': [
					'your',
					'for',
					'broken',
					'buying'
				]
			}
		}

	def assess_match(self, result):
		print('this is where a match score will be calculated for consoles once the child class is filled out. for now, use parent class MatchFinder.')

if __name__ == '__main__':
	print('running ' + __file__)

	example_wants = []
	example_disambig = []
	example_want_ps4 = {
		'id': '001',
		'type': 'console',
		'name': 'PlayStation 4',
		'name_group': 'PlayStation',
		'abbreviation_official': 'PS4',
		'developer': 'Sony',
		'manufacturers': [],
		'generation': None,
		'variations': [
			{
				'id': '01',
				'name': None,
				'model_no': 'CUH-1115A',
				'storage_capacity': '500GB',
				'editions': [
					{
						'name': None,
						'colors': ['white']
					}
				]
			},
			{
				'id': '02',
				'name': 'Pro',
				'model_no': 'CUH-7116B',
				'storage_capacity': '1TB',
				'editions': [
					{
						'name': None,
						'colors': ['black']
					}
				]
			},
			{
				'id': '03',
				'name': 'Slim',
				'model_no': 'CUH-7116B',
				'storage_capacity': '1TB',
				'editions': [
					{
						'name': None,
						'colors': ['black']
					}
				]
			}
		]
	}
	example_want_ps1 = {
		'id': '004',
		'type': 'console',
		'name': 'PlayStation',
		'name_group': 'PlayStation',
		'abbreviation_official': 'PS',
		'developer': 'Sony',
		'manufacturers': ['Sony'],
		'generation': 5,
		'names_other': [
			'PS1',
			'PSX'
		],
		'variations': [
			{
				'id': '01',
				'name': None,
				'model_no': 'SCPH-1001',
				'storage_capacity': None,
				'editions': [
					{
						'name': None,
						'colors': ['gray']
					}
				]
			},
			{
				'id': '02',
				'name': 'PS One',
				'model_no': 'SCPH-101',
				'storage_capacity': None,
				'editions': [
					{
						'name': None,
						'colors': ['white']
					}
				]
			}
		]
	}
	example_want2 = {
		'id': '002',
		'type': 'console',
		'name': 'Wii U',
		'name_group': 'Wii',
		'abbreviation_official': None,
		'developer': 'Nintendo',
		'manufacturers': ['Nintendo', 'Foxconn', 'Mitsumi'],
		'generation': 8,
		'names_other': [
		],
		'variations': [
			{
				'id': '01',
				'name': 'Basic',
				'model_no': 'WUP-001',
				'storage_capacity': '8GB',
				'editions': [
					{
						'name': None,
						'colors': ['white']
					}
				]
			},
			{
				'id': '02',
				'name': 'Deluxe',
				'model_no': 'WUP-101',
				'storage_capacity': '32GB',
				'editions': [
					{
						'name': None,
						'colors': ['black']
					},
					{
						'name': 'Legend of Zelda: Wind Waker Edition',
						'colors': ['black', 'gold']
					}
				]
			}
		]
	}
	example_want3 = {
		'id': '003',
		'type': 'console',
		'name': 'Wii',
		'name_group': 'Wii',
		'abbreviation_official': None,
		'developer': 'Nintendo',
		'manufacturers': ['Foxconn'],
		'generation': 7,
		'names_other': [
			'Revolution'
		],
		'variations': [
			{
				'id': '01',
				'name': None,
				'model_no': 'RVL-001',
				'storage_capacity': '512MB',
				'editions': [
					{
						'name': None,
						'colors': ['white']
					},
					{
						'name': None,
						'colors': ['black']
					},
					{
						'name': '25th Anniversary Edition',
						'colors': ['red']
					}
				]
			},
			{
				'id': '02',
				'name': 'Family Edition',
				'model_no': 'RVL-101',
				'storage_capacity': '512MB',
				'editions': [
					{
						'name': None,
						'colors': ['white']
					},
					{
						'name': None,
						'colors': ['black']
					},
					{
						'name': None,
						'colors': ['blue']
					}
				]
			},
			{
				'id': '03',
				'name': 'Mini',
				'model_no': 'RVL-201',
				'storage_capacity': None,
				'editions': [
					{
						'name': None,
						'colors': ['red', 'black']
					}
				]
			}
		]
	}
	example_wants.append(example_want_ps4)
	example_disambig.append(example_want_ps1)

	import pprint
	pp = pprint.PrettyPrinter(indent=2)
	
	result = {
		'datetime': '2019-10-16 20:08',
		'neighborhood': '(Bryant)',
		'price': 0,
		'title': 'playstation 4 pro',
		'url': 'https://seattle.craigslist.org/see/vgm/d/seattle-playstation-4-pro/6999023452.html'
	}

	pp.pprint(example_want1)
	matcher = MatchFinder(example_want_ps4, example_disambig)
	print(matcher.assess_match(result))
	# matches = [x for x in lst if fulfills_some_condition(x)]
