import json
import typing
import pathlib
import sqlite3

from . import fetch
from . import typed_rows
from .helpers import ACCENT_E

engage_datapath = pathlib.Path(__file__).parent.parent.joinpath("data","engage")

#####################################################
# SQLite adapters and converters and connections
#####################################################
def adapt_json(_json:typing.Union[list,dict]):
    return str(_json)
def convert_json(s:bytes):
    # s = repr(s.decode("utf-8"))
    # s = s.replace("'",'"')
    s = s.decode("utf-8").replace("'",'"')
    return json.loads(s)
sqlite3.register_adapter(dict, adapt_json)
sqlite3.register_adapter(list, adapt_json)
sqlite3.register_converter("JSON", convert_json)

def dict_factory(cursor, row):
    colnames = [c[0] for c in cursor.description]
    return {k:v for k,v in zip(colnames, row)}

def db_connection():
    dbpath = engage_datapath.joinpath("engage.db")
    conn = sqlite3.connect(dbpath,detect_types=sqlite3.PARSE_COLNAMES|sqlite3.PARSE_DECLTYPES)
    conn.row_factory = dict_factory
    return conn
#####################################################
#####################################################

def _keyify(s:str):
    return s.replace("+","").replace("!","").replace("?","").replace("-","_").replace(" ","_").lower().strip()

def character_base_stats_table():
    data = fetch.character_base_stats()
    for d in data: d["name"] = d["name"].replace(ACCENT_E,"e")
        
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS CharacterBaseStats
            """
        )
        c.execute(
            """
            CREATE TABLE CharacterBaseStats (
                name TEXT,
                level INTEGER,
                class TEXT,
                hp INTEGER,
                str INTEGER,
                mag INTEGER,
                dex INTEGER,
                spd INTEGER,
                def INTEGER,
                res INTEGER,
                lck INTEGER,
                bld INTEGER,
                mov INTEGER
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO CharacterBaseStats ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()

def character_base_stats() -> typing.List[typed_rows._CharacterBaseStat]:
    """
    Get character base stats.
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM CharacterBaseStats")
        return c.fetchall()
        

        
def character_growth_rates_table():
    data = fetch.character_growth_rates()
    for d in data: d["name"] = d["name"].replace(ACCENT_E,"e")
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS CharacterGrowthRates
            """
        )
        c.execute(
            """
            CREATE TABLE CharacterGrowthRates (
                name TEXT,
                hp INTEGER,
                str INTEGER,
                mag INTEGER,
                dex INTEGER,
                spd INTEGER,
                def INTEGER,
                res INTEGER,
                lck INTEGER,
                bld INTEGER,
                mov INTEGER
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO CharacterGrowthRates ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()
        
def character_growth_rates() -> typing.List[typed_rows._CharacterGrowthRate]:
    """
    Get character growth rates. (Numbers should be added to the character base stats)
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM CharacterGrowthRates")
        return c.fetchall()


        
def character_other_data_table():
    data = fetch.character_other_data()
    for d in data: d["name"] = d["name"].replace(ACCENT_E,"e")
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS CharacterOtherData
            """
        )
        c.execute(
            """
            CREATE TABLE CharacterOtherData (
                name TEXT,
                age TEXT,
                gender TEXT,
                birthday TEXT,
                proficiency TEXT,
                sp INTEGER
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO CharacterOtherData ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()

def character_other_data() -> typing.List[typed_rows._CharacterOtherData]:
    """
    Get additional details for each character
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM CharacterOtherData")
        return c.fetchall()
        
        
        
def character_skills_table():
    data = fetch.character_skills()
    for d in data: 
        d["name"] = d["name"].replace(ACCENT_E,"e")
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS CharacterSkills
            """
        )
        c.execute(
            """
            CREATE TABLE CharacterSkills (
                name TEXT,
                key TEXT,
                character TEXT,
                description TEXT,
                icon_url TEXT
            )
            """
        )
        
        for d in data:
            icon_url:str = d["icon"]
            # icon_key = icon_url[icon_url.rfind("/")+1:].strip(".png")
            icon_key = _keyify(d["name"])
            d["character"] = d["character"].replace(ACCENT_E,"e")
            row_data = {"name": d["name"], "character": d["character"], "key": icon_key, "description": d["description"], "icon_url": icon_url}
            c.execute(
                """
                INSERT INTO CharacterSkills (name, key, character, description, icon_url) 
                VALUES (:name, :key, :character, :description, :icon_url);
                """,
                row_data
            )
            
        
        conn.commit()

def character_skills() -> typing.List[typed_rows._CharacterSkill]:
    """
    Get skill details for each character
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM CharacterSkills")
        return c.fetchall()
    


def learnable_skills_table():
    data = fetch.learnable_skills()
        
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS LearnableSkills
            """
        )
        c.execute(
            """
            CREATE TABLE LearnableSkills (
                name TEXT,
                key TEXT,
                class JSON,
                description TEXT,
                icon_url TEXT
            )
            """
        )
        
        for d in data:
            icon_url:str = d["icon"]
            # icon_key = icon_url[icon_url.rfind("/")+1:].strip(".png")
            icon_key = _keyify(d["name"])
            # if "Fell" in str(d['class']):
                # print(d['class'])
            d["class"] = [_class.replace("'","\u2017") for _class in d["class"]]
            row_data = {"name": d["name"], "class": d["class"], "key": icon_key, "description": d["description"], "icon_url": icon_url}
            c.execute(
                """
                INSERT INTO LearnableSkills (name, key, class, description, icon_url) 
                VALUES (:name, :key, :class, :description, :icon_url);
                """,
                row_data
            )
        
        conn.commit()

