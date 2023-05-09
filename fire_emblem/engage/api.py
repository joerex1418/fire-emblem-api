import json
import pathlib

from . import helpers
from . import database
from . import typed_rows
from .helpers import CHARACTER_NAME_MAP

def get_character(character_name:str) -> typed_rows._Character:
    base_stats = database.character_base_stats(character_name)[0]
    growth_rates = database.character_growth_rates(character_name)[0]
    other = database.character_other_data(character_name)[0]
    ally_notebook_entry = database.ally_notebook(character_name)
    skills = []
    for sk in database.character_skills(character_name):
        sk.pop("character")
        skills.append(sk)
    
    if len(ally_notebook_entry) > 0:
        ally_notebook_entry = ally_notebook_entry[0]
        bio = ally_notebook_entry["initial"]["basic_info"]
    else:
        bio = None
    
    name = base_stats.pop("name")
    true_name = CHARACTER_NAME_MAP[name]
    initial_class = base_stats.pop("class")
    initial_level = base_stats.pop("level")
    
    growth_rates.pop("name")
    
    image_files = [f"{name}.png"]
    if name == "Alear":
        image_files = ["Alear_Male.png","Alear_Female.png"]
    
    data = {
        "name": true_name,
        "class": initial_class,
        "level": initial_level,
        "proficiency": other["proficiency"],
        "sp": other["sp"],
        "age": other["age"],
        "birthday": other["birthday"],
        "gender": other["gender"],
        "bio": bio,
        "base_stats": base_stats,
        "growth_rates": growth_rates,
        "skills": skills,
        "image_files": image_files,
    }
    
    return data

def get_weapons(weapon_name:str=None,weapon_type:str=None,is_engage:bool=None):
    return database.Weapons(weapon_name,weapon_type,is_engage)
