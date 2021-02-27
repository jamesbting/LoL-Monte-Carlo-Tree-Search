from math import sqrt, log
class Node:
    def __init__(self, parent = None, player = None, possible_actions = None):
        self.wins = 0
        self.visits = 0
        self.children = []
        self.player = player
        self.parent = parent
        self.possible_actions = possible_actions
    def select_child_UCB1(self):
        s = sorted(self.children, key = lambda c: c.wins / c.visits + sqrt(2*(log(self.visits))/(c.visits)))
        return s[-1]

    def select_child(self):
        s = sorted(self.children, key = lambda c: c.wins / c.visits)
        return s[-1]
    def expand (self, action, player, untried_actions):
        child = Node(parent = self, player = player)
        self.possible_actions.remove(action)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result