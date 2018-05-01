from nba_py.player import *
from nba_py import shotchart
import pandas as pd
import numpy as np
import pickle
import requests_cache
from scraping import write_to_csv

requests_cache.install_cache('demo_cache')

pid_dict = pickle.load(open('pid_dict.pickle','rb'))

for pid in pid_dict:
    shots = shotchart.ShotChart(pid,season='2017-18').shot_chart()
    if shots.empty:
        pass
    else:
        write_to_csv(shots=shots,name=pid,year='2017-18')
