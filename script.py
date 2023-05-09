import re
import json
import pathlib
import requests
import urllib.request

import bs4

import fire_emblem.engage.api

import fire_emblem.engage.api as engage
from fire_emblem.engage.api import get_character
from fire_emblem.engage import fetch
from fire_emblem.engage import database

from fire_emblem.debug import console

root = pathlib.Path(__file__).parent.joinpath("fire_emblem")

HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0"}
def _retrieve_character_images():
    url = "https://fireemblem.fandom.com/wiki/List_of_characters_in_Fire_Emblem_Engage"
    r = requests.get(url,headers=HEADERS)
    soup = bs4.BeautifulSoup(r.text,"html.parser")

    for i in soup.find_all("img"):
        i: bs4.Tag
        if i.parent.name == "a":
            href:str = i.parent.get("href")
            filename = i.get("data-image-name")
            if not filename: continue
            filepath = root.joinpath("character_images",filename)
            if not filepath.exists():
                urllib.request.urlretrieve(href,filepath)


data = fetch._weapon_data_fandom()
data = fetch._skills_data_fandom()

# with root.joinpath("data","engage","files","weapons.json").open("w+") as fp:
#     json.dump(data,fp,sort_keys=False,indent=2)

# with root.joinpath("data","engage","files","weapons.json").open("r") as fp:
#     data = json.load(fp)
#     for d in data:
#         icon_url = d["icon_url"]
#         icon_name = d["icon_name"]
#         filename = root.joinpath("data","engage","images","weapons",f"{icon_name}.png")
#         urllib.request.urlretrieve(icon_url,filename)

fandom_data = fetch._weapon_data_fandom()
serenes_data = engage.get_weapons()
console.print(fandom_data[0])
print()
console.print(serenes_data[0])