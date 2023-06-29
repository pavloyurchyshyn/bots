from core.mech.skills.constants import INFINITE_VALUE
from core.mech.skills.skill import BaseSkill
from core.validators.skill import SkillsValidations
from core.entities.simple_effects import SimpleDamageBuff
from core.entities.entity import BaseEntity


class DoubleDamageAttrs:
    spell_cost = 3
    cooldown = 10

    damage_boost_mul_add = 0
    damage_boost_mul_val = 1



class DoubleDamageEffect(SimpleDamageBuff):
    is_positive = True
    name = 'double_damage_effect'
    verbal_name = 'Double Damage Effect'
    
    def __init__(self, uid: str, dealer, target):
        super().__init__(uid=uid,
                         dealer=dealer, target=target,
                         duration=1,
                         mul_dmg=DoubleDamageAttrs.damage_boost_mul_val,
                         add_dmg=DoubleDamageAttrs.damage_boost_mul_add)
    
class DoubleDamage(BaseSkill):
    name = 'double_damage'
    verbal_name = 'Double Damage'
    targets = BaseSkill.TargetsConst.AnyMech,


    def __init__(self, num, unique_id):
        super(DoubleDamage, self).__init__(unique_id=unique_id, num=num,
                                           energy_cost=DoubleDamageAttrs.spell_cost,
                                           cooldown=DoubleDamageAttrs.cooldown,
                                           target_validation_func=SkillsValidations.validate_target_is_mech,
                                           cast_range=INFINITE_VALUE,
                                           )


    def use(self, player, game_obj, target_xy, mech: BaseEntity, skill_cast_uid: str, **__) -> None:
        effect = DoubleDamageEffect(dealer=player.mech, target=mech, uid=skill_cast_uid)
        mech.effects_manager.add_effect(effect)
        effect.affect()
        mech.spend_energy(self.energy_cost)
        self.set_on_cooldown()


    def get_dict(self) -> dict:
        return self.get_base_dict()

    def update_attrs(self, attrs: dict) -> None:
        self.update_base_attrs(attrs=attrs)