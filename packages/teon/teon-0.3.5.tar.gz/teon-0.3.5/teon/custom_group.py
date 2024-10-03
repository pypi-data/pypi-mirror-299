import pygame

from random import randint
from teon.other import Timer,Vec2


class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = Vec2()
        self.camera_speed = 0.1
        self.player = 0

        self.is_shaking = False

        self.shaking_strength = 0

        self.shaking_time = Timer(1)

    def shake(self,strength,time):
        self.is_shaking = True
        self.shaking_strength = strength
        self.shaking_time = Timer(time)
        self.shaking_time.activate()

    def get_player(self,player):
        self.player = player

    def get_class(self):
        from teon.core import Teon
        self._core_class = Teon._instances[0]

    def lerp(self, start, end, t):
        return start + (end - start) * t

    def draw(self, surface):
        offset_x = randint(-self.shaking_strength,self.shaking_strength)
        offset_y = randint(-self.shaking_strength,self.shaking_strength)
        self.shaking_time.update()
        if not self.shaking_time.active:
            self.is_shaking = False
        else:
            self.is_shaking = True
        if self.player != 0:
            self.camera_speed = self.player.camera_speed
            if self.player.camera == "platformer":
                self.offset.x = -(self.player.rect.centerx - pygame.display.get_window_size()[0] / 2)

            if self.player.camera == "topdown":
                self.offset.x = -(self.player.rect.centerx - pygame.display.get_window_size()[0] / 2)
                self.offset.y = -(self.player.rect.centery - pygame.display.get_window_size()[1] / 2)

            if self.player.camera == "smooth_platformer":
                target_offset_x = -(self.player.rect.centerx - pygame.display.get_window_size()[0] / 2)
                self.offset.x = self.lerp(self.offset.x, target_offset_x, self.camera_speed)

            if self.player.camera == "smooth_topdown":
                target_offset_x = -(self.player.rect.centerx - pygame.display.get_window_size()[0] / 2)
                target_offset_y = -(self.player.rect.centery - pygame.display.get_window_size()[1] / 2)
                self.offset.x = self.lerp(self.offset.x, target_offset_x, self.camera_speed)
                self.offset.y = self.lerp(self.offset.y, target_offset_y, self.camera_speed)
                
        if not self.is_shaking:
            offset_x,offset_y = 0,0

        sorted_sprites = sorted(self.sprites(), key=lambda sprite: (sprite.z, sprite.rect.bottom))
        self._core_class.__class__._offset = self.offset + (offset_x,offset_y)
        for sprite in sorted_sprites:
            if sprite.visible:
                if sprite.is_ui:
                    surface.display.blit(sprite.image, sprite.rect.topleft)
                

                elif self._core_class.frustum_culling:
                    if sprite._occlusion_rect.colliderect(self.player._occluder_rect):
                        sprite._positionn = sprite.rect.topleft + self.offset + (offset_x,offset_y)
                        surface.display.blit(sprite.image, sprite.rect.topleft + self.offset + (offset_x,offset_y))
                
                else:
                    sprite._positionn = sprite.rect.topleft + self.offset + (offset_x,offset_y)
                    surface.display.blit(sprite.image, sprite.rect.topleft + self.offset + (offset_x,offset_y))