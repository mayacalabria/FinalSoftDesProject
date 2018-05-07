"""main web app file"""

from flask import *
from bokeh.embed import server_session
from bokeh.client import pull_session
from map_classes import Player,Team

app = Flask(__name__)

@app.route('/')
def home_page():
    """initial page"""
    return render_template('home_page.html')

@app.route('/backend', methods=['POST','GET'])
def backend():
    if request.method == 'POST':
        if request.form['choice']=='project':
            return project_description()
        if request.form['choice']=='player':
            return player_heat()
        if request.form['choice']=='team':
            return team_heat()
    return render_template('home_page.html')

@app.route('/project_description', methods=['POST','GET'])
def project_description():
    return 'Project Description Coming'

@app.route('/player', methods=['POST','GET'])
def player_heat():
    session = pull_session(url='http://localhost:5006/GUI')
    session.document.roots[0].children[1].title.text = 'I do not know what this will do'
    script = server_session(None,session.id,url='http://localhost:5006/GUI')
    return render_template('interactive_data.html',bokS=script,template="Flask")

@app.route('/viz_player', methods=['POST','GET'])
def find_player():
    if request.method == 'POST':
        name = request.form['player_name']
        player = Player(name).hex()
        return render_template_string(player)

# @app.route('/team', methods=['POST','GET'])
# def team_heat():


if __name__=='__main__':
    app.run()
