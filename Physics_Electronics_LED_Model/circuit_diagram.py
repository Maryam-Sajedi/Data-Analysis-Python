"""
circuit_diagram.py
===================
Draws the LED circuit schematic (constant voltage source -> LED ->
resistor -> ground, in a series loop) and saves it as a PNG.

Run this file directly to (re)generate images/circuit_schematic.png,
or import `draw_circuit()` from another script.
"""

import os

import schemdraw
import schemdraw.elements as elm

from led_model import V_SUPPLY, R_RESISTOR, VT


def draw_circuit(path="images/circuit_schematic.png",
                  v_supply=V_SUPPLY, r_resistor=R_RESISTOR, vt=VT):
    """Draw the LED + resistor + DC source circuit and save it as an image."""
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with schemdraw.Drawing(file=path) as d:
        d += elm.SourceV().up().label(f"{v_supply:g} V")
        d += elm.Line().right()
        d += elm.LED().right().label(f"LED\nVt={vt:g} V", loc="top")
        d += elm.Line().down()
        d += elm.Resistor().down().label(f"{r_resistor:g} \u03a9")
        d += elm.Line().left()
        d += elm.Ground()
    return path


if __name__ == "__main__":
    out_path = draw_circuit()
    print(f"Circuit schematic saved to {out_path}")
