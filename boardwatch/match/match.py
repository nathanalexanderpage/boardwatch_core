class Match():
    matches = {}

    def __init__(self, score, start, end, item, listing):
        """
        Create a new match object.
        """
        self.score = score
        self.start = start
        self.end = end
        self.item = item
        
        if Match.matches[listing.id]:
            Match.matches[listing.id].append(self)
        else:
            Match.matches[listing.id] = list(self)

    def remove_competing_matches(self):
        """
        Examine all matches to eliminate those which correspond to the same text.
        """
        pass
