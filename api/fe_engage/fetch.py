import re
import json
import typing
import pathlib
import requests
import urllib.request

import bs4

from .helpers import STAT_MAP
from .helpers import CHARACTER_STATS
from .helpers import ACCENT_E, LONG_HYPHEN

datapath = pathlib.Path(__file__).parent.parent.joinpath("data")

def character_base_stats() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/characters/base-stats/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    table: bs4.Tag = soup.find_all("table")[1]

    rows: list[bs4.Tag] = table.find_all("tr")
    columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
    
    data = []
    for row in rows:
        if row.find("th") != None: continue
        
        row_data = {}
        for td_idx, td in enumerate(row.find_all("td")):
            value = str(td.text).strip()
            if value.isdigit():
                row_data[columns[td_idx]] = int(value)
            else:
                row_data[columns[td_idx]] = value
        
        data.append(row_data)
        
    return data

def character_growth_rates() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/characters/growth-rates/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    table: bs4.Tag = soup.find("table")
    
    rows: list[bs4.Tag] = table.find_all("tr")
    columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
    
    data = []
    for row in rows:
        if row.find("th") != None: continue
        
        row_data = {}
        for td_idx, td in enumerate(row.find_all("td")):
            value = str(td.text).strip()
            if value.isdigit():
                row_data[columns[td_idx]] = int(value)
            else:
                row_data[columns[td_idx]] = value
        
        data.append(row_data)
    
    return data

def character_other_data() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/characters/other-data/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    table: bs4.Tag = soup.find_all("table")[1]
    
    rows: list[bs4.Tag] = table.find_all("tr")
    columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
    
    data = []
    for row in rows:
        if row.find("th") != None: continue
        
        row_data = {}
        for td_idx, td in enumerate(row.find_all("td")):
            value = str(td.text).strip()
            if value.isdigit():
                row_data[columns[td_idx]] = int(value)
            else:
                row_data[columns[td_idx]] = value
        
        data.append(row_data)
    return data

def character_skills() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/characters/personal-skills/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    tables: typing.List[bs4.Tag] = soup.find_all("table")
    
    data = []
    
    table: bs4.Tag
    for table_idx, table in enumerate(tables):
        rows: list[bs4.Tag] = table.find_all("tr")
        columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
        
        is_engage = False if table_idx == 0 else True
            
        for row in rows:
            if row.find("th") != None: continue
            
            row_data = {}
            for td_idx, td in enumerate(row.find_all("td")):
                value = str(td.text).strip()
                
                if td.find("img"):
                    row_data[columns[td_idx]] = td.find("img").get("src")
                    continue
                
                if value.isdigit():
                    row_data[columns[td_idx]] = int(value)
                else:
                    row_data[columns[td_idx]] = value
            
            data.append(row_data)
    
    return data    

def learnable_skills() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/characters/learnable-skills/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    tables: typing.List[bs4.Tag] = soup.find_all("table")
    
    data = []
    
    table: bs4.Tag
    for table_idx, table in enumerate(tables):
        rows: list[bs4.Tag] = table.find_all("tr")
        columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
        for row in rows:
            if row.find("th") != None: continue
            
            row_data = {}
            for td_idx, td in enumerate(row.find_all("td")):
                value = str(td.text).strip()
                
                if td.find("img"):
                    row_data[columns[td_idx]] = td.find("img").get("src")
                    continue
                
                if value.isdigit():
                    row_data[columns[td_idx]] = int(value)
                else:
                    row_data[columns[td_idx]] = value
            
            data.append(row_data)
    
    for d in data:
        d["class"] = [s.strip() for s in d["class"].split(",")]
    
    return data


def _add_missing_keys(row_data:dict):
    for possible_key in ("mt","hit","crit","wt","rng","lvl","exp","uses"):
        if possible_key not in row_data.keys():
            row_data[possible_key] = None
            
    return row_data

class weapons:
    @staticmethod
    def swords() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/swords/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                        
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "sword"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def lances() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/lances/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "lance"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def axes() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/axes/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "axe"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def bows() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/bows/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "axe"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def knives() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/knives/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                    
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "knife"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def tomes() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/tomes/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "tome"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def staves() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/staves/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "stave"
                
                data.append(row_data)
        
        return data
    
    @staticmethod
    def arts() -> typing.List[typing.Dict]:
        r = requests.get("https://serenesforest.net/engage/weapons-items/arts/")
        soup = bs4.BeautifulSoup(r.text,"html.parser")
        
        tables: typing.List[bs4.Tag] = soup.find_all("table")
        
        data = []
        
        table: bs4.Tag
        for table_idx, table in enumerate(tables):
            rows: list[bs4.Tag] = table.find_all("tr")
            columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
            is_engage = False if table_idx == 0 else True
                
            for row in rows:
                if row.find("th") != None: continue
                
                row_data = {}
                for td_idx, td in enumerate(row.find_all("td")):
                    value = str(td.text).strip()
                    
                    if td.find("img"):
                        row_data[columns[td_idx]] = td.find("img").get("src")
                        continue
                    
                    if value.isdigit():
                        row_data[columns[td_idx]] = int(value)
                    else:
                        row_data[columns[td_idx]] = value
                
                row_data = _add_missing_keys(row_data)
                row_data["notes"] = row_data.pop("notes/description")
                row_data["is_engage"] = is_engage
                row_data["type"] = "art"
                
                data.append(row_data)
        
        return data


