"""
rashba_model.py
================
Pure-numpy re-implementation of the physics from the Igor Pro procedure
file (Rashba_func / Rashba_func2). No plotting or GUI code lives here -
this module only builds the numeric arrays, so it can be reused,
tested, or imported by any front-end (Tkinter GUI, a Jupyter notebook,
a plain script, etc).

Physics
-------
The two Igor functions build a simulated ARPES (angle-resolved
photoemission) image of a Rashba-split band: two spin-polarised
parabolic bands, offset from each other in momentum by `dk`, each
broadened along the energy axis by a Gaussian of width `width`.

For a given momentum k, the two band energies are:

    E_plus(k)  = e0 + (hh2m/meff) * (k - center + dk/2)^2
    E_minus(k) = e0 + (hh2m/meff) * (k - center - dk/2)^2

and the simulated intensity at (E, k) is the sum of two Gaussians
centred on those two energies:

    I(E, k) = gauss(E, E_plus(k),  width) + gauss(E, E_minus(k), width)

where gauss(x, x0, w) = exp( -((x - x0) / w)^2 ), which is exactly how
Igor Pro's built-in `gauss()` function is defined.
"""

import numpy as np

# ---------------------------------------------------------------------
# Default model parameters (same numbers as in the Igor procedure)
# ---------------------------------------------------------------------
DK = 0.086          # Rashba splitting in k (Niesner splitting), 1/Angstrom
WIDTH = 0.18         # Gaussian broadening (energy resolution), eV
CENTER = -0.74       # k position of the band minimum, 1/Angstrom
E0 = 1.4             # binding energy of the band minimum, eV
HH2M = 3.8099        # hbar^2 / (2m_e) in eV*Angstrom^2 (as used in Igor code)
MEFF = 0.17751       # effective mass, in units of the free-electron mass

# Grid size / range, chosen to match the axes seen in the original
# Igor graphs: K|| from 0 to -1.1 (1/Angstrom), binding energy from
# 0 to ~2.9 eV. The Igor wave was 461 (energy) x 413 (k) points.
N_ENERGY = 461
N_K = 413
E_MIN, E_MAX = 0.0, 2.9
K_MIN, K_MAX = 0.0, -1.1


def gauss(x, x0, width):
    """Same definition as Igor Pro's built-in gauss() function."""
    return np.exp(-((x - x0) / width) ** 2)


def band_energy(k, sign, center=CENTER, dk=DK, e0=E0, hh2m=HH2M, meff=MEFF):
    """
    Energy of one Rashba branch at momentum k.
    sign = +1 for the "+dk/2" branch, -1 for the "-dk/2" branch.
    """
    return e0 + (hh2m / meff) * (k - center + sign * dk / 2) ** 2


def build_rashba_bands(
    dk=DK, width=WIDTH, center=CENTER, e0=E0, hh2m=HH2M, meff=MEFF,
    n_energy=N_ENERGY, n_k=N_K,
    e_min=E_MIN, e_max=E_MAX, k_min=K_MIN, k_max=K_MAX,
):
    """
    Build the simulated ARPES intensity map.

    Returns
    -------
    E : 1D array, length n_energy      - binding energy axis (eV)
    k : 1D array, length n_k           - momentum axis (1/Angstrom)
    rashba  : 2D array (n_energy, n_k) - sum of both bands  (Rashba_func)
    rashba1 : 2D array (n_energy, n_k) - "+dk/2" band only  (Rashba_func2)
    rashba2 : 2D array (n_energy, n_k) - "-dk/2" band only  (Rashba_func2)
    """
    E = np.linspace(e_min, e_max, n_energy)
    k = np.linspace(k_min, k_max, n_k)

    EE, KK = np.meshgrid(E, k, indexing="ij")  # EE varies along axis 0, KK along axis 1

    E_plus = band_energy(KK, +1, center, dk, e0, hh2m, meff)
    E_minus = band_energy(KK, -1, center, dk, e0, hh2m, meff)

    rashba1 = gauss(EE, E_plus, width)
    rashba2 = gauss(EE, E_minus, width)
    rashba = rashba1 + rashba2

    return E, k, rashba, rashba1, rashba2


def extract_edc(E, k, band_2d, k_value):
    """
    Extract an Energy Distribution Curve (EDC): a 1D cut of a 2D band
    array at the k-index nearest to `k_value`.
    Equivalent to Igor's `EDCw[][curpos]` column extraction.

    Returns (edc, actual_k) where actual_k is the k-axis value of the
    column that was actually used (nearest neighbour of k_value).
    """
    idx = int(np.argmin(np.abs(k - k_value)))
    return band_2d[:, idx], k[idx]


def extract_mdc(E, k, band_2d, energy_value):
    """
    Extract a Momentum Distribution Curve (MDC): a 1D cut of a 2D band
    array at the energy-index nearest to `energy_value`. This is a
    horizontal slice through the band map instead of a vertical one -
    equivalent to what Igor's image line-profile tool produces when you
    draw a horizontal line across the image (e.g. "rashba_Prof1").

    Because each Rashba branch is a full parabola in k, a cut taken
    above the band bottom crosses each of the two branches twice,
    which is why an MDC through this model shows four peaks instead
    of two.

    Returns (mdc, actual_E) where actual_E is the energy-axis value of
    the row that was actually used (nearest neighbour of energy_value).
    """
    idx = int(np.argmin(np.abs(E - energy_value)))
    return band_2d[idx, :], E[idx]
