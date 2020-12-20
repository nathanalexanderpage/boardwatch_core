import os

from boardwatch_models import Listing, PlatformEdition

from .profilers import Profiler

class Matcher():
	def __init__(self):
		# positive matches
		self.match_strings = {
			'exact': [],
			'strong': [],
			'weak': [],
			'minor': []
		}

		# negative matches
		self.antimatch_strings = {
			'anywhere': [],
			'before': {
				'space_separated_yes': [],
				'space_separated_no': []
			},
			'after': {
				'space_separated_yes': [],
				'space_separated_no': []
			}
		}
	def get_antimatch_strings(self, want):
		# conditional execution based on class name
		if type(want).__name__ == 'Platform':
			self.type = 'platform'
			self.attr = 'used to determine whether or not a block of text contains mention of a given gaming platform'
			self.antimatch_strings['anywhere'].extend([
				'I will',
				'wanted:',
				'no console',
				'box only',
				'repair',
				'broken',
				'busted',
				'defective'
			])
			self.antimatch_strings['before']['space_separated_yes'].extend([
				'for',
				'for the',
				'buying',
				'your',
				'looking for',
				'looking for a',
				'no',
				'compatible with'
			])
			# self.antimatch_strings['before']['space_separated_no'].extend([])
			self.antimatch_strings['after']['space_separated_yes'].extend([
				'compatible',
				'for parts',
				'for pieces',
				'accessory',
				'accessories',
				'controller',
				'control',
				'pad'
			])
			self.antimatch_strings['after']['space_separated_no'].extend([
				'-compatible'
			])

			# FIXME: More complicated language logic TBD

			# self.seek_modifiers = {
			# 	'anywhere': [
			# 		'Limited Edition'
			# 	],
			# 	'before': {
			# 		'space_separated_yes': [
			# 			'+',
			# 			'&',
			# 			',',
			# 			';',
			# 			'.',
			# 			'!',
			# 			'and',
			# 			'plus',
			# 			'with',
			# 			'also'
			# 		],
			# 		'space_separated_no': []
			# 	},
			# 	'after': {
			# 		'space_separated_yes': [
			# 			'with',
			# 			'plus'
			# 		],
			# 		'space_separated_no': []
			# 	}
			# }

		else:
			raise Exception('Wanted item is of type ' + type(want) + ', which has not been configured for profile creation in code.')
