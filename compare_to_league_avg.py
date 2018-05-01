from map_test import *
import csv
import pandas as pd
import os
import pickle
import numpy as np

def add_zone_percentages(shots,percentage_dict):

    percentage_list = []

    for i in range(len(shots)):
        zone_basic = shots['SHOT_ZONE_BASIC'].iloc[i]
        zone_area = shots['SHOT_ZONE_AREA'].iloc[i]
        ranges = shots['SHOT_ZONE_RANGE'].iloc[i]

        dict_key = (zone_basic,zone_area,ranges)

        percentage_list.append(percentage_dict[dict_key])
        #shots['ZONE_PERCENTAGE'].iloc[i] = percentage_dict[dict_key]

    #df_dict = {'ZONE_PERCENTAGE': percentage_list}
    shots.loc[:,'ZONE_PERCENTAGE'] = pd.Series(percentage_list,index=shots.index)
    #new_df = pd.DataFrame(data=df_dict)

    #shots['ZONE_PERCENTAGE'] = new_df

    return shots

shots = generate_shots('Kevin','Durant','2016-17')
percentage_dict = calc_all_zone_percentage(shots,'2016-17')

print(add_zone_percentages(shots,percentage_dict))
