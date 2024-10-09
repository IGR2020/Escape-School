"Core Assets Loading File For Pygame Games"

from Game.functions import load_assets

GUI_scale = 1

assets = load_assets("Game/assets")
assets.update(load_assets("Game/assets/GUI", scale=GUI_scale))
assets.update(load_assets("Game/assets/objects"))

fontLocation = "Game/assets/fonts/"