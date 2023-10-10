from core.entities.effects.simple_effects.attrs_effects import SimpleDamageBuff
from core.mech.skills.skill import BaseSkill

damage_boost_mul_add = 0
damage_boost_mul_val = 1


class DoubleDamageEffect(SimpleDamageBuff):
    is_positive = True
    name = 'double_damage_effect'
    verbal_name = 'Double Damage Effect'

    def __init__(self, uid: str, dealer, target, parent_skill: BaseSkill, duration: int = 1, serializing: bool = False):
        super().__init__(uid=uid,
                         dealer=dealer, target=target,
                         parent_skill=parent_skill,
                         duration=duration,
                         mul_dmg=damage_boost_mul_val,
                         add_dmg=damage_boost_mul_add,
                         serializing=serializing,
                         )
