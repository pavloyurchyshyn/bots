from pygame import Surface

from settings.screen.size import scaled_w, scaled_h
from visual.UI.base.button import Button
from visual.UI.base.text import Text
from game_client.stages.styles import get_green_btn_style, get_red_btn_style


class MapRect:
    H_size = scaled_w(0.8)
    V_size = scaled_h(0.7)
    X = 0
    Y = scaled_h(0.005)
    rect = (X, Y, H_size, V_size)


class NameInput:
    H_size = 0.11
    V_size = 0.05
    X = 0.802
    Y = 0.005


class MapsButtonsContainer:
    X = 0.802
    Y = 0.057
    H_size = 0.196
    V_size = 0.5


from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from visual.UI.base.abs import ShapeAbs


class MapFuncElCons:
    X = 0.01
    Y = 0.01
    H_size = 0.98
    V_size = .1

    LBtnX = 0.74
    LBtnY = 0.015
    LBtnH_size = 0.15
    LBtnV_size = 0.97

    DltBtnX = 0.895
    DltBtnY = 0.015
    DltBtnH_size = 0.1
    DltBtnV_size = 0.97


class MapFuncUI(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    def __init__(self, uid, map_name: str, can_be_deleted=True, **kwargs):
        super(MapFuncUI, self).__init__(uid,
                                        x_k=MapFuncElCons.X,
                                        y_k=MapFuncElCons.Y,
                                        h_size_k=MapFuncElCons.H_size,
                                        v_size_k=MapFuncElCons.V_size,
                                        **kwargs)

        self.text = Text(uid=f'{uid}_txt',
                         parent=self,
                         from_left=True,
                         text=map_name.replace('.json', ''),
                         x_k=0.03,
                         y_k=0.01,
                         h_size_k=0.5,
                         v_size_k=0.98,
                         )

        self.load_btn: Button = Button(f'{uid}_load_btn',
                                       text='load', parent=self,
                                       x_k=MapFuncElCons.LBtnX,
                                       y_k=MapFuncElCons.LBtnY,
                                       h_size_k=MapFuncElCons.LBtnH_size,
                                       v_size_k=MapFuncElCons.LBtnV_size,
                                       style=get_green_btn_style())

        self.delete_btn: Button = Button(f'{uid}_dlt_btn',
                                         text='X', parent=self,
                                         x_k=MapFuncElCons.DltBtnX,
                                         y_k=MapFuncElCons.DltBtnY,
                                         h_size_k=MapFuncElCons.DltBtnH_size,
                                         v_size_k=MapFuncElCons.DltBtnV_size,
                                         active=can_be_deleted,
                                         visible=can_be_deleted,
                                         style=get_red_btn_style(),
                                         )

        self.build()

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)
        # self.load_btn.draw()
        # self.delete_btn.draw()

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def build(self, **kwargs):
        self.render()
        return self

    def render(self, **kwargs):
        self.fill_surface()
        self.text.draw()
        self.load_btn.draw()
        self.delete_btn.draw()
        self.draw_border()

    def move(self, xy):
        pass

    def get_surface(self, **kwargs) -> Surface:
        return self.get_rect_surface(self.h_size, self.v_size,
                                     transparent=self.style.surface_transparent,
                                     flags=self.style.surface_flags)

    def fill_surface(self, surface=None, color=(100, 100, 100)) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def init_shape(self) -> None:
        self.init_rect_shape()
