from logging import Logger
from typing import Dict, Union, Type, List

from core.mech.base.mech import BaseMech
from core.mech.base.details.detail import BaseDetail
from interfaces.skills_pool_interface import SkillsPoolInterface

from game_logic.game_data.id_generator import IdGenerator


class DetailsPoolInterface:
    logger: Logger
    skills_pool: SkillsPoolInterface
    details: List[BaseDetail]
    id_to_detail: Dict[str, BaseDetail]
    classes_dict: Dict[str, Type[BaseDetail]]
    id_generator: IdGenerator

    def get_class_by_name(self, name: str):
        pass

    def load_details_classes_list(self, details_list: [(str, int), ]):
        pass

    def get_detail_by_id(self, unique_id: str) -> Union[BaseDetail, 'BaseBody']:
        pass

    def create_add_and_get_detail_to_pool(self, detail_class_name: str,
                                          unique_id: str = None) -> Union[BaseDetail, 'BaseBody']:
        pass

    def add_detail_to_pool(self, detail: BaseDetail) -> None:
        pass

    def get_new_detail_by_class_name(self, detail_class_name: str, unique_id: str = None) -> Type[BaseDetail]:
        pass

    def collect_details_classes(self):
        pass

    def get_dict(self):
        pass

    def get_simple_mech(self, position=(0, 0)) -> BaseMech:
        pass

