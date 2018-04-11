import pandas as pd
# import nba_data as nba
import numpy as np
import requests as r
import json
from nba_py.player import get_player
from nba_py import shotchart

player_id = get_player('Kevin','Durant')

kevin_durant = shotchart.ShotChart(player_id,season='2012-13')

shots = kevin_durant.shot_chart()





# # shots_url = 'https://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=33&CFPARAMS=2017-18&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID=&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID=202330&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5=&VsTeamID=.json'
# # # player_list = nba.player.commonallplayers(currentseason=0)
# headers = {
# 'User-Agent':'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
# }
# player_id = 201939
# season = '2015-16'
# season_type = 'Regular Season'
#
# # request parameters
# req_params = {
#  'AheadBehind': '',
#  'ClutchTime': '',
#  'ContextFilter': '',
#  'ContextMeasure': 'FGA',
#  'DateFrom': '',
#  'DateTo': '',
#  'EndPeriod': '',
#  'EndRange': '',
#  'GameID': '',
#  'GameSegment': '',
#  'LastNGames': 0,
#  'LeagueID': '00',
#  'Location': '',
#  'Month': 0,
#  'OpponentTeamID': 0,
#  'Outcome': '',
#  'Period': 0,
#  'PlayerID': player_id,
#  'PointDiff': '',
#  'Position': '',
#  'RangeType': '',
#  'RookieYear': '',
#  'Season': season,
#  'SeasonSegment': '',
#  'SeasonType': season_type,
#  'StartPeriod': '',
#  'StartRange': '',
#  'TeamID': 0,
#  'VsConference': '',
#  'VsDivision': ''
# }
#
# res = r.get('http://stats.nba.com/stats/shotchartdetail', params=req_params, headers=headers)
#
#
# # response.raise_for_status()
# shots = res.json()
# rows = shots['resultSets'][0]['headers']
# shots = shots['resultSets'][0]['rowSet']
# df = pd.DataFrame(shots,columns=rows)
#
#
print(shots)
