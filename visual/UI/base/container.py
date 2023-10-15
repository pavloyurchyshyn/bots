from typing import List
from pygame import Surface
from visual.UI.base.abs import ShapeAbs
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin


class Container(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    STEP_K = 0.01

    def __init__(self, uid, draw_elements=False, scroll_k=0.24, **kwargs):
        super(Container, self).__init__(uid=uid, **kwargs)
        ShapeAbs.__init__(self, **kwargs)

        self.__elements: List[BaseUI] = []
        self.__elements_dict = {}
        self.draw_elems = draw_elements

        self.summary_els_height = 0
        self.dy = 0
        self.scroll_speed = 0
        self.scroll_k = scroll_k
        self.update_scroll_speed()

    def update_scroll_speed(self):
        if self.__elements:
            self.scroll_speed = self.summary_els_height / len(self.__elements) * self.scroll_k
        else:
            self.scroll_speed = 0

    @property
    def elements(self) -> List[BaseUI]:
        return self.__elements.copy()

    def clear(self):
        self.__elements.clear()

    def change_dy(self, dy):
        if dy == 0:
            return
        if self.summary_els_height > self.height:
            self.dy += dy * self.scroll_speed
            step = self.v_size * self.STEP_K
            steps_h = step * (len(self.__elements) + 1.5)
            if steps_h + self.summary_els_height + self.dy < self.height:
                self.dy = self.height - steps_h - self.summary_els_height
            if self.dy > 0:
                self.dy = 0
            self.calculate_elements_position()
            self.render()
        else:
            self.dy = 0

    def add_element(self, element: BaseUI, render: bool = True):
        self.__elements.append(element)
        self.__elements_dict[element.uid] = element
        self.summary_els_height += element.height
        self.calculate_elements_position()
        if render:
            self.render()
        self.update_scroll_speed()

    def delete_element(self, element: BaseUI):
        if element in self.__elements:
            self.__elements.remove(element)
        self.summary_els_height -= element.height
        self.__elements_dict.pop(element.uid, None)
        self.calculate_elements_position()
        self.render()
        self.update_scroll_speed()

    def calculate_elements_position(self):
        step = self.v_size * self.STEP_K
        y = step + self.dy
        for el in self.__elements:
            el.move((el.x, y))
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
        for el in self.__elements:
            el.draw()
