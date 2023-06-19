from typing import Callable, Dict, List, Any, Optional, Tuple
from core.entities.position import EntityPositionPart
from core.entities.stats_attrs import EntityBaseAttrsPart


class EventsManagerAbc:
    Events = None
    def __init__(self, entity):
        self.entity = entity
        self.subs: Dict[str, List[Callable]] = {}

    def sub_func(self, func: Callable):
        pass


    def unsub_func(self, func: Callable):
        pass

    def do_(self, event: str, *args, **kwargs) -> List[Any]:
        pass

class EffectsManagerAbc:
    entity: 'BaseEntityAbc'
    effects: List['BaseEffect']
    def __init__(self, entity: Optional['BaseEntityAbc'] = None, effects: Optional[List['BaseEffect']] = None):
        pass

    def apply_effects(self):
        pass

    def add_effect(self, effect: 'BaseEffect'):
        pass

    def remove_effect(self, effect: 'BaseEffect'):
        pass

    def do_effects_tick(self):
        pass

    def get_effects_by_type(self, type_: str) -> Tuple['BaseEffect']:
        pass

    def get_effects_by_types(self, types: Tuple[str]) -> Tuple['BaseEffect']:
        pass

    @property
    def positive_effects(self) -> Tuple['BaseEffect']:
        pass

    @property
    def negative_effects(self) -> Tuple['BaseEffect']:
        pass


class BaseEntityAbc(EntityPositionPart, EntityBaseAttrsPart):
    events_manager: EventsManagerAbc
    effects_manager: EffectsManagerAbc