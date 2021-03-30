from math import pow, sqrt, log
from random import random as random


class Node(object):
    players = {"blue": 0, "red": 1}

    def __init__(self, parent=None, state=None, player=players["blue"], depth=0):
        self.q = 0
        self.n = 0
        self.children = []
        self.parent = parent
        self.state = state
        self.player = 1 - self.parent.player if parent is not None else player
        self.possible_actions = self.generate_possible_actions()
        self.depth = depth

    def expand(self):
        action = self.possible_actions[int(random() * (len(self.possible_actions) - 1))]
        self.possible_actions.remove(action)
        new_child = Node(parent=self, state=action, player=(1 - self.player), depth=self.depth + 1)
        self.children.append(new_child)
        return new_child

    def best_child(self, exploration_term=pow(2, -0.5)):
        confidence_bounds = [c.q / c.n + (exploration_term * sqrt(2 * log(self.n) / c.n)) for c in self.children]
        max_index = 0
        for i in range(len(confidence_bounds)):
            if confidence_bounds[i] > confidence_bounds[max_index]:
                max_index = i
        return self.children[max_index]

    def is_terminal(self):
        blueTeamSelected = 0
        redTeamSelected = 0
        for selection in self.state:
            if selection == 1:
                blueTeamSelected += 1
            elif selection == -1:
                redTeamSelected += 1
        return blueTeamSelected == 5 and redTeamSelected == 5

    def generate_possible_actions(self):
        res = []
        #check for which champions have been selected already
        selected = set()
        for champ in self.state:
            selected.add(champ)
        start = 0 if self.player == Node.players["blue"] else 5
        offset = 0
        while(self.state[start + offset] != 0 and offset < 5):
            offset += 1
        if offset >= 5:
            return res
        #154 champions
        for i in range(154):
            if i not in selected:
                next_action = list(self.state)
                next_action[start + offset] = i
                res.append(tuple(next_action))
        return res

    def __str__(self):
        return f"Node:\n q:{self.q};\n n:{self.n};\n state:{self.state};\n depth:{self.depth}"

    @staticmethod
    def determine_next_pick(state):
        blue = 0
        red = 0

        for i in range(5):
            if state[i] != 0:
                blue += 1
            if state[i+5] != 0:
                red += 1

        if blue == 0 and red == 0:
            return "blue"
        if blue == 5 and red == 5:
            raise ValueError
        if blue == 5 and red < 5:
            return "blue"
        if  blue < 5 and red == 5:
            return "red"

        return "blue" if blue < red else "red"
