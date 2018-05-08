from flask import *
from bokeh.embed import server_session,server_document
from bokeh.client import pull_session
from map_classes import Player,Team

app = Flask(__name__)

@app.route('/')
def home_page():
    """initial page"""
    return render_template('architecture.html')

app.run()
