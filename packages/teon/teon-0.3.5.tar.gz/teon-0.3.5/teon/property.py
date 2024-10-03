class Position:
    def __init__(self, x=0, y=0, entity=None):
        self._x = x
        self._y = y
        self._entity = entity

    @property
    def x(self):
        return self._entity._positionn.x

    @x.setter
    def x(self, value):
        self._x = value
        self._entity.rect.centerx = self._x

    @property
    def y(self):
        return self._entity._positionn.y

    @y.setter
    def y(self, value):
        self._y = value
        self._entity.rect.centery = self._y

    def __iadd__(self, value):
        dx, dy = value
        self.x = self._x + dx
        self.y = self._y + dy

        return self