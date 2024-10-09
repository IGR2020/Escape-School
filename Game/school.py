import pygame as pg
from Game.collision import * 
from Game.functions import setAssetsToAlpha
from Game.game import CoreGame

class School(CoreGame):
    "School Environment (level 1)"

    def __init__(self, resolution: tuple[int, int], fps: int = 60) -> None:
        super().__init__(resolution, fps)
        pg.display.set_caption("School")

        self.player = Player(self.width/2, self.height/2, "Player", pg.Rect(0, 0, 40, 5), scale=4)
        self.objects = []

        self.x_offset, self.y_offset = 0, 0


    def event(self, event) -> None:
        super().event(event)

    def tick(self) -> None:
        super().tick()

        self.player.script(self.x_offset, self.y_offset)
        self.player.collide(self.objects)

    def display(self) -> None:
        self.window.fill((255, 255, 255))

        self.player.display(self.window, self.x_offset, self.y_offset)

        pg.display.update()

    def start(self) -> None:
        super().start()
