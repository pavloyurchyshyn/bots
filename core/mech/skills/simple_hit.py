from core.mech.base.skills.skill import BaseSkill
from core.mech.base.exceptions import OnCooldownException
from core.mech.base.mech import BaseMech


class SimpleStepAttrs:
    name = 'simple_step'
    spell_cost = 1
    cooldown = 0


class SimpleHit(BaseSkill):
    name = 'simple_hit'
    targets = BaseSkill.TargetsConst.Tile,

    def __init__(self, num, unique_id):
        super(SimpleHit, self).__init__(unique_id=unique_id, num=num,
                                        energy_cost=SimpleStepAttrs.spell_cost,
                                        cooldown=SimpleStepAttrs.cooldown)

    def use(self, *args, **kwargs):
        if not self.on_cooldown():
            mech: BaseMech = kwargs.get('mech')
            mech.spend_energy(self.energy_cost)

        else:
            raise OnCooldownException
