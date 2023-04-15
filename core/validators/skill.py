from settings.localization.validation import ValidationMsg


class ValidationError(Exception):
    def __init__(self, msg: str = 'Unable to use'):
        self.msg = msg

    def __str__(self):
        return self.msg


class SkillsValidations:
    @classmethod
    def skill_not_on_cooldown(cls, skill, **kwargs):
        if skill.on_cooldown:
            raise ValidationError(ValidationMsg.SkillOnCooldown)

    @classmethod
    def skill_exists_in_pool(cls, skill_uid: str, skill_pool, **kwargs):
        if skill_uid not in skill_pool.id_to_skill:
            raise ValidationError(ValidationMsg.SkillNotInPull)

    @classmethod
    def player_owns_skill(cls, player, skill, **kwargs):
        if skill not in player.skills:
            raise ValidationError(ValidationMsg.PlayerDoesntOwnSkill)

    @classmethod
    def player_owns_skill_by_uid(cls, player, skill_uid: str, skill_pool, **kwargs):
        cls.skill_exists_in_pool(skill_uid=skill_uid, skill_pool=skill_pool)
        cls.player_owns_skill(player=player, skill=skill_pool.get_skill_by_id(skill_uid))

    @classmethod
    def player_has_enough_of_energy(cls, player, skill, **kwargs):
        if player.mech.energy < skill.energy_cost:
            raise ValidationError(ValidationMsg.NotEnoughEnergy)

    @classmethod
    def validate_tile_target(cls, xy, skill, world, **kwargs):
        tile = world.get_tile_by_xy(xy)
        if skill.TargetsConst.Tile not in skill.targets:
            raise ValidationError(ValidationMsg.BadTargetType)

        if tile is None:
            raise ValidationError(ValidationMsg.NoSuchTile)

        if tile.not_passable:
            raise ValidationError(ValidationMsg.TileNotPassable)
