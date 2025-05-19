from __future__ import annotations

import gdsfactory as gf
from gdsfactory.generic_tech.layer_map import LAYER


def test_write_labels() -> None:
    """Write labels to a CSV file."""
    c = gf.c.straight()
    c = gf.add_pins.add_pins_siepic_container(c)

    gdspath = c.write_gds()
    labels = list(
        gf.labels.find_labels(gdspath, layer_label=LAYER.PORT, prefixes=["o"])
    )
    gf.labels.write_labels(gdspath, layer_label=LAYER.PORT, prefixes=["o"])
    assert len(labels) == 2
