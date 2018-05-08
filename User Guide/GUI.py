
'''
Complete integration of Bokeh widget based GUI with bokeh hxbin plots.
Use the ``bokeh serve`` command to run the webapp by executing:
    bokeh serve GUI.py
at your command prompt.
Then navigate to the URL
    http://localhost:5006/GUI
in your browser.

or use the command:
    bokeh serve --show GUI.py
'''
from bokeh.io import output_file, show,curdoc
from bokeh.layouts import widgetbox, gridplot, layout,row,column
from bokeh.models.widgets import Slider, TextInput, Dropdown, Toggle,RadioButtonGroup
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, IndexFilter,Button, CustomJS
from bokeh.events import ButtonClick
from bokeh.util.hex import hexbin
from bokeh.client import push_session
import pandas as pd
import csv
import pickle
import os
import numpy as np
import map_classes
from map_classes import *

# Set up plot
"""Deifnes default player plot that will be shown when the page is rendered for the first time"""

player = map_classes.Player('Kevin Durant')
p1 = player.hex_accuracy('2017-18')

# Set up widgets
"""Creates the objects from bokeh.widgets that will be used to interact with the plot"""

search_bar = TextInput(title="Search (eg. Kevin Durant or GSW)", value='Kevin Durant')
search = Button(label="Go", button_type="success")
slider = Slider(start=2007, end=2017, value=2017, step=1, title="Season",name="slider",callback_policy = "mouseup")
button_group1 = RadioButtonGroup(labels=["Player", "Team"], active=0)
button_group2 = RadioButtonGroup(labels=["Accuracy", "Frequency"], active=0)

# Set up layouts and add to document
"""Sets up the widgets and plot in an html document that will be pushed to the website"""

inputs = widgetbox(button_group1, search_bar,search, button_group2, slider,name='Widgets')
mainLayout = row(column(inputs),p1,name='mainLayout')
curdoc().add_root(mainLayout)

#Callback Functions
"""Callback functions define what happens when the user interacts with the html document on their browser. Each widget has their own individual function in order to udate the plot according to the user's input. """

def update_search_term(attrname, old, new):
    """Activated by the search button callback. It will check for if the player is looking for a player or a team, then it will checks the style of plot requested. The function will then generate the desired plot and update the values of the slider to match the active years of the player or team """
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    if button_group2.active == 1:
        if button_group1.active == 0:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            player = map_classes.Player(search_bar.value)
            season = player.final_season()
            p2 = player.hex_freq(season)
            rookie = player.rookie_season()
            final = player.final_season()
            index1 = int(rookie[0:4])
            index2 = int(final[0:4])
            if index1==index2:
                index1 = index2-1
            slider = curdoc().get_model_by_name('slider')
            slider.start = index1
            slider.end = index2
            slider.value = index2
            plotToAdd = p2
        else:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            team = map_classes.Team(search_bar.value)
            p2 = team.hex_freq('2017-18')
            slider = curdoc().get_model_by_name('slider')
            slider.start = 1996
            slider.end = 2017
            slider.value = 2017
            plotToAdd = p2
    else:
        if button_group1.active == 0:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            player = map_classes.Player(search_bar.value)
            season = player.final_season()
            p2 = player.hex_accuracy(season)
            rookie = player.rookie_season()
            final = player.final_season()
            index1 = int(rookie[0:4])
            index2 = int(final[0:4])
            if index1==index2:
                index1 = index2-1
            slider = curdoc().get_model_by_name('slider')
            slider.start = index1
            slider.end = index2
            slider.value = index2
            plotToAdd = p2
        else:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            team = map_classes.Team(search_bar.value)
            p2 = team.hex_accuracy('2017-18')
            slider = curdoc().get_model_by_name('slider')
            slider.start = 1996
            slider.end = 2017
            slider.value = 2017
            plotToAdd = p2

def update_plot_type(attrname, old, new):
    """Activted by the radio button callback function when the staus of the button pressed changes. The function will check the new state and display the desired frequency or accuracy plot for the team or player string in the search input box"""
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    if button_group1.active == 0:
        if button_group2.active == 1:
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            player = map_classes.Player(search_bar.value)
            season = str(slider.value)+'-'+str(slider.value+1)[2:4]
            p2 = player.hex_freq(season)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)
        else:
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            player = map_classes.Player(search_bar.value)
            season = str(slider.value)+'-'+str(slider.value+1)[2:4]
            p2 = player.hex_accuracy(season)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)
    else:
        if button_group2.active == 1:
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            team = map_classes.Team(search_bar.value)
            season = str(slider.value)+'-'+str(slider.value+1)[2:4]
            p2 = team.hex_freq(season)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)
        else:
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            team = map_classes.Team(search_bar.value)
            season = str(slider.value)+'-'+str(slider.value+1)[2:4]
            p2 = team.hex_accuracy(season)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)

def update_year(attrname, old, new):
    """Activates when the mouse is released over a new slider position or when a new palyer/team is requested. The plot for the correct year is generated using the slider value to create a string for the correct season to pass to map_classes (eg. 2017 --> '2018-2018'). The script removes the old plot from the layout matrix and renders the new one in its place. Both radio button groups are also checked to provide the correct plot type."""
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    if button_group1.active == 0:
        if button_group2.active == 1:
            print (slider.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            player = map_classes.Player(search_bar.value)
            nextyear = str(slider.value+1)
            years = str(slider.value)+'-'+nextyear[2:4]
            p2 = player.hex_freq(season=years)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)

        else:
            print (slider.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            player = map_classes.Player(search_bar.value)
            nextyear = str(slider.value+1)
            years = str(slider.value)+'-'+nextyear[2:4]
            p2 = player.hex_accuracy(season=years)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)
    else:
        if button_group2.active == 1:
            print (slider.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            team = map_classes.Team(search_bar.value)
            nextyear = str(slider.value+1)
            years = str(slider.value)+'-'+nextyear[2:4]
            p2 = team.hex_freq(season=years)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)
        else:
            print (slider.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            listOfSubLayouts.remove(plotToRemove)
            team = map_classes.Team(search_bar.value)
            nextyear = str(slider.value+1)
            years = str(slider.value)+'-'+nextyear[2:4]
            p2 = team.hex_accuracy(years)
            plotToAdd = p2
            listOfSubLayouts.append(plotToAdd)

#Set up callback event behavior
""" These define the attribute of each widget that is continiously checked and defines the callback functions to be run when the atribute is changed by the user."""
search.on_change('clicks', update_search_term, update_year)
button_group2.on_change('active', update_plot_type)
slider.on_change('value',update_year)

#Name the html document
curdoc().title = "GUI"
