from game_client.stages.maps_editor.settings.uids import UIDs
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs
from game_client.stages.styles import get_green_btn_style
from core.world.base.logic.save_and_load_map import save_world
from visual.UI.base.button import Button


def save(b: Button):
    world = b.parent.w
    world_name = b.parent.name_inp.str_text
    save_world(world_name, world)


BUTTONS_DATA = {
    'save': {
        'kwargs': {
            ButtonAttrs.UID: UIDs.SaveMap,
            ButtonAttrs.Text: 'Save',
            ButtonAttrs.XK: 0.918,
            ButtonAttrs.YK: 0.005,
            ButtonAttrs.HSizeK: 0.08,
            ButtonAttrs.VSizeK: 0.05,
            ButtonAttrs.Style: get_green_btn_style(),
            ButtonAttrs.OnClickAction: save,
            ButtonAttrs.TextKwargs: {
                TextAttrs.FontSize: 30,
            }
        }
    }

}
