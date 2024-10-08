import pygame as pg
import Game.assets

class School:
    "School Environment (level 1)"

    def __init__(self, resolution: tuple[int, int], fps: int = 60) -> None:

        # pygame window config
        self.height, self.width = resolution
        self.window = pg.display.set_mode(resolution)
        pg.display.set_caption("School")

        self.run = True
        self.clock = pg.time.Clock()
        self.fps = fps

    def event(self, event):
        if event.type == pg.QUIT:
            self.run = False

    def tick(self):
        self.clock.tick(self.fps)

    def display(self):
        self.window.fill((255, 255, 255))
        pg.display.update()

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.display()
        
