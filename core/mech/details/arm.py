from core.mech.details.detail import BaseDetail
from core.mech.details.slot import WeaponSlot
from core.mech.details.constants import *

__all__ = ['BaseArm', ]


class BaseArm(BaseDetail):
    is_limb = True
    detail_type = DetailsTypes.ARM_TYPE
    can_handle_weapon = False

    def __init__(self, unique_id=None, weapon=None, **kwargs):
        super().__init__(unique_id=unique_id, **kwargs)
        self.__weapon = WeaponSlot(weapon=weapon, is_open=self.can_handle_weapon)

    def set_weapon(self, weapon):
        self.__weapon.set_detail(weapon)

    def remove_weapon(self):
        return self.__weapon.get_and_clear()

    @property
    def weapon(self):
        if self.__weapon:
            return self.__weapon.detail
        else:
            return None
