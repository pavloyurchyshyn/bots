from core.mech.skills.skill import BaseSkill
from core.mech.skills.exceptions import OnCooldownError
from core.mech.mech import BaseMech

class SimpleStepAttrs:
    name = 'simple_step'
    spell_cost = 1
    cooldown = 1


class SimpleHit(BaseSkill):
    name = 'simple_hit'
    verbal_name = 'Simple Hit'
    targets = BaseSkill.TargetsConst.AnyMech, BaseSkill.TargetsConst.Tile

    def __init__(self, num, unique_id):
        super(SimpleHit, self).__init__(unique_id=unique_id, num=num,
                                        energy_cost=SimpleStepAttrs.spell_cost,
                                        cooldown=SimpleStepAttrs.cooldown,
                                        target_validation_func=lambda **_: _)

    @staticmethod
    def __target_fileter_func(mech: BaseMech, target_xy_coord: tuple) -> bool:
        return mech.position == target_xy_coord and mech.health_points > 0
    def use(self, **kwargs):
        if not self.on_cooldown:
            mech: BaseMech = kwargs.get('mech')
            mech.spend_energy(self.energy_cost)

        else:
            raise OnCooldownError
    def get_dict(self) -> dict:
        return self.get_base_dict()

    def update_attrs(self, attrs: dict) -> None:
        self.update_base_attrs(attrs)