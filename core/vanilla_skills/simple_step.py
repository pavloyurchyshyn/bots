from core.mech.skills.skill import BaseSkill
from core.validators.skill import SkillsValidations
from core.mech.mech import BaseMech


class SimpleStep(BaseSkill):
    name = 'simple_step'
    verbal_name = 'Step'
    targets = BaseSkill.TargetsConst.Tile,

    def __init__(self, num, unique_id):
        super(SimpleStep, self).__init__(unique_id=unique_id, num=num,
                                         energy_cost=1,
                                         cooldown=1,
                                         target_validation_func=SkillsValidations.validate_another_tile_target,
                                         )

    def use(self, player, game_obj, target_xy, mech: BaseMech = None, **_):
        mech.events_manager.do_pre_skill_use_event(skill=self)
        mech.spend_energy(self.energy_cost)

        mech: BaseMech = player.mech

        mech.change_position(target_xy)

        self.set_on_cooldown()
        mech.events_manager.do_post_skill_use_event(skill=self)

    def get_dict(self) -> dict:
        return self.get_base_dict()

    def update_attrs(self, attrs: dict) -> None:
        self.update_base_attrs(attrs)
