from core.mech.mech import BaseMech
from core.vanile_details import MetalArm, MetalLeg, MetalBody


class MetalMech(BaseMech):
    def __init__(self, position):
        super(MetalMech, self).__init__(position=position, body_detail=MetalBody(0))
        self.set_detail(self._left_slots, 0, MetalArm(1), update_attr=False)
        self.set_detail(self._right_slots, 0, MetalArm(2), update_attr=False)

        self.set_detail(self._left_slots, 1, MetalLeg(3), update_attr=False)
        self.set_detail(self._right_slots, 1, MetalLeg(4), update_attr=False)

        self.update_details_and_attrs()

        self.set_max_hp()
        self.set_max_energy()


if __name__ == '__main__':
    a = MetalMech((1, 1))
    print(a.attr_dict())
    print(a.details)
    print(a.skills)
