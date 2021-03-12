from math import pow, sqrt, log
from random import random as random


# states will be a N-dimensional vector, where N is the number champions, and the following values:
# 1: Champion selected by blue team
# -1: Champion selected by red team
# 0: unselected
class Node(object):
    players = {"blue": 0, "red": 1}

    def __init__(self, parent=None, state=None, player=players["blue"]):
        self.q = 0
        self.n = 0
        self.children = []
        self.parent = parent
        self.state = state
        self.expanded = False
        self.player = 1 - self.parent.player if parent is not None else player
        self.possible_actions = self.generate_possible_actions()

    def expand(self):
        self.expanded = True
        if len(self.possible_actions) == 0:
            return self.best_child()
        action = self.possible_actions[int(random() * len(self.possible_actions))]
        self.possible_actions.remove(action)
        new_child = Node(parent=self, state=action, player=(1 - self.player))
        self.children.append(new_child)
        return new_child

    def best_child(self, exploration_term=pow(2, -0.5)):
        s = sorted(self.children, key=lambda c: c.q / c.n + (exploration_term * sqrt(2 * log(self.n) / c.n)))
        return s[len(s) - 1]

    def is_terminal(self):
        blueTeamSelected = 0
        redTeamSelected = 0
        for selection in self.state:
            if selection == 1:
                blueTeamSelected += 1
            elif selection == -1:
                redTeamSelected += 1
        return blueTeamSelected == 5 and redTeamSelected == 5

    def is_expandable(self):
        # if nonterminal_state and unexpanded_children then true
        for child in self.children:
            if not child.expanded:
                return not self.is_terminal()

        return not self.is_terminal() and len(self.possible_actions) != 0

    def generate_possible_actions(self):
        res = []
        selection = 1 if self.player == Node.players["blue"] else -1

        for i in range(len(self.state)):
            if self.state[i] == 0:
                action = list(self.state)[:]
                action[i] = selection
                res.append(tuple(action))
        return res

    def __str__(self):
        return f'Node:\n q:{self.q};\n n:{self.n};\n state:{self.state}'
