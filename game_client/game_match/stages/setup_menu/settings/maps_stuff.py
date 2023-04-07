from pygame import Surface
from global_obj.main import Global
from visual.UI.base.text import Text
from visual.UI.base.abs import ShapeAbs
from visual.UI.base.button import Button
from visual.UI.base.container import Container
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from core.world.base.map_save import MapSave
from visual.styles import get_green_btn_style
from settings.screen.size import scaled_w, scaled_h
from server_stuff.constants.requests import SetupStageReq
from settings.localization.menus.UI import UILocal


class MapRect:
    H_size = scaled_w(0.6)
    V_size = scaled_h(0.6)
    X = 0
    Y = scaled_h(0.05)
    rect = (X, Y, H_size, V_size)


class MapsButtonsContainer:
    X = 0.6
    Y = 0.155
    H_size = 0.196
    V_size = 0.5


class MapFuncElCons:
    X = 0.01
    Y = 0.05
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


class MapChooseUI(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    parent: Container

    def __init__(self, uid,
                 map_save: MapSave,
                 menu,
                 index: int,
                 x_k=MapFuncElCons.X,
                 y_k=MapFuncElCons.Y,
                 h_size_k=MapFuncElCons.H_size,
                 v_size_k=MapFuncElCons.V_size,
                 **kwargs):
        super(MapChooseUI, self).__init__(uid,
                                          x_k=x_k,
                                          y_k=y_k,
                                          h_size_k=h_size_k,
                                          v_size_k=v_size_k,
                                          **kwargs)
        ShapeAbs.__init__(self, **kwargs)
        self.save: MapSave = map_save
        self.menu_ui = menu
        self.index = index
        self.text = Text(uid=f'{uid}_txt',
                         parent=self,
                         from_left=True,
                         text=map_save.name.replace('.json', ''),
                         x_k=0.03,
                         y_k=0.01,
                         h_size_k=0.5,
                         v_size_k=0.98,
                         )

        self.chosen_btn: Button = Button(f'{uid}_choose_btn',
                                         text='+',
                                         inactive_text='-',
                                         parent=self,
                                         active=Global.network_data.is_admin,
                                         visible=Global.network_data.is_admin,
                                         x_k=MapFuncElCons.LBtnX,
                                         y_k=MapFuncElCons.LBtnY,
                                         h_size_k=MapFuncElCons.LBtnH_size,
                                         v_size_k=MapFuncElCons.LBtnV_size,
                                         on_click_action=self.choose_btn_action,
                                         style=get_green_btn_style())
        self.build()

    def choose_btn_action(self, b: Button):
        if Global.network_data.is_admin:
            Global.connection.send_json({SetupStageReq.Player.ChooseMap: self.index})

    def choose(self):
        self.chosen_btn.activate()
        self.render()

    def unchoose(self):
        self.chosen_btn.surface = self.chosen_btn.inactive_surface
        self.render()

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def build(self, **kwargs):
        self.render()
        self.chosen_btn.build()
        self.init_rect_shape()

        return self

    def render(self, **kwargs):
        self.fill_surface()
        self.text.draw()
        self.chosen_btn.draw()
        self.draw_border()

    def move(self, xy):
        self.x, self.y = xy
        self.init_shape()
        self.chosen_btn.init_shape()

    def get_surface(self, **kwargs) -> Surface:
        return self.get_rect_surface(self.h_size, self.v_size,
                                     transparent=self.style.surface_transparent,
                                     flags=self.style.surface_flags)

    def fill_surface(self, surface=None, color=(100, 100, 100)) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def init_shape(self) -> None:
        self.init_rect_shape()
