from pygame import Surface
from pygame.transform import smoothscale
from global_obj.main import Global
from visual.UI.utils import get_surface
from visual.UI.base.element import BaseUI
from visual.UI.base.font import get_custom_font
from visual.UI.constants.attrs import Attrs, TextAttrs
from settings.visual.graphic import GraphicConfig


class Text(BaseUI):
    TAB_VALUE = '  '

    def __init__(self, uid: str, text: str = '', raw_text=True, color=None, **kwargs):

        super().__init__(uid=uid, **kwargs, build_surface=True)
        self.color = color if color else self.style.color
        self.raw_text = raw_text
        self.capitalize = kwargs.get(TextAttrs.Capitalize, False)
        self.original_text = text
        self.str_text = self.get_localization_text(str(text), self.raw_text)
        if self.capitalize:
            self.str_text = self.str_text.capitalize()

        self.unlimited_h_size = kwargs.get(TextAttrs.UnlimitedHSize, False)
        self.unlimited_v_size = kwargs.get(TextAttrs.UnlimitedVSize, False)

        self.font_size = kwargs.get(TextAttrs.FontSize, GraphicConfig.FontSize)
        self.font_name = kwargs.get(TextAttrs.FontName, GraphicConfig.FontName)
        self.font = get_custom_font(self.font_size, self.font_name)

        self.scale_font = kwargs.get(TextAttrs.ScaleFont, False)

        self.split_lines = kwargs.get(TextAttrs.SplitLines, True)
        self.split_words = kwargs.get(TextAttrs.SplitWords, True)

        self.auto_draw = kwargs.get(Attrs.AutoDraw, True)

        self.from_left = kwargs.get(TextAttrs.FromLeft, False)

        if not kwargs.get(Attrs.PostponeBuild, False):
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
            x = 2
        else:
            x = (self.surface.get_width() - rendered_text.get_width()) // 2

        if self.style.from_top:
            y = 1
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
        lines = [line for line in self.str_text.replace('.', " ").splitlines() if line]
        if self.unlimited_h_size:
            return self.simple_render(lines=lines)
        else:
            lines_to_render = []
            x = 0
            space_size = self.font.size(' ')[0]
            new_line = []
            for line in lines:
                for word in line.split(' '):
                    if not word:
                        continue

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
        if not self.unlimited_h_size and self.h_size_is_bigger(h_size):
            f_size = int(self.font_size / h_size * self.h_size)
            font = get_custom_font(f_size, self.font_name)

        v_size = self.font.size(max(lines, key=len))[1] * len(lines)
        if not self.unlimited_v_size and self.v_size_is_bigger(v_size):
            f_size = int(self.font_size / v_size * self.v_size)
            font = get_custom_font(f_size, self.font_name)

        return self.simple_render(font)

    def split_lines_words(self, lines, font):
        if not self.h_size_is_bigger(font.size(max(lines, key=len))[0]):
            return lines

        lines_ = []
        space_size = self.font.size(' ')[0]
        new_line = []
        for line_i in range(len(lines)):
            line = lines[line_i].split()
            if new_line:
                line = [*new_line, *line]
                new_line.clear()

            line_h = font.size(" ".join(line))[0]
            if self.h_size_is_bigger(line_h):
                line_h_ = 0
                for word in line:
                    word_size = font.size(word)[0]
                    line_h__ = line_h_ + word_size
                    if self.h_size_is_bigger(line_h__):
                        d_size = line_h__ - self.h_size
                        px_per_letter = word_size / len(word)
                        if d_size >= word_size or (px_per_letter >= d_size and d_size <= word_size):
                            lines_.append(" ".join(new_line))
                            new_line.clear()
                            new_line.append(word)
                        else:
                            letters_count = int(d_size // px_per_letter) - 2
                            new_line.append(word[:letters_count])
                            lines_.append(" ".join(new_line))
                            new_line.clear()
                            new_line.append(word[letters_count:])

                    else:
                        new_line.append(word)
                        line_h_ += space_size + word_size
            else:
                lines_.append(lines[line_i])
                continue

        lines_.append(" ".join(new_line))
        new_line.clear()

        return lines_

    def v_size_is_bigger(self, v_size):
        return v_size > self.v_size - 1

    def h_size_is_bigger(self, h_size):
        return h_size > self.h_size - 1

    def simple_render(self, font=None, lines=None):
        lines = lines if lines else [line for line in self.str_text.splitlines() if line]
        if not lines:
            return get_surface(1, 1, 1)
        font = font if font else self.font

        if self.split_words and not self.unlimited_h_size:
            lines = self.split_lines_words(lines=lines, font=font)

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
        v_k = 1
        h_k = 1
        if not self.unlimited_h_size and h_size > self.h_size:
            h_k = h_size / self.h_size
            bigger = True
        if not self.unlimited_v_size and v_size > self.v_size:
            v_k = v_size / self.v_size
            bigger = True

        if self.unlimited_v_size:
            self.v_size = v_size

        if bigger:
            k = v_k if v_k > h_k else h_k
            text_surf = smoothscale(text_surf, (h_size // k, v_size // k))

        return text_surf

    def draw(self, parent_surface: Surface = None, dx: int = 0, dy: int = 0):
        self.default_draw(parent_surface=parent_surface, dx=dx, dy=dy)

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
        return str(text) if raw else str(Global.localization.get_text_with_localization(text))

    def reload_text(self) -> None:
        self.str_text = self.get_localization_text(str(self.str_text), self.raw_text)

    def init_shape(self) -> None:
        self.shape = None

    def move(self, xy):
        self.x, self.y = xy
        if self.auto_draw:
            self.draw()

    def change_color(self, color):
        if self.color != color:
            self.color = color
            self.render()
