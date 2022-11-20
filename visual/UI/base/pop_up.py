from abc import ABC

from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from visual.UI.base.mixins import CreateButtonMixin


class PopUpBase(BaseUI, GetSurfaceMixin, DrawBorderMixin, CreateButtonMixin, ABC):

    def render(self):
        self.surface = self.get_rect_surface(self.h_size, self.v_size)
        self.draw_border()

    def __init__(self, uid: str, buttons_data: dict, **kwargs):
        super(PopUpBase, self).__init__(uid, **kwargs)

        self.buttons = self.create_button_from_data(buttons_data)


class PopUp(PopUpBase, BuildRectShapeMixin):
    def reload_shape_position(self) -> None:
        BuildRectShapeMixin.reload_shape_position(self)

    def init_shape(self) -> None:
        self.init_rect_shape()

    def build_position(self) -> None:
        self.default_build_position()

    def move(self, xy):
        self.move_rect_shape(xy)

