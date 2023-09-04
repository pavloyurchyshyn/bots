from pygame import mouse


class Mouse:

    def __init__(self, rel=None, pos=None, pressed=None):
        self.mouse = mouse
        self._rel = self.mouse.get_rel() if rel is None else rel
        self._pos = self.mouse.get_pos() if pos is None else pos
        self._pressed = self.mouse.get_pressed() if pressed is None else pressed

        # self.mouse.set_visible(False)

        self.l_up = 0
        self.r_up = 0
        self.m_up = 0

        self.l_down = 0
        self.m_down = 0
        self.r_down = 0

        self._scroll = 0

    def update(self):
        self._rel = self.mouse.get_rel()
        self._pos = [*self.mouse.get_pos()]
        self._pressed = list(self.mouse.get_pressed())
        self._scroll = 0

        self.l_up = 0
        self.r_up = 0
        self.m_up = 0

        self.l_down = 0
        self.r_down = 0
        self.m_down = 0

    def set_position(self, pos):
        self.mouse.set_pos(pos)

    @property
    def m_hold(self):
        return self._pressed[1] and not self.m_down

    @property
    def l_hold(self):
        return self._pressed[0] and not self.l_down

    @property
    def r_hold(self):
        return self._pressed[2] and not self.l_down

    @property
    def l_pressed(self):
        return self._pressed[0]

    @l_pressed.setter
    def l_pressed(self, val):
        self._pressed[0] = val

    @property
    def r_pressed(self):
        return self._pressed[2]

    @r_pressed.setter
    def r_pressed(self, val):
        self._pressed[2] = val

    @property
    def m_pressed(self):
        return self._pressed[1]

    @m_pressed.setter
    def m_pressed(self, val):
        self._pressed[1] = val

    @property
    def scroll(self):
        return self._scroll

    @scroll.setter
    def scroll(self, value):
        self._scroll = value

    @property
    def rel(self):
        return self._rel

    @property
    def pos(self):
        return self._pos

    @property
    def x(self):
        return self._pos[0]

    @property
    def y(self):
        return self._pos[1]

    @property
    def pressed(self):
        return self._pressed

    @property
    def rel_x(self):
        return self.rel[0]

    @property
    def rel_y(self):
        return self.rel[1]

    def test(self):
        print('up', self.l_up, self.r_up, '| down', self.l_down, self.r_down, '| hold', self.l_hold, self.r_hold)

    @property
    def position(self):
        return self._pos