from core.entities.entity import BaseEntity
from core.entities.effects.base import BaseEffect
from core.entities.effects.constants import EffectType
from core.entities.stats_attrs import EntityAttrs


class SimpleAttrEffect(BaseEffect):
    is_positive = True
    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 attr: str,
                 mul_value: float = 0.01, add_value: float = 0.01,
                 duration: int = 5):
        super().__init__(uid=uid, dealer=dealer, target=target, duration=duration)

        self.add_value: float = add_value
        self.mul_value: float = mul_value
        self.attr: str = attr

    def affect(self):
        super().affect()
        if hasattr(self.target, f"{self.attr}_attr"):
            getattr(self.target, f"{self.attr}_attr").add_multiplayer(self.mul_value)
            getattr(self.target, f"{self.attr}_attr").add_value(self.add_value)
        return self

    def on_end(self):
        super().on_end()
        if hasattr(self.target, f"{self.attr}_attr"):
            getattr(self.target, f"{self.attr}_attr").minus_multiplayer(self.mul_value)
            getattr(self.target, f"{self.attr}_attr").minus_value(self.add_value)

        return self


class SimpleDamageBuff(SimpleAttrEffect):
    types = (EffectType.DamageIncrease, )
    name = 'damage_boost'
    verbal_name = 'Damage Boost'

    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 mul_dmg: int = 0.01, add_dmg: int = 0.01,
                 duration: int = 5):
        super().__init__(uid=uid,
                         dealer=dealer, target=target,
                         mul_value=mul_dmg, add_value=add_dmg,
                         duration=duration,
                         attr=EntityAttrs.Damage)


class SimpleDamageDebuff(SimpleAttrEffect):
    is_positive = False
    types = (EffectType.DamageDecrease, )
    name = 'damage_deboost'
    verbal_name = 'Damage deboost'

    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 mul_dmg: int = 0.01, add_dmg: int = 0.01,
                 duration: int = 5):
        super().__init__(uid=uid, dealer=dealer, target=target,
                         mul_value=mul_dmg, add_value=add_dmg,
                         duration=duration,
                         attr=EntityAttrs.Damage)



class SimpleHPRegenBuff(SimpleAttrEffect):
    is_positive = True
    types = (EffectType.HpRegenIncrease, )
    name = 'hp_regen_boost'
    verbal_name = 'HP regen boost'

    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 mul_hp_r: int = 0.01, add_hp_r: int = 0.01,
                 duration: int = 5):
        super().__init__(dealer=dealer, target=target,
                         mul_value=mul_hp_r, add_value=add_hp_r,
                         duration=duration,
                         attr=EntityAttrs.HPRegen, uid=uid)


class SimpleHPRegenDebuff(SimpleAttrEffect):
    is_positive = False
    types = (EffectType.HpRegenDecrease, )
    name = 'hp_regen_deboost'
    verbal_name = 'HP regen deboost'

    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 mul_hp_r: int = 0.01, add_hp_r: int = 0.01,
                 duration: int = 5):
        super().__init__(dealer=dealer, target=target,
                         mul_value=mul_hp_r, add_value=add_hp_r,
                         duration=duration,
                         attr=EntityAttrs.HPRegen, uid=uid)



class SimpleHPIncrease(SimpleAttrEffect):
    types = (EffectType.HpIncrease, )
    name = 'hp_increase'
    verbal_name = 'HP Increase'


    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 mul_hp_r: int = 0.01, add_hp_r: int = 0.01,
                 duration: int = 5):
        super().__init__(dealer=dealer, target=target,
                         mul_value=mul_hp_r, add_value=add_hp_r,
                         duration=duration,
                         attr=EntityAttrs.MaxHP, uid=uid)


class SimpleHPDecrease(SimpleAttrEffect):
    types = (EffectType.HpDecrease, )
    name = 'hp_decrease'
    verbal_name = 'HP Decrease'


    def __init__(self, uid: str, dealer: BaseEntity, target: BaseEntity,
                 mul_hp_r: int = -0.01, add_hp_r: int = -0.01, duration: int = 5):
        super().__init__(dealer=dealer, target=target,
                         mul_value=mul_hp_r, add_value=add_hp_r,
                         duration=duration,
                         attr=EntityAttrs.MaxHP, uid=uid)

# TODO do all attrs