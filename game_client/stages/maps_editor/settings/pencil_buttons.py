from pygame import Surface

from global_obj.main import Global
from visual.UI.base.button import Button
from visual.UI.base.container import Container
from visual.UI.base.abs import ShapeAbs
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from visual.UI.base.text import Text
from core.world.base.logic.tile_data.tile_abs import TileDataAbs
from visual.styles import get_green_btn_style


class PencilElement(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    parent: Container

    def __init__(self,
                 tile_class: TileDataAbs,
                 uid=None,
                 x_k=0.0125,
                 h_size_k=0.98,
                 v_size_k=0.10,
                 chosen: bool = False,
                 **kwargs):
        super(PencilElement, self).__init__(uid if uid else f'{tile_class.name}_pencil_id',
                                            x_k=x_k,
                                            h_size_k=h_size_k,
                                            v_size_k=v_size_k,
                                            **kwargs)
        ShapeAbs.__init__(self, **kwargs)

        self.tile_class = tile_class
        self.choose_btn: Button = Button(uid=f'{tile_class.name}_btn',
                                         text='+',
                                         style=get_green_btn_style(),
                                         parent=self,
                                         surface_color=(50, 255, 60),
                                         on_click_action=self.choose_pencil_on_click,
                                         x_k=0.9,
                                         h_size_k=0.1, v_size_k=0.98)

        self.name_txt: Text = Text(uid=f'{tile_class.name}_text',
                                   text=tile_class.verbose_name,
                                   parent=self,
                                   h_size_k=0.5)

        self.chosen_surface: Surface = None
        self.unchosen_surface: Surface = None
        self.chosen: bool = chosen
        self.build()

    def choose(self):
        self.chosen = True
        self.surface = self.chosen_surface
        self.choose_pencil_on_click()

    def unchose(self):
        self.chosen = False
        self.surface = self.unchosen_surface

    def set_chosen(self, chosen: bool):
        self.choose() if chosen else self.unchose()

    def choose_pencil_on_click(self, *_, **__):
        if self.parent.parent.chosen_pencil:
            self.parent.parent.chosen_pencil.unchose()
        self.parent.parent.chosen_pencil = self
        self.parent.parent.update_pencil_tile_icon()
        Global.logger.info(f'Chosen pencil: {self.tile_class.name}')

    def render_unchosen_surface(self):
        surface = self.get_rect_surface(*self.surface.get_size())
        self.fill_surface_due_to_border_attrs(surface=surface, color=(50, 50, 50))
        self.name_txt.draw(parent_surface=surface)
        self.draw_border(surface=surface, color=(100, 100, 100))
        self.unchosen_surface = surface

    def render(self, **kwargs):
        self.fill_surface()
        self.choose_btn.draw()
        self.name_txt.draw(self.surface)
        self.draw_border()
        self.chosen_surface = self.surface
        self.render_unchosen_surface()

    def build(self, **kwargs):
        self.init_rect_shape()
        self.choose_btn.build()
        self.name_txt.build()
        self.render()

        self.surface = self.chosen_surface if self.chosen else self.unchosen_surface

        return self

    def move(self, xy):
        self.x, self.y = xy
        self.init_shape()
        self.choose_btn.init_shape()

    def init_shape(self) -> None:
        self.init_rect_shape()

    def draw(self) -> 'BaseUIAbs':
        self.default_draw()

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def get_surface(self, **kwargs) -> Surface:
        return self.default_get_surface(**kwargs)

    def fill_surface(self, surface=None, color=(100, 100, 100)) -> None:
        self.fill_surface_due_to_border_attrs(surface=surface, color=color)
