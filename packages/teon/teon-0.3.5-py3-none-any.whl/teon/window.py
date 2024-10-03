import pygame

from teon.functions import _repair_vec2

class Window:
    def __init__(self,**kwargs):
        self._size = _repair_vec2(kwargs.get("size",(1000,600)))
        self._caption = kwargs.get("caption", "Teon")
        self._icon = kwargs.get("icon", "none")
        self._fullscreen = kwargs.get("fullscreen", False)
        self._resizable = kwargs.get("window_resizable",False)
        self.fps = kwargs.get("fps",60)
        self.aspect_ratio = kwargs.get("aspect_ratio",(1000,600))
        
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode(self._size,pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(self._size)

        pygame.display.set_caption(self._caption)
        
        if self._icon != "none":
            pygame.display.set_icon(self._icon)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self,caption):
        self._caption = caption
        pygame.display.set_caption(self._caption)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,size):
        self._size = _repair_vec2(size)
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode(self._size,pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(self._size)

    @property
    def resizable(self):
        return self._resizable

    @resizable.setter
    def resizable(self,bool):
        self._resizable = bool
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode(self._size,pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(self._size)

    @property
    def icon(self):
        return self._icon
    
    @icon.setter
    def icon(self,icon):
        self._icon = icon
        pygame.display.set_icon(self._icon)

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self,bool):
        self._fullscreen = bool
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode(self._size,pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(self._size)