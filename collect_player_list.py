from nba_py.player import *
from nba_py import shotchart
import requests
import json
import numpy as np
import pickle

iterate_through_seasons = range(1996,2018)
seasons = []

for idx,val in enumerate(iterate_through_seasons):
    seasons.append(str(val) + '-' + str(val+1)[2:])
#
# test = PlayerList(only_current=0)
# player_list = []
#
# for idx in range(len(test.info().DISPLAY_FIRST_LAST)):
#     player_list.append(test.info().DISPLAY_FIRST_LAST[idx])
#
# pickle.dump(player_list,open('player_list.pickle','wb'))

player_list = pickle.load(open('player_list.pickle','rb'))

usable_pids = []
all_info = []

for i in player_list[:6]:
    if i == 'Yao Ming':
        first = i
        last = None
    else:
        name = i.split()
        first = name[0]
        last = None
        if len(name)>1:
            last = name[1]

    try:
        usable_pids.append(get_player(first,last))
        all_info.append(get_player(first,last,just_id=False))
    except PlayerNotFoundException:
        pass

shot_data_list = []
#test = shotchart.ShotChart(usable_pids[4],season=seasons[0])

for idx1,i in enumerate(all_info):
    if int(i.TO_YEAR)>1996:
        for idx2,j in enumerate(seasons):
            if idx2==3:
                second_half = '2000'
            else:
                second_half = j[:2]+j[5:]
            if int(second_half) <= int(i.TO_YEAR):
                #print(usable_pids[idx1])
                shot_data_list.append(shotchart.ShotChart(usable_pids[idx1],season=j))


#print(get_player('Kevin','Durant',just_id=False).TO_YEAR)
for i in shot_data_list:
    print(i.json['parameters']['Season'])
