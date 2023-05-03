from flask import request
from flask.app import Flask
from flask.json import jsonify
from flask.templating import render_template
from flask.helpers import url_for
from flask_assets import Environment, Bundle

from api import fe_engage
from api.debug import console

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

assets = Environment(app)
scss = Bundle('style.scss',filters='pyscss',output='style.css')
assets.register('style',scss)

@app.context_processor
def inject_dict_for_all_templates():
    content = dict(enumerate=enumerate)
    content["console"] = console
    return content

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/game/engage")
def game_engage():
    character_data = fe_engage.character_base_stats()
    return render_template('games/engage.html',
                           title="Fire Emblem: Engage",
                           character_data=character_data)
    


if __name__ == "__main__":
    app.run("127.0.0.1",port=5000,debug=True)