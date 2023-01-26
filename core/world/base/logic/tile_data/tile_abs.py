from core.world.base.logic.tile_data.const import TileAttrs


class TileDataAbs:
    name: str
    verbose_name: str
    hp: float = 0.
    move_energy_k: float = 0.
    eternal: bool = False
    destroyed_type = None
    height: int = 0

    img: int = 0
    direction: int = 0

    def __init__(self, **kwargs):
        self.name = kwargs[TileAttrs.Name] if TileAttrs.Name in kwargs else self.name
        self.verbose_name = kwargs[TileAttrs.VerboseName] if TileAttrs.VerboseName in kwargs else self.verbose_name
        self.hp = kwargs.get(TileAttrs.Hp, self.hp)

        self.move_energy_k = kwargs.get(TileAttrs.MoveEnergyK, self.move_energy_k)
        self.move_energy_k = kwargs[TileAttrs.MoveEnergyK] if TileAttrs.MoveEnergyK in kwargs else self.move_energy_k
        self.eternal = kwargs.get(TileAttrs.Eternal, self.eternal)
        self.destroyed_type = kwargs.get(TileAttrs.DestroyedType, self.destroyed_type)
        self.height = kwargs.get(TileAttrs.Height, self.height)
        self.init_additional_attrs(**kwargs)

        self.direction = kwargs.get(TileAttrs.Direction, 0)
        self.img = kwargs.get(TileAttrs.Img, 0)

    def init_additional_attrs(self, **kwargs):
        pass

    def get_data_dict(self) -> dict:
        return self.parameters_to_dict(self)

    @staticmethod
    def parameters_to_dict(self) -> dict:
        des_type = None
        if self.destroyed_type:
            des_type = self.destroyed_type if type(self.destroyed_type) is str else self.destroyed_type.name
        return {
            TileAttrs.Name: self.name,
            TileAttrs.Hp: self.hp,
            TileAttrs.MoveEnergyK: self.move_energy_k,
            TileAttrs.Eternal: self.eternal,
            TileAttrs.DestroyedType: des_type,
            TileAttrs.VerboseName: self.verbose_name,
            TileAttrs.Direction: self.direction,
            TileAttrs.Height: self.height,
            TileAttrs.Img: self.img,
        }
