import pygame

from teon.other import _key_map,_yek_map,Vec2

class _CollidingType:
    def __init__(self,bool,entity):
        self.colliding = bool
        self.entity = entity

    def __bool__(self):
        return self.colliding

def colliding(entity1,entity2,specific_rect : tuple = (False,False)):
        from teon.entity import Entity
        collider1 = entity1.hitbox

        if specific_rect[0] != False:
            collider1 = entity1.colliders[specific_rect[0]]
        
        if isinstance(entity2,Entity):
            collider2 = entity2.hitbox
                
            if specific_rect[1] != False:
                collider2 = entity2.colliders[specific_rect[1]]

            return _CollidingType(collider1.colliderect(collider2),entity2)
        
        elif isinstance(entity2,list):
            for entity in entity2:
                collider = entity.collider
                if specific_rect[1] != False:
                    collider = entity.colliders[specific_rect[1]]
                if collider1.colliderect(collider):
                    return _CollidingType(collider1.colliderect(collider),entity)
            return _CollidingType(False,None)

def _repair_vec2(vec2):
    if isinstance(vec2,tuple):
        return Vec2(vec2[0],vec2[1])
    return vec2

def mouse_position():
    return _repair_vec2(pygame.mouse.get_pos())

def window_size():
    return _repair_vec2(pygame.display.get_window_size())

def screen_size():
    return _repair_vec2(pygame.display.get_desktop_sizes()[0])

def key_pressed(key):
    '''
    Returns true if the given key is pressed down
    '''
    return pygame.key.get_pressed()[tr_key(key)]

def load_animation(path,name,int_range):
    '''
    All the animation frames must be in the same folder and have the same name, but diffrent numeration
    '''
    x,y = int_range
    for i in range(x,y + 1):
        load_image(path + "/" + name + i)

def load_image(path):
    '''
    Give the image path, and it returns the loaded image
    '''
    return pygame.image.load(path).convert_alpha()

def tr_key(key):
    '''
    Don't use this
    '''
    return _key_map[key]

def rt_key(key):
    '''
    Don't use this
    '''
    return _yek_map[key]

def mouse_pressed():
    '''
    Returns tuple(bool,bool,bool) 0 is the left mouse button, 1 is the scroll wheel, 2 is the right mouse button. \n
    Returns the current state of the mouse button, True if held down
    '''
    return pygame.mouse.get_pressed()

ASPECT_SIZE = (1000,600)

def scale_def():
    '''
    Don't use this
    '''
    x,y = ASPECT_SIZE
    xx,yy = pygame.display.get_window_size()
    dx = xx / x
    dy = yy / y
    if dx >= dy:
        return dy
    else:
        return dx