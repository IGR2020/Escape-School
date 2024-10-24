"""Core Collision Module For Pygame Games"""
import time

import  pygame as pg
import math

# Expects all images to be in a single dictionary with string keys
try:
    from Game.assets import assets
except:
    assets = {}

# objectMap defined at bottom of file

def clamp(
    minValue: int | float, value: int | float, maxValue: int | float
) -> int | float:
    return min(maxValue, max(minValue, value))


# -----------Base Class For All Classes -----------#


class CoreObject:

    def __init__(
        self, x: int, y: int, name: str, scale: int = 1, angle: int = 0, size: tuple[int, int] | list[int, int] = None
    ) -> None:
        self.name = name
        self.rect: pg.Rect = assets[name].get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(assets[name])
        self.scale = scale
        self.angle = angle
        if size is None:
            self.size = self.rect.width, self.rect.height
        else:
            self.size = size
        self.size = [self.size[0], self.size[1]]
        self.reload()
        self.type = "Object"

    def resetSize(self) -> None:
        self.size = [assets[self.name].get_width(), assets[self.name].get_height()]

    def reload(self) -> None:
        self.morphedImage = pg.transform.scale(assets[self.name], self.size)
        self.scaledImage = pg.transform.scale_by(self.morphedImage, self.scale)
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def rotate(self) -> None:
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0) -> None:
        window.blit(self.rotatedImage, (self.rect.x - x_offset, self.rect.y - y_offset))

    def pack(self):
        self.morphedImage, self.scaledImage, self.rotatedImage, self.mask = None, None, None, None

    def unpack(self):
        self.reload()


# -----------Base Player Class For All Collision Classes----------- #


class CorePlayer(CoreObject):
    x_vel, y_vel = 0, 0
    maxSpeed = 5
    isSitting = True
    satUp = False
    satUpCoolDown = 0.5
    timeSinceSatUp = 0

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

    def eventControls(self, event):
        if not event.type == pg.KEYDOWN:
            return
        if event.key == pg.K_LSHIFT:
            self.timeSinceSatUp = time.time()
            self.satUp = True
        else: self.satUp = False

    def collide(self, objects):
        for _ in range(round(abs(self.x_vel))):
            self.rect.x += self.x_vel / abs(self.x_vel)
            for obj in objects:
                obj.resolveXCollision(self)

        for _ in range(round(abs(self.y_vel))):
            self.rect.y += self.y_vel / abs(self.y_vel)
            for obj in objects:
                obj.resolveYCollision(self)


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
        hitbox -> either image or a rect which is relative to the x and y,
        the hitbox will scale automatically"""
        # code order fix
        self.hitbox = None

        super().__init__(x, y, name, scale, angle)
        self.correctionAngle = correctionAngle
        
        # stable collision
        if isinstance(hitbox, pg.Surface):
            hitbox = pg.transform.scale_by(hitbox, self.scale)
            self.mask = pg.mask.from_surface(hitbox)
        else:
            hitbox[0] *= scale
            hitbox[1] *= scale
            hitbox[2] *= scale
            hitbox[3] *= scale
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


# -----------Chair (Interactive)----------- #


class Chair(Object):
    def __init__(self, x: int, y: int, name: str, scale: int = 1, angle: int = 0, size: tuple[int, int] | list[int] = None) -> None:
        super().__init__(x, y, name, scale, angle, size)
        self.type = "Chair"

    def resolveXCollision(self, player: CorePlayer) -> CorePlayer:
        if not pg.sprite.collide_mask(self, player):
            return player
        if player.isSitting and time.time() - player.timeSinceSatUp > player.satUpCoolDown:
            player.rect.center = self.rect.center
        elif player.satUp:
            player.rect.bottom = self.rect.top
        else:
            return super().resolveXCollision(player)
        return player

    def resolveYCollision(self, player: CorePlayer) -> CorePlayer:
        if player.satUp:
            player.rect.bottom = self.rect.top
        if not pg.sprite.collide_mask(self, player):
            return player
        if player.isSitting:
            player.rect.center = self.rect.center
        else:
            return super().resolveYCollision(player)
        return player


# -----------Door (Interactive)----------- #


class Door(Object):
    def __init__(self, x: int, y: int, name: str, scale: int = 1, angle: int = 0, size: tuple[int, int] | list[int] = None) -> None:
        super().__init__(x, y, name, scale, angle, size)
        self.orentation = "horizontal"
        self.iter = 0
        self.maxSwing = 15

    def resolveXCollision(self, player: CorePlayer) -> CorePlayer:
        if self.orentation == "horizontal":
            return super().resolveXCollision(player)
        while pg.sprite.collide_mask(self, player) and self.iter < self.maxSwing:
            try:
                self.angle += (player.x_vel / abs(player.x_vel)) * -1
            except ZeroDivisionError:
                break
            self.iter += 1
        self.rotate()
        self.iter = 0
        return player

    def resolveYCollision(self, player: CorePlayer) -> CorePlayer:
        if self.orentation == "vertical":
            return super().resolveYCollision(player)
        while pg.sprite.collide_mask(self, player) and self.iter < self.maxSwing:
            try:
                self.angle += (player.y_vel / abs(player.x_vel)) * -1
            except ZeroDivisionError:
                break
            self.iter += 1
        
        self.rotate()
        self.iter = 0
        return player

if False:
    class Door:
        def __init__(self, x, y, name) -> None:
            self.image = assets[name]
            self.rotatedImage = assets[name]
            self.rect = self.image.get_rect(topleft=(x, y))
            self.name = name
            self.pivot = "topleft"
            self.orientation = "horizontal"
            self.angle = 0
            self.mask = pg.mask.from_surface(self.rotatedImage)
            self.iter = 0
            self.maxSwing = 15
            self.topLev = True

        def display(self, window: pg.Surface):
            window.blit(self.rotatedImage, self.rect)

        def reload(self):
            self.rect = self.rotatedImage.get_rect(topleft=self.rect.topleft)
            self.mask = pg.mask.from_surface(self.rotatedImage)

        def aftScript(self):
            self.topLev = True

        def script(self, player: CorePlayer):
            if not pg.sprite.collide_mask(self, player) and self.topLev:
                self.angle += 1
                self.angle = min(max(self.angle, -90), 0)
                self.rotatedImage = pg.transform.rotate(self.image, self.angle)
                self.reload()
                return
            elif not pg.sprite.collide_mask(self, player):
                self.iter = 0
                return
            if player.rect.y < self.rect.bottom:
                self.angle -= 1
                self.angle = min(max(self.angle, -90), 0)
                self.rotatedImage = pg.transform.rotate(self.image, self.angle)
            self.reload()
            self.iter += 1
            if self.iter > self.maxSwing:
                self.iter = 0
                return
            self.topLev = False
            self.script(player)


# -----------Mouse Click Collision Object----------- #


class MouseClick(Object):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, "Flat Black", 1, 0)


# -----------Object Map----------- #
objectMap = {"Object": Object, "Chair": Chair}