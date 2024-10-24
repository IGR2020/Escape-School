"GUI For Pygame Games"

import pygame as pg
from Game.assets import *

mouseButtonMap = {"left": 1, "middle": 2, "right": 3}

pg.font.init()

class Button:

    def __init__(self, pos, releasedImage: str | pg.Surface, pressedImage: str | pg.Surface, *args):

        # conversion of images to pygame.Surface
        if isinstance(releasedImage, str):
            releasedImage = assets[releasedImage]
        if isinstance(pressedImage, str):
            pressedImage = assets[pressedImage]

        # creating rect
        x, y = pos
        width, height = (
            releasedImage.get_width(),
            releasedImage.get_height(),
        )
        self.rect = pg.Rect(x, y, width, height)

        # setting pressed state
        self.releasedImage = releasedImage
        self.pressedImage = pressedImage

        # associated info
        if len(args) == 1:
            self.info = args[0]
        else:
            self.info = args

        # clicking
        self.is_pressed = False
        self.height_diffrence = (
            self.releasedImage.get_height() - self.pressedImage.get_height()
        )

        self.type = "Button"

    def display(self, window: pg.Surface, background=None):
        """
        background can be any RGB value
        """
        if background is not None:
            pg.draw.rect(window, background, self.rect)
        if self.is_pressed:
            window.blit(self.pressedImage, self.rect)
        else:
            window.blit(self.releasedImage, self.rect)

    def pressed(self, event, pos=None, clicked_button: int | str = None) -> bool:
        "Call inside of event loop inside if if event.type == pygame.MOUSEBUTTONDOWN:"
        if isinstance(clicked_button, str):
            clicked_button = mouseButtonMap[clicked_button.lower()]
        if clicked_button is not None:
            if event.button != clicked_button:
                return False
        if pos is None:
            pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos) and event.button in (1, 2, 3):
            self.is_pressed = True
            self.rect.y += self.height_diffrence
            return True
        return False
        

    def released(self) -> bool:
        "Call inside of event loop inside if if event.type == pygame.MOUSEBUTTONUP:"
        if self.is_pressed:
            self.rect.y -= self.height_diffrence
            self.is_pressed = False
            return True
        return False


class Text:
    def __init__(self, text, x, y, color, size, font,  center=False, centerx=False, centery=False) -> None:

        # saving reconstruction data
        self.text = str(text)
        self.color = color
        self.size = size
        self.font = font

        # creating text surface
        font_style = pg.font.Font(fontLocation + self.font + ".ttf", self.size)
        text_surface = font_style.render(self.text, True, self.color)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2
        else:
            if centerx:
                x -= text_surface.get_width() // 2
            if centery:
                y -= text_surface.get_height() // 2

        self.image = text_surface
        self.rect = text_surface.get_rect(topleft=(x, y))
        
        self.type = "Text"

    
    def reload(self, reloadRect=True):
        font_style = pg.font.Font(fontLocation + self.font + ".ttf", self.size)
        text_surface = font_style.render(self.text, True, self.color)

        self.image = text_surface

        if reloadRect:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)        

    def display(self, window):
        window.blit(self.image, self.rect)

class TextBox():
    def __init__(self,  imageName, selectedImageName, border: tuple[int, int] | int, x, y, color, size, font, text="", center=False) -> None:
        
        # saving reconstruction data
        super().__init__()
        self.text = str(text)
        self.color = color
        self.size = size
        self.font = font


        self.boxImage = imageName
        self.selectedBoxName = selectedImageName

        if isinstance(border, int):
            self.border = (border, border)   
        else:         
            self.border = border

        if center:
            self.rect = assets[self.boxImage].get_rect(center=(x, y))
        else:            
            self.rect = assets[self.boxImage].get_rect(topleft=(x, y))

        self.image = None
        Text.reload(self, False)

        self.selected = False
        self.type = "TextBox"

    def reload(self):
        Text.reload(self, False)

    def display(self, window):
        if self.selected:
            window.blit(assets[self.selectedBoxName], self.rect)
        else:            
            window.blit(assets[self.boxImage], self.rect)
        window.blit(self.image, (self.rect.x + self.border[0], self.rect.y + self.border[1]))

    def select(self, pos=None, clicked_button=None) -> bool:
        if pos is None:
            pos = pg.mouse.get_pos()
        x, y = pos
        mouseDown = pg.mouse.get_pressed()
        if clicked_button is None:
            if True in mouseDown:
                mouseDown = True
            else:
                mouseDown = False
        else:
            mouseDown = mouseDown[clicked_button]

        if self.rect.collidepoint((x, y)) and mouseDown:
            self.selected = True
        elif not self.rect.collidepoint((x, y)) and mouseDown:
            self.selected = False
            self.reload()

        return self.selected
    
    def update_text(self, event):
        """Call inside event loop"""
        if event.type != pg.KEYDOWN or not self.selected:
            return
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            self.text += "|"
        elif event.unicode == "\r":
            self.selected = False
            self.text += "|"
        else:
            self.text += event.unicode
            self.text += "|"
        self.reload()
        self.text = self.text[:-1]