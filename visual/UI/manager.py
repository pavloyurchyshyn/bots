from typing import Dict, Iterable, Union
from visual.UI.base.element import BaseUI


class NotUniqueID(Exception):
    pass


class UIManager:
    def __init__(self):
        self.uid_to_element: Dict[str, BaseUI] = {}
        self.updates_pool = []

    def reload(self) -> None:
        self.uid_to_element.clear()
        self.updates_pool.clear()

    def update(self) -> None:
        for element in self.updates_pool.copy():
            element.update()

    def add_element_to_update_pool_by_id(self, uid: str) -> None:
        if element := self.uid_to_element.get(uid):
            self.updates_pool.append(element)

    def add_element_to_update_pool(self, element: BaseUI) -> None:
        self.updates_pool.append(element)

    def remove_from_update_pool_by_id(self, uid: str) -> None:
        if element := self.uid_to_element.get(uid):
            self.remove_from_update_pool(element)

    def remove_from_update_pool(self, element: BaseUI) -> None:
        if element in self.updates_pool:
            self.updates_pool.remove(element)

    def add_element(self, element: BaseUI) -> None:
        if element.uid in self.uid_to_element:
            raise NotUniqueID
        self.uid_to_element[element.uid] = element

    def add_elements(self, elements: Iterable[BaseUI]) -> None:
        for element in elements:
            self.add_element(element)

    def get_by_uid(self, uid: str) -> Union[BaseUI, None]:
        return self.uid_to_element.get(uid)
