import json

from filter import clean_data as filter
from monte_carlo import UCTSearch as UCT

config = {
    'filter': {
        'enabled': False,
        'desiredColumns': [
            'teams.0.win',
            'participants.0.championId',
            'participants.1.championId',
            'participants.2.championId',
            'participants.3.championId',
            'participants.4.championId',
            'participants.5.championId',
            'participants.6.championId',
            'participants.7.championId',
            'participants.8.championId',
            'participants.9.championId', ],
        'fileName': "../../../data/post-cleaning-dataset.csv",
        'outputFileName': "data/filtered-dataset.csv"
    },
    'champions': {
        'fileName': "../data/champions-cleaned.json"
    },
    'iterations': 1000
}


def main():
    if config['filter']['enabled']:
        filter(config['filter']["fileName"], config['filter']["outputFileName"], config['filter']["desiredColumns"])
    champion_pool = json.load(open(config['champions']['fileName'], 'r'))
    initial_state = generate_initial_state(['121', '24', '18'], ['11', '26'], champion_pool)
    res = UCT(initial_state, config['iterations'])
    print('Result:', res)


def is_terminal(state):
    blueTeamSelected = 0
    redTeamSelected = 0
    for selection in state:
        if selection == 1:
            blueTeamSelected += 1
        elif selection == -1:
            redTeamSelected += 1
    return blueTeamSelected == 5 and redTeamSelected == 5


def generate_initial_state(blue_team, red_team, champion_pool):
    arr = [0] * len(champion_pool.keys())
    for blue in blue_team:
        arr[int(blue)] = 1
    for red in red_team:
        arr[int(red)] = -1
    return tuple(arr)


def is_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


if __name__ == '__main__':
    main()
