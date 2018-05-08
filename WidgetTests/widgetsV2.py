
''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/widgetsV2
in your browser.
'''
from bokeh.io import output_file, show,curdoc
from bokeh.layouts import widgetbox, gridplot, layout,row
from bokeh.models.widgets import Slider, TextInput, Dropdown, Toggle,RadioButtonGroup
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, IndexFilter,Button, CustomJS
from bokeh.events import ButtonClick
import csv
import pickle
import os
import numpy as np

# Set up data
source = ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5]))


# Set up plot
p = figure(plot_height=300, plot_width=300)
p.circle(x="x", y="y", size=10, hover_color="red", source=source)


# Set up widgets
search_bar = TextInput(title="Search", value='e.g Lebron James or Cleveland Cavaliers')
slider = Slider(start=2003, end=2017, value=1, step=1, title="Season")
button_group = RadioButtonGroup(labels=["Player", "Team"], active=0)
# Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    year = slider.value
    print(year)
    # Generate the new curve
    x=[1, 2, 3, 4, 5]
    y = y=[2, 2, 2, 2, 2]

    source.data = dict(x=x, y=y)

def update_search(attrname, old, new):
    search = search_bar.value
    slider.on_change('value', update_data)

search_bar.on_change('value', update_search)


# Set up layouts and add to document
inputs = widgetbox(search_bar, slider, button_group)

curdoc().add_root(row(inputs, p, width=800))
curdoc().title = "widgetsV2"
