
class MaterialTypes:
    """
    Material types constants.
    """
    METAL_TYPE = 'metal'
    ELECTRIC_TYPE = 'electric'
    STEAM_TYPE = 'steam'
    BIO_TYPE = 'bio'





class SpecialValues:
    NoCD = 'NoCD'
    NoEnergy = 'NoEnrg'


class MechAttrs:
    Skills: str = 'skills'



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
    UID = 'uid'
    Body: str = 'body'
    LeftSlots: str = 'left_slots'
    RightSlots: str = 'right_slots'
    Weapon: str = 'weapon'
    Detail: str = 'detail'
    Effects: str = 'effects'
