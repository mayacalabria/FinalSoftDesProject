import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import display

shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPAR;'\
                'AMS=2014-15&ContextFilter;=&ContextMeasure;=FGA&DateFrom;=&D;'\
                'ateTo=&GameID;=&GameSegment;=&LastNGames;=0&LeagueID;=00&Loca;'\
                'tion=&MeasureType;=Base&Month;=0&OpponentTeamID;=0&Outcome;=&'\
                'PaceAdjust=N&PerMode;=PerGame&Period;=0&PlayerID;=201935&Plu;'\
                'sMinus=N&Position;=&Rank;=N&RookieYear;=&Season;=2014-15&Seas;'\
                'onSegment=&SeasonType;=Regular+Season&TeamID;=0&VsConferenc;'\
                'e=&VsDivision;=&mode;=Advanced&showDetails;=0&showShots;=1&sh;'\
                'owZones=0'

# Get the webpage containing the data
response = requests.get(shot_chart_url)
# Grab the headers to be used as column headers for our DataFrame
headers = response.json()['resultSets'][0]['headers']
# Grab the shot chart data
right = shot_df[shot_df.SHOT_ZONE_AREA == "Right Side(R)"]
plt.figure(figsize=(12,11))
plt.scatter(right.LOC_X, right.LOC_Y)
plt.xlim(-300,300)
plt.ylim(-100,500)
plt.show()
