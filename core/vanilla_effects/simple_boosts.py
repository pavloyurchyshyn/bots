from core.entities.base.entity import BaseEntity
from core.entities.base.effects.base import BaseEffect
from core.entities.base.effects.constants import EffectType


class SimpleDamageBuff(BaseEffect):
    is_positive = True
    types = (EffectType.DamageIncrease, )
    name = 'damage_boost'
    verbal_name = 'Damage Boost'

    def __init__(self, dealer: BaseEntity, target: BaseEntity,
                 mul_dmg: int = 2, add_dmg: int = 1,  duration: int = 5):
        super().__init__(dealer=dealer, target=target, duration=duration)
        self.mul_dmg = mul_dmg
        self.add_dmg = add_dmg

    def affect(self):
        super().affect()
        self.target.damage_attr.add_multiplayer(self.mul_dmg)
        self.target.damage_attr.add_value(self.add_dmg)

    def on_end(self):
        super().on_end()
        self.target.damage_attr.minus_multiplayer(self.mul_dmg)
        self.target.damage_attr.minus_value(self.add_dmg)


# TODO remove its from here
class SimpleDamageDeBuff(SimpleDamageBuff):
    is_positive = False
    name = 'damage_deboost'
    verbal_name = 'Damage Deboost'

    def __init__(self, dealer: BaseEntity, target: BaseEntity,
                 mul_dmg: int = -2, minus_dmg: int = -1,  duration: int = 5):
        super().__init__(dealer=dealer, target=target, mul_dmg=mul_dmg, add_dmg=minus_dmg, duration=duration)