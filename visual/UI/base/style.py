from typing import Tuple
from enum import Enum

from visual.UI.settings import UIDefault
from visual.UI.base.abs import StyleBaseAbs, ButtonStyleBaseAbs
from visual.UI.constants.attrs import StyleAttrs, ButtonStyleAttrs


class StyleBase:
    def __init__(self, attrs_enums: Tuple[Enum], default_style: StyleBaseAbs = None, **kwargs):
        self.dict = {}
        self.default_style = default_style
        self.attr_enums = attrs_enums
        self.collect_attrs(**kwargs)

    def collect_attrs(self, **attrs):
        for enum in self.attr_enums:
            for e in enum:
                attr = e.value
                attr_value = attrs.get(attr, getattr(self.default_style, attr, getattr(UIDefault, e.name, None)))
                setattr(self, attr, attr_value)
                self.dict[attr] = attr_value

    def get(self, key):
        return self.dict.get(key, )


class Style(StyleBase, StyleBaseAbs):
    def __init__(self, default_style=None, **kwargs):
        super().__init__(attrs_enums=(StyleAttrs,), default_style=default_style, **kwargs)


class ButtonStyle(StyleBase, ButtonStyleBaseAbs):
    def __init__(self, default_style=None, **kwargs):
        super().__init__(attrs_enums=(StyleAttrs, ButtonStyleAttrs), default_style=default_style, **kwargs)


if __name__ == '__main__':
    a = Style(surface_color=(10, 10, 10))
    print(a.dict)
    b = ButtonStyle()
    print(b.dict)
