"""
NBA code

Project: NBA shot data visualization
Authors: Bryce Mann, Juan Carlos del Rio, Maya Calabria
Abstract: This project will pull data directly from https://stats.nba.com/ to offer
            users a interactive map to visually explore the history of shot trends by
            team, player, or conference.
"""



import pandas as pd
# import nba_data as nba
import numpy as np
import requests as r
import json


# Call data
def data_construction():
    """ Calls data from NBA as a JSON file and stores as a CSV """
    pass

def update_data():
    """ Update data CSV with only new data, ignores old data """
    pass

# Parse court SVG
def find_zones():
    """ Find the lines on SVG file and name them accordingly """
    pass

# Sorting data
def find_location():
    pass

def avg_shot():
    """ Averages data based on what category is passed
    i.e. team, specific player """
    pass

# Plotting data
def build_heat_map():
    pass

def plot_heat_map():
    """ Plots and saves file """
    pass

# UI wrapper
### pygame?
### drop down data set selection menu (year, division team, player, etc)
### time scroll

# Web app wrapper
### prepare py files
### upload to server
### scaling?


if __name__ == "__main__":
    print(shots.head())
