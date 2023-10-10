
from typing import Type

from global_obj.main import Global
from core.entities.entity import BaseEntity
from core.entities.effects.base import BaseEffect
from core.entities.effects.constants import SerializeConst
from core.mech.skills.skill import BaseSkill


def deserialize_effect(effect_dict: dict, effect_class: Type[BaseEffect] = BaseEffect) -> BaseEffect:
    all_entities = (*Global.game.players_meches, *Global.game.other_entities)
    target_uid: str = effect_dict[SerializeConst.Target]
    dealer_uid: str = effect_dict[SerializeConst.Dealer]
    target: BaseEntity = tuple(filter(lambda e: e.uid == target_uid, all_entities))[0]
    dealer: BaseEntity = tuple(filter(lambda e: e.uid == dealer_uid, all_entities))[0]

    name = effect_dict[SerializeConst.Name]

    found_class = Global.effects_pool.get_class_by_name(name)
    if found_class:
        effect_class = found_class

    uid = effect_dict[SerializeConst.UID]
    duration = effect_dict[SerializeConst.Duration]
    parent_skill: BaseSkill = Global.skill_pool.get_skill_by_id(effect_dict[SerializeConst.ParentSkill])
    effect = effect_class(uid=uid,
                          target=target, dealer=dealer,
                          parent_skill=parent_skill,
                          duration=duration,
                          serializing=True)
    if not found_class:
        effect.name = name
        effect.types = effect_dict[SerializeConst.Types]
        effect.is_positive = effect_dict[SerializeConst.IsPositive]

    return effect
