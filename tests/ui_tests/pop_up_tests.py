from launch import GameRunner
from visual.UI.ok_popup import OkPopUp
from visual.UI.yes_no_popup import YesNoPopUp
from visual.UI.base.pop_up import PopUpsController
from global_obj import Global


class Body:
    def __init__(self):
        self.popups = PopUpsController()

        self.popups.add_popup(YesNoPopUp('test_pop_yes_no', text='Do you want to close popup?',
                                         yes_on_click_action=lambda b: b.parent.close(b)))
        self.popups.add_popup(OkPopUp('test_pop_1', text='aaa'))
        self.popups.add_popup(OkPopUp('test_pop_1', text='This is a normal message, just click Ok!'))
        self.popups.add_popup(OkPopUp('test_pop_2',
                                      text="0" * 100, ))
        self.popups.add_popup(OkPopUp('test_pop_3',
                                      h_size_k=0.5,
                                      text="\tThis is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
                                           "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
                                           "\t\t\tThis function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
                                           "text will disappear underneath the surface", ))

    def game_loop(self):
        if Global.mouse.l_up and not self.popups.popups:
            raise Exception

        self.popups.default_update_popups()
        self.popups.draw_popups()


if __name__ == '__main__':
    GameRunner(Body()).run()
