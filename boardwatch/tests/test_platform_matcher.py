from console_data_resource import *
from match_finder import *
from trial_result_generator import *

title_tests = {
	'PlayStation 4': {
		'passes': [
			'PlayStation 4 Pro and PlayStation VR Bundle',
			'Ps4 500gb',
			'God of War PS4 Pro with Extra Controller',
			'Playstation 4 (PS4) Original Edition 500GB Black Console',
			'Sony PlayStation 4 - 500 GB Slim - Glacier White + Accessories',
			'Sony PlayStation 4 Ps4 Slim 1Tb Console Cuh-2215B Jet Black',
			'Sony Dualshock Wireless Controller for PlayStation 4 Black CUH-ZCT2U',
			'Playstation 4 PS4 500gb'
		],
		'fails': [
			'Defective PS4, xbox one and nintendo switch for sale',
			'Battlefield Hardline for PS4',
			'Rage 2 (PS4)',
			'Tomb Raider (PS4)',
			'Horizon zero dawn (PS4)',
			'Days Gone (PS4)',
			'Metro Exodus (PS4)'
		]
	}
}

def match_pos_neg(console_names):
	test_consoles = list(filter(lambda console: console['name'] == console_names, consoles))
	for console in test_consoles:
		matcher = PlatformMatchFinder(console, {})
		for title in title_tests[console['name']]['passes']:
			result = FakeResult(title)
			print(title)
			assert matcher.assess_match(result.data) == True, 'Should be match-positive'
		for title in title_tests[console['name']]['fails']:
			result = FakeResult(title)
			print(title)
			assert matcher.assess_match(result.data) == False, 'Should be match-negative'

if __name__ == '__main__':
	consoles_to_test = [
		'PlayStation 4'
	]
	for console in consoles_to_test:
		match_pos_neg(console)
	print('All tests passed.')