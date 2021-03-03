from filter import clean_data as filter
from monte_carlo import UCTSearch as UCT
import json
config = {
    'filter' : {
        'enabled': False,
        'desiredColumns':  [
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
            'participants.9.championId',],
        'fileName': "../../../data/post-cleaning-dataset.csv",
        'outputFileName':"data/filtered-dataset.csv"
        },
    'champions' : {
       'fileName': "data/champions-cleaned.json"
    }
}

def main():
    if(config['filter']['enabled']):
        filter(config['filter']["fileName"], config['filter']["outputFileName"],config['filter']["desiredColumns"])
    champion_pool = json.load(open('data/champions-cleaned.json','r'))
    initial_state = tuple([0] * len(champion_pool.keys()))
    UCT(initial_state, 5000)


if __name__ == '__main__':
    main()