import numpy as np
from nba_py.player import get_player
from nba_py import shotchart
import matplotlib.pyplot as plt
import plotly.plotly as py
from scipy.stats import kendalltau
import seaborn as sns

def generate_shots(first,last,season):
    """ Takes first, last, and season as string,
    returns pandas structure of all shots
    """
    player_id = get_player(first,last)
    player = shotchart.ShotChart(player_id,season=season)
    shots = player.shot_chart()
    return shots


def generate_scatter(shots):
    """ Creates scatter plot of all shots taken by player over season """
    for i in range(len(shots)):
        x = shots["LOC_X"][i]
        y = shots["LOC_Y"][i]
        if shots["SHOT_MADE_FLAG"][i] == 1:
            plt.plot(x,y,'go')
        else:
            plt.plot(x,y,'ro')
        plt.axis('equal')
        plt.ylim(-100,400)



### Trying to plot only the shots that were made
# success = []
# for i in range(len(shots)):
#     # x = shots["LOC_X"][i]
#     # y = shots["LOC_Y"][i]
#     if shots["SHOT_MADE_FLAG"][i] == 1:
#         shots.pop(shots.iloc[i])


def success_heat_map(shots,display=True):
    """ Creates heat map of all made shots from a pandas structure
    resources: https://seaborn.pydata.org/examples/hexbin_marginals.html
    """
    successes = shots[(shots.SHOT_MADE_FLAG==1)]
    sns.set_style("white")
    xs = successes["LOC_X"]
    ys = successes["LOC_Y"]
    sns.jointplot(xs, ys, kind="kde", stat_func=None, color="#57c838") ##4CB391
    if display == True:
        title = '{} {}'.format(shots["PLAYER_NAME"][0], 'made shots')
        plt.title(title, x=-4,y=1.2)
        plt.ylim(-100,400)
        plt.show()

def full_heat_map(shots,display=True):
    """ Creates heat map of all attempted shots from a pandas structure """
    sns.set_style("white")
    xs = shots["LOC_X"]
    ys = shots["LOC_Y"]
    sns.jointplot(xs, ys, kind="kde", stat_func=None, color="#bb38c8") ##4CB391
    if display == True:
        title = '{} {}'.format(shots["PLAYER_NAME"][0], 'attempted shots')
        plt.title(title, x=-4,y=1.2)
        plt.ylim(-100,400)
        plt.show()



if __name__ == "__main__":
    # # Kevin Durant
    durant_shots = generate_shots('Kevin','Durant','2017-18')
    generate_scatter(durant_shots)
    full_heat_map(durant_shots)
    success_heat_map(durant_shots)

    # # James Harden
    harden_shots = generate_shots('James','Harden','2017-18')
    generate_scatter(harden_shots)
    success_heat_map(harden_shots)
    full_heat_map(harden_shots)
