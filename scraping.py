"""
TO INSTALL:
pip nba_py
"""
import pandas as pd
# import nba_data as nba
import numpy as np
import requests as r
import json
from nba_py.player import get_player
from nba_py import shotchart
import csv

def get_data():
    first = 'Lebron'
    last = 'James'
    year = '2012-13'
    player_id = get_player(first, last)
    Lebron_James = shotchart.ShotChart(player_id,season = year)
    shots = Lebron_James.shot_chart()
    return shots

def write_to_csv():
    to_write = get_data()
    fieldnames = []
    for row in to_write:
        fieldnames = fieldnames +[row]

    with open('shot_database_plus.csv', 'w+', newline='') as database:
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

write_to_csv()
