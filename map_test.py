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


### Trying to plot only the shots that were made
# success = []
# for i in range(len(shots)):
#     x = shots["LOC_X"][i]
#     y = shots["LOC_Y"][i]
#     if shots["SHOT_MADE_FLAG"][i] == 1:
#         shots.pop(shots.iloc[i])


def heat_map(shots):
    """ Creates heat map from a pandas structure
    resources: https://seaborn.pydata.org/examples/hexbin_marginals.html
    """

    sns.set(style="ticks")
    xs = shots["LOC_X"]
    ys = shots["LOC_Y"]
    sns.jointplot(xs, ys, kind="kde", stat_func=kendalltau, color="#FF1200") ##4CB391



if __name__ == "__main__":
    # Kevin Durant
    durant_shots = generate_shots('Kevin','Durant','2017-18')
    generate_scatter(durant_shots)
    heat_map(durant_shots)

    # James Harden
    harden_shots = generate_shots('James','Harden','2017-18')
    generate_scatter(harden_shots)
    heat_map(harden_shots)

    plt.show()
