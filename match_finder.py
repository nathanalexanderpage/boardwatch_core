class MatchFinder():
    def __init__(self):
        self

if __name__ == '__main__':
    print('running ' + __file__)

    example_wants = []
    example_want1 = {
        'item': 'PlayStation 4',
        'type': 'console',
        'company': 'Sony',
        'match_strong': [
            'PS4',
            'PlayStation4',
            'PlayStation 4',
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