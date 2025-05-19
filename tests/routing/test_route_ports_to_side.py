from __future__ import annotations

import sys

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Test is ignored on Windows.",
)
def test_route_ports_to_side(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    c = gf.Component()
    cross_section = "strip"
    dummy = gf.c.nxn(north=2, south=2, west=2, east=2, cross_section=cross_section)
    dummy_ref = c << dummy
    routes, _ = gf.routing.route_ports_to_side(
        c,
        ports=dummy_ref.ports,
        side="south",
        cross_section=cross_section,
        y=-91,
        x=-100,
    )

    if check:
        lengths = {i: route.length for i, route in enumerate(routes)}
        data_regression.check(lengths)


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Test is ignored on Windows.",
)
def test_route_ports_to_x(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    c = gf.Component()
    cross_section = "strip"
    dummy = gf.c.nxn(north=2, south=2, west=2, east=2, cross_section=cross_section)
    dummy_ref = c << dummy
    routes, _ = gf.routing.route_ports_to_side(
        c,
        ports=dummy_ref.ports,
        cross_section=cross_section,
        x=50,
        side="east",
    )
    if check:
        lengths = {i: route.length for i, route in enumerate(routes)}
        data_regression.check(lengths)


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Test is ignored on Windows.",
)
def test_route_ports_to_y(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    c = gf.Component()
    cross_section = "strip"
    dummy = gf.c.nxn(north=2, south=2, west=2, east=2, cross_section=cross_section)
    dummy_ref = c << dummy
    routes, _ = gf.routing.route_ports_to_side(
        c,
        ports=dummy_ref.ports,
        cross_section=cross_section,
        y=50,
        side="north",
    )
    if check:
        lengths = {i: route.length for i, route in enumerate(routes)}
        data_regression.check(lengths)
