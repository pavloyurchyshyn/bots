from core.mech.skills.skill import BaseSkill
from core.validators.skill import SkillsValidations


class SimpleStep(BaseSkill):
    name = 'simple_step'
    verbal_name = 'Step'
    targets = BaseSkill.TargetsConst.Tile,

    def __init__(self, num, unique_id):
        super(SimpleStep, self).__init__(unique_id=unique_id, num=num,
                                         energy_cost=1,
                                         cooldown=0,
                                         target_validation_func=SkillsValidations.validate_tile_target,
                                         )

    def use(self, player, game_obj, target_xy, **kwargs):
        print(self.name, 'used')
        # TODO
        # if not self.on_cooldown:
        #     self.logger.error(f"{self.unique_id} -> {str(kwargs)}")
        #     # mech: BaseMech = kwargs.get(self.Mech)
        #     # mech.change_position(kwargs.get(UseKeys.NewPos))
        #     # mech.spend_energy(self.energy_cost)
        #
        # else:
        #     raise OnCooldownError

    def get_dict(self) -> dict:
        return self.get_base_dict()

    def update_attrs(self, attrs: dict) -> None:
        self.update_base_attrs(attrs)
