"""
Tools → Manage packages → search "scipy" → Install)

led_model.py
============
Physics and circuit equations only - no plotting, no GUI. This module
can be imported anywhere: a script, a notebook, or another program.

Circuit
-------
A constant DC voltage source drives a series loop of one diode (used
here as an LED) and one current-limiting resistor, referenced to
ground:

    +-------[ LED ]-------+
    |                      |
   (V)                   [ R ]
    |                      |
    +----------+-----------+
               |
              ---  ground

Diode model
-----------
The diode is modelled with the standard exponential (Shockley) diode
law:

    I_diode = Ids * (exp(V_diode / Vt) - 1) + V_diode / R_parallel

- `Ids`         - reverse saturation current
- `Vt`          - thermal voltage (kT/q at room temperature is about
                  0.026 V, which is also used here as a fit parameter
                  rather than a strict physical temperature voltage)
- `R_parallel`  - a very large parallel leakage resistance (a detail
                  most simple diode equations omit; it only matters at
                  reverse bias or very low forward voltage, and is
                  included here for completeness)

Circuit equation
-----------------
Kirchhoff's voltage law around the loop gives:

    V_supply = V_diode + I_diode * R_resistor

Since `I_diode` is itself a (nonlinear, exponential) function of
`V_diode`, this can't be solved algebraically - it's solved
numerically for the diode voltage that satisfies both equations at
once, using bisection (`scipy.optimize.brentq`).
"""

import numpy as np
from scipy.optimize import brentq

# ---------------------------------------------------------------------
# Default circuit parameters (same values as the original circuit)
# ---------------------------------------------------------------------
V_SUPPLY = 5.0        # supply voltage, V
R_RESISTOR = 330.0    # current-limiting resistor, Ohm
VT = 0.026            # diode thermal/fit voltage, V
IDS = 1e-9            # diode reverse saturation current, A
R_PARALLEL = 1e8      # diode parallel leakage resistance, Ohm


def diode_current(v_diode, vt=VT, ids=IDS, r_parallel=R_PARALLEL):
    """
    Shockley diode equation with an added parallel leakage resistance,
    the same form used by standard circuit-simulator diode models.
    """
    return ids * (np.exp(v_diode / vt) - 1.0) + v_diode / r_parallel


def circuit_residual(v_diode, v_supply=V_SUPPLY, r=R_RESISTOR, vt=VT, ids=IDS,
                      r_parallel=R_PARALLEL):
    """
    Kirchhoff's voltage law, rearranged to equal zero at the solution:
        v_supply - v_diode - I_diode(v_diode) * r = 0
    """
    i = diode_current(v_diode, vt, ids, r_parallel)
    return v_supply - v_diode - i * r


def solve_operating_point(v_supply=V_SUPPLY, r=R_RESISTOR, vt=VT, ids=IDS,
                           r_parallel=R_PARALLEL):
    """
    Solve the series LED + resistor circuit for its DC operating point.

    Returns a dict with the diode voltage/current, the resistor
    voltage/current (equal to the diode current, since it's a series
    loop), and the power dissipated in each component.
    """
    # A forward-biased silicon-type diode sits well under 1.5 V in this
    # kind of low-current circuit, and v_diode can never exceed
    # v_supply, so (0, v_supply) safely brackets the root.
    v_diode = brentq(
        circuit_residual, 0.0, v_supply,
        args=(v_supply, r, vt, ids, r_parallel),
        xtol=1e-12, rtol=1e-12,
    )
    i_diode = diode_current(v_diode, vt, ids, r_parallel)
    v_resistor = v_supply - v_diode
    i_resistor = i_diode  # series loop: same current everywhere

    return {
        "v_supply": v_supply,
        "v_diode": v_diode,
        "i_diode": i_diode,
        "v_resistor": v_resistor,
        "i_resistor": i_resistor,
        "p_diode": v_diode * i_diode,
        "p_resistor": v_resistor * i_resistor,
    }


def sweep_supply_voltage(v_min=0.0, v_max=5.0, n_points=200, r=R_RESISTOR,
                          vt=VT, ids=IDS, r_parallel=R_PARALLEL):
    """
    Solve the circuit's operating point at many supply voltages, to
    build up an I-V-style sweep (e.g. for plotting current vs supply
    voltage, or the diode's own I-V curve as it's swept through this
    circuit).

    Returns (v_supply_array, v_diode_array, i_diode_array).
    """
    v_supply_array = np.linspace(v_min, v_max, n_points)
    v_diode_array = np.empty_like(v_supply_array)
    i_diode_array = np.empty_like(v_supply_array)

    for idx, vs in enumerate(v_supply_array):
        if vs <= 0:
            v_diode_array[idx] = 0.0
            i_diode_array[idx] = 0.0
            continue
        point = solve_operating_point(vs, r, vt, ids, r_parallel)
        v_diode_array[idx] = point["v_diode"]
        i_diode_array[idx] = point["i_diode"]

    return v_supply_array, v_diode_array, i_diode_array
