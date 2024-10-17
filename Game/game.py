"Core Game Functions & Classes"
from Game.collision import *
import pygame as pg
from Game.GUI import *
from Game.config import BaseConfig, configMap
from Game.functions import setAssetsToAlpha, loadData, saveData
from time import time
from copy import deepcopy

class CoreGame:
    "The Base Class For All Game Objects"

    def __init__(self, resolution: tuple[int, int], fps: int = 60) -> None:
        global assets

        # pygame window config
        self.width, self.height = resolution
        self.window = pg.display.set_mode(resolution)

        # conversion of all assets to alpha
        assets = setAssetsToAlpha(assets)

        self.run = True
        self.clock = pg.time.Clock()
        self.fps = fps

    def event(self, event):
        if event.type == pg.QUIT:
            self.run = False
            self.quit()

    def tick(self):
        self.clock.tick(self.fps)

    def display(self): ...

    def quit(self): ...

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.display()


class LevelEditor(CoreGame):
    def __init__(self, resolution: tuple[int, int], dataLocation: str, fps: int = 60, *imports) -> None:
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
                print(
                    "objectMap can be defined as objectMap = {name: object}, do NOT use objectMap = {name: object()}, do not call the init"
                )
                continue
            print(f"[Objects] Using {ObjImport} objects")

        super().__init__(resolution, fps)
        pg.display.set_caption("Level Editor")
        self.dataLocation  = dataLocation
        try:
            self.objects = loadData(self.dataLocation)
            for obj in self.objects:
                obj.unpack()
        except:
            self.objects = []
        self.selectedObj = None
        self.dupeCoolDown = 1
        self.TSdupeCoolDown = time()

        # creating buttons
        self.buttons = []
        startX = 0
        fontSize = 35
        pressedColor = (100, 100, 100)
        releasedColor = (0, 0, 0)
        for objName in objectMap:
            text = Text(
                objName,
                startX,
                self.height - fontSize,
                releasedColor,
                fontSize,
                "Arialblack",
            )
            pressedText = Text(
                objName,
                startX,
                self.height - fontSize,
                pressedColor,
                fontSize,
                "Arialblack",
            )
            self.buttons.append(
                Button((startX, 0), text.image, pressedText.image, objName)
            )
            startX += text.rect.width

        self.data = {"Button Menu Bottom": fontSize * 2}

        self.configMenu = None

        self.x_offset, self.y_offset = 0, 0

        self.moveCoolDown = 4
        self.timeSinceMoveCoolDown = 0

    def quit(self):
        for obj in self.objects:
            obj.pack()
        saveData(self.objects, self.dataLocation)

    def display(self):
        self.window.fill((255, 255, 255))

        for obj in self.objects:
            obj.display(self.window, self.x_offset, self.y_offset)

        for button in self.buttons:
            button.display(self.window)

        if self.configMenu is not None:
            self.configMenu.display(self.window)

        pg.display.update()

    def keydown(self, event):
        if event.key == pg.K_DELETE and self.selectedObj is not None:
            self.objects.remove(self.selectedObj)
            self.selectedObj = None
        if self.selectedObj is None:
            return
        if event.key == pg.K_LEFT:
            self.selectedObj.rect.x -= 1
        if event.key == pg.K_RIGHT:
            self.selectedObj.rect.x += 1        
        if event.key == pg.K_UP:
            self.selectedObj.rect.y -= 1        
        if event.key == pg.K_DOWN:
            self.selectedObj.rect.y += 1

    def selectObj(self):
        x, y = pg.mouse.get_pos()
        pos = MouseClick(x+self.x_offset, y+self.y_offset)
        for obj in self.objects:
            if pg.sprite.collide_mask(obj, pos):
                self.selectedObj = obj
                try:
                    self.configMenu = configMap[obj.type](
                        obj, 0, self.data["Button Menu Bottom"]
                    )
                except:
                    self.configMenu = BaseConfig(
                        obj, 0, self.data["Button Menu Bottom"]
                    )
                break

    def event(self, event):
        super().event(event)
        if self.configMenu is not None:
            self.configMenu.event(event)
        if event.type == pg.KEYDOWN:
            self.keydown(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            self.selectedObj = None
            for button in self.buttons:
                if button.pressed(event):
                    self.objects.append(
                        self.objectMap[button.info](
                            self.width / 2, self.height / 2, "Crate"
                        )
                    )
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
        elif mouseDown[2]:
            self.x_offset -= mouseRelX
            self.y_offset -= mouseRelY
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL] and keys[pg.K_d] and self.selectedObj is not None and time() - self.TSdupeCoolDown > self.dupeCoolDown:
            self.selectedObj.pack()
            self.objects.append(deepcopy(self.selectedObj))
            self.objects[-1].unpack()
            self.selectedObj.unpack()
            self.TSdupeCoolDown = time()
