from typing import Tuple, Union
from core.world.base.hex_utils import EntityPosition, HexMath


class EntityPositionPart:
    def __init__(self, position: Union[Tuple[int, int], EntityPosition]):
        self._position = self.get_position_obj(position=position)

    @property
    def position(self) -> Tuple[int, int]:
        return self._position.xy_id

    @position.setter
    def position(self, xy_id) -> None:
        self._position = EntityPosition(*xy_id)

    @property
    def position_qr(self) -> Tuple[int, int]:
        return self._position.qr

    @position_qr.setter
    def position_qr(self, qr):
        self._position = EntityPosition(*HexMath.qr_to_xy_id(*qr))

    @property
    def position_qrs(self) -> Tuple[int, int, int]:
        return self._position.qrs

    @staticmethod
    def get_position_obj(position: Union[Tuple[int, int], EntityPosition]) -> EntityPosition:
        return position if isinstance(position, EntityPosition) else EntityPosition(*position)

    def change_position(self, position: Union[Tuple[int, int], EntityPosition]):
        self._position = self.get_position_obj(position=position)
