import inspect
from typing import Dict, Union
from global_obj.logger import get_logger

from core.mech.mech import BaseMech
from core.vanilla_details.names import DetailNames
from core import vanilla_details as details_module
from core.mech.details.detail import BaseDetail
from core.mech.exceptions import ThisDetailClassDoesntExist
from core.pools.skills_pool import SkillsPool

from game_logic.game_data.id_generator import IdGenerator


class DetailsPool:
    logger = get_logger()

    def __init__(self, id_generator: IdGenerator):
        self.skills_pool: SkillsPool = SkillsPool()
        self.details = []
        self.id_to_detail: Dict[str, BaseDetail] = {}
        self.classes_dict: dict = {}
        self.collect_details_classes()
        self.id_generator: IdGenerator = id_generator

    def get_class_by_name(self, name: str):
        return self.classes_dict.get(name)

    def load_details_classes_list(self, details_list: [(str, int), ]):
        """
        List of tuples where first value class name. the second detail id.
        """
        self.details.clear()
        self.id_to_detail.clear()
        self.logger.debug(f'Loading list: {len(details_list)} {details_list}')
        for class_name, unique_id in details_list:
            self.create_add_and_get_detail_to_pool(class_name, unique_id)
        self.logger.debug(f'Details loaded {tuple(map(str, self.details))}')

    def get_detail_by_id(self, unique_id: str) -> Union[BaseDetail, 'BaseBody']:
        return self.id_to_detail.get(unique_id)

    def create_add_and_get_detail_to_pool(self, detail_class_name: str,
                                          unique_id: str = None) -> [BaseDetail, 'BaseBody']:
        detail = self.get_new_detail_by_class_name(detail_class_name, unique_id=unique_id)
        self.add_detail_to_pool(detail)
        return detail

    def add_detail_to_pool(self, detail: BaseDetail) -> None:
        self.details.append(detail)
        self.id_to_detail[detail.unique_id] = detail
        for skill in detail.skills:
            self.skills_pool.add_skill(skill)

    def get_new_detail_by_class_name(self, detail_class_name: str, unique_id: str = None) -> BaseDetail:
        unique_id = self.id_generator.get_id() if unique_id is None else unique_id
        detail_class = self.classes_dict.get(detail_class_name)
        if detail_class is None:
            raise ThisDetailClassDoesntExist(detail_class_name)
        return detail_class(unique_id=unique_id)

    def collect_details_classes(self):
        self.classes_dict.clear()
        for part in inspect.getmembers(details_module, inspect.isclass):
            self.classes_dict[part[1].name] = part[1]

    def get_dict(self):
        return [(detail.name, unique_id) for unique_id, detail in self.id_to_detail.items()]

    def get_simple_mech(self, position=(0, 0)) -> BaseMech:
        mech: BaseMech = BaseMech(position)
        body = self.create_add_and_get_detail_to_pool(DetailNames.SimpleMetal.Body)
        mech.set_body(body)

        left_arm = self.create_add_and_get_detail_to_pool(DetailNames.SimpleMetal.Arm)
        mech.set_left_detail(0, left_arm)
        right_arm = self.create_add_and_get_detail_to_pool(DetailNames.SimpleMetal.Arm)
        mech.set_right_detail(0, right_arm)

        left_leg = self.create_add_and_get_detail_to_pool(DetailNames.SimpleMetal.Leg)
        mech.set_left_detail(1, left_leg)
        right_leg = self.create_add_and_get_detail_to_pool(DetailNames.SimpleMetal.Leg)
        mech.set_right_detail(1, right_leg)

        mech.refill_energy_and_hp()

        return mech

