from core.mech.skills.skill import BaseSkill
from core.mech.skills.exceptions import OnCooldownError


class SimpleStep(BaseSkill):
    name = 'simple_step'
    verbal_name = 'Step'
    targets = BaseSkill.TargetsConst.Tile,

    def __init__(self, num, unique_id):
        validators = ()
        super(SimpleStep, self).__init__(unique_id=unique_id, num=num,
                                         energy_cost=1,
                                         cooldown=0, validators=validators,
                                         )

    def use(self, **kwargs):
        if not self.on_cooldown:
            self.logger.error(f"{self.unique_id} -> {str(kwargs)}")
            # mech: BaseMech = kwargs.get(self.Mech)
            # mech.change_position(kwargs.get(UseKeys.NewPos))
            # mech.spend_energy(self.energy_cost)

        else:
            raise OnCooldownError

    def get_dict(self) -> dict:
        base_d = self.get_base_dict()

        return base_d

    def update_attrs(self, attr: dict) -> None:
        pass
