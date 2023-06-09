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
    content = dict(enumerate=enumerate,range=range)
    content["console"] = console
    content["CHARACTER_NAME_MAP"] = engage.CHARACTER_NAME_MAP
    return content

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/engage/characters")
def engage_charachters():
    return render_template("engage/characters.html")

@app.route("/api/engage")
def api_engage_character():
    character_name = request.args.get("name").capitalize()
    
    base_stats = [d for d in engage.character_base_stats() if d["name"] == character_name]
    growth_rates = [d for d in engage.character_growth_rates() if d["name"] == character_name]
    skills = [d for d in engage.character_skills() if d["character"] == character_name]
    other = [d for d in engage.character_other_data() if d["name"] == character_name]
    
    data = {
        "base": base_stats[0],
        "growth_rate": growth_rates[0],
        "skills": skills[0],
        "other": other[0],
        "likes": "",
        "image_path": url_for('static',filename=f'images/characters/engage/{character_name}.jpg'),
    }
    console.print_json(data=data)
    
    character_html = render_template("games/engage_character.html",data=data)
    data["html"] = character_html
    return jsonify(data)
    

host = "10.0.1.250"
# host = "127.0.0.1"
if __name__ == "__main__":
    app.run(host,port=5500,debug=True)