"Core Collision Module For Pygame Games"

import pygame as pg
import math

# Expects all images to be in a single dictionary with string keys
try:
    from Game.assets import assets
except:
    assets = {}


def clamp(
    minValue: int | float, value: int | float, maxValue: int | float
) -> int | float:
    return min(maxValue, max(minValue, value))


# -----------Base Class For All Classes -----------#


class CoreObject:

    def __init__(
        self, x: int, y: int, name: str, scale: int = 1, angle: int = 0
    ) -> None:
        self.name = name
        self.rect = assets[name].get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(assets[name])
        self.scale = scale
        self.angle = angle
        self.reload()

    def reload(self) -> None:
        self.scaledImage = pg.transform.scale_by(assets[self.name], self.scale)
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def rotate(self) -> None:
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0) -> None:
        window.blit(self.rotatedImage, (self.rect.x - x_offset, self.rect.y - y_offset))


# -----------Base Player Class For All Collision Classes----------- #


class CorePlayer(CoreObject):
    x_vel, y_vel = 0, 0
    maxSpeed = 5

    def script(self):
        self.x_vel, self.y_vel = 0, 0

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.y_vel -= self.maxSpeed
        if keys[pg.K_a]:
            self.x_vel -= self.maxSpeed     
        if keys[pg.K_s]:
            self.y_vel += self.maxSpeed       
        if keys[pg.K_d]:
            self.x_vel += self.maxSpeed

    def collide(self, objects):
        for _ in range(round(abs(self.x_vel))):
            self.rect.x += self.x_vel / abs(self.x_vel)
            for obj in objects:
                self = obj.resolveXCollision(self)

        for _ in range(round(abs(self.y_vel))):
            self.rect.y += self.y_vel / abs(self.y_vel)
            for obj in objects:
                self = obj.resolveYCollision(self)
        

# -----------Base Class For All Collision Classes----------- #


class Object(CoreObject):

    # Call this method after adding a player's x velocity / player's x velocity
    def resolveXCollision(self, player: CorePlayer) -> CorePlayer:
        if not pg.sprite.collide_mask(self, player):
            return player
        player.rect.x -= player.x_vel / abs(player.x_vel)
        return player


    # Call this method after adding a player's y velocity / player's y velocity
    def resolveYCollision(self, player: CorePlayer) -> CorePlayer:
        if not pg.sprite.collide_mask(self, player):
            return player
        player.rect.y -= player.y_vel / abs(player.y_vel)
        return player


# -----------Free Moving, Mouse Facing Player----------- #


class Player(CorePlayer):
    angle = 0
    speed = 0.0
    acceleration = 0.3
    rotateSpeed = 10

    def __init__(self, x: int, y: int, name: str, hitbox: pg.Rect | pg.Surface, correctionAngle: int = 0, scale: int = 1, angle: int = 0) -> None:
        """correctionAngle -> should make it so that when the
        object is rotated by that amount it faces up.\n
        hitbox -> either a image or a rect which is relative to the x and y,
        the hitbox will scale automaticaly"""
        # code order fix
        self.hitbox = None

        super().__init__(x, y, name, scale, angle)
        self.correctionAngle = correctionAngle
        
        # stable collision
        if isinstance(hitbox, pg.Surface):
            self.mask = pg.mask.from_surface(hitbox)
        else:
            hitbox.x *= scale
            hitbox.y *= scale
            hitbox.width *= scale
            hitbox.height *= scale
            image = pg.Surface((self.rect.width, self.rect.height)).convert_alpha()
            image.fill((0, 0, 0, 0))
            image.fill((255, 255, 255, 255), hitbox)
            self.mask = pg.mask.from_surface(image)
        self.hitbox: pg.mask.Mask = self.mask

    def reload(self) -> None:
        super().reload()
        self.mask = self.hitbox  

    def rotate(self) -> None:
        tempRect = self.rect
        super().rotate()
        self.mask = self.hitbox
        self.rect = tempRect    

    def setXYFromSpeed(self):
        radians = math.radians(self.angle - self.correctionAngle - 180)
        self.x_vel = math.sin(radians) * self.speed
        self.y_vel = math.cos(radians) * self.speed

    def script(self, x_offset: int = 0, y_offset: int = 0):

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.speed += self.acceleration
        elif keys[pg.K_s]:
            self.speed -= self.acceleration
        elif -0.5 < self.speed < 0.5: self.speed = 0
        elif self.speed < 0: self.speed += 1
        elif self.speed > 0: self.speed -= 1

        self.speed = clamp(-self.maxSpeed, self.speed, self.maxSpeed)

        mouseX, mouseY = pg.mouse.get_pos()
        mouseX += x_offset
        mouseY += y_offset

        # distance from mouse
        dx, dy = (
            mouseX - self.rect.centerx,
            self.rect.centery - mouseY,
        )

        self.angle = math.degrees(math.atan2(dy, dx)) - self.correctionAngle - 90

        self.rotate()

        self.setXYFromSpeed()
