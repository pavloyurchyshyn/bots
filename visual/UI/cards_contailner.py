from typing import List
from visual.UI.base.element import BaseUI
from visual.UI.base.abs import ShapeAbs
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin


class CardsContainer(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._cards: List
