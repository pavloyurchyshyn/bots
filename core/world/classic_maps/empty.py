from core.world.base.map_save import MapSave


class Empty(MapSave):
    default = True

    def __init__(self, x_size=53, y_size=30):
        dict_tiles_data = [[0 for _ in range(x_size)] for _ in range(y_size)]
        super(Empty, self).__init__(name='Empty',
                                    path='classic',
                                    dict_tiles_data=dict_tiles_data,
                                    odd=True,
                                    flat=True,
                                    )
