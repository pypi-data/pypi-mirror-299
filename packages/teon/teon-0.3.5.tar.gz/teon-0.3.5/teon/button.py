
from teon.widget import Widget

class Button(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.pressed = False

        if kwargs.get("on_pressed","none") != "none":
            self.on_pressed = kwargs.get("on_pressed","none")

    def on_pressed(self):
        pass

    def input(self,key):
        if self.hovered and key == "left mouse":
            self.pressed = True
            if self.on_pressed != "none":
                self.on_pressed()
        else:
            self.pressed = False