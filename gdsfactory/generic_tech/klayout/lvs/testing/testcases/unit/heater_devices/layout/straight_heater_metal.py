import os
from functools import partial

import gdsfactory as gf

straight_heater_metal_mk = (47, 1)
metal3 = gf.cross_section.metal3


@gf.cell
def straight_heater_metal_lvs() -> gf.Component:
    c = gf.Component()

    strip_hm10 = gf.cross_section.strip_heater_metal(heater_width=10)
    strip_hm35 = gf.cross_section.strip_heater_metal(heater_width=10)
    strip_hm100 = gf.cross_section.strip_heater_metal(heater_width=10)
    strip_hm50 = gf.cross_section.strip_heater_metal(heater_width=10)
    strip_hm30 = gf.cross_section.strip_heater_metal(heater_width=10)
    strip_hm40 = gf.cross_section.strip_heater_metal(heater_width=10)
    strip_hm500 = gf.cross_section.strip_heater_metal(heater_width=500)

    c1 = c << gf.components.straight_heater_metal(length=50, cross_section=strip_hm10)
    c1_mk = c << gf.components.rectangle(size=(50, 10), layer=straight_heater_metal_mk)

    c2 = c << gf.components.straight_heater_metal(length=70, cross_section=strip_hm35)
    c2_mk = c << gf.components.rectangle(size=(70, 35), layer=straight_heater_metal_mk)

    c3 = c << gf.components.straight_heater_metal(length=50, cross_section=strip_hm100)
    c3_mk = c << gf.components.rectangle(size=(50, 100), layer=straight_heater_metal_mk)

    c4 = c << gf.components.straight_heater_metal(length=100, cross_section=strip_hm50)
    c4_mk = c << gf.components.rectangle(size=(100, 50), layer=straight_heater_metal_mk)

    c5 = c << gf.components.straight_heater_metal(length=80, cross_section=strip_hm30)
    c5_mk = c << gf.components.rectangle(size=(80, 30), layer=straight_heater_metal_mk)

    c6 = c << gf.components.straight_heater_metal(length=60, cross_section=strip_hm40)
    c6_mk = c << gf.components.rectangle(size=(60, 40), layer=straight_heater_metal_mk)

    c7 = c << gf.components.straight_heater_metal(length=200, cross_section=strip_hm10)
    c7_mk = c << gf.components.rectangle(size=(200, 10), layer=straight_heater_metal_mk)

    c8 = c << gf.components.straight_heater_metal(length=120, cross_section=strip_hm100)
    c8_mk = c << gf.components.rectangle(
        size=(120, 100), layer=straight_heater_metal_mk
    )

    c9 = c << gf.components.straight_heater_metal(length=150, cross_section=strip_hm50)
    c9_mk = c << gf.components.rectangle(size=(150, 50), layer=straight_heater_metal_mk)

    c10 = c << gf.components.straight_heater_metal(
        length=500, cross_section=strip_hm500
    )
    c10_mk = c << gf.components.rectangle(
        size=(500, 500), layer=straight_heater_metal_mk
    )

    c1.xmin = 0
    c2.xmin = 0
    c3.xmin = 0
    c4.xmin = 0
    c5.xmin = 0
    c6.xmin = 0
    c7.xmin = 0
    c8.xmin = 0
    c9.xmin = 0
    c10.xmin = 0

    c1.ymin = 0
    c2.ymin = c1.ymax + 50
    c3.ymin = c2.ymax + 50
    c4.ymin = c3.ymax + 50
    c5.ymin = c4.ymax + 50
    c6.ymin = c5.ymax + 50
    c7.ymin = c6.ymax + 50
    c8.ymin = c7.ymax + 50
    c9.ymin = c8.ymax + 50
    c10.ymin = c9.ymax + 50

    c1_mk.center = c1.center
    c2_mk.center = c2.center
    c3_mk.center = c3.center
    c4_mk.center = c4.center
    c5_mk.center = c5.center
    c6_mk.center = c6.center
    c7_mk.center = c7.center
    c8_mk.center = c8.center
    c9_mk.center = c9.center
    c10_mk.center = c10.center

    route_single = partial(gf.routing.route_single, port_type="electrical")

    route_single(c, c1.ports["o1"], c2.ports["o1"], cross_section=metal3)
    route_single(c, c2.ports["o2"], c3.ports["o2"], cross_section=metal3)
    route_single(c, c3.ports["o1"], c4.ports["o1"], cross_section=metal3)
    route_single(c, c4.ports["o2"], c5.ports["o2"], cross_section=metal3)
    route_single(c, c5.ports["o1"], c6.ports["o1"], cross_section=metal3)
    route_single(c, c6.ports["o2"], c7.ports["o2"], cross_section=metal3)
    route_single(c, c7.ports["o1"], c8.ports["o1"], cross_section=metal3)
    route_single(c, c8.ports["o2"], c9.ports["o2"], cross_section=metal3)
    route_single(c, c9.ports["o1"], c10.ports["o1"], cross_section=metal3)
    return c


if __name__ == "__main__":
    testcase_path = os.path.dirname(os.path.abspath(__file__))
    heater_path = os.path.join(testcase_path, "straight_heater_metal.gds")

    c = straight_heater_metal_lvs()
    c.show()
    c.write_gds(heater_path)
