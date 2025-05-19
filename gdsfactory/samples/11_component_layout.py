"""Lets create a new component.

We create a function which returns a gf.Component.

Lets build straight crossing out of a vertical and horizontal arm

- Create a component using a function with the cell decorator to define the name automatically and uniquely.
- Define the polygons in the component
- Add ports to the component so you can connect it with other components

"""

from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component


@gf.cell
def crossing_arm(
    wg_width: float = 0.5,
    r1: float = 3.0,
    r2: float = 1.1,
    taper_width: float = 1.2,
    taper_length: float = 3.4,
) -> Component:
    """Returns a crossing arm.

    Args:
        wg_width: waveguide width.
        r1: radius of the ellipse.
        r2: radius of the ellipse.
        taper_width: width of the taper.
        taper_length: length of the taper.

    """
    c = gf.Component()
    _ = c << gf.components.ellipse(radii=(r1, r2), layer=(2, 0))

    xmax = taper_length + taper_width / 2
    h = wg_width / 2
    taper_points = [
        (-xmax, h),
        (-taper_width / 2, taper_width / 2),
        (taper_width / 2, taper_width / 2),
        (xmax, h),
        (xmax, -h),
        (taper_width / 2, -taper_width / 2),
        (-taper_width / 2, -taper_width / 2),
        (-xmax, -h),
    ]

    c.add_polygon(taper_points, layer=(1, 0))

    c.add_port(
        name="o1", center=(-xmax, 0), orientation=180, width=wg_width, layer=(1, 0)
    )

    c.add_port(name="o2", center=(xmax, 0), orientation=0, width=wg_width, layer=(1, 0))
    return c


if __name__ == "__main__":
    c = crossing_arm()
    c.show()
