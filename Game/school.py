import pygame as pg
from Game.collision import * 
from Game.functions import setAssetsToAlpha, loadData, saveData
from Game.game import CoreGame

class School(CoreGame):
    "School Environment (level 1)"

    def __init__(self, resolution: tuple[int, int], dataLocation: str, fps: int = 60) -> None:
        super().__init__(resolution, fps)
        pg.display.set_caption("School")

        self.player = Player(self.width/2, self.height/2, "Player", assets["Player Hitbox"], scale=2)
        self.dataLocation  = dataLocation
        try:
            self.objects = loadData(self.dataLocation)
            for obj in self.objects:
                obj.unpack()
        except:
            self.objects = []

        self.x_offset, self.y_offset = 0, 0


    def event(self, event) -> None:
        super().event(event)

        self.player.eventControls(event)

    def tick(self) -> None:
        super().tick()

        self.player.script(self.x_offset, self.y_offset)
        self.player.collide(self.objects)

        self.x_offset, self.y_offset = (self.player.rect.centerx - self.width/2, self.player.rect.centery - self.height/2)

    def display(self) -> None:
        self.window.fill((255, 255, 255))

        for obj in self.objects:
            if obj.type == "Chair":
                obj.display(self.window, self.x_offset, self.y_offset)

        self.player.display(self.window, self.x_offset, self.y_offset)

        for obj in self.objects:
            if obj.type == "Chair":
                continue      
            obj.display(self.window, self.x_offset, self.y_offset)

        pg.display.update()

    def start(self) -> None:
        super().start()
