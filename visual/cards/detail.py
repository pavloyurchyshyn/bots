from visual.cards.base import Card
from core.mech.base.details.detail import BaseDetail
from visual.UI.utils import get_surface
from visual.UI.base.text import Text
from settings.visual.cards import DetailCardSize
from visual.UI.base.style import Style


class DetailCard(Card):

    def __init__(self, uid: str,
                 detail: BaseDetail,
                 x, y,
                 style: Style = None,
                 size_x=DetailCardSize.X_SIZE, size_y=DetailCardSize.Y_SIZE):
        super().__init__(uid, x, y, style=style, size_x=size_x, size_y=size_y)
        self.detail: BaseDetail = detail
        self.surface = get_surface(self.size_x, self.size_y, color=(50, 50, 50))
        self.text: Text = Text(uid='',
                               text=detail.verbal_name,  # TODO add localization
                               y_k=0.01,
                               v_size_k=0.2,
                               h_size_k=0.98,
                               parent_surface=self.surface, auto_draw=False)
        self.render()

    def render(self):
        self.fill_surface_due_to_border_attrs(self.surface, (50, 50, 50))
        self.text.draw()
        self.draw_border(self.surface)
