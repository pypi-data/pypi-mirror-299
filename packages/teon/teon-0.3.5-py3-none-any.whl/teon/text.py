import pygame

from teon.entity import Entity
from teon.other import Vec2
from teon.functions import scale_def,_repair_vec2
from teon.font import Font

class Text(Entity):
    def __init__(self, text, font=None, size=10, **kwargs):
        '''
        Text class used to display text in the UI and in the game world. \n

        Keyword Arguments: \n
        antialias: self explanatory \n
        background_color: the background color of the text, default is None \n 
        is_ui: if True, the text will stay on the screen and not move \n 
        color: the color of the text \n 
        font can either be a literal font or teon.Font class \n
        anchor: offset the text based on the collider anchor
        '''
        self._font = font
        self._text = text
        self._size = int(size * scale_def())
        self._antialias = kwargs.get("antialias", False)
        self._background_color = kwargs.get("background_color", None)
        self._color = kwargs.get("color", (255, 255, 255))
        self._anchor = kwargs.get("anchor","topleft")
        self._screen_bound = kwargs.get("screen_bound",False)
        

        super().__init__(**kwargs)
        self.position = _repair_vec2(kwargs.get("position",Vec2((0,0))))

        self._anchor_dict = {
            "topleft": self.rect.topleft,
            "midleft": self.rect.midleft,
            "bottomleft": self.rect.bottomleft,
            "midtop": self.rect.midtop,
            "center": self.rect.center,
            "midbottom": self.rect.midbottom,
            "topright": self.rect.topright,
            "midright": self.rect.midright,
            "bottomright": self.rect.bottomright
        }
        
        self._position = (pygame.display.get_window_size()[0] * self.position.x,pygame.display.get_window_size()[1] * self.position.y)
        self.anchor = self._anchor
        self._render_text()
        self.is_ui = kwargs.get("is_ui", True)
        self.collidable = False


    def _render_text(self):
        """Helper method to render text."""
        if isinstance(self._font, Font):
            self.image = pygame.font.Font(self._font.path, self._size).render(self._text, self._antialias, self._color, self._background_color)
        else:
            self.image = pygame.font.Font(self._font, self._size).render(self._text, self._antialias, self._color, self._background_color)

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self,anchor):
        if self.is_ui:
            if self._anchor in self._anchor_dict:
                self._anchor = anchor
                self._position = (pygame.display.get_window_size()[0] * self.position.x,pygame.display.get_window_size()[1] * self.position.y)
                self.rect = self.image.get_rect()
                if self._anchor == "topleft":
                    self.rect.topleft = self._position
                elif self._anchor == "center":
                    self.rect.center = self._position
                elif self._anchor == "midright":
                    self.rect.midright = self._position
                elif self._anchor == "midleft":
                    self.rect.midleft = self._position
                elif self._anchor == "midtop":
                    self.rect.midtop = self._position
                elif self._anchor == "midbottom":
                    self.rect.midbottom = self._position
                elif self._anchor == "bottomleft":
                    self.rect.bottomleft = self._position
                elif self._anchor == "topright":
                    self.rect.topright = self._position
                elif self._anchor == "bottomright":
                    self.rect.bottomright = self._position
            else:
                print("The anchor provided doesn't represent a point on the text collider, for more help take a look at the Teon documentation.")

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self,color):
        self._background_color = color
        self._render_text()

    @property
    def antialias(self):
        return self._antialias

    @antialias.setter
    def antialias(self,bool):
        self._antialias = bool
        self._render_text()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._render_text()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = int(size * scale_def())
        self._render_text()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._render_text()
    
    def update(self):
        self.anchor = self._anchor