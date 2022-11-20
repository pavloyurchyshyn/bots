from pygame import Surface, SRCALPHA
from settings.graphic import GraphicConfig

from global_obj import Global
from visual.UI.settings import UIDefault
from visual.UI.base.element import BaseUI, GetSurfaceMixin
from visual.UI.base.font import DEFAULT_FONT_NAME, get_custom_font, DEFAULT_FONT_SIZE
from visual.UI.constants.attrs import Attrs


class Text(BaseUI, GetSurfaceMixin):

    def __init__(self, uid: str, text: str = '', **kwargs):
        super().__init__(uid=uid, postpone_render=kwargs.pop(Attrs.PostponeRender, True), **kwargs)

        self.raw_text = kwargs.get(Attrs.RawText, True)
        self.str_text = self.__get_text_for_render(str(text), self.raw_text).replace('\t', '    ')

        self.color = kwargs.get(Attrs.Color, UIDefault.TextColor)
        self.text_back_color = kwargs.get(Attrs.TextBackColor)

        font_name = kwargs.get(Attrs.FontName, DEFAULT_FONT_NAME)
        font_size = kwargs.get(Attrs.FontSize, DEFAULT_FONT_SIZE)
        self.font = get_custom_font(font_size, font_name)

        self.antialiasing = kwargs.get(Attrs.AA, GraphicConfig.AntialiasingText)

        self.build()

    def render(self):
        if '\n' in self.str_text:
            texts_renders = []
            v_size = 0
            for t in self.str_text.split('\n'):
                rendered = self.get_rendered_text(t)
                texts_renders.append(rendered)
                v_size += rendered.get_height()

            h_size = max(texts_renders, key=lambda e: e.get_width()).get_width()
            text_surf = self.get_rect_surface(h_size, v_size)
            y = 0
            for t in texts_renders:
                x = 1 if self.from_left else (h_size - t.get_width()) // 2
                text_surf.blit(t, (x, y))
                y += t.get_height()

            self.surface = text_surf
        else:
            text = self.get_rendered_text(self.str_text)
            self.surface = self.get_rect_surface(*text.get_size())
            self.surface.blit(text, (0, 0))

        self.check_for_place_inside()

        self.h_size, self.v_size = self.surface.get_size()

    def get_rendered_text(self, text: str) -> Surface:
        return self.font.render(text, self.antialiasing, self.color, self.text_back_color)

    def __get_text_for_render(self, text: str, raw: bool) -> str:
        return text if raw else Global.localization.get_text_with_localization(text)

    def reload_text(self) -> None:
        self.str_text = self.__get_text_for_render(str(self.str_text), self.raw_text).replace('\t', '    ')

    def init_shape(self) -> None:
        self.shape = None

    def build_position(self) -> None:
        self.default_build_position()

    def move(self, xy):
        self.x, self.y = xy
        if self.auto_draw:
            self.draw()