def items() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/weapons-items/items/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    tables: typing.List[bs4.Tag] = soup.find_all("table")
    
    data = []
    
    table: bs4.Tag
    for table_idx, table in enumerate(tables):
        rows: list[bs4.Tag] = table.find_all("tr")
        columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
        
        is_engage = False if table_idx == 0 else True
            
        for row in rows:
            if row.find("th") != None: continue
            
            row_data = {}
            for td_idx, td in enumerate(row.find_all("td")):
                value = str(td.text).strip()
                
                if td.find("img"):
                    row_data[columns[td_idx]] = td.find("img").get("src")
                    continue
                
                if value.isdigit():
                    row_data[columns[td_idx]] = int(value)
                else:
                    row_data[columns[td_idx]] = value
            
            row_data["is_engage"] = is_engage
            row_data["notes"] = row_data.pop("notes/description")
            
            data.append(row_data)
    
    return data

def materials() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/weapons-items/materials/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    tables: typing.List[bs4.Tag] = soup.find_all("table")
    
    data = []
    
    table: bs4.Tag
    for table_idx, table in enumerate(tables):
        rows: list[bs4.Tag] = table.find_all("tr")
        columns = [str(x.text).strip().lower() for x in rows[0].find_all("th")]
            
        for row in rows:
            if row.find("th") != None: continue
            
            row_data = {}
            for td_idx, td in enumerate(row.find_all("td")):
                value = str(td.text).strip()
                
                if td.find("img"):
                    row_data[columns[td_idx]] = td.find("img").get("src")
                    continue
                
                if value.isdigit():
                    row_data[columns[td_idx]] = int(value)
                else:
                    value = None if value.encode("utf-8") == b'\xe2\x80\x94' else value
                    row_data[columns[td_idx]] = value
            
            row_data["notes"] = row_data.pop("notes/description")
            
            data.append(row_data)
    
    return data
    
def ally_notebook() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/script/ally-notebook/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    h4_tags: typing.List[bs4.Tag] = soup.find_all("h4")
    
    data = []
    for h4_tag in h4_tags:
        data_name = h4_tag.text.strip()
        data_name = data_name.replace(ACCENT_E,'e')
        
        data_initial = {"class": None, "birthday": None, "basic_info": None}
        data_c = {"likes": None, "dislikes": None}
        data_b = {"hobbies": None, "talents": None, "background": None}
        data_a = {"height": None, "ring_size": None, "personality": None}
        data_s = {"life": None}
        
        table: bs4.Tag = h4_tag.find_next("table")
        tr_tag: typing.List[bs4.Tag] = table.find_all("tr")[1]
        td_tags: typing.List[bs4.Tag] = tr_tag.find_all("td")
        
        td_initial, td_c, td_b, td_a, td_s = td_tags

        for b_tag in td_initial.find_all("b"):
            if "class" in b_tag.text.lower():
                data_initial["class"] = b_tag.next_sibling.text.strip()
            elif "birthday" in b_tag.text.lower():
                data_initial["birthday"] = b_tag.next_sibling.text.strip()
            elif "info" in b_tag.text.lower():
                data_initial["basic_info"] = b_tag.next_sibling.text.strip()
                
        for b_tag in td_c.find_all("b"):
            _datalist = [s.strip() for s in b_tag.next_sibling.text.strip().split(",")]
            
            if "likes" in b_tag.text.lower() and "dislikes" not in b_tag.text.lower():
                data_c["likes"] = _datalist
            elif "dislikes" in b_tag.text.lower():
                data_c["dislikes"] = _datalist
                
        for b_tag in td_b.find_all("b"):
            if "hobbies" in b_tag.text.lower():
                _datalist = [s.strip() for s in b_tag.next_sibling.text.strip().split(",")]
                data_b["hobbies"] = _datalist
            elif "talents" in b_tag.text.lower():
                _datalist = [s.strip() for s in b_tag.next_sibling.text.strip().split(",")]
                data_b["talents"] = _datalist
            elif "background" in b_tag.text.lower():
                data_b["background"] = b_tag.next_sibling.text.strip()
                
        for b_tag in td_a.find_all("b"):
            _data = b_tag.next_sibling.text.strip()
            if "height" in b_tag.text.lower():
                data_a["height"] = _data
            elif "ring" in b_tag.text.lower():
                data_a["ring_size"] = _data
            elif "personality" in b_tag.text.lower():
                data_a["personality"] = _data
        
        for strong_tag in td_s.find_all("strong"):
            if "life with" in strong_tag.text.lower():
                data_s["life"] = strong_tag.next_sibling.text.strip(":").strip()

        data.append({
            "name": data_name,
            "initial": data_initial,
            "c_rank": data_c, "b_rank": data_b, "a_rank": data_a, "s_rank": data_s
        })
    
    return data
    

