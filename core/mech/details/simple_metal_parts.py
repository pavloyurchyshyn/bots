from core.mech.base.details.body import BaseBody
from core.mech.base.details.arm import BaseArm
from core.mech.base.details.leg import BaseLeg

from core.mech.skills.simple_step import SimpleStep
from core.mech.skills.simple_hit import SimpleHit

from core.mech.base.details.constants import *
from core.mech.details.names import DetailNames

__all__ = ['MetalArm', 'MetalLeg', 'MetalBody']


class MetalArm(BaseArm):
    name = DetailNames.SimpleMetal.Arm
    original_name = 'Metal Arm'

    def __init__(self, unique_id):
        skills = [SimpleHit, ]

        super(MetalArm, self).__init__(unique_id=unique_id, damage=1, armor=1, add_hp=1,
                                       skills=skills,
                                       energy_regen=0.25)


class MetalLeg(BaseLeg):
    name = DetailNames.SimpleMetal.Leg
    original_name = 'Metal Leg'

    def __init__(self, unique_id):
        skills = [SimpleStep, ]
        data = {
            DetailsAttrs.AddEnergy: 1,
            DetailsAttrs.HPRegen: 0.25,
            DetailsAttrs.AddHP: 1,
        }
        super(MetalLeg, self).__init__(unique_id=unique_id, damage=1, armor=1, skills=skills, **data)


class MetalBody(BaseBody):
    name = DetailNames.SimpleMetal.Body
    original_name = 'Metal Body'

    def __init__(self, unique_id):
        data = {DetailsAttrs.EnergyRegen: 1,
                DetailsAttrs.AddEnergy: 10,
                DetailsAttrs.AddHP: 10,
                DetailsAttrs.HPRegen: 1}
        super(MetalBody, self).__init__(unique_id=unique_id, damage=1, armor=1, **data)



