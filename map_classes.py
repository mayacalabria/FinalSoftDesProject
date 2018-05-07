import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import plotly.plotly as py
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from bokeh.models import ColorBar,LinearColorMapper, Title, HoverTool
from bokeh.models.tickers import BasicTicker
from bokeh.models.glyphs import Text
from bokeh.models.annotations import Label
from bokeh.resources import CDN
from bokeh.embed import file_html
import pickle
import os.path
import pandas as pd
import colorcet as cc
from map_test import sort_all_bins, sort_hex_bin, draw_court, sort_all_bins_freq



class Player():

    def __init__(self,name):
        """ Takes string for name with following formatting:
        'Kevin Durant', 'LeBron James', "Shaquille O'Neal"
        """
        pid_dict = pickle.load(open('pid_dict.pickle','rb'))
        new_dict = {v: k for k, v in pid_dict.items()}
        if name in new_dict:
            self.name = name
            self.id = new_dict[name]
            self.percent_low = -10
            self.percent_hi = 10
            self.error_flag = 0
        else:
            self.error_flag = 1

    def final_season(self):
        """ Returns the last season that a player played in. """
        if self.error_flag == 1:
            return '2017-18'
        else:
            player_dir = os.listdir(os.path.join(os.getcwd(),'../PlayerData2/'+self.id))
            years = []
            for i in range(len(player_dir)):
                year = player_dir[i]
                years.append(year)
            final_season = max(years)
            return final_season[0:-4] # last season, removes '.csv'

    def rookie_season(self):
        """ Returns first season of player's career. """
        if self.error_flag == 1:
            return '2016-17'
        else:
            player_dir = os.listdir(os.path.join(os.getcwd(),'../PlayerData2/'+self.id))
            years = []
            for i in range(len(player_dir)):
                year = player_dir[i]
                years.append(year)
            final_season = min(years)
            return final_season[0:-4] # first season, removes '.csv'

    def generate_shots(self,season=None):
        """ Takes season, and returns all player shot data for that season as a pandas frame. """
        if season == None:  # defaults to the most recent season played, if no season passed
            season = self.final_season()
        shots_dir = os.path.abspath(os.path.join(os.getcwd(),'../PlayerData2/'+self.id+'/'+season+'.csv'))
        if os.path.exists(shots_dir):
            return pd.DataFrame.from_csv(shots_dir)
        else:
            return pd.DataFrame()

    def scatter(self,season=None):
        """ Generates a scatter plot of made and missed shots over the course of a season. """
        shots = self.generate_shots(season)

        for i in range(len(shots)):
            x = shots["LOC_X"].iloc[i]
            y = shots["LOC_Y"].iloc[i]

            #plot made shots as green and missed shots as red
            if shots["SHOT_MADE_FLAG"].iloc[i] == 1:
                plt.plot(x,y,'go')
            else:
                plt.plot(x,y,'ro')
        plt.axis('equal')
        plt.ylim(-100,400)
        plt.title(self.name+' shot locations')
        plt.show()

    def hex_accuracy(self,season=None):
        """ Generates a hex bin plot that compares a player's shooting percentages to the
        leagues by zone. Shows accuracy compared to league.
        Takes season as a string, defaults to last played season"""
        if self.error_flag == 1:
            error = Error()
            return error.error_graph()
        else:
            shots = self.generate_shots(season)
            if shots.empty:
                p = figure(title='No Data for the Selected Season',
                    tools="wheel_zoom,reset", match_aspect=True,
                    background_fill_color='#BB7E3B',name='plot')
                p.grid.visible = False
                p.axis.visible = False
                draw_court(p)
            else:
                all_bins = sort_all_bins(shots)
                p = figure(title=self.name+' Heatmap: accuracy compared to league',
                    tools="wheel_zoom,reset", match_aspect=True,
                    background_fill_color='#BB7E3B',name='plot')
                p.grid.visible = False
                p.axis.visible = False
                p.hex_tile(q="q", r="r", size=0.1, line_color='black', source=all_bins,
                    fill_color=linear_cmap('counts', cc.coolwarm, self.percent_low, self.percent_hi))
                draw_court(p)
                color_mapper = LinearColorMapper(palette=cc.coolwarm,low=self.percent_low,high=self.percent_hi)
                color_bar = ColorBar(color_mapper=color_mapper, location=(0,0))
                p.add_layout(color_bar, 'right')
                p.add_layout(Title(text="Shooting percentage difference from league",align = 'center'),'right')

                hover = HoverTool(tooltips=[("%" + "difference", "@counts"+"%")],
                          mode="mouse", point_policy="follow_mouse")

                p.add_tools(hover)

        return p

    def hex_freq(self,season=None):
        """ Generates a hex bin plot that compares a player's shooting percentages to the
        leagues by zone. Shows accuracy compared to league.
        Takes season as a string, defaults to last played season"""
        if self.error_flag == 1:
            error = Error()
            return error.error_graph()
        else:
            shots = self.generate_shots(season)
            if shots.empty:
                p = figure(title='No Data for the Selected Season',
                    tools="wheel_zoom,reset", match_aspect=True,
                    background_fill_color='#BB7E3B',name='plot')
                p.grid.visible = False
                p.axis.visible = False
                draw_court(p)
            else:
                all_bins = sort_all_bins_freq(shots)
                p = figure(title=self.name+' Heatmap: frequency compared to league',tools="wheel_zoom,reset", match_aspect=True,
                    background_fill_color='#BB7E3B', name='plot')
                p.grid.visible = False
                p.axis.visible= False
                p.hex_tile(q="q", r="r", size=0.1, line_color='black', source=all_bins,
                    fill_color=linear_cmap('counts', cc.coolwarm, self.percent_low/2, self.percent_hi/2))
                draw_court(p)
                color_mapper = LinearColorMapper(palette=cc.coolwarm,low=self.percent_low/2,high=self.percent_hi/2)
                color_bar = ColorBar(color_mapper=color_mapper, location=(0,0))
                p.add_layout(color_bar, 'right')
                p.add_layout(Title(text="Percentage of shots taken in zone compared to league",align = 'center'),'right')

                hover = HoverTool(tooltips=[("%" + "difference", "@counts"+"%")],
                          mode="mouse", point_policy="follow_mouse")

                p.add_tools(hover)

        return p

