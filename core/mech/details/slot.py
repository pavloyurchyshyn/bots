from global_obj.logger import get_logger
from core.mech.exceptions import *
from core.mech.details.detail import BaseDetail
from core.mech.details.constants import DetailsTypes
from core.mech.exceptions import SlotIsFullError, WrongDetailType

__all__ = ['BaseSlot', 'ArmSlot', 'LegSlot', 'WeaponSlot']


class BaseSlot:
    logger = get_logger()

    def __init__(self, detail: BaseDetail = None, detail_types: list[DetailsTypes: str, ] = None, is_open=True):
        self.__open = is_open
        self.__detail: BaseDetail = detail
        self.__detail_types = detail_types

    def type_is_ok(self, detail) -> bool:
        return detail.detail_type in self.__detail_types

    def switch_detail(self, detail) -> BaseDetail:
        detail_ = self.detail
        self.clear()
        try:
            self.set_detail(detail)
        except WrongDetailType as e:
            self.logger.error(e)
            self.__detail = detail_
            return detail
        else:
            self.logger.debug(f"Detail {detail_} successfully changed to {detail}")
            return detail_

    def set_detail(self, detail):
        if detail is None:
            return

        if self.is_closed:
            raise SlotIsClosed

        if self.__detail:
            raise SlotIsFullError(self)

        elif not self.type_is_ok(detail):
            raise WrongDetailType(detail, self.__detail_types)

        else:
            self.__detail = detail

    def clear(self):
        self.__detail = None

    def get_and_clear(self):
        d = self.__detail
        self.clear()
        return d

    def open(self):
        self.__open = True

    def close(self):
        self.__open = False

    @property
    def is_open(self):
        return self.__open

    @property
    def is_closed(self):
        return not self.__open

    @property
    def is_empty(self):
        return not bool(self.__detail)

    @property
    def is_full(self):
        return bool(self.__detail)

    @property
    def detail(self):
        return self.__detail

    @property
    def types(self):
        return self.__detail_types

    def __str__(self):
        return f'Slot for {self.__detail_types}'


class ArmSlot(BaseSlot):
    def __init__(self, detail: BaseDetail = None, is_open: bool = True):
        super().__init__(detail=detail, is_open=is_open,
                         detail_types=[DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE])


class LegSlot(BaseSlot):
    def __init__(self, detail: BaseDetail = None, is_open: bool = True):
        super().__init__(detail=detail, is_open=is_open,
                         detail_types=[DetailsTypes.LEG_TYPE, DetailsTypes.ARM_AND_LEG_TYPE])


class WeaponSlot(BaseSlot):
    def __init__(self, weapon=None, is_open: bool = True):
        super(WeaponSlot, self).__init__(detail=weapon, is_open=is_open, detail_types=[DetailsTypes.WEAPON_TYPE, ])
