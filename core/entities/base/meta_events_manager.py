from typing import List, Any
from global_obj.main import Global
from core.entities.base.entity import BaseEntity
from core.entities.base.events import BaseEventsEnum


# TODO
class MetaEventsManager:
    def __init__(self):
        self.entities: List[BaseEntity] = []

    def react_on_event(self, event: str, *args, **kwargs) -> Any:
        return [entity.events_manager.do_(event, *args, **kwargs) for entity in self.entities]


    def add_entity(self, entity: BaseEntity):
        self.entities.append(entity)


    def remove_entity(self, entity: BaseEntity):
        if entity in self.entities:
            self.entities.remove(entity)

    def do_pre_action_event(self, *args, **kwargs):
        self.react_on_event(event=BaseEventsEnum.PreActionEvent, *args, **kwargs)


    def do_post_action_event(self, *args, **kwargs):
        self.react_on_event(event=BaseEventsEnum.PostActionEvent, *args, **kwargs)

    def do_pre_round_event(self, *args, **kwargs):
        self.react_on_event(event=BaseEventsEnum.PreRoundEvent, *args, **kwargs)

    def do_post_round_event(self, *args, **kwargs):
        self.react_on_event(event=BaseEventsEnum.PostRoundEvent, *args, **kwargs)