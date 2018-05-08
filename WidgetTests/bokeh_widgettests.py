"""
Test for bokeh drop down menus and Slider
"""

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, gridplot, layout
from bokeh.models.widgets import Slider, TextInput, Dropdown, Toggle
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, IndexFilter,Button, CustomJS
from bokeh.events import ButtonClick
import csv
import pickle
import os

pid_dict = pickle.load(open('pid_dict.pickle','rb'))
output_file("dropdown.html")
menu = [("Player", "player"), ("Team", "team"),("Conference", "conference")]
dropdown = Dropdown(label="Search by", button_type="warning", menu=menu)

output_file("text_input.html")
text_input = TextInput(value=" ")


source = ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5]))
p = figure(plot_height=300, plot_width=300)
p.circle(x="x", y="y", size=10, hover_color="red", source=source)

source2 = ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[2, 2, 2, 2, 2]))
f = figure(plot_height=300, plot_width=300)
f.circle(x="x", y="y", size=10, hover_color="red", source=source2)


output_file("slider.html")

output_file("Search.html")
toggle = Toggle(label="Search", button_type="success")

button = Button()

def callback(event):
    return show(f)

button.on_event(ButtonClick, callback)

slider = Slider(start=2003, end=2017, value=1, step=1, title="Season")

l = layout([
   [widgetbox(dropdown)],
   [widgetbox(text_input),widgetbox(button)],
   [p],
   [widgetbox(slider)],])

show(l)
