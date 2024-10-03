import pygame
import time

from teon.window import Window
from teon.entity import Entity

from teon.text import Text

from teon.level import Level,LevelEditor

from teon.functions import rt_key

import teon.functions

class Teon:
    _instances = []
    _offset = (0,0)
    def __init__(self,**kwargs):
        '''Teon Engine main class
        
        Keyword Arguments: \n
        size (tuple(int,int)): set the size of the window \n
        full_screen (bool): set the window to the size of the display \n
        key_press_time (int): set the time window in which a press is counted (in s) \n
        caption (string): set the window caption \n
        icon (.ico): set the window icon \n
        resizable (bool): the window can be resized if true \n
        fps (int or float): set the fps cap for the window, set to -1 for no limit \n
        aspect_ratio (tuple(int,int)): in pixels, just set to the size of your screen for best performance \n
        '''

        pygame.init()

        self.debug_mode = kwargs.get("debug_mode", False)
        self.key_press_time = kwargs.get("key_press_time",0.2)
        self.frustum_culling = kwargs.get("frustum_culling",False)

        self.window = Window(**kwargs)
        self.time = pygame.time.Clock()

        self.level_editor = LevelEditor()
        Entity.level_editor = self.level_editor

        Level(index = 0)

        self.level_editor.set_active_level(0)

        Teon._instances.append(self)

    def input(self,key):
        pass

    @property
    def entities(self):
        entites = []
        for level in self.level_editor.levels:
            for entity in level.entities:
                entites.append(entity)
        return entites
    
    def update(self):
        pass

    def input(self):
        pass

    def run(self,update_func = None,input_func = None):
        '''
        This is the last function of the program, nothing after this will be run. \n
        If you have a function you want to run every frame, put it in the update function.
        '''
        if update_func != None:
            self.update = update_func
        
        if input_func != None:
            self.input = input_func

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    key_pressed = event.key if event.type == pygame.KEYDOWN else event.button
                    key_pressed_time = time.time()

                elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    if key_pressed is not None:
                        key_released = event.key if event.type == pygame.KEYUP else event.button
                        if key_pressed == key_released:
                            key_released_time = time.time()
                            if key_released_time - key_pressed_time <= self.key_press_time:
                                for entity in self.entities:
                                    entity.input(rt_key(key_pressed))
                                self.input(rt_key(key_pressed))
                                
                        key_pressed = None
                        
            self.window.display.fill((0, 0, 0))
            self.dt = self.time.tick(self.window.fps) / 1000

            if self.dt != 0:
                self.true_fps = 1 / self.dt

            teon.functions.ASPECT_SIZE = self.window.aspect_ratio

            for entity in Entity.level_editor.active_level.entities:
                if entity.has_tag("dt"):
                    entity.dt = self.dt

            self.level_editor.lvldyt()

            self.level_editor.update()
            self.level_editor.draw(self.window)

            self.update()

            if self.debug_mode:
                for entity in self.entities:
                    debug_collider(entity.collider)
                    if len(entity.colliders) > 0:
                        for _,collider in entity.colliders.items():
                            debug_collider(collider)

            pygame.display.update()

def debug_collider(collider,color = (255,0,0),**kwargs):
    collider = pygame.Rect(collider.x + Teon._offset[0],collider.y + Teon._offset[1],collider.width,collider.height)
    pygame.draw.rect(pygame.display.get_surface(),color,collider,2)
    if kwargs.get("name") is not None:
        text = Text(text = kwargs.get("name"),size = kwargs.get("size",30),color = color)
        text.anchor = "center"
        pygame.display.get_surface().blit(text.image,(collider.center[0] - text.rect.width / 2,collider.center[1] - text.rect.height / 2))