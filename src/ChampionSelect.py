import json
from random import random as random
from player import player
#states should be a tuple of tuples to be hashable eg. ((1,2,3,4,5),(6,7,8,9,10))
class ChampionSelect:
    def __init__(self):
        with open('data/champions-cleaned.json', 'r') as f:
            self.validChampions = json.loads(f.read)
        f.close()
        self.selectedChampions = set()
        self.current_player = None
        self.next_player = 1 if random() > 0.5 else 0
        self.players = [redteamplayer, redteamplayer]

    def current_player(self, state):
        blue_team = state[0]
        red_team = state[1]

    def next_state(self, state, play):
        pass
    def legal_plays(self, state_history):
        pass
    def winner(self, state_history):
        pass
        