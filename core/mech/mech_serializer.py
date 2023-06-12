from global_obj.logger import get_logger
from core.mech.mech import BaseMech
from core.mech.details.body import BaseBody
from core.pools.details_pool import DetailsPool
from core.mech.details.constants import MechSerializeConst, DetailsTypes, MechAttrs


class MechSerializer:
    logger = get_logger()

    def __init__(self, details_pool: DetailsPool):
        self.details_pool: DetailsPool = details_pool

    def mech_to_dict(self, mech: BaseMech) -> dict:
        data = {
            # MechAttrs.Position: mech.position,
            # MechAttrs.CurrentHP: mech.health_points,
            # MechAttrs.CurrentEnergy: mech.energy,
            MechAttrs.Attrs: mech.attr_dict(),
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
        Dict with data in string format about vanile_details
        :param data:
        :return:
        """
        body: BaseBody = self.details_pool.get_detail_by_id(data.get(MechSerializeConst.Body))
        mech = BaseMech(tuple(data.get(MechAttrs.Position, (-100, -100))), body_detail=body)

        self.update_mech_details(mech, data)

        # mech.set_energy(data.get(MechAttrs.CurrentEnergy, 0))
        # mech.set_health_points(data.get(MechAttrs.CurrentHP, 0))
        mech.set_attrs(data.get(MechAttrs.Attrs, {}))

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


if __name__ == '__main__':
    from core.mech.test_mech import MetalMech
    from game_logic import IdGenerator

    builder = MechSerializer(DetailsPool(IdGenerator()))
    builder.details_pool.load_details_classes_list([
        ('simple_metal_body', 0),
        ('simple_metal_arm', 1),
        ('simple_metal_arm', 2),
        ('simple_metal_leg', 3),
        ('simple_metal_leg', 4),
    ])

    m = MetalMech((1, 0))
    print('mech', m.__dict__)
    d = builder.mech_to_dict(m)
    print('mech dict', d)
    m1 = builder.dict_to_mech(d)

    print()
    print(d)
    print('# ===================')
    print(m.__dict__)
    print(m1.__dict__)

    print(m.attr_dict(), m.attr_dict() == m1.attr_dict(), m1.attr_dict())
