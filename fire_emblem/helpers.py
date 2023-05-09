import pathlib

from .fe_engage.fetch import datapath

def engage_character_image(name:str):
    imgpath = datapath.joinpath("engage","images",f"{name}.jpg")
    return str(imgpath.resolve())