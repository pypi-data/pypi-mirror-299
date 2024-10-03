import teon.functions
import ursina
from teon.entity import Entity
from teon.custom_group import CustomGroup
from teon.extra.controller import Controller2D

class Level:
    def __init__(self,index=0):
        self.index = index
        self.entities = CustomGroup()
        self.active = False

        Entity.level_editor.add_level(self)

        self.done = False

    def add_entity(self, entity):
        self.entities.add(entity)

    def load_level(self,filee):
        list = []
        file = filee
        for line in file:
            line = line.strip()
            filename, x, y,xs,ys,vis,coll,z,_ = line.split(":")
            if vis == "True":
                vis = True
            else:
                vis = False

            if coll == "True":
                coll = True
            else:
                coll = False

            list.append((filename, (int(x), int(y)), (int(xs),int(ys)),vis,coll,int(z),_))

        for filename, (x, y), (xs,ys),vis,coll,z,_ in list:
            try:
                img = teon.functions.load_image(filename)
            except:
                img = teon.functions.load_image("LevelEditor/files/uis/missing_texture.png")
                print(f"Couldn't import texture at given location: {filename}")

            ent = globals()[_](image = img,position = (x, y),z = z,collidable = coll,visible = vis)
            ent.scale(xs,ys)
            self.entities.add(ent)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def add_player(self):
        if len(Controller2D._instances) == 1 and not self.done:
            self.entities.get_player(Controller2D._instances[0])
            self.done = True

    def draw(self, surface):
        self.entities.draw(surface)

    def update(self):
        self.entities.update()

class LevelEditor:
    def __init__(self):
        self.levels = []
        self.active_level = None

    def add_level(self, level):
        self.levels.append(level)

    def lvldyt(self):
        for level in self.levels:
            level.add_player()
            level.entities.get_class()

    def add_entity_to_level(self, entity):
        level_index = entity.level_index
        for level in self.levels:
            if level.index == level_index:
                level.add_entity(entity)
                break

    def set_active_level(self, level_index):
        '''
        Give the index of the level of the level itself
        '''

        if isinstance(level_index,Level):
            level_index = level_index.index

        if 0 <= level_index < len(self.levels):
            if self.active_level is not None:
                self.active_level.active = False
            self.active_level = self.levels[level_index]
            self.active_level.active = True

    def draw(self, surface):
        if self.active_level and self.active_level.active:
            self.active_level.draw(surface)

    def update(self):
        if self.active_level and self.active_level.active:
            self.active_level.update()