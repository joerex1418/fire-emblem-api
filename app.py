from flask import request
from flask.app import Flask
from flask.json import jsonify
from flask.templating import render_template
from flask.helpers import url_for
from flask_assets import Environment, Bundle

from fire_emblem import engage
from fire_emblem.helpers import engage_character_image
from fire_emblem.debug import console

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

assets = Environment(app)
scss = Bundle('style.scss',filters='pyscss',output='style.css')
assets.register('style',scss)

@app.context_processor
def inject_dict_for_all_templates():
    content = dict(enumerate=enumerate,range=range,print=print)
    content["console"] = console
    content["CHARACTER_NAME_MAP"] = engage.CHARACTER_NAME_MAP
    return content

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/engage")
def fe_engage():
    character_data = engage.api.get_character("Lapis")
    character_data["image_files"] = [url_for('static',filename=f'images/engage/characters/{image_file}') for image_file in character_data["image_files"]]
    character_data["proficiency_images"] = [url_for('static',filename=f'images/engage/icons/{p}.webp') for p in character_data["proficiency_list"]]
    # console.print(character_data)
    return render_template("fe-engage.html",character_data=character_data,engage=engage)

@app.route("/engage/characters")
def engage_characters():
    return render_template("engage/characters.html")

@app.route("/api/engage/character")
def api_engage_character():
    name = request.args.get("name")
    character_data = engage.api.get_character(name)
    character_data["image_files"] = [url_for('static',filename=f'images/engage/characters/{image_file}') for image_file in character_data["image_files"]]
    character_data["proficiency_images"] = [url_for('static',filename=f'images/engage/icons/{p}.webp') for p in character_data["proficiency_list"]]
    character_data["html"] = render_template("engage/character_container_data.html",character_data=character_data,engage=engage)
    return jsonify(character_data)
    

host = "10.0.1.250"
host = "127.0.0.1"
if __name__ == "__main__":
    app.run(host,port=5500,debug=True)