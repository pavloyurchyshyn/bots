class SkillsValidations:
    @classmethod
    def skill_on_cooldown(cls, skill, **kwargs):
        return not skill.on_cooldown

    @classmethod
    def uid_skill_exists(cls, skill_uid: str, skill_pool, **kwargs) -> bool:
        return skill_uid in skill_pool.id_to_skill

    @classmethod
    def player_owns_skill(cls, player, skill, **kwargs) -> bool:
        return skill in player.skills

    @classmethod
    def player_owns_skill_by_uid(cls, player, skill_uid: str, skill_pool, **kwargs) -> bool:
        if cls.uid_skill_exists(skill_uid=skill_uid, skill_pool=skill_pool):
            return cls.player_owns_skill(player=player, skill=skill_pool.get_skill_by_id(skill_uid))
        else:
            return False

    @classmethod
    def player_has_enough_of_energy(cls, player, skill, **kwargs) -> bool:
        return player.mech.energy >= skill.energy_cost

    @classmethod
    def validate_tile_target(cls, xy, skill, world, **kwargs) -> bool:
        tile = world.get_tile_by_xy(xy)
        if (skill.TargetsConst.Tile not in skill.targets) or (tile is None) or (not tile.passable):
            return False

        return True
