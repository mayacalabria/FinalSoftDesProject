import numpy as np
from nba_py.player import get_player
from nba_py import shotchart
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import plotly.plotly as py
from scipy.stats import kendalltau
import seaborn as sns
from PIL import Image
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from bokeh.models import LogColorMapper,LogTicker,ColorBar,LinearColorMapper
from bokeh.models.tickers import BasicTicker
import pickle
import os.path
import pandas as pd
import colorcet as cc

def generate_shots_fromNBA(first,last,season):
    """ Takes first, last, and season as string,
    returns pandas structure of all shots
    """
    player_id = get_player(first,last)
    player = shotchart.ShotChart(player_id,season=season)
    shots = player.shot_chart()
    return shots

def generate_shots(first,last=None,season='2017-18'):
    """ Takes first, last, and season as string,
    returns pandas structure of all shots from locally stored
    data CSVs
    """

    pid_dict = pickle.load(open('pid_dict.pickle','rb'))
    new_dict = {v: k for k, v in pid_dict.items()}
    if last:
        player_id = new_dict[first+' '+last]
    else:
        player_id = new_dict[first]
    # shots_dir should be named relatively eventually
    shots_dir = os.path.abspath(os.path.join(os.getcwd(),'../PlayerData3/'+player_id+'/'+season+'.csv'))
    shots = pd.read_csv(shots_dir)
    return shots

def generate_team_shots(team_abv,season='2017-18'):
    """ Takes first, last, and season as string,
    returns pandas structure of all shots from locally stored
    data CSVs
    """

    teamid_dict = pickle.load(open('teamid_dict.pickle','rb'))
    new_dict = {v: k for k, v in teamid_dict.items()}
    teamid = str(new_dict[team_abv])
    team_shots_dir = os.path.abspath(os.path.join(os.getcwd(),
        '../TeamData3/'+teamid+'/'+season+'.csv'))
    shots = pd.DataFrame.from_csv(team_shots_dir)
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

def hex_plot_player(shots):
    """ Takes pandas DataFrame of shots and creates Bokeh hex plot,
    optional binsize, controls resolution
    """
    #sort all bins by zone and percentage for that zone
    all_bins = sort_all_bins(shots)
    title = shots['PLAYER_NAME'].iloc[0]
    p = figure(title=title, tools="wheel_zoom,reset", match_aspect=True,
        background_fill_color='#BB7E3B')
    p.grid.visible = False

    p.hex_tile(q="q", r="r", size=0.1, line_color='black', source=all_bins,
        fill_color=linear_cmap('counts', cc.coolwarm, -10, 10))
    draw_court(p)
    color_mapper = LinearColorMapper(palette=cc.coolwarm,low=-10,high=10)
    color_bar = ColorBar(color_mapper=color_mapper, location=(0,0),)
    p.add_layout(color_bar, 'right')

    show(p)

def hex_plot_player_freq(shots):
    """ Takes pandas DataFrame of shots and creates Bokeh hex plot,
    optional binsize, controls resolution
    """
    #sort all bins by zone and percentage for that zone
    all_bins = sort_all_bins_freq(shots)
    title = shots['PLAYER_NAME'].iloc[0]
    p = figure(title=title, tools="wheel_zoom,reset", match_aspect=True,
        background_fill_color='#BB7E3B')
    p.grid.visible = False

    p.hex_tile(q="q", r="r", size=0.1, line_color='black', source=all_bins,
        fill_color=linear_cmap('counts', cc.coolwarm, -5, 5))
    draw_court(p)
    color_mapper = LinearColorMapper(palette=cc.coolwarm,low=-5,high=5)
    color_bar = ColorBar(color_mapper=color_mapper, location=(0,0),)
    p.add_layout(color_bar, 'right')

    show(p)

