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

    def use(self, player, game_obj, target_xy, mech: BaseMech = None, **kwargs):
        mech: BaseMech = mech if mech else player.mech
        mech.spend_energy(self.energy_cost)

        attack_tile = True
        if meches:= game_obj.players_meches:
            for mech in meches:
                if mech.position == target_xy:
                    mech.deal_damage(mech.damage)
                    attack_tile = False
                    break
        if attack_tile:
            if tile:= game_obj.world.get_tile_by_xy(target_xy):
                tile.damage(mech.damage)

        self.set_on_cooldown()



    def get_dict(self) -> dict:
        return self.get_base_dict()

    def update_attrs(self, attrs: dict) -> None:
        self.update_base_attrs(attrs)