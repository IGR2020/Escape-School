import pygame as pg
import Game.assets
from Game.collision import * 

class School:
    "School Environment (level 1)"

    def __init__(self, resolution: tuple[int, int], fps: int = 60) -> None:

        # pygame window config
        self.height, self.width = resolution
        self.window = pg.display.set_mode(resolution)
        pg.display.set_caption("School")

        # conversion of all assets to alpha
        for asset in assets:
            assets[asset] = assets[asset].convert_alpha()

        self.run = True
        self.clock = pg.time.Clock()
        self.fps = fps

        self.player = Player(self.width/2, self.height/2, "Door", pg.Rect(0, 0, 40, 5), scale=4)
        self.objects = []

        self.x_offset, self.y_offset = 0, 0

    def event(self, event):
        if event.type == pg.QUIT:
            self.run = False

    def tick(self):

        self.clock.tick(self.fps)

        self.player.script(self.x_offset, self.y_offset)
        self.player.collide(self.objects)

    def display(self):
        self.window.fill((255, 255, 255))

        self.player.display(self.window, self.x_offset, self.y_offset)

        pg.display.update()

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.display()
        
