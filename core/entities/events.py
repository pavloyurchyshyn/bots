from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, List, Any


class BaseEventsEnum:
    OnDamageEvent = 'on_damage_event'
    PreDamageEvent = 'pre_damage_event'
    PostDamageEvent = 'post_damage_event'

    OnDealDamageEvent = 'on_deal_damage_event'
    PreMoveEvent = 'pre_move_event'
    PostMoveEvent = 'pre_move_event'

    PreSkillUseEvent = 'pre_skill_use_event'
    PostSkillUseEvent = 'post_skill_use_event'
    OnSkillUseEvent = 'on_skill_use_event'

    OnEffectApplyEvent = 'on_effect_apply_event'
    OnEffectEndEvent = 'on_effect_end_event'

class PreRoundEventAbcMixin(ABCMeta):
    """Before any round"""

    @abstractmethod
    def pre_round_event(self, *_, **__):
        raise NotImplementedError


class PostRoundEventAbcMixin(ABCMeta):
    """After any round"""

    @abstractmethod
    def post_round_event(self, *_, **__):
        raise NotImplementedError


class PreActionEventAbcMixin(ABCMeta):
    """Before any action"""

    @abstractmethod
    def pre_action_event(self, *_, **__):
        raise NotImplementedError


class PostActionEventAbcMixin(ABCMeta):
    """After any action"""

    @abstractmethod
    def post_action_event(self, *_, **__):
        raise NotImplementedError


class PreDamageEventAbcMixin(ABCMeta):
    """When entity getting damage"""

    @abstractmethod
    def pre_damage_event(self, damage_obj):
        raise NotImplementedError


class PostDamageEventAbcMixin(ABCMeta):
    """When entity got damage"""

    @abstractmethod
    def post_damage_event(self, damage_obj):
        raise NotImplementedError


class OnDealDamageEventAbcMixin(ABCMeta):
    """When entity dealing damage"""

    @abstractmethod
    def on_deal_damage_event(self, *_, **__):
        raise NotImplementedError


class PreMoveEventAbcMixin(ABCMeta):
    """Before entity move"""

    @abstractmethod
    def pre_move_event(self, entity, position, *args, **kwargs):
        raise NotImplementedError


class PostMoveEventAbcMixin(ABCMeta):
    """After entity move"""

    @abstractmethod
    def pre_move_event(self, entity, position, *args, **kwargs):
        raise NotImplementedError


class PreSkillUseEventAbcMixin(ABCMeta):
    """Before skill use by entity"""

    @abstractmethod
    def pre_skill_use_event(self, *_, **__):
        raise NotImplementedError


class PostSkillUseEventAbcMixin(ABCMeta):
    """After skill use by entity"""

    @abstractmethod
    def post_skill_use_event(self, *_, **__):
        raise NotImplementedError


class OnSkillUseEventAbcMixin(ABCMeta):
    """When skill used on entity"""

    @abstractmethod
    def on_skill_use_event(self, *_, **__):
        raise NotImplementedError


# class OnStunEventAbcMixin(ABCMeta):
#     """Stun used on entity"""
#
#     @abstractmethod
#     def on_stun_event(self, *_, **__):
#         raise NotImplementedError
#
#
# class OnSilenceEventAbcMixin(ABCMeta):
#     """Silence used on entity"""
#
#     @abstractmethod
#     def on_silence_event(self, *_, **__):
#         raise NotImplementedError


class OnDeathEventAbcMixin(ABCMeta):
    """Death of entity"""

    @abstractmethod
    def on_silence_event(self, *_, **__):
        raise NotImplementedError


# class OnEquipDetailEventAbcMixin(ABCMeta):
#     """When entity equips detail"""
#
#     @abstractmethod
#     def on_equip_detail_event(self, *_, **__):
#         raise NotImplementedError
#
#
class OnEffectApplyEventAbcMixin(ABCMeta):
    """When new effect applied"""

    @abstractmethod
    def on_effect_apply_event(self, *_, **__):
        raise NotImplementedError