def hex_plot_team(shots):
    """ Takes pandas DataFrame of shots and creates Bokeh hex plot,
    optional binsize, controls resolution
    """
    #sort all bins by zone and percentage for that zone
    all_bins = sort_all_bins(shots)
    title = shots['TEAM_NAME'].iloc[0]
    p = figure(title=title, tools="wheel_zoom,reset", match_aspect=True,
        background_fill_color='#BB7E3B')
    p.grid.visible = False

    p.hex_tile(q="q", r="r", size=0.1, line_color='black', source=all_bins,
        fill_color=linear_cmap('counts', cc.coolwarm, -5, 5))
    draw_court(p)
    color_mapper = LinearColorMapper(palette=cc.coolwarm,low=-5,high=5)
    color_bar = ColorBar(color_mapper=color_mapper, location=(0,0),)
    p.add_layout(color_bar, 'right')

    show(p)

def hex_plot_team_freq(shots):
    """ Takes pandas DataFrame of shots and creates Bokeh hex plot,
    optional binsize, controls resolution
    """
    #sort all bins by zone and percentage for that zone
    all_bins = sort_all_bins_freq(shots)
    title = shots['TEAM_NAME'].iloc[0]
    p = figure(title=title, tools="wheel_zoom,reset", match_aspect=True,
        background_fill_color='#BB7E3B')
    p.grid.visible = False

    p.hex_tile(q="q", r="r", size=0.1, line_color='black', source=all_bins,
        fill_color=linear_cmap('counts', cc.coolwarm, -2.5, 2.5))
    draw_court(p)
    color_mapper = LinearColorMapper(palette=cc.coolwarm,low=-2.5,high=2.5)
    color_bar = ColorBar(color_mapper=color_mapper, location=(0,0),)
    p.add_layout(color_bar, 'right')

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

def league_average(season=None, first='Kevin', last='Durant'):
    """ Generates the leage averages by zone for the given season
    default value for first/last name is Kevin Durant, but any player
    could be used to initialize the ShotChart class from nba_py
    takes season as a string and defaults to current season

    returns: Pandas DataFrame
    """
    player = shotchart.ShotChart('201142',season=season)
    league_average = player.league_average()
    return league_average



def sort_successes(shots):
    """ Takes a pandas DataFrame of a players shots and returns a data set
    with only shots that were successful
    """
    successes = shots[(shots.SHOT_MADE_FLAG==1)]
    return successes

def calc_all_zone_percentage(shots,season='2017-18'):
    """ Takes a pandas DataFrame of a players shots and the season to calculate
    their shooting percentage by zone, returns a dictionary of the players zone
    percentage minus the league average percentage for that zone
    """
    basic_zones = ['Above the Break 3', 'Above the Break 3',
        'Above the Break 3', 'Above the Break 3', 'Backcourt',
        'In The Paint (Non-RA)', 'In The Paint (Non-RA)',
        'In The Paint (Non-RA)', 'In The Paint (Non-RA)', 'Left Corner 3',
        'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range',
        'Mid-Range', 'Mid-Range', 'Mid-Range', 'Restricted Area',
        'Right Corner 3']
    zone_areas = ['Back Court(BC)', 'Center(C)', 'Left Side Center(LC)',
        'Right Side Center(RC)', 'Back Court(BC)', 'Center(C)', 'Center(C)',
        'Left Side(L)', 'Right Side(R)', 'Left Side(L)', 'Center(C)',
        'Center(C)', 'Left Side Center(LC)', 'Left Side(L)', 'Left Side(L)',
        'Right Side Center(RC)', 'Right Side(R)', 'Right Side(R)', 'Center(C)',
        'Right Side(R)']
    ranges = ['Back Court Shot', '24+ ft.', '24+ ft.', '24+ ft.',
        'Back Court Shot', '8-16 ft.', 'Less Than 8 ft.', '8-16 ft.',
        '8-16 ft.', '24+ ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.',
        '16-24 ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.', '8-16 ft.',
        'Less Than 8 ft.', '24+ ft.']

    all_percentages = {}
    league_avg = league_average(season=season)

    for i in range(len(zone_areas)):
        league_percent = 100 * (league_avg['FG_PCT'].iloc[i])
        zone_percent = calc_zone_percentage(shots,str(zone_areas[i]),
            str(ranges[i]),str(basic_zones[i]))
        relative_zone_percent = zone_percent - league_percent
        dict_key = (str(basic_zones[i]),str(zone_areas[i]),str(ranges[i]))
        all_percentages[dict_key] = relative_zone_percent

    return all_percentages

