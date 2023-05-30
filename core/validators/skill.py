from core.world.base.hex_utils import HexMath
from core.mech.skills.constants import INFINITE_VALUE
from core.validators.errors import *


class SkillsValidations:
    @classmethod
    def skill_not_on_cooldown(cls, skill, **_):
        if skill.on_cooldown:
            raise OnCooldownValError

    @classmethod
    def skill_exists_in_pool(cls, skill_uid: str, skill_pool, **_):
        if skill_uid not in skill_pool.id_to_skill:
            raise SkillNotInPullValError

    @classmethod
    def player_owns_skill(cls, player, skill, **_):
        if skill and skill not in player.skills:
            raise PlayerDoesntOwnSkillValError

    @classmethod
    def player_owns_skill_by_uid(cls, player, skill_uid: str, skill_pool, **_):
        cls.skill_exists_in_pool(skill_uid=skill_uid, skill_pool=skill_pool)
        cls.player_owns_skill(player=player, skill=skill_pool.get_skill_by_id(skill_uid))

    @classmethod
    def player_has_enough_of_energy(cls, player, skill, **kwargs):
        if player.mech.energy < skill.energy_cost:
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
    def target_in_range(cls, skill, target_xy_coord, player, **_):
        if skill.cast_range != INFINITE_VALUE and \
                HexMath.get_xy_distance(player.mech.position, target_xy_coord) > skill.cast_range:
            raise OutOfRangeValError
