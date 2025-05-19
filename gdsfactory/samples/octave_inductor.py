from __future__ import annotations

import gdsfactory as gf

@gf.cell
def octave_inductor(
    radius: float = 30.0,
    turns: int = 2,
    width: float = 10.0,
    arm_opening: float = 20.0,
) -> gf.Component:
    """Returns a simple octave (figure eight) inductor.

    Args:
        radius: radius for each circular loop in microns.
        turns: number of loops (typically 2 for a figure eight).
        width: track width in microns.
        arm_opening: separation between the loop centers minus twice the radius.
    """
    p = gf.Path()
    spacing = 2 * radius + arm_opening

    # use metal routing cross section and set the width
    xs = gf.cross_section.metal3(width=width)

    # create the first loop
    p.append(gf.path.arc(radius=radius, angle=360))

    for _ in range(1, turns):
        p.append(gf.path.straight(length=spacing, npoints=2))
        p.append(gf.path.arc(radius=radius, angle=360))

    c = p.extrude(cross_section=xs)
    return c


if __name__ == "__main__":
    c = octave_inductor()
    c.show()
    c.write_gds("octave_inductor.gds")
