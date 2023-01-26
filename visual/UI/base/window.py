from abc import abstractmethod
from global_obj.main import Global


class Window:
    def __init__(self, uid, parent, x, y, h_size, v_size, surface=None):
        self.uid = uid
        self.parent = parent
        self.x, self.y = x, y
        self.h_size, self.v_size = h_size, v_size
        self.surface = surface if surface else Global.display

    @property
    def real_position(self) -> (int, int):
        return self.x, self.y

    @property
    def size(self):
        return self.h_size, self.v_size

    @abstractmethod
    def update(self):
        raise NotImplementedError
