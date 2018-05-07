"""Script to write location frequency data to existing team csvs"""

import pandas as pd
import os
import csv
import pickle
import numpy as np

#dictionary where each key is a season, and each value is a list of the league
#average zone frequencies, corresponding to the zone lists in
#calc_all_zone_frequency
avg_zone_frequency = pickle.load(open('avg_zone_frequency.pickle','rb'))

def calc_zone_frequency(shots,basic_zone,zone_area,zone_range):
    """takes a dataframe of shot data and returns a dictionary with each
    zones relative frequency"""

    basic = shots[(shots.SHOT_ZONE_BASIC==basic_zone)]#filters for basic zone
    zone = basic[(basic.SHOT_ZONE_AREA==zone_area)]#filters for only the area
    fin_range = zone[(zone.SHOT_ZONE_RANGE==zone_range)]#gets all from a specific range in that area

    zone_percentage = 100 * (len(fin_range.index)/len(shots.index))

    return zone_percentage

def calc_all_zone_frequency(shots,season,league_average):
    """takes a dataframe from a specific season and calculates
    the zone frequency of the dataframe to the league average
    from those zones"""

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

    season_avgs = league_average[season]
    all_frequencies = {}

    for i in range(len(basic_zones)):

        league_zone_frequency = season_avgs[i]
        df_frequency = calc_zone_frequency(shots,basic_zones[i],zone_areas[i],
            ranges[i])
        relative_frequency = df_frequency - league_zone_frequency

        dict_key = (str(basic_zones[i]),str(zone_areas[i]),str(ranges[i]))
        all_frequencies[dict_key] = relative_frequency

    return all_frequencies

teamid_dict = pickle.load(open('teamid_dict.pickle','rb'))
team_directory = os.path.abspath(os.path.join(os.getcwd(),'../../TeamData2'))

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
    new_team_path = os.path.abspath(os.path.join(os.getcwd(),'../../TeamData3/'+team))
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
        all_frequencies = calc_all_zone_frequency(df,year_file[:7],avg_zone_frequency)
        #open the old file for reading, and create the new one to write to
        csv_r = csv.reader(open(year_filepath,'r'))
        csv_w = csv.writer(open(new_file,'w'))
        #loop through rows of old csv
        for idx,row in enumerate(csv_r):
            #write the headers without modification on the first iteration
            if idx == 0:
                row.append('ZONE FREQUENCY')
                csv_w.writerow(row)
            #after the first iteration use the percentages dictionary and
            #the current shots zone to replace the ZONE PERCENTAGE column with
            #the correct one
            else:
                dict_key = (row[4],row[5],row[6])
                row.append(all_frequencies[dict_key])
                csv_w.writerow(row)
