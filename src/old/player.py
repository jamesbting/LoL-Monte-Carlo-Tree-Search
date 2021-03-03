import json

class Player (object):
    def __init__(self):
        self.champion_pool = json.load(open('data/champions-cleaned.json','r'))


class RandomPlayer(Player):
    def __init__(self):
        super().__init__()