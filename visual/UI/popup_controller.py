from typing import List, Any, Callable
from visual.UI.base.pop_up import PopUpBase
from visual.UI.ok_popup import OkPopUp
from visual.UI.yes_no_popup import YesNoPopUp


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

    def add_ok_popup(self, msg: str, ok_text: str = None, raw_text: bool = False):
        self.add_popup(OkPopUp(f'ok_{len(self.popups)}_popup', text=msg,
                               raw_text=raw_text, ok_text=ok_text))

    def add_yes_no_popup(self, msg: str, raw_text: bool = False,
                         yes_text: str = None, no_text: str = None,
                         yes_uid: str = None, no_uid: str = None,
                         on_click_action: Callable = None,
                         yes_is_default: bool = True,
                         yes_action: Callable = None, no_action: Callable = None, parent=None):

        no_action = no_action if no_action else lambda button: button.parent.close(button)
        self.add_popup(YesNoPopUp(uid=f'yes_{len(self.popups)}_popup',
                                  text=msg, raw_text=raw_text,
                                  yes_text=yes_text, no_text=no_text,
                                  yes_uid=yes_uid, no_uid=no_uid,
                                  yes_on_click_action=yes_action, no_on_click_action=no_action,
                                  yes_is_default=yes_is_default,
                                  on_click_action=on_click_action,
                                  parent=parent))

    def clear_popups(self):
        self.popups.clear()

    def do_popups_enter_stuff(self) -> Any:
        if self.popups:
            return self.popups[0].on_enter_action()
        else:
            return None
