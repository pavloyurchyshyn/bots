from visual.UI.base.input import InputBase
from game_client.stages.maps_editor.settings.uids import UIDs
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs
from game_client.stages.styles import get_btn_style
from visual.UI.constants.attrs import ButtonStyleAttrs
BUTTONS_DATA = {
    'save': {
        'kwargs': {
            ButtonAttrs.UID: UIDs.SaveMap,
            ButtonAttrs.Text: 'Save',
            ButtonAttrs.XK: 0.920,
            ButtonAttrs.YK: 0.005,
            ButtonAttrs.HSizeK: 0.08,
            ButtonAttrs.VSizeK: 0.05,
            ButtonAttrs.Style: get_btn_style(),
        }
    }

}
