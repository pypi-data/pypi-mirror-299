import pygame

from teon.functions import scale_def,_repair_vec2

class Collider(pygame.Rect):
    def __init__(self,parent,position_offset,scale_offset):
        super().__init__(parent.rect.topleft[0] + (position_offset[0] * scale_def()),parent.rect.topleft[1] + (position_offset[1] * scale_def()),parent.rect.width * scale_offset[0],parent.rect.height * scale_offset[1])
        self.position_offset = _repair_vec2(position_offset)
        self.scale_offset = _repair_vec2(scale_offset)
        self.parent = parent

    def update(self):
        self.topleft = (self.parent.rect.topleft[0] + (self.position_offset[0] * scale_def()),self.parent.rect.topleft[1] + (self.position_offset[1] * scale_def()))
        self.width,self.height = (self.parent.rect.width * self.scale_offset[0],self.parent.rect.height * self.scale_offset[1])