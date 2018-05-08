from map_test import *
import csv
import pandas as pd
import os
import pickle
import numpy as np

def add_zone_percentages(shots,percentage_dict):
    """takes a shot dataframe and the corresponding percentage dictionary
    and adds the relevant zone percentages to the rows.
    Used in collect_player_list to build zone percentages as player data
    is collected"""

    percentage_list = []
    #loop through all of the shots
    for i in range(len(shots)):
        #store the zone for the current row
        zone_basic = shots['SHOT_ZONE_BASIC'].iloc[i]
        zone_area = shots['SHOT_ZONE_AREA'].iloc[i]
        ranges = shots['SHOT_ZONE_RANGE'].iloc[i]
        dict_key = (zone_basic,zone_area,ranges)
        #append the percentage for the row to a list
        percentage_list.append(percentage_dict[dict_key])
    #for all of the rows in the new column ZONE_PERCENTAGE, insert the
    #corresponding zone percentage
    shots.loc[:,'ZONE_PERCENTAGE'] = pd.Series(percentage_list,index=shots.index)

    return shots