def calc_zone_percentage(shots,zone_area,zone_range,basic_zone):
    """calculates an individual zone percentage in a dataframe of shot data
    """
    basic = shots[(shots.SHOT_ZONE_BASIC==basic_zone)]#filters for basic zone
    zone = basic[(basic.SHOT_ZONE_AREA==zone_area)]#filters for only the area
    fin_range = zone[(zone.SHOT_ZONE_RANGE==zone_range)]#gets all from a specific range in that area
    if len(fin_range.index)==0:
        return 0.0
    fin_range_s = fin_range[(fin_range.SHOT_MADE_FLAG==1)]#isolate all of the successful shots
    zone_percentage = 100 * (len(fin_range_s.index)/len(fin_range.index))#calculate percentage

    return zone_percentage

def sort_hex_bin(shots,zone_area,zone_range,basic_zone):
    """given 3 parameters to define a zone output all of the x,y position data
    for that zone"""
    basic = shots[(shots.SHOT_ZONE_BASIC==basic_zone)]#filters for basic zone
    zone = basic[(basic.SHOT_ZONE_AREA==zone_area)]#filters for only the area
    fin_range = zone[(zone.SHOT_ZONE_RANGE==zone_range)]

    xs = fin_range['LOC_X']
    ys = fin_range['LOC_Y']
    zone_percentage = fin_range['ZONE_PERCENTAGE']

    return xs, ys, zone_percentage

def sort_all_bins(shots):

    basic_zones = ['Above the Break 3', 'Above the Break 3',
        'Above the Break 3', 'Above the Break 3', 'Backcourt',
        'In The Paint (Non-RA)', 'In The Paint (Non-RA)',
        'In The Paint (Non-RA)', 'In The Paint (Non-RA)', 'Left Corner 3',
        'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range',
        'Mid-Range', 'Mid-Range', 'Mid-Range', 'Restricted Area',
        'Right Corner 3']
    zone_areas = ['Back Court(BC)', 'Center(C)', 'Left Side Center(LC)',
        'Right Side Center(RC)', 'Back Court(BC)', 'Center(C)', 'Center(C)',
        'Left Side(L)', 'Right Side(R)', 'Left Side(L)', 'Center(C)',
        'Center(C)', 'Left Side Center(LC)', 'Left Side(L)', 'Left Side(L)',
        'Right Side Center(RC)', 'Right Side(R)', 'Right Side(R)', 'Center(C)',
        'Right Side(R)']
    ranges = ['Back Court Shot', '24+ ft.', '24+ ft.', '24+ ft.',
        'Back Court Shot', '8-16 ft.', 'Less Than 8 ft.', '8-16 ft.',
        '8-16 ft.', '24+ ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.',
        '16-24 ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.', '8-16 ft.',
        'Less Than 8 ft.', '24+ ft.']

    list_of_bins = []

    for i in range(len(ranges)):
        if i==0 or i==4:
            pass
        else:
            xs,ys,percentage = sort_hex_bin(shots,zone_areas[i],ranges[i],basic_zones[i])
            bin = hexbin(np.array(xs),np.array(ys),7.5)
            if len(bin) == 0:
                bin['counts'] = 0
            else:
                bin['counts'] = percentage.iloc[0]
            list_of_bins.append(bin)

    all_bins = pd.concat(list_of_bins,ignore_index=True)

    return all_bins

