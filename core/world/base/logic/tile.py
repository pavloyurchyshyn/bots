from typing import Union
from core.world.base.logic.tiles_data import TileDataAbs, IMPASSABLE_VALUE, TileTypes


class LogicTile:

    def __init__(self, xy_id: tuple[int, int], tile_data: Union[str, TileDataAbs], at_edge: bool = False):
        self.id_x, self.id_y = xy_id

        if type(tile_data) is str:
            tile_data = TileTypes.types_dict[tile_data]
        self.tile_data = tile_data
        self.name = tile_data.name
        self.verbose_name = tile_data.verbose_name
        self.hp: float = tile_data.hp
        self.eternal: bool = tile_data.eternal
        self.move_energy_k: float = tile_data.move_energy_k
        self.destroyed_type: Union[str, TileDataAbs, None] = tile_data.destroyed_type
        self.direction = tile_data.direction
        self.height = tile_data.height
        self.at_edge = at_edge

    def apply_type(self, tile_type: Union[str, TileDataAbs]) -> None:
        tile_type = TileTypes.types_dict[tile_type] if type(tile_type) is str else tile_type
        self.tile_data = tile_type
        self.name = tile_type.name
        self.hp: float = tile_type.hp
        self.eternal: bool = tile_type.eternal
        self.move_energy_k: float = tile_type.move_energy_k
        self.destroyed_type: Union[str, TileDataAbs, None] = tile_type.destroyed_type

    def damage(self, dmg: float) -> None:
        if not self.eternal and self.hp > 0:
            self.hp -= dmg
            if self.hp < 0:
                self.hp = 0

            if self.hp <= 0.:
                if self.destroyed_type:
                    self.apply_type(self.destroyed_type)
                else:
                    if self.hp < 0:
                        self.hp = 0
                    self.eternal = True

    @property
    def passable(self):
        return self.move_energy_k != IMPASSABLE_VALUE

    def get_data_dict(self):
        return self.tile_data.parameters_to_dict(self)

    @property
    def id_xy(self) -> tuple:
        return self.id_x, self.id_y


if __name__ == '__main__':
    tile = LogicTile((0, 0), TileTypes.PrivateHouse)
    print(tile.__dict__)
    tile.damage(tile.hp)
    print(tile.__dict__)
    tile = LogicTile((0, 0), TileTypes.Field)
    print(tile.__dict__)
    tile.damage(tile.hp)
    print(tile.__dict__)

    print(tile.get_data_dict())
