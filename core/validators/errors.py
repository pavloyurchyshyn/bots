from settings.localization.validation import ValidationMsg as ValidationLoc


class ValidationError(Exception):
    def __init__(self, msg: str = 'Unable to use'):
        self.msg = msg

    def __str__(self):
        return self.msg


class NoEmptyStepError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.NoEmptyStepError)

class OnCooldownValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.SkillOnCooldown)

class SkillNotInPullValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.SkillNotInPull)


class PlayerDoesntOwnSkillValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.PlayerDoesntOwnSkill)

class NotEnoughEnergyValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.NotEnoughEnergy)


class BadTargetTypeValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.BadTargetType)



class NoSuchTileValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.NoSuchTile)


class TileNotPassableValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.TileNotPassable)


class OutOfRangeValError(ValidationError):
    def __init__(self):
        super().__init__(ValidationLoc.OutOfRange)