def draw_court(fig_obj,line_width=3,line_color='black',line_alpha=1):
    """takes a bokeh hex plot figure object and draws court lines over
    the figure"""
    lw = line_width
    lc = line_color
    la = line_alpha
    #3pt line
    fig_obj.line(x=[-2.9, -2.9],y=[-.5, 1.3],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.line(x=[2.9, 2.9],y=[-.5, 1.3],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.arc(x=0,y=0,radius=3.178,start_angle=.4214,end_angle=2.7202,line_width=lw,
        line_color=lc,line_alpha=la)
    #baseline, sidelines, centercourt boundries
    fig_obj.line(x=[-3.5, 3.5],y=[-.5, -.5],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.line(x=[-3.5, -3.5],y=[-.5, 5.892],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.line(x=[3.5, 3.5],y=[-.5, 5.892],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.line(x=[-3.5, 3.5],y=[5.892, 5.892],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.arc(x=0,y=5.892,radius=.3,start_angle=np.pi,end_angle=2*np.pi,
        line_width=lw,line_color=lc,line_alpha=la)
    fig_obj.arc(x=0,y=5.892,radius=.9,start_angle=np.pi,end_angle=2*np.pi,
        line_width=lw,line_color=lc,line_alpha=la)
    #hoop, backboard, restricted Area
    fig_obj.arc(x=0,y=0,radius=.1,start_angle=0,end_angle=np.pi*2,
        line_width=lw,line_color=lc,line_alpha=la)
    fig_obj.line(x=[-.4,.4],y=[-.1,-.1],line_width=lw,line_color=lc,
        line_alpha=la)
    fig_obj.arc(x=0,y=0,radius=.533,start_angle=0,end_angle=np.pi,
        line_width=lw,line_color=lc,line_alpha=la)
    #key, free throw lines
    fig_obj.rect(x=.933,y=.7635,width=.266,height=2.527,fill_alpha=0,
        line_width=lw,line_color=lc,line_alpha=la)
    fig_obj.rect(x=-.933,y=.7635,width=.266,height=2.527,fill_alpha=0,
        line_width=lw,line_color=lc,line_alpha=la)
    fig_obj.arc(x=0,y=2.027,radius=.8,start_angle=0,end_angle=np.pi,
        line_width=lw,line_color=lc,line_alpha=la)
    fig_obj.arc(x=0,y=2.027,radius=.8,start_angle=np.pi,end_angle=np.pi*2,
        line_width=lw,line_color=lc,line_alpha=la,line_dash='dashed')
    fig_obj.line(x=[-.8, .8],y=[2.027, 2.027],line_width=lw,line_color=lc,
        line_alpha=la)

    return fig_obj

def sort_hex_bin_freq(shots,zone_area,zone_range,basic_zone):
    """given 3 parameters to define a zone output all of the x,y position data
    for that zone"""
    basic = shots[(shots.SHOT_ZONE_BASIC==basic_zone)]#filters for basic zone
    zone = basic[(basic.SHOT_ZONE_AREA==zone_area)]#filters for only the area
    fin_range = zone[(zone.SHOT_ZONE_RANGE==zone_range)]

    xs = fin_range['LOC_X']
    ys = fin_range['LOC_Y']
    zone_freq = fin_range['ZONE FREQUENCY']

    return xs, ys, zone_freq

def sort_all_bins_freq(shots):

    basic_zones = ['Above the Break 3', 'Above the Break 3',
        'Above the Break 3', 'Above the Break 3', 'Backcourt',
        'In The Paint (Non-RA)', 'In The Paint (Non-RA)',
        'In The Paint (Non-RA)', 'In The Paint (Non-RA)', 'Left Corner 3',
        'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range', 'Mid-Range',
        'Mid-Range', 'Mid-Range', 'Mid-Range', 'Restricted Area',
        'Right Corner 3']
    zone_areas = ['Back Court(BC)', 'Center(C)', 'Left Side Center(LC)',
        'Right Side Center(RC)', 'Back Court(BC)', 'Center(C)', 'Center(C)',
        'Left Side(L)', 'Right Side(R)', 'Left Side(L)', 'Center(C)',
        'Center(C)', 'Left Side Center(LC)', 'Left Side(L)', 'Left Side(L)',
        'Right Side Center(RC)', 'Right Side(R)', 'Right Side(R)', 'Center(C)',
        'Right Side(R)']
    ranges = ['Back Court Shot', '24+ ft.', '24+ ft.', '24+ ft.',
        'Back Court Shot', '8-16 ft.', 'Less Than 8 ft.', '8-16 ft.',
        '8-16 ft.', '24+ ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.',
        '16-24 ft.', '8-16 ft.', '16-24 ft.', '16-24 ft.', '8-16 ft.',
        'Less Than 8 ft.', '24+ ft.']

    list_of_bins = []

    for i in range(len(ranges)):
        if i==0 or i==4:
            pass
        else:
            xs,ys,freq = sort_hex_bin_freq(shots,zone_areas[i],ranges[i],basic_zones[i])
            bin = hexbin(np.array(xs),np.array(ys),7.5)
            if len(bin) == 0:
                bin['counts'] = 0
            else:
                bin['counts'] = freq.iloc[0]
            list_of_bins.append(bin)

    all_bins = pd.concat(list_of_bins,ignore_index=True)

    return all_bins

def calc_zone_frequency(shots,basic_zone,zone_area,zone_range):
    """takes a dataframe of shot data and returns a dictionary with each
    zones relative frequency"""

    basic = shots[(shots.SHOT_ZONE_BASIC==basic_zone)]#filters for basic zone
    zone = basic[(basic.SHOT_ZONE_AREA==zone_area)]#filters for only the area
    fin_range = zone[(zone.SHOT_ZONE_RANGE==zone_range)]#gets all from a specific range in that area

    zone_percentage = 100 * (len(fin_range.index)/len(shots.index))

    return zone_percentage

if __name__ == "__main__":

    # # # Kevin Durant
    # durant_shots = generate_shots('Kevin','Durant','2016-17')
    # generate_scatter(durant_shots)
    # full_heat_map(durant_shots)
    # success_heat_map(durant_shots)
    # hist_heat(durant_shots)
    # hex_plot(durant_shots)
    # print(durant_shots)
    # team_test = os.path.abspath(os.path.join(os.getcwd(),'../TeamData2/1610612744/2016-17.csv'))
    # shots = pd.DataFrame.from_csv(team_test)
    shots = generate_shots('LeBron','James','2017-18')
    hist_heat(shots)
    full_heat_map(shots)
    #team_shots = generate_team_shots('GSW','2017-18')
    #hex_plot_team_freq(team_shots)
    #hex_plot_team(team_shots)
    #hex_plot_team(team_shots)
    # # # James Harden
    # harden_shots = generate_shots('James','Harden','2016-17') ## consider point weighting
    # hex_plot(harden_shots)
    # generate_scatter(harden_shots)
    # success_heat_map(harden_shots)
    # full_heat_map(harden_shots)
    # im = plt.imread('court.png')
    # implot = plt.imshow(im)
    # plt.show()

    #durant = generate_shots('Russell','Westbrook',season='2016-17')
    #sort_all_bins(durant)
    #hex_plot(durant)
    #hex_plot(durant)
    # durant_success = sort_successes(durant)
    # league_avg = league_average(season='2016-17')
    # print(league_avg)
    # league_avg2 = league_average(season='2017-18')
    # # print(durant_success,league_avg)
    #
    # print(calc_all_zone_percentage(durant))
    # # successes = shots[(shots.SHOT_ZONE_BASIC==Center(C))]
    # Center = durant[durant.SHOT_ZONE_AREA=='Center(C)']  #filters for only Center court shots
    # Center_8_16 = Center[Center.SHOT_ZONE_RANGE=='8-16 ft.'] #Center shots range (8-16 ft)
    # Center_8_16_s = Center_8_16[(Center_8_16.SHOT_MADE_FLAG==1)] # only successful center 8-16 ft shots
    # percent = len(Center_8_16_s.index)/len(Center_8_16.index)
    # #print(percent)
    # print(durant)

    # league = durant.league_average()
    # print(league)
