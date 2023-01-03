from pygame import Surface
from typing import List
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from visual.UI.base.abs import ShapeAbs


class Container(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    def __init__(self, uid, draw_elements=False, **kwargs):
        super(Container, self).__init__(uid=uid, **kwargs)
        ShapeAbs.__init__(self, **kwargs)

        # self.surface = self.get_surface()
        self.__elements: List[BaseUI] = []
        self.__elements_dict = {}
        self.draw_elems = draw_elements
        self.dy = 0

    @property
    def elements(self):
        return self.__elements.copy()

    def add_element(self, element: BaseUI):
        self.__elements.append(element)
        self.__elements_dict[element.uid] = element
        self.calculate_elements_position()
        self.render()

    def delete_element(self, element: BaseUI):
        if element in self.__elements:
            self.__elements.remove(element)
        self.__elements_dict.pop(element.uid, None)
        self.calculate_elements_position()
        self.render()

    def calculate_elements_position(self):
        step = self.v_size * 0.01
        y = self.v_size * 0.01 + self.dy
        if y < step:
            self.dy = 0
            y = step

        for el in self.__elements:
            el.y = y
            y += step + el.v_size

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def move(self, xy):
        return
        self.move_rect_shape(xy)
        self.x, self.y = xy

    def fill_surface(self, surface=None, color=None) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def build(self, **kwargs) -> 'Container':
        self.render()
        self.init_shape()
        return self

    def get_surface(self, h_size=None, v_size=None, transparent=None, color=None, flags=None, **kwargs) -> Surface:
        h_size = self.h_size if h_size is None else h_size
        v_size = self.v_size if v_size is None else v_size
        transparent = self.style.surface_transparent if transparent is None else transparent
        color = self.style.color if color is None else color
        flags = self.style.surface_flags if flags is None else flags
        return self.get_rect_surface(h_size, v_size,
                                     transparent=transparent,
                                     flags=flags,
                                     color=color,
                                     )

    def init_shape(self) -> None:
        self.init_rect_shape()

    def render(self, **kwargs):
        self.fill_surface()
        self.draw_elements()

    def draw(self):
        if self.visible:
            self.parent_surface.blit(self.surface, self.position)
            self.draw_border(self.parent_surface, rect=self.shape.get_rect())

    def draw_elements(self):
        print(self.__elements)
        for el in self.__elements:
            el.draw()
