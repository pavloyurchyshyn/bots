from abc import ABC
from typing import List
from visual.UI.base.style import Style
from visual.UI.base.button import Text
from visual.UI.base.abs import ShapeAbs
from visual.UI.constants.attrs import Attrs, TextAttrs, StyleAttrs

from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin, UpdateInterface


class PopUpBase(BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin, UpdateInterface, ShapeAbs, ABC):
    DEFAULT_H_SIZE = 0.2
    DEFAULT_V_SIZE = 0.15
    default_text_style = Style()
    default_style = Style(**{StyleAttrs.BorderSize.value: 2,
                             StyleAttrs.SurfaceColor.value: (50, 50, 50),
                             }, )

    def __init__(self, **kwargs):
        h_size_k = kwargs.pop(Attrs.HSizeK, self.DEFAULT_H_SIZE)
        v_size_k = kwargs.pop(Attrs.VSizeK, self.DEFAULT_V_SIZE)
        super(PopUpBase, self).__init__(h_size_k=h_size_k, v_size_k=v_size_k, **kwargs)
        ShapeAbs.__init__(self, **kwargs)

        text_kwargs = kwargs.pop(Attrs.TextKwargs, {})
        text = kwargs.pop(Attrs.Text, text_kwargs.pop(Attrs.Text, ''))
        raw_text = kwargs.pop(TextAttrs.RawText, text_kwargs.pop(TextAttrs.RawText, False))
        text_uid = text_kwargs.pop(Attrs.UID, f'{self.uid}_txt')
        text_kwargs[Attrs.Style] = text_kwargs.get(Attrs.Style, self.default_text_style)
        text_kwargs[Attrs.HSizeK] = text_kwargs.get(Attrs.HSizeK, 0.98)
        text_kwargs[Attrs.VSizeK] = text_kwargs.get(Attrs.VSizeK, 0.65)
        text_kwargs[Attrs.YK] = text_kwargs.get(Attrs.YK, 0.05)
        text_kwargs[TextAttrs.SplitLines] = text_kwargs.get(TextAttrs.SplitLines, True)

        self.text = Text(uid=text_uid, text=text, raw_text=raw_text, **text_kwargs, parent=self, postpone_build=True)
        self.buttons = []

    def make_inactive_and_invisible(self) -> None:
        super().make_inactive_and_invisible()
        for b in self.buttons:
            b.make_inactive_and_invisible()

    def make_active_and_visible(self) -> None:
        super().make_active_and_visible()
        for b in self.buttons:
            b.make_active_and_visible()


class PopUpsController:
    def __init__(self):
        self.popups: List[PopUpBase] = []

    def default_update_popups(self):
        if self.popups:
            self.popups[0].update()
            if self.popups[0].inactive:
                self.popups.remove(self.popups[0])

    def draw_popups(self):
        if self.popups:
            self.popups[0].draw()

    def remove_popup(self, pop_up: PopUpBase):
        if pop_up in self.popups:
            self.popups.remove(pop_up)

    def add_popup(self, pop_up: PopUpBase):
        self.popups.append(pop_up)

    def clear_popups(self):
        self.popups.clear()
