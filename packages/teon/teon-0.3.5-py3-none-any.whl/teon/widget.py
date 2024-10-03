import pygame

from teon.entity import Entity
from teon.functions import _repair_vec2,window_size,mouse_position,mouse_pressed
from teon.other import Vec2,Timer

class Widget(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.is_ui = True

        self.position = _repair_vec2(kwargs.get("position",Vec2((0,0))))
        self._position = _repair_vec2((window_size().y * self.position.x,window_size().y * self.position.y))
        self.anchor = kwargs.get("anchor","topleft")
        self.held_time = kwargs.get("held_time",200)
        self._held_timer = Timer(self.held_time)
        self._held_timer.activate()
        self.rect.center = self._position

        self.collidable = False

        self.hovered = False
        self.held = False

    def _get_held(self):
        if mouse_pressed()[0] and self.hovered:

            self._held_timer.update()
            if not self._held_timer.active:
                self.held = True
            else:
                self.held = False
        
        else:
            self._held_timer.activate()
            self.held = False

    def update(self):
        self.hovered = self.rect.collidepoint(mouse_position())
        self._get_held()
        