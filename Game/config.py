from Game.GUI import *


class BaseConfig:
    def __init__(self, obj, x, y) -> None:
        self.pos = x, y
        self.obj = obj

    def script(self): ...

    def display(self, window): ...

    def event(self, event): ...


class ObjectConfig(BaseConfig):
    def __init__(self, obj, x, y) -> None:
        super().__init__(obj, x, y)
        textSize = 35
        self.namebox = TextBox("Textbox", "Textbox", (5*GUI_scale, 3*GUI_scale), x, y, (0, 0, 0), textSize, "Arialblack", obj.name)
        self.angleText = Text("Angle", x, y+50, (0, 0, 0), textSize, "Arialblack")
        self.anglebox = TextBox("Textbox", "Textbox", (5*GUI_scale, 3*GUI_scale), x, y+100, (0, 0, 0), textSize, "Arialblack", obj.angle)
        self.scaleText = Text("Scale", x, y+150, (0, 0, 0), textSize, "Arialblack")
        self.scalebox = TextBox("Textbox", "Textbox", (4*GUI_scale, 5*GUI_scale), x, y+200, (0, 0, 0), textSize, "Arialblack", obj.scale)


    def script(self):
        self.anglebox.select()
        self.namebox.select()
        self.scalebox.select()

    def event(self, event):
        self.anglebox.update_text(event)
        self.namebox.update_text(event)
        self.scalebox.update_text(event)
        try:
            self.obj.angle = float(self.anglebox.text)
            self.obj.rotate()
        except:
            pass
        if self.namebox.text in list(assets.keys()):
            self.obj.name = self.namebox.text
        try:
            self.obj.scale = float(self.scalebox.text)
            self.obj.reload()
        except:
            pass

    def display(self, window):
        self.angleText.display(window)
        self.anglebox.display(window)
        self.namebox.display(window)
        self.scaleText.display(window)
        self.scalebox.display(window)

configMap = {"Object": ObjectConfig}