from pygame import Surface
from pygame.transform import smoothscale
from global_obj.main import Global
from visual.UI.base.element import BaseUI
from visual.UI.base.font import DEFAULT_FONT_NAME, get_custom_font, DEFAULT_FONT_SIZE
from visual.UI.constants.attrs import Attrs, TextAttrs
from visual.UI.utils import get_surface


class Text(BaseUI):
    TAB_VALUE = '  '
    MAX_SPEED = 4

    def __init__(self, uid: str, text: str = '', raw_text=True, color=None, **kwargs):

        super().__init__(uid=uid, **kwargs, build_surface=True)
        self.color = color if color else self.style.color
        self.raw_text = raw_text
        self.str_text = self.get_localization_text(str(text), self.raw_text)

        self.unlimited_h_size = kwargs.get(TextAttrs.UnlimitedHSize, False)
        self.unlimited_v_size = kwargs.get(TextAttrs.UnlimitedVSize, False)

        self.font_size = kwargs.get(TextAttrs.FontSize, DEFAULT_FONT_SIZE)
        self.font_name = kwargs.get(TextAttrs.FontName, DEFAULT_FONT_NAME)
        self.font = get_custom_font(self.font_size, self.font_name)
        self.scale_font = kwargs.get(TextAttrs.ScaleFont, False)

        self.split_lines = kwargs.get(TextAttrs.SplitLines, True)

        self.auto_draw = kwargs.get(Attrs.AutoDraw, True)

        self.from_left = kwargs.get('from_left', False)

        if not kwargs.get(Attrs.PostponeBuild):
            self.build()

    def build(self):
        self.render()
        if self.auto_draw:
            self.draw()

    def render(self, **kwargs):
        rendered_text = self.render_text()
        if self.unlimited_v_size or self.unlimited_h_size:
            self.surface = rendered_text.copy()
        if self.style.from_left or self.from_left:
            x = int(self.parent_surface.get_width() * 0.02)
        else:
            x = (self.surface.get_width() - rendered_text.get_width()) // 2

        if self.style.from_top:
            y = 0
        elif self.style.from_bot:
            y = self.v_size - rendered_text.get_height() if self.v_size > rendered_text.get_height() else 0
        else:
            y = (self.surface.get_height() - rendered_text.get_height()) // 2

        self.fill_surface()

        self.surface.blit(rendered_text, (x, y))

    def get_x(self) -> int:
        if self.x_k is not None:
            return int(self.parent_surface.get_width() * self.x_k)
        elif self.style.from_left:
            return 1
        else:
            return 0

    def get_y(self) -> int:
        if self.y_k is not None:
            return int(self.parent_surface.get_height() * self.y_k)
        else:
            return 1

    def get_surface(self, **kwargs) -> Surface:
        return self.default_get_surface(h_size=None, v_size=None,
                                        transparent=None, color=None,
                                        flags=None,
                                        fill=True)

    def fill_surface(self, surface=None, color=None) -> None:
        self.default_fill_surface(surface, color)

    def render_text(self) -> Surface:
        if self.scale_font:
            return self.scaled_font_render()
        elif self.split_lines:
            return self.split_lines_render()
        else:
            return self.simple_render()

    def split_lines_render(self) -> Surface:
        lines = [line for line in self.str_text.splitlines() if line]
        if self.unlimited_h_size:
            return self.simple_render(lines=lines)
        else:
            lines_to_render = []
            x = 0
            space_size = self.font.size(' ')[0]
            new_line = []
            for line in lines:
                for word in line.split(' '):
                    h_s = self.font.size(word)[0]

                    if x + h_s + space_size >= self.h_size:
                        x = 0
                        lines_to_render.append(' '.join(new_line))
                        new_line.clear()
                        new_line.append(word)

                    else:
                        x += h_s + space_size
                        new_line.append(word)

                x = 0
                lines_to_render.append(' '.join(new_line))
                new_line.clear()

            return self.simple_render(lines=lines_to_render)

    def scaled_font_render(self) -> Surface:
        lines = [line for line in self.str_text.splitlines() if line]
        h_size, v_size = self.font.size(max(lines, key=len))
        font = None
        if not self.unlimited_h_size and h_size > self.h_size:
            f_size = int(self.font_size / h_size * self.h_size)
            font = get_custom_font(f_size, self.font_name)

        v_size = self.font.size(max(lines, key=len))[1] * len(lines)
        if not self.unlimited_v_size and v_size > self.v_size:
            f_size = int(self.font_size / v_size * self.v_size)
            font = get_custom_font(f_size, self.font_name)

        return self.simple_render(font)

    def simple_render(self, font=None, lines=None):
        lines = lines if lines else [line for line in self.str_text.splitlines() if line]
        if not lines:
            return get_surface(1, 1, 1)
        font = font if font else self.font
        h_size, v_size = font.size(max(lines, key=len))
        if not self.unlimited_h_size and h_size < self.h_size:
            h_size = self.h_size
        if self.unlimited_h_size:
            self.h_size = h_size

        v_size *= len(lines)

        text_surf = get_surface(h_size, v_size, transparent=1)

        y = 0
        for line in lines:
            text = self.get_rendered_text(line, font)
            if self.style.from_left or self.from_left:
                x = 0
            elif h_size > text.get_width():
                x = (h_size - text.get_width()) // 2
            else:
                x = 0

            text_surf.blit(text, (x, y))
            y += text.get_height()

        bigger = False
        if not self.unlimited_h_size and h_size > self.h_size:
            h_size = self.h_size
            bigger = True
        if not self.unlimited_v_size and v_size > self.v_size:
            bigger = True
            v_size = self.v_size

        if self.unlimited_v_size:
            self.v_size = v_size

        if bigger:
            text_surf = smoothscale(text_surf, (h_size, v_size))

        return text_surf

    def draw(self):
        self.default_draw()

    def change_text(self, text: str) -> None:
        self.str_text = self.get_localization_text(text, self.raw_text)
        self.render()

    def get_rendered_text(self, text: str, font=None) -> Surface:
        font = font if font else self.font
        return font.render(text.replace('\t', self.TAB_VALUE),
                           self.style.antialiasing_text,
                           self.color,
                           self.style.text_back_color,
                           )

    @staticmethod
    def get_localization_text(text: str, raw: bool) -> str:
        return text if raw else Global.localization.get_text_with_localization(text)

    def reload_text(self) -> None:
        self.str_text = self.get_localization_text(str(self.str_text), self.raw_text)

    def init_shape(self) -> None:
        self.shape = None

    def move(self, xy):
        self.x, self.y = xy
        if self.auto_draw:
            self.draw()
