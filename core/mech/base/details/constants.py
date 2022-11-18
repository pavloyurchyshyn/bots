class MaterialTypes:
    """
    Material types constants.
    """
    METAL_TYPE = 'metal'
    ELECTRIC_TYPE = 'electric'
    STEAM_TYPE = 'steam'
    BIO_TYPE = 'bio'


class DetailsAttrs:
    Id: str = 'unique_id'
    Damage: str = 'damage'
    Armor: str = 'armor'
    AddHP: str = 'add_hp'
    HPRegen: str = 'hp_regen'  # regeneration
    AddEnergy: str = 'add_energy'
    EnergyRegen: str = 'energy_regen'
    Skills: str = 'skills'


class SpecialValues:
    NoCD = 'NoCD'
    NoEnergy = 'NoEnrg'


class MechAttrs:
    Position: str = 'position'
    CurrentHP: str = 'current_hp'
    CurrentEnergy: str = 'current_energy'


class DetailsTypes:
    """
    Details types constants.
    """
    BODY = 'body'
    MOD_TYPE = 'mod'
    WEAPON_TYPE = 'weapon'
    BODY_MOD_TYPE = 'body_mod'
    ARM_AND_LEG_TYPE = 'arm_and_leg'
    ARM_TYPE = 'arm'
    LEG_TYPE = 'leg'


class SlotNames:
    Arm = 'arm_slot'
    Leg = 'leg_slot'
    Weapon = 'weapon_slot'


class MechSerializeConst:
    Body: str = 'body'
    LeftSlots: str = 'left_slots'
    RightSlots: str = 'right_slots'
    Weapon: str = 'weapon'
    Detail: str = 'detail'
