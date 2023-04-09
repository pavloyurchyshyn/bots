from core.mech.base.test_mech import MetalMech
from core.mech.base.pools.skills_pool import SkillsPool
from core.mech.base.mech_serializer import MechSerializer
from core.mech.base.pools.details_pool import DetailsPool


def test():
    builder = MechSerializer(DetailsPool(SkillsPool()))
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
    assert m.attr_dict() == m1.attr_dict()


if __name__ == '__main__':
    test()
