"Core Functions For Pygame Games"

import pygame as pg
from os import listdir
from os.path import isfile, isdir, join
import json


def blit_text(
    win,
    text,
    pos,
    colour=(0, 0, 0),
    size=30,
    font="arialblack",
    blit=True,
    centerx=False,
    centery=False,
    center=False,
):
    text = str(text)
    x, y = pos
    font_style = pg.font.SysFont(font, size)
    text_surface = font_style.render(text, True, colour)
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    else:
        if centerx:
            x -= text_surface.get_width() // 2
        if centery:
            y -= text_surface.get_height() // 2
    if blit:
        win.blit(text_surface, (x, y))
    return text_surface


def load_assets(path, size: int = None, scale: float = None, getSubDirsAsList=False, scaleifsize=None):
    sprites = {}
    for file in listdir(path):
        if getSubDirsAsList and isdir(join(path, file)):
            sprites[file.replace(".png", "")] = load_assets_list(
                join(path, file), size, scale
            )
            continue
        elif not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites[file.replace(".png", "")] = pg.image.load(join(path, file))
        elif scale is not None:
            image = pg.image.load(join(path, file))
            if scaleifsize and image.get_size() != scaleifsize:
                  sprites[file.replace(".png", "")] = image
                  continue
            sprites[file.replace(".png", "")] = pg.transform.scale_by(
                image, scale
            )
        else:
            sprites[file.replace(".png", "")] = pg.transform.scale(
                pg.image.load(join(path, file)), size
            )
    return sprites


def load_assets_list(path, size: int = None, scale: float = None):
    sprites = []
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites.append(pg.image.load(join(path, file)))
        elif scale is not None:
            sprites.append(
                pg.transform.scale_by(pg.image.load(join(path, file)), scale)
            )
        else:
            sprites.append(pg.transform.scale(pg.image.load(join(path, file)), size))
    return sprites


def loadJson(path):
    with open(path) as file:
        data = json.load(file)
        file.close()
    return data