import json
import pathlib

from . import helpers
from . import database
from . import typed_rows
from .helpers import CHARACTER_NAME_MAP
from ..debug import console

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
        ally_notebook_entry = {}
        bio = None
    
    name = base_stats.pop("name")
    true_name = CHARACTER_NAME_MAP[name]
    
    birthday = other["birthday"] if true_name != "Alear" else helpers.LONG_HYPHEN
    gender = other["gender"] if true_name != "Alear" else helpers.LONG_HYPHEN
    
    initial_class = base_stats.pop("class")
    initial_level = base_stats.pop("level")
    
    growth_rates.pop("name")
    
    proficiency_list = []
    innate_proficiency = []
    for p in other["proficiency"].split(","):
        p = p.lower()
        is_innate = False if "innate" not in p else True
        
        for k in ("sword","axe","bow","knife","lance","staff","tome","arts"):
            if k in p:
                proficiency_list.append(k)
                if is_innate: innate_proficiency.append(k)
    
    image_files = [f"{name}.png"]
    if name == "Alear":
        image_files = ["Alear_Male.png","Alear_Female.png"]

    data = {
        "name": true_name,
        "class": initial_class,
        "level": initial_level,
        "proficiency": other["proficiency"],
        "proficiency_list": proficiency_list,
        "innate_proficiency": innate_proficiency,
        "sp": other["sp"],
        "age": other["age"],
        "likes": ally_notebook_entry.get("c_rank",{}).get("likes",[]),
        "dislikes": ally_notebook_entry.get("c_rank",{}).get("dislikes",[]),
        "hobbies": ally_notebook_entry.get("b_rank",{}).get("hobbies",[]),
        "talents": ally_notebook_entry.get("b_rank",{}).get("talents",[]),
        "birthday": birthday,
        "gender": gender,
        "bio": "" if bio == None else bio,
        "personality": ally_notebook_entry.get("a_rank",{}).get("personality",""),
        "base_stats": base_stats,
        "growth_rates": growth_rates,
        "skills": skills,
        "image_files": image_files,
    }
    
    return data

def get_weapons(weapon_name:str=None,weapon_type:str=None,is_engage:bool=None):
    return database.Weapons(weapon_name,weapon_type,is_engage)

proficiency = {
        "sword": "Sword",
        "axe": "Axe",
        "lance": "Lance",
        "tome": "Tome",
        "arts": "Arts",
        "breath": "Breath",
        "staff": "Staff",
        "knife": "Knife",
        "bow": "Bow"
    }
