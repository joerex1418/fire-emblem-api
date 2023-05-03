import typing


_CharacterBaseStat = typing.TypedDict("_CharacterBaseStat",{
    "name": str,
    "hp": int,
    "str": int,
    "mag": int,
    "dex": int,
    "spd": int,
    "def": int,
    "res": int,
    "lck": int,
    "bld": int,
    "mov": int,
    })

_CharacterGrowthRate = typing.TypedDict("_CharacterGrowthRate",{
    "name": str,
    "hp": int,
    "str": int,
    "mag": int,
    "dex": int,
    "spd": int,
    "def": int,
    "res": int,
    "lck": int,
    "bld": int
    })

_BondRing = typing.TypedDict("_BondRing",{
    "emblem": str,
    "bond_ring": str,
    "bond_rank": str,
    "bond_skill": str,
    "hp": int,
    "str": int,
    "mag": int,
    "dex": int,
    "spd": int,
    "def": int,
    "res": int,
    "lck": int,
    "bld": int,
    "mov": int,
    })

_Weapon = typing.TypedDict("_Weapon",{
    "name": str,
    "icon_url": str,
    "mt": int,
    "hit": int,
    "crit": int,
    "wt": int,
    "rng": int,
    "lvl": str,
    "price": int,
    "notes": str,
    "is_engage": bool,
    "type": str,
    })

class _Item(typing.TypedDict):
    name: str
    uses: typing.Optional[typing.Union[str,int]]
    price: int
    notes: str
    is_engage: bool
    
class _Material(typing.TypedDict):
    name: str
    uses: typing.Optional[int]
    price: int
    notes: str

class _CharacterOtherData(typing.TypedDict):
    name: str
    age: str
    gender: str
    birthday: str
    proficiency: str
    sp: int

_CharacterSkill = typing.TypedDict("_CharacterSkill",{
    "name": str,
    "key": str,
    "character": str,
    "description": str,
    })
    
_LearnableSkill = typing.TypedDict("_LearnableSkill",{
    "name": str,
    "key": str,
    "class": typing.List[str],
    "description": str,
    })

initial = typing.TypedDict("initial",{"class":str,"birthday":str,"basic_info":str})
c_rank = typing.TypedDict("c_rank",{"likes":typing.List[str],"dislikes":typing.List[str]})
b_rank = typing.TypedDict("b_rank",{"hobbies":typing.List[str],"talents":typing.List[str],"background":str})
a_rank = typing.TypedDict("a_rank",{"height":str,"ring_size":str,"personality":str})
s_rank = typing.TypedDict("s_rank",{"life":str})
_AllyNotebookEntry = typing.TypedDict("_AllyNotebookEntry",{
    "name": str,
    "initial": initial,
    "c_rank": c_rank,
    "b_rank": b_rank,
    "a_rank": a_rank,
    "s_rank": s_rank,
    })
