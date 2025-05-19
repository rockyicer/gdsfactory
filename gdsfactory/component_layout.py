"""Helper functions for layout.

Adapted from PHIDL https://github.com/amccaugh/phidl/ by Adam McCaughan
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

from gdsfactory.port import to_dict

if TYPE_CHECKING:
    from typing import Any


import numpy as np
import numpy.typing as npt
from numpy import cos, pi, sin
from numpy.linalg import norm
from rich.console import Console
from rich.table import Table

import gdsfactory as gf
from gdsfactory.typings import Axis, Coordinate, Port


def pprint_ports(ports: Sequence[gf.Port]) -> None:
    """Prints ports in a rich table."""
    console = Console()
    table = Table(show_header=True, header_style="bold")
    ports_list = ports
    if not ports_list:
        return
    p0 = ports_list[0]
    filtered_dict = {
        key: value for key, value in to_dict(p0).items() if value is not None
    }
    keys = filtered_dict.keys()

    for key in keys:
        table.add_column(key)

    for port in ports_list:
        port_dict = to_dict(port)
        row = [str(port_dict.get(key, "")) for key in keys]
        table.add_row(*row)

    console.print(table)


def rotate_points(
    points: npt.NDArray[np.floating[Any]],
    angle: float = 45,
    center: Coordinate = (0, 0),
) -> npt.NDArray[np.floating[Any]]:
    """Rotates points around a centerpoint defined by ``center``.

    ``points`` may be input as either single points [1,2] or array-like[N][2],
    and will return in kind.

    Args:
        points : array-like[N][2]
            Coordinates of the element to be rotated.
        angle : int or float
            Angle to rotate the points.
        center : array-like[2]
            Centerpoint of rotation.

    Returns:
        A new set of points that are rotated around ``center``.
    """
    if angle == 0:
        return points
    angle = angle * pi / 180
    ca = float(cos(angle))
    sa = float(sin(angle))
    sa_array = np.array((-sa, sa))
    c0 = np.array(center)
    if np.asarray(points).ndim == 2:
        return (points - c0) * ca + (points - c0)[:, ::-1] * sa_array + c0  # type: ignore[no-any-return]
    if np.asarray(points).ndim == 1:
        return (points - c0) * ca + (points - c0)[::-1] * sa_array + c0  # type: ignore[no-any-return]
    raise ValueError("Input points must be array-like[N][2] or array-like[2]")


def reflect_points(
    points: npt.NDArray[np.floating[Any]],
    p1: Coordinate = (0, 0),
    p2: Coordinate = (1, 0),
) -> npt.NDArray[np.floating[Any]]:
    """Reflects points across the line formed by p1 and p2.

    from https://github.com/amccaugh/phidl/pull/181

    ``points`` may be input as either single points [1,2] or array-like[N][2],
    and will return in kind.

    Args:
        points : array-like[N][2]
            Coordinates of the element to be reflected.
        p1 : array-like[2]
            Coordinates of the start of the reflecting line.
        p2 : array-like[2]
            Coordinates of the end of the reflecting line.

    Returns:
        A new set of points that are reflected across ``p1`` and ``p2``.
    """
    original_shape = np.shape(points)
    points = np.atleast_2d(points)
    p1_array = np.asarray(p1)
    p2_array = np.asarray(p2)

    line_vec = p2_array - p1_array
    line_vec_norm = norm(line_vec) ** 2

    # Compute reflection
    proj = np.sum(line_vec * (points - p1_array), axis=-1, keepdims=True)
    reflected_points = (
        2 * (p1_array + (p2_array - p1_array) * proj / line_vec_norm) - points
    )
    return reflected_points if original_shape[0] > 1 else reflected_points[0]  # type: ignore[no-any-return]


def parse_coordinate(
    c: Coordinate | Port | npt.NDArray[np.floating[Any]],
) -> Coordinate:
    """Translates various inputs (lists, tuples, Ports) to an (x,y) coordinate.

    Args:
        c: array-like[N] or Port
            Input to translate into a coordinate.

    Returns:
        c : array-like[2]
            Parsed coordinate.
    """
    if isinstance(c, Port):
        return c.center
    elif np.array(c).size == 2:
        return cast(tuple[float, float], tuple(c))
    raise ValueError(
        "Could not parse coordinate, input should be array-like (e.g. [1.5,2.3] or a Port"
    )


def parse_move(
    origin: Coordinate | npt.NDArray[np.floating[Any]],
    destination: Coordinate | npt.NDArray[np.floating[Any]] | None,
    axis: Axis | None = None,
) -> tuple[float, float]:
    """Translates input coordinates to changes in position in the x and y directions.

    Args:
        origin : array-like[2] of int or float, Port, or key
            Origin point of the move.
        destination : array-like[2] of int or float, Port, key, or None
            Destination point of the move.
        axis : {'x', 'y'} Direction of move.

    Returns:
        dx : int or float
            Change in position in the x-direction.
        dy : int or float
            Change in position in the y-direction.
    """
    # If only one set of coordinates is defined, make sure it's used to move things
    if destination is None:
        destination = origin
        origin = (0, 0)

    d = parse_coordinate(destination)
    o = parse_coordinate(origin)
    if axis == "x":
        d = (d[0], o[1])
    if axis == "y":
        d = (o[0], d[1])
    dx, dy = np.array(d) - o

    return dx, dy