class Team(Player):

    def __init__(self,abrv):
        """ Takes abrv as a string that has to be all caps, three letters like
        "GSW", "BOS", etc.

         """
        teamid_dict = pickle.load(open('teamid_dict.pickle','rb'))
        new_dict = {v: k for k, v in teamid_dict.items()}
        if abrv in new_dict:
            self.name = abrv
            self.id = str(new_dict[self.name])
            self.percent_low = -5
            self.percent_hi = 5
            self.error_flag = 0
        else:
            self.error_flag = 1

    def generate_shots(self,season=None):
        """ Takes season, and returns all team shot data for that season as a pandas frame.
        Takes season as a string, defaults to '2017-18' """
        if season == None:
            season = '2017-18'
        shots_dir = os.path.abspath(os.path.join(os.getcwd(),'../TeamData2/'+self.id+'/'+season+'.csv'))
        if os.path.exists(shots_dir):
            shots = pd.DataFrame.from_csv(shots_dir)
        else:
            shots = pd.DataFrame()
        return shots

class Error():
    """ An class used by player or team classes when the name/team entered is not found in database. """
    def __init__(self):
        pass

    def error_graph(self):
        p = figure(title='Uh oh!', x_range=(0,1), y_range=(0,2),
            tools="wheel_zoom,reset", match_aspect=True, name='plot')

        text1 ='Uh oh! It looks like you misspelled a word. If you are searching for'
        text2 ='a player make sure that their full name is spelled correctly. If you'
        text3 ='are looking for a team make sure that their 3 letter, NBA specific'
        text4 ='abbreviation is correct.'

        mytext1 = Label(x=0.1,y=1.4,text=text1)
        mytext2 = Label(x=0.1,y=1.2,text=text2)
        mytext3 = Label(x=0.1,y=1,text=text3)
        mytext4 = Label(x=0.35,y=.8,text=text4)

        p.add_layout(mytext1)
        p.add_layout(mytext2)
        p.add_layout(mytext3)
        p.add_layout(mytext4)

        p.grid.visible = False
        p.axis.visible = False
        p.toolbar.logo = None
        p.toolbar_location = None
        return p




if __name__ == "__main__":
    durant = Player('Steen Curry')
    show(durant.hex_freq())
