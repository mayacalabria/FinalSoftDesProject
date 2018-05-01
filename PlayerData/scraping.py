"""
Development environment for scraping shot data from nba.com and storing it to a local csv
by JC del Rio
Uses nba_py to insterface with nba.com JSON data files
TO INSTALL:
pip nba_py
"""
import pandas as pd
import numpy as np
import requests as r
import json
from nba_py.player import get_player
from nba_py import shotchart
import csv
import os

# Uses integrated classes from nba.py to pull shot data for a given player and year
def get_data():
    #Lebron is a place holder, first, last and year will be inputs int the future
    first = 'Lebron'
    last = 'James'
    year = '2012-13'
    player_id = get_player(first, last)
    #ShotChart creates a readable dictionary of all the data
    Lebron_James = shotchart.ShotChart(player_id,season = year)
    shots = Lebron_James.shot_chart()
    return shots

# Takes the data obtained by get_data and creates a csv with the stored data
#will take desired csv name as an input in the future
def write_to_csv(shots, year, pid):
    #creates temporary structure form the data from get_data
    #to_write = get_data()
    to_write = shots
    fieldnames = []
    #looks at to_write and obtains the headers for each column
    for row in to_write:
        fieldnames = fieldnames +[row]

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r''+str(pid))

    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    filename = os.path.join(final_directory, year+'.csv')
    #creates csv file, the  name will be pulled in as an input
    #with open('Lebron_James_2012_2013.csv', 'w+', newline='') as database:
    with open(filename, 'w+', newline='') as database:
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(to_write)):
            writer.writerow({'GRID_TYPE': to_write.GRID_TYPE[i],
            'GAME_ID':to_write.GAME_ID[i],'GAME_EVENT_ID':to_write.GAME_EVENT_ID[i],
            'PLAYER_ID':to_write.PLAYER_ID[i],'PLAYER_NAME':to_write.PLAYER_NAME[i],
            'TEAM_ID':to_write.TEAM_ID[i],'TEAM_NAME':to_write.TEAM_NAME[i],
            'PERIOD':to_write.PERIOD[i],'MINUTES_REMAINING':to_write.MINUTES_REMAINING[i]
            ,'SECONDS_REMAINING':to_write.SECONDS_REMAINING[i],
            'EVENT_TYPE':to_write.EVENT_TYPE[i],'ACTION_TYPE':to_write.ACTION_TYPE[i],
            'SHOT_TYPE':to_write.SHOT_TYPE[i],'SHOT_ZONE_BASIC':to_write.SHOT_ZONE_BASIC[i],
            'SHOT_ZONE_AREA':to_write.SHOT_ZONE_AREA[i],'SHOT_ZONE_RANGE':to_write.SHOT_ZONE_RANGE[i],
            'SHOT_DISTANCE':to_write.SHOT_DISTANCE[i],'LOC_X': to_write.LOC_X[i],
            'LOC_Y': to_write.LOC_Y[i],'SHOT_ATTEMPTED_FLAG': to_write.SHOT_ATTEMPTED_FLAG[i],
            'SHOT_MADE_FLAG': to_write.SHOT_MADE_FLAG[i],'GAME_DATE': to_write.GAME_DATE[i],
            'HTM': to_write.HTM[i],'VTM': to_write.VTM[i]})

#write_to_csv('LebronJames','2012-13')
