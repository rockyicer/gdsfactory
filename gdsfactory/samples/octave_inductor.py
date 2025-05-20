from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import CrossSectionSpec


@gf.cell
def octave_inductor(
    radius: float = 30.0,
    turns: int = 2,
    width: float = 10.0,
    arm_opening: float = 20.0,
    cross_section: CrossSectionSpec = gf.cross_section.metal3,
) -> gf.Component:
    """Octave (figure-eight) shaped inductor.

    Supports arbitrary number of turns, radius, track width and arm opening.

    Args:
        radius: radius for each loop in um.
        turns: number of loops.
        width: track width in um.
        arm_opening: spacing between adjacent loop centers minus twice the radius.
        cross_section: cross section specification used for routing.
    """

    xs = gf.get_cross_section(cross_section, width=width)
    spacing = 2 * radius + arm_opening

    p = gf.Path()
    for i in range(turns):
        angle = 360 if i % 2 == 0 else -360
        p.append(gf.path.arc(radius=radius, angle=angle))
        if i < turns - 1:
            p.append(gf.path.straight(length=spacing, npoints=2))

    return p.extrude(cross_section=xs)


if __name__ == "__main__":
    c = octave_inductor(turns=3)
    c.show()
    c.write_gds("octave_inductor.gds")