def learnable_skills() -> typing.List[typed_rows._LearnableSkill]:
    """
    Get learnable skill details
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM LearnableSkills")
        return c.fetchall()



def bond_rings_table():
    data = fetch.bond_rings()
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS BondRings
            """
        )
        c.execute(
            """
            CREATE TABLE BondRings (
                emblem TEXT,
                bond_ring TEXT,
                bond_rank TEXT,
                bond_skill TEXT,
                hp INTEGER,
                str INTEGER,
                mag INTEGER,
                dex INTEGER,
                spd INTEGER,
                def INTEGER,
                res INTEGER,
                lck INTEGER,
                bld INTEGER,
                mov INTEGER
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO BondRings ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()

def bond_rings(emblem:str=None,rank:str=None) -> typing.List[typed_rows._BondRing]:
    """
    Get details for each Emblem's Bond Rings
    """
    with db_connection() as conn:
        c = conn.cursor()
        
        querylist = []
        values = []
        if emblem:
            querylist.append("emblem=?")
            values.append(emblem.capitalize())
        if rank:
            querylist.append("bond_rank=?")
            values.append(rank.upper())
        
        if len(querylist) > 0:
            queries = " AND ".join(querylist)
            c.execute(f"SELECT * FROM BondRings WHERE {queries};",values)
        else:
            c.execute("SELECT * FROM BondRings;")
        
        return c.fetchall()
    


def weapons_table():
    data = []
    for funcname in ("swords","lances","axes","bows","knives","tomes","staves","arts"):
        func = getattr(fetch.weapons,funcname)
        weapon_data = func()
        data.extend(weapon_data)
    
    for d in data:
        d["icon_url"] = d.pop("icon")
        d["rng"] = str(d["rng"]).replace("~","-")
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS Weapons
            """
        )
        c.execute(
            """
            CREATE TABLE Weapons (
                name TEXT,
                icon_url TEXT,
                mt INTEGER,
                hit INTEGER,
                crit INTEGER,
                wt INTEGER,
                rng TEXT,
                lvl TEXT,
                exp INTEGER,
                uses TEXT,
                price INTEGER,
                notes TEXT,
                is_engage INTEGER,
                type TEXT
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO Weapons ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()
        
def weapons(weapon_name:str=None,weapon_type:str=None,is_engage:bool=None) -> typing.List[typed_rows._Weapon]:
    """
    Get weapon stats (includes engage weapons)
    """
    with db_connection() as conn:
        c = conn.cursor()
        
        querylist = []
        values = []
        if weapon_name:
            querylist.append("name=?")
            values.append(weapon_name)
        if weapon_type:
            querylist.append("type=?")
            values.append(weapon_type)
        if is_engage != None:
            querylist.append("is_engage=?")
            values.append(is_engage)
        
            
        if len(querylist) > 0:
            queries = " AND ".join(querylist)
            c.execute(f"SELECT * FROM Weapons WHERE {queries};",values)
        else:
            c.execute("SELECT * FROM Weapons;")
        
        return c.fetchall()
    
   
 
def items_table():
    data = fetch.items()
    for d in data:
        d["icon_url"] = d.pop("icon")
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS Items
            """
        )
        c.execute(
            """
            CREATE TABLE Items (
                name TEXT,
                icon_url TEXT,
                uses TEXT,
                price INTEGER,
                notes TEXT,
                is_engage INTEGER
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO Items ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()

def items() -> typing.List[typed_rows._Item]:
    """
    Get item data (includes engage items)
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM Items")
        return c.fetchall()
    


def materials_table():
    data = fetch.materials()
    for d in data:
        d["icon_url"] = d.pop("icon")
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS Materials
            """
        )
        c.execute(
            """
            CREATE TABLE Materials (
                name TEXT,
                icon_url TEXT,
                uses INTEGER,
                price INTEGER,
                notes TEXT
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO Materials ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()
        
def materials() -> typing.List[typed_rows._Material]:
    """
    Get data for different materials
    """
    with db_connection() as conn:
        c = conn.execute("SELECT * FROM Materials")
        return c.fetchall()
    


def ally_notebook_table():
    data = fetch.ally_notebook()
    for d in data:
        for key in typed_rows.initial.__annotations__.keys():
            if isinstance(d["initial"][key],list):
                d["initial"][key] = [s.replace("'",'"') for s in d["initial"][key]]
            elif isinstance(d["initial"][key],str):
                d["initial"][key] = d["initial"][key].replace("'",'"')
        
        for key in typed_rows.c_rank.__annotations__.keys():
            if isinstance(d["c_rank"][key],list):
                d["c_rank"][key] = [s.replace("'",'"') for s in d["c_rank"][key]]
            elif isinstance(d["c_rank"][key],str):
                d["c_rank"][key] = d["c_rank"][key].replace("'",'"')
                
        for key in typed_rows.b_rank.__annotations__.keys():
            if isinstance(d["b_rank"][key],list):
                d["b_rank"][key] = [s.replace("'",'"') for s in d["b_rank"][key]]
            elif isinstance(d["b_rank"][key],str):
                d["b_rank"][key] = d["b_rank"][key].replace("'",'"')
                
        for key in typed_rows.a_rank.__annotations__.keys():
            if isinstance(d["a_rank"][key],list):
                d["a_rank"][key] = [s.replace("'",'"') for s in d["a_rank"][key]]
            elif isinstance(d["a_rank"][key],str):
                d["a_rank"][key] = d["a_rank"][key].replace("'",'"')
                
        for key in typed_rows.s_rank.__annotations__.keys():
            if isinstance(d["s_rank"][key],list):
                d["s_rank"][key] = [s.replace("'",'"') for s in d["s_rank"][key]]
            elif isinstance(d["s_rank"][key],str):
                d["s_rank"][key] = d["s_rank"][key].replace("'",'"')
    
    with db_connection() as conn:
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS AllyNotebook
            """
        )
        c.execute(
            """
            CREATE TABLE AllyNotebook (
                name TEXT,
                initial JSON,
                c_rank JSON,
                b_rank JSON,
                a_rank JSON,
                s_rank JSON
            )
            """
        )
        
        column_labels = ",".join([c for c in data[0].keys()])
        insert_labels = ",".join([f":{c}" for c in data[0].keys()])
        
        c.executemany(f"INSERT INTO AllyNotebook ({column_labels}) VALUES({insert_labels})",data)
        
        conn.commit()

def ally_notebook(character_name:str=None) -> typing.List[typed_rows._AllyNotebookEntry]:
    """
    Get ally support data
    """
    character_name = character_name.replace(ACCENT_E,"e")
    with db_connection() as conn:
        c = conn.cursor()
        
        querylist = []
        values = []
        if character_name:
            querylist.append("name=?")
            values.append(character_name)
            
        if len(querylist) > 0:
            queries = " AND ".join(querylist)
            c.execute(f"SELECT * FROM AllyNotebook WHERE {queries};",values)
        else:
            c.execute("SELECT * FROM AllyNotebook;")
        
        return c.fetchall()