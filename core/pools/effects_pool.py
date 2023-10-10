import inspect
from typing import Type, Dict
from core import vanilla_effects as effects_module


class EffectsPool:
    def __init__(self):
        self.classes_dict: Dict[str, Type] = {}
        self.collect_effects_classes()

    def collect_effects_classes(self):
        self.classes_dict.clear()
        for _, effect_class in inspect.getmembers(effects_module, inspect.isclass):
            self.classes_dict[effect_class.name] = effect_class

    def get_class_by_name(self, name: str):
        return self.classes_dict.get(name)
