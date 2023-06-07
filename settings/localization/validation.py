from settings.localization import build_path


class ValidationMsg:
    UI_path = build_path('validation', 'msgs')

    BadTargetType = build_path(UI_path, 'bad_target_type')

    SkillOnCooldown = build_path(UI_path, 'skill_on_cooldown')
    NotEnoughEnergy = build_path(UI_path, 'not_enough_energy')
    SkillNotInPull = build_path(UI_path, 'skill_not_in_pool')
    PlayerDoesntOwnSkill = build_path(UI_path, 'player_doesnt_own_skill')

    BadTileTarget = build_path(UI_path, 'bad_tile_target')
    NoSuchTile = build_path(UI_path, 'no_such_tile')
    TileNotPassable = build_path(UI_path, 'tile_not_passable')
    OutOfRange = build_path(UI_path, 'out_of_range')
    NoEmptyStepError = build_path(UI_path, 'no_empty_steps')