"""main web app file"""

from flask import *
import os
from bokeh.embed import server_session,server_document
from bokeh.client import pull_session
from map_classes import Player,Team

app = Flask(__name__)

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home_page():
    """initial page"""
    return render_template('home_page.html')

@app.route('/backend', methods=['POST','GET'])
def backend():
    if request.method == 'POST':
        if request.form['choice']=='README':
            return readme()
        if request.form['choice']=='Documentation':
            return documentation()
        if request.form['choice']=='Code Architecture':
            return code_architecture()
        if request.form['choice']=='Interactive Visualization Tool':
            return data_viz()
    return render_template('home_page.html')

@app.route('/readme', methods=['POST'])
def readme():
    return render_template('README.html')

@app.route('/index', methods=['POST'])
def documentation():
    return('index.html')

@app.route('/code_architecture', methods=['POST'])
def code_architecture():
    return render_template('architecture.html')

@app.route('/player', methods=['POST','GET'])
def data_viz():
    # session = pull_session(url='http://localhost:5006/GUI')
    # script = server_session(None,session.id,url='http://localhost:5006/GUI')
    script = server_document(url='http://localhost:5006/GUI')
    return render_template('interactive_data.html',bokS=script,template="Flask")

if __name__=='__main__':
    app.run()
