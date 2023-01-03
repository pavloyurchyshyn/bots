from math import cos
from pygame.draw import rect as draw_rect
from global_obj import Global
from visual.UI.base.button import Button
from visual.UI.settings import UIDefault


class CreateButtonMixin:
    buttons: list[Button]

    def create_button_from_data(self, buttons_data: dict):
        buttons = []
        for button_name, button_data in buttons_data.items():
            b = Button(*button_data.get('args', ()),
                       **button_data.get('kwargs', {}),
                       parent=self)
            buttons.append(b)
            setattr(self, button_name, b)

        buttons.sort(key=lambda e: e.y)
        buttons.sort(key=lambda e: e.layer)

        return buttons


class DrawElementBorderMixin:
    @staticmethod
    def draw_border_around_element(element: Button):
        r_c = UIDefault.CollidedElBorder.r_0 + UIDefault.CollidedElBorder.r_1 * abs(cos(Global.clock.time))
        g_c = UIDefault.CollidedElBorder.g_0 + UIDefault.CollidedElBorder.g_1 * abs(cos(Global.clock.time))
        b_c = UIDefault.CollidedElBorder.b_0 + UIDefault.CollidedElBorder.b_1 * abs(cos(Global.clock.time))
        draw_rect(Global.display, (r_c, g_c, b_c), element.shape.get_rect(), 2, *element.border_round_attrs)
