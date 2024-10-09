"Core Game Functions & Classes"
from Game.collision import *
import pygame as pg
from Game.GUI import *
from Game.config import ObjectConfig

class CoreGame:
    "The Base Class For All Game Objects"

    def __init__(self, resolution: tuple[int, int], fps: int = 60) -> None:

        # pygame window config
        self.height, self.width = resolution
        self.window = pg.display.set_mode(resolution)

        self.run = True
        self.clock = pg.time.Clock()
        self.fps = fps


    def event(self, event):
        if event.type == pg.QUIT:
            self.run = False

    def tick(self):
        self.clock.tick(self.fps)

    def display(self): ...

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.display()


class LevelEditor(CoreGame):
    def __init__(self, resolution: tuple[int, int], fps: int = 60, *imports) -> None:
        "*imports -> add the names of the modules you want to import from"

        self.objectMap = objectMap

        # Importing all wanted objects
        print("[Objects] Using collision.py objects")
        for ObjImport in imports:
            try:
                exec(f"import {ObjImport}")
                exec(f"self.objectMap.update({ObjImport}.objectMap)")
            except:
                print(f"[Objects] Failed to use {ObjImport} (No objectMap)")
                print("objectMap can be defined as objectMap = {name: object}, do NOT use objectMap = {name: object()}, do not call the init")
                continue
            print(f"[Objects] Using {ObjImport} objects")

        super().__init__(resolution, fps)
        pg.display.set_caption("Level Editor")
        self.objects = []
        self.selectedObj = None

        # creating buttons
        self.buttons = []
        startX = 0
        fontSize = 35
        pressedColor = (100, 100, 100)
        releasedColor = (0, 0, 0)
        for objName in objectMap:
            text = Text(objName, startX, self.height - fontSize, releasedColor, fontSize, "Arialblack")
            pressedText = Text(objName, startX, self.height - fontSize, pressedColor, fontSize, "Arialblack")
            self.buttons.append(Button((startX, 0), text.image, pressedText.image, objName))
            startX += text.rect.width

        self.data = {"Button Menu Bottom": fontSize*2}

        self.configMenu = None

    def display(self):
        self.window.fill((255, 255, 255))

        for obj in self.objects:
            obj.display(self.window)

        for button in self.buttons:
            button.display(self.window)

        if self.configMenu is not None:
            self.configMenu.display(self.window)

        pg.display.update()

    def selectObj(self):
        for i, obj in enumerate(self.objects):
            if obj.rect.collidepoint(pg.mouse.get_pos()):
                self.selectedObj = obj
                self.configMenu = ObjectConfig(obj, 0, self.data["Button Menu Bottom"])
                break

    def event(self, event):
        super().event(event)
        if self.configMenu is not None:
            self.configMenu.event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.pressed(event):
                    self.objects.append(self.objectMap[button.info](self.width/2, self.height/2, "Crate"))
                    break
            else:
                self.selectObj()
        if event.type == pg.MOUSEBUTTONUP:
            for button in self.buttons:
                button.released()

    def tick(self):
        super().tick()
        if self.configMenu is not None:
            self.configMenu.script()
        mouseDown = pg.mouse.get_pressed()
        mouseRelX, mouseRelY = pg.mouse.get_rel()
        if True in mouseDown and self.selectedObj is not None:
            self.selectedObj.rect.x += mouseRelX
            self.selectedObj.rect.y += mouseRelY



    