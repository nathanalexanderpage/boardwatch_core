class MatchFinder():
    def __init__(self):
        self.type = 'all-purpose'

    def assess_match(self, result):
        match_score = 0.9
        for match_keyword_strong in result['match_strong']:
            if match_keyword_strong in result['title']:
                match_score *= 1.5
        for match_keyword_weak in result['match_weak']:
            if match_keyword_weak in result['title']:
                match_score *= 1.2
        return match_score

if __name__ == '__main__':
    print('running ' + __file__)

    example_wants = []
    example_want1 = {
        'item': 'PlayStation 4',
        'type': 'console',
        'company': 'Sony',
        'match_strong': [
            'PS4',
            'PlayStation 4',
            'PlayStation4',
            'Play Station 4',
            'PS 4'
        ],
        'match_weak': [
            'PlayStation',
            'Play Station',
            'PS'
        ]
    }
    example_wants.append(example_want1)

    print(example_want['item'])
    # matches = [x for x in lst if fulfills_some_condition(x)]