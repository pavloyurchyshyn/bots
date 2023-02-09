from core.mech.base.mech import BaseMech
from core.mech.base.skills.skill import BaseSkill
from core.mech.base.exceptions import OnCooldownException


class SimpleStep(BaseSkill):
    name = 'simple_step'
    verbal_name = 'Step'
    targets = BaseSkill.TargetsConst.Tile,

    def __init__(self, num, unique_id):
        super(SimpleStep, self).__init__(unique_id=unique_id, num=num,
                                         energy_cost=1,
                                         cooldown=0)

    def use(self, **kwargs):
        if not self.on_cooldown():
            mech: BaseMech = kwargs.get('mech')
            mech.change_position(kwargs.get('new_pos'))
            mech.spend_energy(self.energy_cost)

        else:
            raise OnCooldownException
