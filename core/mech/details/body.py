from typing import Tuple, Union
from core.mech.details.constants import *
from core.mech.details.detail import BaseDetail
from core.mech.details.slot import ArmSlot, LegSlot
__all__ = ['BaseBody', ]


class BaseBody(BaseDetail):
    detail_type = DetailsTypes.BODY

    class Sides:
        LeftSlots = 'left_slots_classes'
        RightSlots = 'right_slots_classes'

    def __init__(self, unique_id=None, damage=0, armor=0, **kwargs):
        super(BaseBody, self).__init__(unique_id=unique_id, damage=damage, armor=armor, **kwargs)

        self.left_slots_classes: Tuple[Union[ArmSlot, LegSlot]] = kwargs.get(BaseBody.Sides.LeftSlots,
                                                                             (ArmSlot, LegSlot))
        self.right_slots_classes: Tuple[Union[ArmSlot, LegSlot]] = kwargs.get(BaseBody.Sides.RightSlots,
                                                                              (ArmSlot, LegSlot))

    def get_left_slots(self) -> Tuple[Union[ArmSlot, LegSlot]]:
        return self.left_slots_classes

    def get_right_slots(self) -> Tuple[Union[ArmSlot, LegSlot]]:
        return self.right_slots_classes

    @property
    def skills(self):
        return self._skills

