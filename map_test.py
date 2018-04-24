import numpy as np
from nba_py.player import get_player
from nba_py import shotchart
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import plotly.plotly as py
from scipy.stats import kendalltau
import seaborn as sns
from PIL import Image
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
import pickle
import os.path
import pandas as pd

def generate_shots_fromNBA(first,last,season):
    """ Takes first, last, and season as string,
    returns pandas structure of all shots
    """
    player_id = get_player(first,last)
    player = shotchart.ShotChart(player_id,season=season)
    shots = player.shot_chart()
    return shots
    ### rewrite to pull the correct csv


def generate_shots(first,last,season):

    pid_dict = pickle.load(open('pid_dict.pickle','rb'))
    new_dict = {v: k for k, v in pid_dict.items()}
    player_id = new_dict[first.title()+' '+last.title()]
    # playerData = '/home/maya/miniprojects/PlayerData'
    shots_dir = os.path.abspath(os.path.join(os.getcwd(),'../PlayerData/'+player_id+'/'+season+'.csv'))
    # shots = open(shots_dir,'r')
    shots = pd.DataFrame.from_csv(shots_dir)
    return shots

def generate_scatter(shots):
    """ Creates scatter plot of all shots taken by player over season """
    #evaluate each shot individually
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
    plt.show()

def hist_heat(shots, bin_size = 60):
    """ Uses matplotlib to generate a 2D histogram and display heat map """
    xs = []
    ys = []
    for i in range(len(shots)):
        x = shots["LOC_X"].iloc[i]
        y = shots["LOC_Y"].iloc[i]
        xs.append(x)
        ys.append(y)
    heatmap, xedges, yedges = np.histogram2d(ys,xs, bins=(bin_size,bin_size))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    title = '{} {}'.format(shots["PLAYER_NAME"].iloc[0], 'attempted shots')
    plt.imshow(heatmap,extent=extent)
    plt.title(title)
    plt.axis('off')
    plt.show()

def hex_plot(shots):
    xs = []
    ys = []
    for i in range(len(shots)):
        x = shots["LOC_X"].iloc[i]
        y = shots["LOC_Y"].iloc[i]
        xs.append(x)
        ys.append(y)
    bins = hexbin(np.array(xs),np.array(ys), 5)

    p = figure(tools="wheel_zoom,reset", match_aspect=True,background_fill_color='#440154')
    p.grid.visible = False

    p.hex_tile(q="q", r="r", size=0.1, line_color=None, source=bins,
           fill_color=linear_cmap('counts', 'Viridis256', 0, max(bins.counts)))

    show(p)


def success_heat_map(shots,display=True):
    """ Creates heat map of all made shots from a pandas structure
    resources: https://seaborn.pydata.org/examples/hexbin_marginals.html
    """
    #create separate pandas structure for made shots
    successes = shots[(shots.SHOT_MADE_FLAG==1)]
    sns.set_style("white")
    xs = successes["LOC_X"]
    ys = successes["LOC_Y"]
    #heat map of made shots
    sns.jointplot(xs, ys, kind="kde", stat_func=None, color="#57c838") ##4CB391
    if display == True:
        title = '{} {}'.format(shots["PLAYER_NAME"].iloc[0], 'made shots')
        plt.title(title, x=-4,y=1.2)
        plt.ylim(-100,400)
        plt.show()

def full_heat_map(shots,display=True):
    """ Creates heat map of all attempted shots from a pandas structure """
    sns.set_style(None)
    xs = shots["LOC_X"]
    ys = shots["LOC_Y"]
    #heat map of all shots
    sns.jointplot(xs, ys, kind="kde", stat_func=None, color="#bb38c8", zorder=1) ##4CB391
    if display == True:
        title = '{} {}'.format(shots["PLAYER_NAME"].iloc[0], 'attempted shots')
        plt.title(title, x=-4,y=1.2)
        plt.ylim(-100,400)
        # plt.plot([0,100],[50,150],zorder=2)
        plt.show()

if __name__ == "__main__":
    # # # Kevin Durant
    # durant_shots = generate_shots('Kevin','Durant','2017-18')
    # generate_scatter(durant_shots)
    # full_heat_map(durant_shots)
    # success_heat_map(durant_shots)
    # hist_heat(durant_shots)
    # hex_plot(durant_shots)
    # print(durant_shots)

    durant = generate_shots('Kevin','Durant','2016-17')
    full_heat_map(durant)

    # print(durant)
    # durant = shotchart.ShotChart(201142)
    # avgs = durant.league_average()
    # print(avgs)
    #
    # # James Harden
    # harden_shots = generate_shots('James','Harden','2017-18') ## consider point weighting
    # generate_scatter(harden_shots)
    # success_heat_map(harden_shots)
    # full_heat_map(harden_shots)
    # im = plt.imread('court.png')
    # implot = plt.imshow(im)
    # plt.show()
