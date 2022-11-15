from pygame import Surface, SRCALPHA
from pygame.transform import smoothscale
from settings.graphic import GraphicConfig
from visual.UI.utils import get_surface
from visual.UI.base.element import BaseUI
from visual.UI.base.font import DEFAULT_FONT_NAME, get_custom_font, DEFAULT_FONT_SIZE
from visual.UI.constants.attrs import Attrs
from visual.UI.constants.colors import CommonColors

from settings.localization import LocalizationLoader, TEXT_PATH_DELIMITER


class LocalizationMixin:
    Delimiter = TEXT_PATH_DELIMITER
    PathSymbol = '@//'
    __localization = LocalizationLoader()

    @staticmethod
    def get_text_with_localization(text: str):
        if text.startswith(LocalizationMixin.PathSymbol):
            return LocalizationMixin.__localization.get_text(text.replace(LocalizationMixin.PathSymbol, ''))
        else:
            return text

    @classmethod
    def build_path(cls, *args):
        return f'{cls.PathSymbol}{cls.Delimiter.join(args)}'


class Text(BaseUI, LocalizationMixin):

    def __init__(self, uid: str, text: str = '', **kwargs):
        super().__init__(uid=uid, **kwargs, postpone_render=True)

        self.raw_text = kwargs.get(Attrs.RawText, True)
        self.str_text = self.__get_text_for_render(text, self.raw_text).replace('\t', '    ')

        self.surface = None
        self.surface_transparent = kwargs.get(Attrs.SurfaceTransparent, 1)
        self.surface_flags = kwargs.get(Attrs.SurfaceFlags, SRCALPHA)
        self.surface_color = kwargs.get(Attrs.SurfaceColor, (0, 0, 0, 0))

        self.color = kwargs.get(Attrs.Color, CommonColors.white)
        self.text_back_color = kwargs.get(Attrs.TextBackColor)

        font_name = kwargs.get(Attrs.FontName, DEFAULT_FONT_NAME)
        font_size = kwargs.get(Attrs.FontSize, DEFAULT_FONT_SIZE)
        self.font = get_custom_font(font_size, font_name)

        self.from_left = kwargs.get(Attrs.FromLeft, False)
        self.from_bot = kwargs.get(Attrs.FromBot, False)
        self.from_top = kwargs.get(Attrs.FromTop, False)
        self.place_inside = kwargs.get(Attrs.PlaceInside, True)
        self.antialiasing = kwargs.get(Attrs.AA, GraphicConfig.Antialiasing)

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
            text_surf = get_surface(h_size, v_size,
                                    transparent=self.surface_transparent,
                                    flags=self.surface_flags,
                                    color=self.surface_color,
                                    )
            y = 0
            for t in texts_renders:
                x = 1 if self.from_left else (h_size - t.get_width()) // 2
                text_surf.blit(t, (x, y))
                y += t.get_height()

            self.surface = text_surf
        else:
            text = self.get_rendered_text(self.str_text)
            self.surface = get_surface(*text.get_size(),
                                       transparent=self.surface_transparent,
                                       flags=self.surface_flags,
                                       color=self.surface_color,
                                       )
            self.surface.blit(text, (0, 0))

        h_size, v_size = self.surface.get_size()
        if self.place_inside:
            scale = 0
            if h_size > (h := self.parent_surface.get_width()):
                h_size = h
                scale = 1
            if v_size > (v := self.parent_surface.get_height()):
                v_size = v
                scale = 1

            if scale:
                self.surface = smoothscale(self.surface, (h_size, v_size))

        self.h_size, self.v_size = self.surface.get_size()
        self.build_position()

    def get_rendered_text(self, text: str) -> Surface:
        return self.font.render(text, self.antialiasing, self.color, self.text_back_color)

    def __get_text_for_render(self, text, raw) -> str:
        return text if raw else self.get_text_with_localization(text)

    def init_shape(self) -> None:
        self.shape = None

    def build_position(self) -> None:

        h_size, v_size = self.surface.get_size()
        ph_size, pv_size = self.parent_surface.get_size()

        if self.x_k is not None:
            self.x = int(ph_size * self.x_k)
        elif self.from_left:
            self.x = 1
        else:
            self.x = (ph_size - h_size) // 2

        if self.y_k is not None:
            self.y = int(pv_size * self.y_k)
        elif self.from_bot and not self.from_top:
            self.y = pv_size - v_size
        elif self.from_top and not self.from_bot:
            self.y = 1
        else:
            self.y = (pv_size - v_size) // 2

    def move(self, xy):
        self.x, self.y = xy
        if self.auto_draw:
            self.draw()
