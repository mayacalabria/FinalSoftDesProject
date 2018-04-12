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

    with open('shot_database.csv', 'w', newline='') as database:
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        i = 0
        for row in to_write:
            writer.writerow({'LOC_X': to_write.LOC_X[250],'LOC_Y': to_write.LOC_Y[250]})
            i = i+1

write_to_csv()
