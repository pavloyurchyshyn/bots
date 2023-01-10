from visual.UI.base.button import Button
from game_client.stages.styles import get_green_btn_style
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs
from game_client.stages.maps_editor.settings.uids import UIDs
from game_client.stages.maps_editor.settings.menu_abs import MenuAbs
from visual.UI.yes_no_popup import YesNoPopUp
from global_obj import Global


def save(b: Button, forced=False):
    try:
        menu: MenuAbs = b.parent
        print(111, menu.current_save.default)
        menu.current_save.set_name(menu.name_inp.str_text)
        menu.current_save.set_world_to_json_data(menu.w)

        menu.current_save.save(forced)
        menu.fill_container()
        menu.unsaved_edit = False
    except FileExistsError:
        b.parent.add_popup(YesNoPopUp(f'{menu.current_save.name}_pop',
                                      text=f'Rewrite {menu.current_save.name}?',
                                      no_on_click_action=lambda n_b: n_b.parent.close(n_b),
                                      yes_on_click_action=lambda y_b: (save(b, True),
                                                                       y_b.parent.close(y_b)
                                                                       ),
                                      )
                           )


def exit_to_main_menu(b):
    if b.parent.unsaved_edit:
        b.parent.add_popup(YesNoPopUp(f'exit_to_main_pop',
                                      text=f'Exit to main menu?',
                                      no_on_click_action=lambda n_b: n_b.parent.close(n_b),
                                      yes_on_click_action=lambda y_b: (y_b.parent.close(y_b),
                                                                       Global.stages.main_menu(),
                                                                       ),
                                      )
                           )

    else:
        Global.stages.main_menu()


BUTTONS_DATA = {
    'save': {
        'kwargs': {
            ButtonAttrs.UID: UIDs.SaveMap,
            ButtonAttrs.Text: 'Save',
            ButtonAttrs.XK: 0.918,
            ButtonAttrs.YK: 0.05,
            ButtonAttrs.HSizeK: 0.08,
            ButtonAttrs.VSizeK: 0.05,
            ButtonAttrs.Style: get_green_btn_style(),
            ButtonAttrs.OnClickAction: save,
            ButtonAttrs.TextKwargs: {
                TextAttrs.FontSize: 30,
            }
        }
    },
    'exit': {
        'kwargs': {
            ButtonAttrs.UID: UIDs.Exit,
            ButtonAttrs.Text: 'X',
            ButtonAttrs.XK: 0.965,
            ButtonAttrs.YK: 0.005,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
            ButtonAttrs.OnClickAction: exit_to_main_menu,
        }
    },

}