def _parse_stat_boosts(sb:str):
    ptrn = re.compile(r"(?P<type>\D{2,4}) \+(?P<boost>\d)")
    sb_list = [s.strip() for s in sb.split(",")]
    sb_list = [ptrn.search(s).groupdict() for s in sb_list]
    
    # stat_boost_list = []
    for sb in sb_list:
        sb["type"] = sb["type"].lower()
        sb["boost"] = int(sb["boost"])
    
    return sb_list

def bond_rings() -> typing.List[typing.Dict]:
    r = requests.get("https://serenesforest.net/engage/weapons-items/bond-rings/")
    soup = bs4.BeautifulSoup(r.text,"html.parser")
    
    world_name_tags = soup.find_all("h4")
    emblem_name_ptrn = re.compile(r"(?<=\()(.*)(?=\))")
    
    data = {}
    
    h4_tag: bs4.Tag
    for h4_tag in world_name_tags:
        emblem_name = emblem_name_ptrn.search(h4_tag.text).group()
        data[emblem_name] = {}
        world_data = {}
        table: bs4.Tag = h4_tag.find_next("table")
        rows: list[bs4.Tag] = table.find_all("tr")
        
        for row in rows:
            if row.find("th"): continue
            
            cells: typing.List[bs4.Tag] = row.find_all("td")
            
            if len(cells) == 4:
                bond_ring_name = cells[0].text.strip()
                rank = cells[1].text.strip()
                
                stat_boost = cells[2].text.strip()
                stat_boost = _parse_stat_boosts(stat_boost)
                
                bond_skill = cells[3].text.strip()
                bond_skill = None if bond_skill.encode("utf-8") == b'\xe2\x80\x94' else bond_skill
                
                world_data[f"{bond_ring_name}-{rank}"] = {"boost": stat_boost, "skill": bond_skill}
            elif len(cells) == 3:
                rank = cells[0].text.strip()
                
                stat_boost = cells[1].text.strip()
                stat_boost = _parse_stat_boosts(stat_boost)
                
                bond_skill = cells[2].text.strip()
                bond_skill = None if bond_skill.encode("utf-8") == b'\xe2\x80\x94' else bond_skill
                
                world_data[f"{bond_ring_name}-{rank}"] = {"boost": stat_boost, "skill": bond_skill}
        
        data[emblem_name] = world_data
    
    data_list = []
    emblem_val:dict
    bond_val:dict
    for emblem_key, emblem_val in data.items():
        for bond_key, bond_val in emblem_val.items():
            bond_name = bond_key[:-2]
            bond_rank = bond_key[-1]
            bond_skill: typing.Optional[str] = bond_val["skill"]
            
            new_data = {
                "emblem": emblem_key,
                "bond_ring": bond_name,
                "bond_rank": bond_rank,
                "bond_skill": bond_skill,
            }
            
            for stat in CHARACTER_STATS:
                new_data[stat] = None
            
            boosts: typing.List[typing.Dict] = bond_val["boost"]
            for boost in boosts:
                new_data[boost["type"]] = boost["boost"]
            
            data_list.append(new_data)
    
    return data_list

def _get_character_image_urls():
    data = {d["name"]: None for d in character_base_stats()}
    
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0"}
    
    with requests.session() as session:
        for character_name in data.keys():
            r = session.get(f"https://www.ign.com/wikis/fire-emblem-engage/{character_name}",headers=headers)
            soup = bs4.BeautifulSoup(r.text,"html.parser",parse_only=bs4.SoupStrainer("meta"))
            meta = soup.find("meta",attrs={"property":"og:image"})
            
            url = meta.get("content")
            data[character_name] = url
    
    with datapath.joinpath("engage","files","character_urls.json").open("w+") as fp:
        json.dump(data,fp)

def _get_character_images():
    with datapath.joinpath("engage","files","character_urls.json").open("r") as fp:
        data: typing.Dict = json.load(fp)

        for name, url in data.items():
            name = name.replace(ACCENT_E,"e")
            imgpath = datapath.joinpath("engage","images","characters",f"{name}.jpg")
            urllib.request.urlretrieve(url, imgpath)
