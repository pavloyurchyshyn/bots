from global_obj.logger import get_logger
from core.mech.mech import BaseMech
from core.mech.details.body import BaseBody
from core.pools.details_pool import DetailsPool
from core.pools.effects_pool import EffectsPool
from core.mech.details.constants import MechSerializeConst, DetailsTypes, MechAttrs
from core.entities.stats_attrs import EntityAttrs
from core.entities.effects.serializer import deserialize_effect


class MechSerializer:
    logger = get_logger()

    def __init__(self, details_pool: DetailsPool, effects_pool: EffectsPool):
        self.details_pool: DetailsPool = details_pool
        self.effects_pool: EffectsPool = effects_pool

    def mech_to_dict(self, mech: BaseMech) -> dict:
        data = {
            # MechAttrs.Position: mech.position,
            # MechAttrs.CurrentHP: mech.health_points,
            # MechAttrs.CurrentEnergy: mech.energy,
            MechSerializeConst.UID: mech.uid,
            EntityAttrs.Attrs: mech.attr_dict(),
            MechSerializeConst.Effects: [effect.get_dict() for effect in mech.effects],
        }
        if mech.body:
            data[MechSerializeConst.Body] = mech.body.unique_id

            for key, slots in (
                    (MechSerializeConst.LeftSlots, mech.left_slots),
                    (MechSerializeConst.RightSlots, mech.right_slots),
            ):

                slots = {num: slot.detail for num, slot in slots.items()}
                for slot_n, detail in slots.items():
                    if detail:
                        slots[slot_n] = {MechSerializeConst.Detail: detail.unique_id}
                        if detail.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE):
                            if detail.weapon:
                                slots[slot_n][MechSerializeConst.Weapon] = detail.weapon.unique_id

                data[key] = slots
        self.logger.debug(f'Serialized mech {mech.__dict__} ')
        self.logger.debug(f'To mech dict {data}')
        return data

    def dict_to_mech(self, data: dict) -> BaseMech:
        """
        Dict with data in string format about vanilla_details
        :param data:
        :return:
        """
        attrs = data.pop(EntityAttrs.Attrs, {})
        body: BaseBody = self.details_pool.get_detail_by_id(data.get(MechSerializeConst.Body))
        mech = BaseMech(uid=data.pop(MechSerializeConst.UID),
                        position=tuple(attrs.get(EntityAttrs.Position, (-100, -100))),
                        body_detail=body)

        self.update_mech_details(mech, data)

        mech.set_attrs(attrs)

        for effect_data in data[MechSerializeConst.Effects]:
            effect = deserialize_effect(effect_dict=effect_data)
            effect.affect()

        return mech

    def update_mech_details(self, mech: BaseMech, data: dict):
        for k, set_slot_detail_func in ((MechSerializeConst.LeftSlots, mech.set_left_detail),
                                        (MechSerializeConst.RightSlots, mech.set_right_detail),
                                        ):
            side_slots = data.get(k, {})
            for slot_num, detail_data in side_slots.items():
                if detail_data and (detail_uid := detail_data[MechSerializeConst.Detail]):
                    detail = self.details_pool.get_detail_by_id(detail_uid)

                    set_slot_detail_func(int(slot_num), detail)
                    if detail.detail_type in (DetailsTypes.ARM_TYPE, DetailsTypes.ARM_AND_LEG_TYPE):
                        if detail_data.get(MechSerializeConst.Weapon):
                            detail.set_weapon(
                                self.details_pool.get_detail_by_id(detail_data.get(MechSerializeConst.Weapon))
                            )
                        else:
                            detail.remove_weapon()
