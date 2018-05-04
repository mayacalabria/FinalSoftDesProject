"""script to calculate the league average percentage of shots taken from
certain zones by year
FILE PATHS NEED TO BE MODIFIED TO WORK ON COMPUTERS NOT OWNED BY BRYCE MANN
"""
import os
import sys
import csv
import pickle
import numpy as np
import pandas as pd
from operator import add

teamid_dict = pickle.load(open('teamid_dict.pickle','rb'))

team_directory = os.path.abspath(os.path.join(os.getcwd(),'../TeamData'))

basic_zones = ['Above the Break 3', 'Above the Break 3',
    'Above the Break 3', 'Above the Break 3', 'Backcourt',
    'In The Paint (Non-RA)', 'In The Paint (Non-RA)',
    'In The Paint (Non-RA)', 'In The Paint (Non-RA)', 'Left Corner 3',
    'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range',
    'Mid-Range', 'Mid-Range', 'Mid-Range', 'Restricted Area',
    'Right Corner 3']
zone_areas = ['Back Court(BC)', 'Center(C)', 'Left Side Center(LC)',
    'Right Side Center(RC)', 'Back Court(BC)', 'Center(C)', 'Center(C)',
    'Left Side(L)', 'Right Side(R)', 'Left Side(L)', 'Center(C)',
    'Center(C)', 'Left Side Center(LC)', 'Left Side(L)', 'Left Side(L)',
    'Right Side Center(RC)', 'Right Side(R)', 'Right Side(R)', 'Center(C)',
    'Right Side(R)']
ranges = ['Back Court Shot', '24+ ft.', '24+ ft.', '24+ ft.',
    'Back Court Shot', '8-16 ft.', 'Less Than 8 ft.', '8-16 ft.',
    '8-16 ft.', '24+ ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.',
    '16-24 ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.', '8-16 ft.',
    'Less Than 8 ft.', '24+ ft.']

seasons_to_calc = range(1996,2019)
seasons = []
#build list of seasons to loop through
for i in range(len(seasons_to_calc)-1):
    season = str(seasons_to_calc[i]) + '-' + str(seasons_to_calc[i+1])[2:]
    seasons.append(season)

avg_zone_frequency = {}

#loop through all seasons
for i in seasons:
    filename = i + '.csv'
    #initialize the count of total shots and total shots per zone for each season
    total_shots = 0
    season_zone_totals = [0]*len(basic_zones)
    #loop through each team folder
    for folder in os.listdir(team_directory):
        #get the file for the current season and team
        file = os.path.abspath(os.path.join(team_directory+'/'+folder,filename))
        #only do something if the file exists
        #necessary because of the one expansion team
        if os.path.exists(file):
            #turn the file into a dataframe
            df = pd.read_csv(file)
            #shots per team for the season added to total shots
            total_shots += len(df.index)
            #initialize list for team zone shots
            team_zone_shots = [0]*len(basic_zones)
            #loop through the zone lists above
            for j in range(len(basic_zones)):

                #isolate shots taken from each zone
                basic = df[(df.SHOT_ZONE_BASIC==basic_zones[j])]
                zone = basic[(basic.SHOT_ZONE_AREA==zone_areas[j])]
                final_zone = zone[(zone.SHOT_ZONE_RANGE==ranges[j])]
                #store total shots from each zone at corresponding index
                team_zone_shots[j] = len(final_zone.index)

            #elementwise addition of shots per zone by team to the total shots
            #per zone that is initialized at the beginning of each season loop
            season_zone_totals = list(map(add,team_zone_shots,season_zone_totals))

    #key of this dictionary is the current season
    #value is a list with corresponding zones, where each element is divided
    #by the total shots
    avg_zone_frequency[i] = [100*(x / total_shots) for x in season_zone_totals]

#store avg_zone_frequency for later use
pickle.dump(avg_zone_frequency,open('avg_zone_frequency.pickle','wb+'))
"""NEXT STEPS:
WRITE A FUNCTION TO TAKE A DATAFRAME OF SHOTS, COMPUTE THAT DATAFRAME'S ZONE
FREQUENCIES, SUBTRACT THE CORRESPONDING LEAGE AVG FROM THOSE, AND RETURN A
DATAFRAME THAT CAN BE ADDED TO THE CSVS WHEN THE DATA IS REBUILT
"""
