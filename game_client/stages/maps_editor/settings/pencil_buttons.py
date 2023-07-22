from visual.UI.base.button import Button
from visual.UI.constants.attrs import ButtonAttrs
from core.world.base.logic.tiles_data import TileTypes, EmptyTile, SpawnTile


def change_tile_type(tile_type):

    def click_func(b: Button):
        b.parent.current_pencil_type = tile_type

    return click_func


PENCIL_BUTTONS = {
    EmptyTile.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{EmptyTile.name}_btn',
            ButtonAttrs.Text: EmptyTile.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(EmptyTile),
            ButtonAttrs.XK: 0.01,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },

    SpawnTile.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{SpawnTile.name}_btn',
            ButtonAttrs.Text: SpawnTile.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(SpawnTile),
            ButtonAttrs.XK: 0.05,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Field.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Field.name}_btn',
            ButtonAttrs.Text: TileTypes.Field.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Field),
            ButtonAttrs.XK: 0.09,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Forest.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Forest.name}_btn',
            ButtonAttrs.Text: TileTypes.Forest.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Forest),
            ButtonAttrs.XK: 0.13,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Hole.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Hole.name}_btn',
            ButtonAttrs.Text: TileTypes.Hole.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Hole),
            ButtonAttrs.XK: 0.17,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Ruins.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Ruins.name}_btn',
            ButtonAttrs.Text: TileTypes.Ruins.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Ruins),
            ButtonAttrs.XK: 0.21,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.PrivateHouse.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.PrivateHouse.name}_btn',
            ButtonAttrs.Text: TileTypes.PrivateHouse.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.PrivateHouse),
            ButtonAttrs.XK: 0.25,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Road.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Road.name}_btn',
            ButtonAttrs.Text: TileTypes.Road.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Road),
            ButtonAttrs.XK: 0.29,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.HighRise.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.HighRise.name}_btn',
            ButtonAttrs.Text: TileTypes.HighRise.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.HighRise),
            ButtonAttrs.XK: 0.33,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.DeepRiver.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.DeepRiver.name}_btn',
            ButtonAttrs.Text: TileTypes.DeepRiver.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.DeepRiver),
            ButtonAttrs.XK: 0.37,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Water.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Water.name}_btn',
            ButtonAttrs.Text: TileTypes.Water.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Water),
            ButtonAttrs.XK: 0.41,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Bridge.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Bridge.name}_btn',
            ButtonAttrs.Text: TileTypes.Bridge.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Bridge),
            ButtonAttrs.XK: 0.45,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
    TileTypes.Wall.name: {
        'kwargs': {
            ButtonAttrs.UID: f'{TileTypes.Wall.name}_btn',
            ButtonAttrs.Text: TileTypes.Wall.verbose_name,
            ButtonAttrs.OnClickAction: change_tile_type(TileTypes.Wall),
            ButtonAttrs.XK: 0.49,
            ButtonAttrs.YK: 0.9,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
        }
    },
}
