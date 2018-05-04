"""This script is meant to be run one time in order to store all of the data
for players who were in the NBA during the time that shot position data was
collected. For the code reviewers, we are going to verify that the loop to
create shot_data_list is storing what we want, and once that is fully verified
we will add code to store that data in files that we can access without pulling
from the internet every time and run this script overnight"""

from nba_py.player import *
from nba_py import shotchart
import pandas as pd
import numpy as np
import pickle
import requests_cache
from scraping import write_to_csv
from map_test import calc_all_zone_percentage, calc_zone_percentage
from compare_to_league_avg import add_zone_percentages

requests_cache.install_cache('demo_cache')

#only seasons where shot position data was collected
iterate_through_seasons = range(1996,2019)
seasons = []

#create list of properly formatted seasons for input into later function and
#class calls
for val in iterate_through_seasons:
    seasons.append(str(val) + '-' + str(val+1)[2:])

#ORIGINAL CODE TO STORE PLAYER LIST
# all_players = PlayerList(only_current=0)
# player_list = []
#
####storing properly formatted player names to be able to pull their player ids
# for idx in range(len(all_players.info().DISPLAY_FIRST_LAST)):
#     player_list.append(all_players.info().DISPLAY_FIRST_LAST[idx])
#
####dump these names into a file so that it doesn't have to be reloaded
# pickle.dump(player_list,open('player_list.pickle','wb'))

#load player list
player_list = pickle.load(open('player_list.pickle','rb'))

#initialize list to store dataframes from NBA.com
all_info = []

#loop through player list to format names correctly for get_player function
for i in player_list:

    #random test revealed Yao Ming's name needed to be formatted this way
    #it might apply to others but that is too much manual checking to do
    if i == 'Yao Ming':
        first = i
        last = None

    #formatting the names in the correct way to be passed to get_player
    else:
        name = i.split()
        first = name[0]
        last = None
        #some players only have a first name. This includes their last name
        #if they have it otherwise keeps only the first name
        if len(name)>1:
            last = name[1]

    #ignoring if a player isn't found; there is enough data that random
    #formatting errors can just be ignored and that player not included
    try:
        #including all info about the player
        all_info.append(get_player(first,last,just_id=False))
    except PlayerNotFoundException:
        pass

#print(str(all_info[0]["PERSON_ID"]).split()[1])
#initialize list of players we can get shot data for
shot_data_list = []
pid_dict = {}


#loop through every person's info
for idx1,i in enumerate(all_info):
    #only continue if they played at all after shot data is collected

    TO_YEAR = str(i["TO_YEAR"]).split()[1]
    FROM_YEAR = str(i["FROM_YEAR"]).split()[1]

    if int(TO_YEAR)>1996:

        #find pid and name of each player and format them how we need
        name = str(i.DISPLAY_FIRST_LAST).split()
        name = ' '.join(name[1:3])
        #need to format pid in this way to store in dictionary
        pid = str(i["PERSON_ID"]).split()[1]
        pid_dict[pid] = name

        #loop through all seasons that have data
        for idx2,j in enumerate(seasons):
            first_half = j[:4]

            #finally add shot data to list
            if int(first_half) >= int(FROM_YEAR):
                #get shot dataframe from nba.com
                shots = shotchart.ShotChart(pid,season=j).shot_chart()
                #dont do anything if dataframe is empty
                if shots.empty:
                    pass
                #calculate percentage by zone, add percentages to dataframe
                #and write to csv file
                else:
                    percentage_dict = calc_all_zone_percentage(shots=shots,season=j)
                    shots = add_zone_percentages(shots,percentage_dict)
                    write_to_csv(shots=shots,pid=pid,year=j)

#pickle player id dictionary for future use
pickle.dump(pid_dict,open('pid_dict.pickle','wb+'))
