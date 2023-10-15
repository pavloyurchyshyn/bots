from core.world.base.logic.tile_data.tile_abs import TileDataAbs
from core.world.base.logic.tile_data.const import IMPASSABLE_VALUE, TileAttrs


class EmptyTile(TileDataAbs):
    name = 'empty'
    verbose_name = 'Empty'
    hp = 0
    move_energy_k: float = IMPASSABLE_VALUE
    eternal: bool = True
    destroyed_type = None
    height: int = 0
    color = (0, 0, 20, 0)

    def __init__(self, **kwargs):
        super().__init__()


class SpawnTile(TileDataAbs):
    name = 'spawn'
    verbose_name = 'Spawn'
    eternal = True
    destroyed_type = None
    height = 0
    spawn = True


class TileData(TileDataAbs):
    destroyed_type: TileDataAbs = None


class EternalTileData(TileDataAbs):
    eternal = True
    destroyed_type: TileDataAbs = None


class TilesNames:
    Ruins = 'ruins'
    Field = 'field'
    Hole = 'hole'
    PrivateHouse = 'privath'
    Forest = 'forest'
    Road = 'road'
    HighRise = 'highh'
    Water = 'water'
    DeepWater = 'deepwater'
    Bridge = 'bridge'
    HighBridge = 'hbridge'
    Wall = 'wall'


class TileTypes:
    class Hole(EternalTileData):
        verbose_name = 'Hole'
        name = TilesNames.Hole
        move_energy_k = 0.2
        color = (50, 100, 50)
        height = 0

    class Field(TileData):
        verbose_name = 'Field'
        name = TilesNames.Field
        hp = 50
        destroyed_type = TilesNames.Hole
        color = (170, 235, 20)
        height = 0

    class Ruins(EternalTileData):
        verbose_name = 'Ruins'
        name = TilesNames.Ruins
        move_energy_k = 0.2
        color = (50, 50, 50)
        height = 3

    class PrivateHouse(TileData):
        name = TilesNames.PrivateHouse
        verbose_name = 'Private house'
        hp = 50
        move_energy_k = 0.5
        destroyed_type = TilesNames.Ruins
        height = 3
        color = (150, 150, 50)

    class Forest(TileData):
        verbose_name = 'Forest'
        name = TilesNames.Forest
        hp = 10
        color = (0, 150, 50)
        height = 30

    class Road(TileData):
        name = TilesNames.Road
        verbose_name = 'Road'
        hp = 0
        move_energy_k = -0.1
        color = (10, 10, 10)
        height = 0

    class HighRise(TileData):
        name = TilesNames.HighRise
        verbose_name = 'High rise'
        hp = 200
        move_energy_k = IMPASSABLE_VALUE
        color = (150, 150, 150)
        height = 20

    class DeepRiver(EternalTileData):
        name = TilesNames.DeepWater
        verbose_name = 'Deep river'
        hp = 0
        eternal = True
        move_energy_k = 1.
        color = (50, 50, 150)
        height = 0

    class Water(TileData):
        name = TilesNames.Water
        verbose_name = 'Water'
        hp = 0
        eternal = True
        move_energy_k = 0.5
        destroyed_type = TilesNames.DeepWater
        color = (50, 50, 250)
        height = 0

    class Bridge(TileData):
        name = TilesNames.Bridge
        verbose_name = 'Bridge'
        hp = 100
        move_energy_k = -0.1
        destroyed_type = TilesNames.Water
        color = (50, 50, 150)
        height = 0

    class HighBridge(TileData):
        name = TilesNames.HighBridge
        verbose_name = 'High bridge'
        hp = 200
        move_energy_k = -0.3
        destroyed_type = TilesNames.Water
        color = (50, 50, 150)
        height = 0

    class Wall(TileData):
        name = TilesNames.Wall
        verbose_name = 'Wall'
        hp = 50
        move_energy_k = IMPASSABLE_VALUE
        destroyed_type = TilesNames.Ruins
        color = (50, 50, 150)
        height = 10

    types_dict = {
        Ruins.name: Ruins,
        PrivateHouse.name: PrivateHouse,
        Forest.name: Forest,
        Road.name: Road,
        HighRise.name: HighRise,
        Water.name: Water,
        DeepRiver.name: DeepRiver,
        Bridge.name: Bridge,
        # HighBridge.name: HighBridge,
        # Wall.name: Wall,
        Field.name: Field,
        # Hole.name: Hole,
        SpawnTile.name: SpawnTile,
        EmptyTile.name: EmptyTile,
    }


def get_tile_from_dict_data(data: dict) -> TileDataAbs:
    return TileTypes.types_dict.get(data[TileAttrs.Name], TileData)(**data)

