"""This script is meant to be run one time in order to store all of the data
for players who were in the NBA during the time that shot position data was
collected. For the code reviewers, we are going to verify that the loop to
create shot_data_list is storing what we want, and once that is fully verified
we will add code to store that data in files that we can access without pulling
from the internet every time and run this script overnight"""

from nba_py.player import *
from nba_py import shotchart
import numpy as np
import pickle

#only seasons where shot position data was collected
iterate_through_seasons = range(1996,2018)
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
for i in player_list[:4]:

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

#initialize list of players we can get shot data for
shot_data_list = []

#loop through every person's info
for idx1,i in enumerate(all_info):
    #only continue if they played at all after shot data is collected
    if int(i.TO_YEAR)>1996:
        #loop through all seasons that have data
        for idx2,j in enumerate(seasons):
            #take care of issue where year is 1999-00
            if idx2==3:
                second_half = '2000'
            #formatting year correctly for integer comparison
            else:
                second_half = j[:2]+j[5:]
            #check if the second half of the current year is still during career
            #of player
            if int(second_half) <= int(i.TO_YEAR):
                #finally add shot data to list
                shot_data_list.append(shotchart.ShotChart(i.PERSON_ID[idx1],season=j))


#quick verification that only data from the correct years are being stored
for i in shot_data_list:
    print(i.json['parameters']['Season'])
