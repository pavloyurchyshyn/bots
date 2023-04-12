from settings.localization import build_path


class ValidationMsg:
    UI_path = build_path('validation', 'msgs')

    SkillOnCooldown = build_path(UI_path, 'skill_on_cooldown')
    NotEnoughEnergy = build_path(UI_path, 'not_enough_energy')
    SkillNotInPull = build_path(UI_path, 'skill_not_in_pool')
    PlayerDoesntOwnSkill = build_path(UI_path, 'player_doesnt_own_skill')

    BadTileTarget = build_path(UI_path, 'bad_tile_target')
