import pygame
import math

from teon.functions import scale_def,_repair_vec2
from teon.other import Vec2
from teon.collider import Collider
from teon.property import Position

def shake_screen(strength,time):
    Entity.level_editor.active_level.entities.shake(strength,time)

class Entity(pygame.sprite.Sprite):

    level_editor = None

    def __init__(self,**kwargs):

        super().__init__()
        texture = kwargs.get("image",0)
        collider = kwargs.get("collider")
        z = kwargs.get("z", 0)
        self._position = _repair_vec2(kwargs.get("position", Vec2((0,0))))
        self._rotation = kwargs.get("rotation", 0)
        vis = kwargs.get("visible", True)
        self._scale = kwargs.get("scale",(1,1))
        collidable = kwargs.get("collidable", True)
        self.tags = kwargs.get("tags",[])
        self.running = kwargs.get("running",True)
        self.color = kwargs.get("color",(255,255,255))
        self.is_ui = kwargs.get("is_ui", False)
        self.level_index = kwargs.get("lindex",0)
        self.position = self._position
        self.colliders = kwargs.get("colliders",{})
        self._collider_size = 0

        self.collidable = collidable
        self.visible = vis
        self.z = z

        x,y = self._position
        x = x * scale_def()
        y = y * scale_def()
        self._position = Vec2((x,y))

        self._scale = (self._scale[0] * scale_def(),self._scale[1] * scale_def())

        if texture == 0:
            self.image = pygame.Surface((100,100))
            self.image.fill(self.color)
        else:
            self.image = texture
            self.image = pygame.transform.scale(texture,(self.image.get_width(),self.image.get_height()))

        self.default_image_x = self.image.get_width()
        self.default_image_y = self.image.get_height()

        self.scale = (self._scale[0],self._scale[1],False)

        
        self.rect = self.image.get_rect(center = self._position)
        self.hitbox = Collider(self,(0,0),(1,1))

        if collider is not None:
            self.hitbox = Collider(self,collider[0],collider[1])

        if self._rotation != 0:
            self.image = pygame.transform.rotozoom(self.image,self._rotation,1)

        if Entity.level_editor:
            Entity.level_editor.add_entity_to_level(self)

        self._default_image = self.image
        
        self._occlusion_rect = pygame.Rect(self.rect.x,self.rect.y,self.image.get_width() * 1.1,self.image.get_height() * 1.1)

        self.position = Position(self.rect.centerx,self.rect.centery,self)

    def add_tag(self,tag):
        self.tags.append(tag)

    def input(self,key):
        pass

    def has_tag(self,tag):
        if tag in self.tags:
            return True
        return False
    
    def _update_colliders(self):
        for _,collider in self.colliders.items():
            collider.update()

    @property
    def collider(self):
        return self.hitbox
    
    def look_at(self, target):
        '''
        Give the entity as input and it will rotate to look at the entity with the top of the image,but the hitbox doesn't change shape
        '''
        if isinstance(target,Entity):
            target = target._position
        direction = pygame.Vector2(target) - self._position
        self._rotation = math.degrees(math.atan2(-direction.y, direction.x))

        self.image = pygame.transform.rotozoom(self._default_image, self._rotation,1)

    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self,degree):
        self._rotation += degree
        self.image = pygame.transform.rotozoom(self._default_image,self._rotation,1)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self,scale : tuple):
        self._scale = scale
        self.image = pygame.transform.scale(self.image,(self.default_image_x * self.scale[0],self.default_image_y * self.scale[1]))
        if len(scale) >= 3 and scale[2]:
            self.rect = self.image.get_rect(center = self.rect.center)
            self.hitbox = self.rect.copy()

    def update(self):
        self.hitbox.update()
        self._occlusion_rect.center = self.rect.center

        self._update_colliders()