from __future__ import annotations

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.difftest import difftest


@gf.cell
def sample_fiber_array() -> Component:
    component = gf.components.coupler(gap=0.2, length=5.0)
    return gf.routing.add_fiber_array(component=component)


@gf.cell
def sample_excluded_ports() -> Component:
    component = gf.components.crossing()
    return gf.routing.add_fiber_array(component=component, excluded_ports=["o1"])


@gf.cell
def sample_fiber_single() -> Component:
    c = gf.components.coupler(gap=0.244, length=5.67)
    return gf.routing.add_fiber_single(component=c)


components = [sample_fiber_array, sample_fiber_single, sample_excluded_ports]


@pytest.fixture(params=components, scope="function")
def component(request: pytest.FixtureRequest) -> Component:
    return request.param()  # type: ignore[no-any-return]


def test_gds(component: Component) -> None:
    """Avoid regressions in GDS geometry shapes and layers."""
    difftest(component)


def test_settings(component: Component, data_regression: DataRegressionFixture) -> None:
    """Avoid regressions when exporting settings."""
    settings = component.to_dict()
    data_regression.check(settings)


if __name__ == "__main__":
    c = sample_excluded_ports()
    c.pprint_ports()
    c.show()
