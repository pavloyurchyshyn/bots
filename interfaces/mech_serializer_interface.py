from logging import Logger
from core.mech.mech import BaseMech
from interfaces.details_pool_interface import DetailsPoolInterface


class MechSerializerInterface:
    logger: Logger
    details_pool: DetailsPoolInterface

    def mech_to_dict(self, mech: BaseMech) -> dict:
        pass

    def dict_to_mech(self, data: dict) -> BaseMech:
        pass

    def update_mech_details(self, mech: BaseMech, data: dict):
        pass

