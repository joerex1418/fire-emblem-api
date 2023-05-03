import re
import json

from api import fe_engage

from api.fe_engage import fetch
from api.fe_engage import database

from api.debug import console


# database.character_base_stats_table()
# database.character_growth_rates_table()
# database.character_other_data_table()
# database.character_skills_table()
# database.learnable_skills_table()
# database.bond_rings_table()
# database.weapons_table()
# database.items_table()
# database.materials_table()
# database.ally_notebook_table()

data = fe_engage.weapons(weapon_type="sword")
# console.print_json(data=data)
console.print(data)

# fetch._get_character_images()

# for key in fetch.weapons.swords()[0].keys():
#     print(f'"{key}": "",')