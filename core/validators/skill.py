from core.world.base.hex_utils import HexMath
from core.mech.skills.constants import INFINITE_VALUE
from core.validators.errors import *


class SkillsValidations:
    @classmethod
    def no_empty_slots(cls, player, skill_uid: str, *_, **__):
        if player.scenario.is_full and not player.scenario.contains_skill(skill_uid):
            raise NoEmptyStepError

    @classmethod
    def skill_not_on_cooldown(cls, skill, **_):
        if skill.on_cooldown:
            raise OnCooldownValError

    @classmethod
    def skill_exists_in_pool(cls, skill_uid: str, skill_pool, **_):
        if skill_uid not in skill_pool.id_to_skill:
            raise SkillNotInPullValError

    @classmethod
    def player_owns_skill(cls, player, skill_uid, **_):
        if skill_uid not in tuple(map(lambda s: s.unique_id, player.latest_scenario_skills)):
            raise PlayerDoesntOwnSkillValError

    @classmethod
    def player_owns_skill_by_uid(cls, player, skill_uid: str, skill_pool, **_):
        cls.skill_exists_in_pool(skill_uid=skill_uid, skill_pool=skill_pool)
        cls.player_owns_skill(player=player, skill_uid=skill_uid)

    @classmethod
    def player_has_enough_of_energy(cls, skill, mech, **_):
        if mech.energy < skill.energy_cost:
            raise NotEnoughEnergyValError

    @classmethod
    def validate_tile_target(cls, target_xy_coord, skill, world, **_):
        tile = world.get_tile_by_xy(target_xy_coord)
        if skill.TargetsConst.Tile not in skill.targets:
            raise BadTargetTypeValError

        if tile is None:
            raise NoSuchTileValError

        if tile.not_passable:
            raise TileNotPassableValError

    @classmethod
    def validate_target_is_mech(cls, target_xy_coord, all_meches, *_, **__):
        return any([mech for mech in all_meches if mech.position == target_xy_coord])

    @classmethod
    def target_in_range(cls, skill, target_xy_coord, mech, **_):
        if skill.cast_range != INFINITE_VALUE and \
                HexMath.get_xy_distance(mech.position, target_xy_coord) > skill.cast_range:
            raise OutOfRangeValError
