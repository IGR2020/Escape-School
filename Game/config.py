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
        self.namebox = TextBox("Textbox", "Textbox", (5*GUI_scale, 0), x, y, (0, 0, 0), textSize, "Arialblack", obj.name)
        self.angleText = Text("Angle", x, y+50, (0, 0, 0), textSize, "Arialblack")
        self.anglebox = TextBox("Textbox", "Textbox", (5*GUI_scale, 0), x, y+100, (0, 0, 0), textSize, "Arialblack", obj.angle)
        self.scaleText = Text("Scale", x, y+150, (0, 0, 0), textSize, "Arialblack")
        self.scalebox = TextBox("Textbox", "Textbox", (5*GUI_scale, 0), x, y+200, (0, 0, 0), textSize, "Arialblack", obj.scale)
        self.widthText = Text("Width", x, y+250, (0, 0, 0), textSize, "Arialblack")
        self.widthbox = TextBox("Textbox", "Textbox", (5*GUI_scale, 0), x, y+300, (0, 0, 0), textSize, "Arialblack", obj.size[0])
        self.heightText = Text("Height", x, y+350, (0, 0, 0), textSize, "Arialblack")
        self.heightbox = TextBox("Textbox", "Textbox", (5*GUI_scale, 0), x, y+400, (0, 0, 0), textSize, "Arialblack", obj.size[1])

    def script(self):
        self.anglebox.select()
        self.namebox.select()
        self.scalebox.select()
        self.widthbox.select()
        self.heightbox.select()

    def event(self, event):
        self.anglebox.update_text(event)
        self.namebox.update_text(event)
        self.scalebox.update_text(event)
        self.widthbox.update_text(event)
        self.heightbox.update_text(event)
        try:
            self.obj.angle = int(self.anglebox.text)
            self.obj.rotate()
        except:
            pass
        if self.namebox.text in list(assets.keys()) and self.namebox.text != self.obj.name:
            self.obj.name = self.namebox.text
            self.obj.resetSize()
            self.widthbox.text = str(self.obj.size[0])
            self.heightbox.text = str(self.obj.size[1])
            self.widthbox.reload()
            self.heightbox.reload()
        try:
            self.obj.scale = float(self.scalebox.text)
            self.obj.reload()
        except:
            pass
        try:
            self.obj.size[0] = int(self.widthbox.text)
            self.obj.reload()
        except:
            pass
        try:
            self.obj.size[1] = int(self.heightbox.text)
            self.obj.reload()
        except:
            pass

    def display(self, window):
        self.angleText.display(window)
        self.anglebox.display(window)
        self.namebox.display(window)
        self.scaleText.display(window)
        self.scalebox.display(window)
        self.widthText.display(window)
        self.widthbox.display(window)
        self.heightbox.display(window)
        self.heightText.display(window)

configMap = {"Object": ObjectConfig, "Chair": ObjectConfig}