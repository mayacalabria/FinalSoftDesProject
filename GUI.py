
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
player = map_classes.Player('Kevin Durant')
p1 = player.hex_accuracy('2017-18')

# Set up widgets
search_bar = TextInput(title="Search (eg. Kevin Durant or GSW)", value='Kevin Durant')
search = Button(label="Go", button_type="success")
slider = Slider(start=2007, end=2017, value=2017, step=1, title="Season",name="slider",callback_policy = "mouseup")
button_group1 = RadioButtonGroup(labels=["Player", "Team"], active=0)
button_group2 = RadioButtonGroup(labels=["Accuracy", "Frequency"], active=0)

# Set up layouts and add to document
inputs = widgetbox(button_group1, search_bar,search, button_group2, slider,name='Widgets')
mainLayout = row(column(inputs),p1,name='mainLayout')
curdoc().add_root(mainLayout)
#session = push_session(curdoc())

#Set up callbacks
def update_search_term(attrname, old, new):
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    if button_group2.active == 1:
        if button_group1.active == 0:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            #listOfSubLayouts.remove(plotToRemove)
            player = map_classes.Player(search_bar.value)
            season = player.final_season()
            p2 = player.hex_freq(season)
            rookie = player.rookie_season()
            final = player.final_season()
            index1 = int(rookie[0:4])
            index2 = int(final[0:4])
            slider = curdoc().get_model_by_name('slider')
            slider.start = index1
            slider.end = index2
            slider.value = index2
            plotToAdd = p2
            #listOfSubLayouts.append(plotToAdd)
        else:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            #listOfSubLayouts.remove(plotToRemove)
            shots,team = map_classes.Team(search_bar.value)
            p2 = team.hex_freq('2017-18')
            slider = curdoc().get_model_by_name('slider')
            slider.start = 1996
            slider.end = 2017
            slider.value = 2017
            plotToAdd = p2
            #listOfSubLayouts.append(plotToAdd)
    else:
        if button_group1.active == 0:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            #listOfSubLayouts.remove(plotToRemove)
            player = map_classes.Player(search_bar.value)
            season = player.final_season()
            p2 = player.hex_accuracy(season)
            rookie = player.rookie_season()
            final = player.final_season()
            index1 = int(rookie[0:4])
            index2 = int(final[0:4])
            slider = curdoc().get_model_by_name('slider')
            slider.start = index1
            slider.end = index2
            slider.value = index2
            plotToAdd = p2
            #listOfSubLayouts.append(plotToAdd)
        else:
            print(search_bar.value)
            plotToRemove = curdoc().get_model_by_name('plot')
            #listOfSubLayouts.remove(plotToRemove)
            team = map_classes.Team(search_bar.value)
            p2 = team.hex_accuracy('2017-18')
            slider = curdoc().get_model_by_name('slider')
            slider.start = 1996
            slider.end = 2017
            slider.value = 2017
            plotToAdd = p2
            #listOfSubLayouts.append(plotToAdd)

def update_plot_type(attrname, old, new):
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

def debounce(fn, model, wait, doc):
    cval = model.value
    def delayed_job():
        if model.value == cval:
            fn()
    doc.add_timeout_callback(delayed_job, wait*1000)

search.on_change('clicks', update_search_term, update_year)
button_group2.on_change('active', update_plot_type)
slider.on_change('value',update_year)
# Set up layouts and add to document
# inputs = widgetbox(button_group1, search_bar,search, button_group2, slider)
# one = row(inputs, plot, width=1200)
# curdoc().add_root(one)
# curdoc().title = "GUI"

#Set up session
# session.show()
# session.loop_until_closed()
