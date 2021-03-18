import json
import time
import psutil
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
        'fileName': "data/champions-cleaned.json"
    },
    'iterations': 1000
}


def main():
    if config['filter']['enabled']:
        filter(config['filter']["fileName"], config['filter']["outputFileName"], config['filter']["desiredColumns"])
    champion_pool = json.load(open(config['champions']['fileName'], 'r'))
    initial_state = generate_initial_state(['121', '24', '18'], ['11', '26'], champion_pool)
    start_time = time.time()
    res = UCT(initial_state, config['iterations'])
    finish_time = time.time()
    show_results(res, finish_time - start_time, psutil.Process().memory_info().peak_wset)

def show_results(result, time, memory_usage):
    print('Result:', result)
    print('Took ',time , ' seconds to run')
    print('Peak memory usage was: ', memory_usage/1000000, 'megabytes')


def generate_initial_state(blue_team, red_team, champion_pool):
    arr = [0] * len(champion_pool.keys())
    for blue in blue_team:
        arr[int(blue)] = 1
    for red in red_team:
        arr[int(red)] = -1
    return tuple(arr)

if __name__ == '__main__':
    main()
