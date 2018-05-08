"""main web app file"""

from flask import *
import os
from bokeh.embed import server_session,server_document
from bokeh.client import pull_session
from map_classes import Player,Team

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def data_viz():
    script = server_document(url='http://localhost:5006/GUI')
    return render_template('interactive_data.html',bokS=script,template="Flask")

if __name__=='__main__':
    app.run()
