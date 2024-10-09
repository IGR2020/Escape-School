"Core Assets Loading File For Pygame Games"

from Game.functions import load_assets
import pygame as pg

GUI_scale = 1

assets = load_assets("Game/assets")
assets.update(load_assets("Game/assets/GUI", scale=GUI_scale))
assets.update(load_assets("Game/assets/objects"))
assets["Flat Black"] = pg.Surface((1, 1))
assets["Flat Black"].fill((0, 0, 0))

fontLocation = "Game/assets/fonts/"