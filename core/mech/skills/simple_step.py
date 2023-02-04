from core.mech.base.skills.skill import BaseSkill
from core.mech.base.exceptions import OnCooldownException
from core.mech.base.mech import BaseMech


class SimpleStepAttrs:
    name = 'simple_step'
    # verbal_name = 'Simple Step'
    spell_cost = 1
    cooldown = 0


class SimpleStep(BaseSkill):
    name = SimpleStepAttrs.name
    verbal_name = 'Step'
    targets = BaseSkill.Targets.Tile,

    def __init__(self, num, unique_id):
        super(SimpleStep, self).__init__(unique_id=unique_id, num=num,
                                         energy_cost=SimpleStepAttrs.spell_cost,
                                         cooldown=SimpleStepAttrs.cooldown)

    def use(self, mech, new_pos, *args, **kwargs):
        if not self.on_cooldown():
            mech: BaseMech = kwargs.get('mech')
            mech.change_position(kwargs.get('new_pos'))
            mech.spend_energy(self.energy_cost)

        else:
            raise OnCooldownException