class OnEffectEndEventAbcMixin(ABCMeta):
    """When new effect applied"""

    @abstractmethod
    def on_effect_end_event(self, *_, **__):
        raise NotImplementedError


class OnAllEventsInterface(PreDamageEventAbcMixin, PostDamageEventAbcMixin,
                           OnDealDamageEventAbcMixin,
                           PreMoveEventAbcMixin, PostMoveEventAbcMixin,
                           PreSkillUseEventAbcMixin, PostSkillUseEventAbcMixin,
                           OnSkillUseEventAbcMixin,

                           # OnStunEventAbcMixin, OnSilenceEventAbcMixin,

                           # OnDeathEventAbcMixin,
                           # OnEquipDetailEventAbcMixin,
                           OnEffectApplyEventAbcMixin, OnEffectEndEventAbcMixin,

                           PreRoundEventAbcMixin, PostRoundEventAbcMixin,
                           PreActionEventAbcMixin, PostActionEventAbcMixin,
                           metaclass=ABCMeta):
    """Class for all events"""


class EventsManager:
    Events = BaseEventsEnum

    def __init__(self, entity):
        self.entity = entity
        self.subs: Dict[str, List[Callable]] = {}

    def sub_func(self, func: Callable):
        if func.__name__ not in self.subs:
            self.subs[func.__name__] = [func]
        else:
            self.subs[func.__name__].append(func)

    def unsub_func(self, func: Callable):
        if func.__name__ in self.subs:
            if func in self.subs[func.__name__]:
                self.subs[func.__name__].remove(func)

    def do_(self, event: str, *args, **kwargs) -> List[Any]:
        # TODO do we need result
        return [func(*args, **kwargs) for func in self.subs.get(event, ())]

    def do_pre_damage_event(self, *args, **kwargs):
        self.do_(self.Events.PreDamageEvent, *args, **kwargs)

    def do_post_damage_event(self, *args, **kwargs):
        self.do_(self.Events.PostDamageEvent, *args, **kwargs)

    def do_deal_damage_event(self, *args, **kwargs):
        self.do_(self.Events.OnDealDamageEvent, *args, **kwargs)

    def do_pre_move_event(self, *args, **kwargs):
        self.do_(self.Events.PreMoveEvent, *args, **kwargs)

    def do_post_move_event(self, *args, **kwargs):
        self.do_(self.Events.PostMoveEvent, *args, **kwargs)

    def do_pre_skill_use_event(self, *args, **kwargs):
        self.do_(self.Events.PreSkillUseEvent, *args, **kwargs)

    def do_post_skill_use_event(self, *args, **kwargs):
        self.do_(self.Events.PostSkillUseEvent, *args, **kwargs)

    def do_on_skill_use_event(self, *args, **kwargs):
        self.do_(self.Events.OnSkillUseEvent, *args, **kwargs)

    # TODO check for positive or negative effect
    def on_effect_apply_event(self, effect: 'BaseEffect', *args, **kwargs):
        self.do_(self.Events.OnEffectApplyEvent, effect=effect, *args, **kwargs)

    def on_effect_end_event(self, *args, **kwargs):
        self.do_(self.Events.OnEffectEndEvent, *args, **kwargs)

    # TODO some methods for common events
    # OnStunEvent = 'on_stun_event'
    # OnSilenceEvent = 'on_silence_event'
    # OnDeathEvent = 'on_silence_event'
    # OnMechKillEvent = 'on_mech_kill_event'
    # OnMechDamageEvent = 'on_mech_damage_event'
    # OnNPCKillEvent = 'on_npc_kill_event'
    # OnNPCDamageEvent = 'on_npc_damage_event'
    # OnEquipDetailEven = 'on_equip_detail_event'
    # PreActionEvent = 'pre_action_event'
    # PostActionEvent = 'post_action_event'
    # PreRoundEvent = 'pre_round_event'
    # PostRoundEvent = 'post_round_event'
