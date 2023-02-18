from core.mech.base.mech import BaseMech
from core.mech.base.skills.skill import BaseSkill
from core.mech.base.skills.constants import UseKeys
from core.mech.base.skills.exceptions import OnCooldownError


class SimpleStep(BaseSkill):
    name = 'simple_step'
    verbal_name = 'Step'
    targets = BaseSkill.TargetsConst.Tile,

    def __init__(self, num, unique_id):
        super(SimpleStep, self).__init__(unique_id=unique_id, num=num,
                                         energy_cost=1,
                                         cooldown=0, validators=[])

    def use(self, **kwargs):
        if not self.on_cooldown:
            mech: BaseMech = kwargs.get(UseKeys.Mech)
            mech.change_position(kwargs.get(UseKeys.NewPos))
            mech.spend_energy(self.energy_cost)

        else:
            raise OnCooldownError
