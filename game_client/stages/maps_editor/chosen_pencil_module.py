from typing import Optional
from pygame import Surface
from game_client.stages.maps_editor.settings.pencil_buttons import PencilElement
from core.world.base.logic.tile_data.tile_abs import TileDataAbs
from game_client.stages.maps_editor.settings.other import PencilIconRect, MapsButtonsContainer,\
    PencilNameRect, PencilAttrsSizes
from pygame.draw import rect as draw_rect
from global_obj.main import Global
from visual.UI.base.text import Text
from core.shape.hex import Hex
from visual.UI.utils import get_surface
from pygame import draw
from settings.visual.graphic import GraphicConfig
from core.world.base.logic.tiles_data import TileTypes
from visual.UI.base.container import Container


class ChosenPencilModule:
    def __init__(self):
        self.icon_tile_radius: int = PencilIconRect.H_size // 2
        self.chosen_pencil: Optional[PencilElement] = None
        self.pencils_container: Container = Container('pencils_container', True,
                                                      parent=self,
                                                      x_k=0.802, y_k=0.55,
                                                      h_size_k=MapsButtonsContainer.H_size,
                                                      v_size_k=MapsButtonsContainer.V_size
                                                      )

        self.pencil_name_txt: Text = Text('pencil_name_txt',
                                          x_k=PencilNameRect.X, y_k=PencilNameRect.Y,
                                          h_size_k=PencilNameRect.H_size, v_size_k=PencilNameRect.V_size)

        self.pencil_hp_txt: Text = Text(uid=f'pencil_hp_txt', from_left=True,
                                        x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.HP_Y,
                                        h_size_k=PencilAttrsSizes.H_size, v_size_k=PencilAttrsSizes.V_size)

        self.pencil_eternal_txt: Text = Text(uid=f'pencil_eternal_txt', from_left=True,
                                             x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.Eternal_Y,
                                             h_size_k=PencilAttrsSizes.H_size, v_size_k=PencilAttrsSizes.V_size)

        self.pencil_height_txt: Text = Text(uid=f'pencil_height_txt', from_left=True,
                                            x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.Height_Y,
                                            h_size_k=PencilAttrsSizes.H_size, v_size_k=PencilAttrsSizes.V_size)

        self.pencil_spawn_txt: Text = Text(uid=f'pencil_spawn_txt', from_left=True,
                                           x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.Spawn_Y,
                                           h_size_k=PencilAttrsSizes.H_size, v_size_k=PencilAttrsSizes.V_size)

        self.pencil_move_energy_k_txt: Text = Text(uid=f'pencil_move_energy_k_txt', from_left=True,
                                                   x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.MoveEnrgK_Y,
                                                   h_size_k=PencilAttrsSizes.H_size,
                                                   v_size_k=PencilAttrsSizes.V_size)

        self.pencil_walkable_txt: Text = Text(uid=f'pencil_walkable_txt', from_left=True,
                                              x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.Walkable_Y,
                                              h_size_k=PencilAttrsSizes.H_size,
                                              v_size_k=PencilAttrsSizes.V_size)

        self.pencil_destroyed_type_txt: Text = Text(uid=f'pencil_destroyed_type_txt', from_left=True,
                                                    x_k=PencilAttrsSizes.X, y_k=PencilAttrsSizes.DestType_Y,
                                                    h_size_k=PencilAttrsSizes.H_size,
                                                    v_size_k=PencilAttrsSizes.V_size)

        self.chosen_pencil: PencilElement = None

        self.pencil_icon: Optional[Surface] = None
        self.missing_pencil_texture: Surface = None
        self.render_pencil_missing_texture()
        self.pencil_tile_icon: Surface = None
        w = Hex(0, 0, r=self.icon_tile_radius).width
        self.pencil_icon_surface_size = w, w

        self.fill_pencils_container()
        self.update_pencil_tile_icon()

    def update_draw_pencils_container(self):
        self.pencils_container.draw()
        if self.pencils_container.collide_point(Global.mouse.pos):
            self.pencils_container.change_dy(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.pencils_container.elements:
                el: PencilElement
                if el.collide_point(mouse_pos):
                    self.draw_border_around_element(el)
                    if Global.mouse.l_up:
                        # el.choose_btn.do_action()
                        el.choose()
                        self.pencils_container.render()
                        break

    def draw_current_pencil_attrs(self):
        self.pencil_name_txt.draw()
        self.pencil_hp_txt.draw()
        self.pencil_eternal_txt.draw()
        self.pencil_height_txt.draw()
        self.pencil_spawn_txt.draw()
        self.pencil_move_energy_k_txt.draw()
        self.pencil_walkable_txt.draw()
        self.pencil_destroyed_type_txt.draw()

    def fill_pencils_container(self):
        self.pencils_container.clear()
        for tile_type in TileTypes.types_dict.values():
            self.pencils_container.add_element(PencilElement(tile_type, parent=self.pencils_container).build())
        self.pencils_container.build()
        self.pencils_container.elements[0].choose()
        self.pencils_container.render()

    def render_pencil_missing_texture(self):
        tile_size = self.pencil_icon_size
        surface: Surface = get_surface(h_size=tile_size[0], v_size=tile_size[1], transparent=1)
        draw.polygon(surface, (200, 0, 0), Hex(0, (tile_size[1] - tile_size[0]) / 2, tile_size[0] // 2).dots[1:])
        text = Text('', text='?', parent_surface=surface, font_size=GraphicConfig.FontSize * 3)
        text.draw()
        self.missing_pencil_texture = surface

    @property
    def pencil_icon_size(self) -> tuple:
        return PencilIconRect.H_size, PencilIconRect.V_size

    @property
    def pencil_icon_position(self) -> tuple:
        return PencilIconRect.X, PencilIconRect.Y

    @property
    def current_pencil_type(self) -> TileDataAbs:
        return self.chosen_pencil.tile_class

    def draw_pencil_icon(self):
        draw_rect(Global.display, (255, 255, 255), PencilIconRect.rect, 1)
        Global.display.blit(self.pencil_tile_icon, self.pencil_icon_position)

    def update_pencil_tile_icon(self):
        self.pencil_name_txt.change_text(self.chosen_pencil.tile_class.verbose_name)
        self.pencil_hp_txt.change_text(f'HP: {int(self.chosen_pencil.tile_class.hp)}')
        self.pencil_eternal_txt.change_text(f'Destroyable: {not self.chosen_pencil.tile_class.eternal}')
        self.pencil_height_txt.change_text(f'Height: {self.chosen_pencil.tile_class.height}')
        self.pencil_spawn_txt.change_text(f'Spawn: {bool(self.chosen_pencil.tile_class.spawn)}')
        self.pencil_move_energy_k_txt.change_text(f'Move energy k: {self.chosen_pencil.tile_class.move_energy_k}')
        self.pencil_walkable_txt.change_text(f'Walkable: {self.chosen_pencil.tile_class.move_energy_k != float("inf")}')
        self.pencil_destroyed_type_txt.change_text(f'Destroyed type: {self.chosen_pencil.tile_class.destroyed_type}')
        self.pencil_tile_icon = self.get_icon_surface()

    def get_icon_surface(self) -> Surface:
        tile = self.current_pencil_type
        try:
            return Global.textures.get_scaled_tile_texture(tile_type=tile.name,
                                                           img=tile.img,
                                                           size=self.pencil_icon_surface_size,
                                                           raise_error=True)
        except Exception:
            return self.missing_pencil_texture
