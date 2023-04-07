from visual.UI.base.button import Button
from core.world.base.visual.world import VisualWorld
from visual.UI.base.input import InputBase
from visual.UI.base.container import Container
from core.world.maps_manager import MapsManager
from core.world.base.map_save import MapSave


class MenuAbs:
    save: Button
    w: VisualWorld
    maps_mngr: MapsManager
    current_save: MapSave
    name_inp: InputBase
    maps_container: Container
    unsaved_edit: bool
