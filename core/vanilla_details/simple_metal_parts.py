from core.mech.details.body import BaseBody
from core.mech.details.arm import BaseArm
from core.mech.details.leg import BaseLeg
from core.entities.stats_attrs import EntityAttrs

from core.vanilla_details.names import DetailNames
from core.vanilla_skills.simple_step import SimpleStep
from core.vanilla_skills.simple_hit import SimpleHit
from core.vanilla_skills.double_damage import DoubleDamage

__all__ = ['MetalArm', 'MetalLeg', 'MetalBody']


class MetalArm(BaseArm):
    name = DetailNames.SimpleMetal.Arm
    original_name = 'Metal Arm'
    verbal_name = 'Metal Arm'

    def __init__(self, unique_id):
        skills = [SimpleHit, DoubleDamage]

        super(MetalArm, self).__init__(unique_id=unique_id, damage=1, armor=1, add_hp=1,
                                       skills=skills,
                                       energy_regen=0.25)


class MetalLeg(BaseLeg):
    name = DetailNames.SimpleMetal.Leg
    original_name = 'Metal Leg'

    def __init__(self, unique_id):
        skills = [SimpleStep, ]
        data = {
            EntityAttrs.AddEnergy: 1,
            EntityAttrs.HPRegen: 0.25,
            EntityAttrs.AddHP: 1,
        }
        super(MetalLeg, self).__init__(unique_id=unique_id, damage=1, armor=1, skills=skills, **data)


class MetalBody(BaseBody):
    name = DetailNames.SimpleMetal.Body
    original_name = 'Metal Body'

    def __init__(self, unique_id):
        data = {EntityAttrs.EnergyRegen: 1,
                EntityAttrs.AddEnergy: 10,
                EntityAttrs.AddHP: 10,
                EntityAttrs.HPRegen: 1}
        super(MetalBody, self).__init__(unique_id=unique_id, damage=1, armor=1, **data)
