from typing import List, Any
from visual.UI.base.pop_up import PopUpBase
from visual.UI.ok_popup import OkPopUp


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

    def add_ok_popup(self, msg: str):
        self.add_popup(OkPopUp(f'ok_{len(self.popups)}', text=msg))

    def clear_popups(self):
        self.popups.clear()

    def do_popups_enter_stuff(self) -> Any:
        if self.popups:
            return self.popups[0].on_enter_action()
        else:
            return None
