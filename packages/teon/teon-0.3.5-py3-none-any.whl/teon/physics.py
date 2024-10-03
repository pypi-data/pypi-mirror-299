import pygame

from teon.entity import Entity
from teon.functions import scale_def
from teon.other import Vec2
from teon.extra.controller import PlayerController2D,Controller2D

class RigidBody(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.bounciness = kwargs.get("bounciness",0.5)
        self.gravity = kwargs.get("gravity",500)
        self.screen_bound = kwargs.get("screen_bound",False)

        self.can_collide = kwargs.get("can_collide",True)
        
        self._position = Vec2(self.rect.center)

        self.velocity = Vec2()

        self.tags.append("dt")

    def update(self):
        super().update()

        self.velocity.y += self.gravity * self.dt * scale_def()
        self._position.y += self.velocity.y * self.dt
        self.rect.centery = self._position.y
        self._collide("vertical")

        self._position.x += self.velocity.x * self.dt
        self.rect.centerx = self._position.x
        self._collide("horizontal")

    def _collide(self,axis):
        if self.can_collide:
            active_level = Entity.level_editor.active_level
            if active_level and active_level.index == self.level_index:
                self.collision_sprites = active_level.entities
                for sprite in self.collision_sprites:
                    if sprite.hitbox.colliderect(self.hitbox) and sprite is not self and sprite.collidable:
                        if axis == "horizontal":
                            if self.hitbox.centerx <= sprite.hitbox.centerx:
                                self.hitbox.right = sprite.hitbox.left
                                self.velocity.x = 0
                            if self.hitbox.centerx > sprite.rect.centerx:
                                self.hitbox.left = sprite.hitbox.right
                                self.velocity.x = 0
                            self._position.x = self.hitbox.centerx
                            self.rect.centerx = self._position.x
                            
                        if axis == "vertical":
                            if self.hitbox.centery <= sprite.hitbox.centery:

                                self.hitbox.bottom = sprite.hitbox.top
                                self.velocity.y = -self.velocity.y * scale_def() * self.bounciness

                            if self.hitbox.centery > sprite.hitbox.centery:

                                self.hitbox.top = sprite.hitbox.bottom

                                self.velocity.y = -self.velocity.y * scale_def() * self.bounciness

                            self._position.y = self.hitbox.centery
                            self.rect.centery = self._position.y