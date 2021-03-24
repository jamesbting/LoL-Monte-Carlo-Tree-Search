from random import random as random
import numpy as np
from math import sqrt
import csv
import torch
from champion_net import ChampionNet
#50/50 chance a winner
#1 if blue team wins and 0 if red team wins
def random_winner(state, simulation_metadata):
    return 1 if random() < 0.5 else 0


#cosine similarity: search the dataset for an exact copy, and if a copy exists, return the winrate, otherwise, perform a cosine similarity to determin
#the most similar combination, and use that similairy as the probablity of blue team winning
def cosine_similarity(state, simulation_metadata):
    combinations = simulation_metadata
    max_similarity = -2
    reward = 0
    #check if state exists
    if state in combinations:
        return combinations[state]

    #no exact copy of state exists so do cosine similarity
    for combination in combinations.keys():
        if cosine(state, combination) > max_similarity:
            max_similarity = cosine(state, combination)
            reward = combinations[combination]
    return reward if random() < max_similarity else 1 - reward

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return np.dot(a, b) / (norm_a * norm_b)

def cosine_metadata(filename):
    res = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            state = convert_to_state(row)
            res[state] = int(row[len(row) - 1])
    return res

def convert_to_state(combination):
    res = [0 for i in range(154)] #154 champions
    for i in range(5):
        res[int(combination[i])] = 1
    
    for i in range(5, 10):
        res[int(combination[i])] = -1
    return tuple(res)



#majority class: always pick the team that wins the most
def majority_class(state, simulation_metadata):
    return 1 if random() < simulation_metadata else 0

def load_win_rate(win_rate_file):
    with open(win_rate_file, 'r') as f:
        content = f.readlines()
        return int(content[0]) / int(content[1])


#nn: get the neural network
def load_nn(filename):
    net_dict = torch.load(filename)
    model = ChampionNet()
    model.load_state_dict(net_dict)
    model.eval()
    return model


def forward_pass(state, simulation_metadata):
    net = simulation_metadata
    inputs = torch.Tensor(state)
    output = net(inputs)
    return torch.argmax(output, 0)