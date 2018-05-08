"""script to take the league avg zone shooting percentages and subtract it from
a teams zone percentage, in order to build a team heat map.
To do this the current team files are read, and then new files are created
in a different folder that has the correct team zone percentages"""

import os
import sys
import csv
import pickle
import numpy as np
import pandas as pd
from map_test import calc_all_zone_percentage


teamid_dict = pickle.load(open('teamid_dict.pickle','rb'))

team_directory = os.path.abspath(os.path.join(os.getcwd(),'../TeamData'))

#lists of corresponding zone elements
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

#loop through team files
for team in os.listdir(team_directory):
    #specify current and new team file paths
    team_path = os.path.abspath(os.path.join(team_directory,team))
    new_team_path = os.path.abspath(os.path.join(os.getcwd(),'../TeamData2/'+team))
    #if the new team folder doesn't exist, create it
    if not os.path.exists(new_team_path):
        os.makedirs(new_team_path)
    #loop through year files in current team folder
    for year_file in os.listdir(team_path):
        #specify old team filepath
        year_filepath = os.path.join(team_path,year_file)
        #specify new team filepath
        new_file = os.path.join(new_team_path,year_file)
        #convert current year file to dataframe to pass to zone calculate function
        df = pd.read_csv(year_filepath)
        all_percentages = calc_all_zone_percentage(df,year_file[:7])
        #open the old file for reading, and create the new one to write to
        csv_r = csv.reader(open(year_filepath,'r'))
        csv_w = csv.writer(open(new_file,'w'))
        #loop through rows of old csv
        for idx,row in enumerate(csv_r):
            #write the headers without modification on the first iteration
            if idx == 0:
                csv_w.writerow(row)
            #after the first iteration use the percentages dictionary and
            #the current shots zone to replace the ZONE PERCENTAGE column with
            #the correct one
            else:
                dict_key = (row[4],row[5],row[6])
                row[-1] = all_percentages[dict_key]
                csv_w.writerow(row)
