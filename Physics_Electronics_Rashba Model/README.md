# Rashba Band Model & EDC Waterfall — Igor Pro → Python

## What this is

This is a Python port from igor pro to python:
simulate a **Rashba-split electronic band** the way it would appear in
an ARPES (angle-resolved photoemission spectroscopy) measurement, and
to inspect it two ways: as a **waterfall plot of EDCs** (Energy
Distribution Curves — vertical cuts through the band map at fixed
momentum), and as a **single MDC profile** (Momentum Distribution
Curve — a horizontal cut through the band map at one fixed binding
energy, like Igor's `rashba_Prof1` image line profile).

The original Igor code did two things:

1. `Rashba_func()` / `Rashba_func2()` built a 2D array simulating the
   ARPES intensity map of two spin-split parabolic bands.
2. A small GUI panel ("waterfall control") let you pick a start
   momentum, an end momentum, a step between cuts, and an amplitude
   factor, then extract and stack the corresponding EDCs into a
   waterfall plot, colour-coded red/blue for the two spin branches.

This project reproduces both pieces in plain Python with a Tkinter
GUI, so it runs anywhere Python + Thonny run — no Igor Pro license
needed.

## The physics (what's actually being simulated)

A Rashba-split band consists of two spin-polarised parabolic bands,
offset from each other in momentum by a splitting `dk`. At a given
momentum `k`, the two band energies are:

```
E₊(k) = e0 + (hh2m/meff) · (k − center + dk/2)²
E₋(k) = e0 + (hh2m/meff) · (k − center − dk/2)²
```

- `e0` — binding energy of the band minimum
- `center` — momentum position of the band minimum
- `hh2m / meff` — sets the curvature of the parabola (an effective-mass parameter)
- `dk` — the Rashba splitting itself (the "Niesner splitting" in the original comment)

The simulated ARPES intensity at a given (energy, momentum) point is
the sum of two Gaussian peaks centred on those two band energies, with
a width representing the finite energy resolution of the measurement:

```
I(E, k) = gauss(E, E₊(k), width) + gauss(E, E₋(k), width)
gauss(x, x0, w) = exp(−((x − x0)/w)²)
```

This is exactly Igor's built-in `gauss()` function, reproduced with
`numpy.exp` in `rashba_model.py`.

All the default parameter values are carried over unchanged from the
Igor code: `dk=0.086`, `width=0.18`, `center=-0.74`, `e0=1.4`,
`hh2m=3.8099`, `meff=0.17751`.

### Why the MDC profile has four peaks, not two

An EDC (a vertical cut at fixed k) crosses each of the two Rashba
branches once, so it shows two peaks. An MDC (a horizontal cut at
fixed energy) is different: each branch is a *complete parabola* in k,
symmetric about its own vertex. Any fixed energy above that vertex
intersects a single parabola **twice** — once on either side of its
minimum. With two branches, that's four crossings total, arranged as
two closely-spaced pairs straddling the overall band centre — exactly
the shape in the `rashba_Prof1` screenshot.

## How the Igor code maps onto the Python files

| Igor Pro                                | Python equivalent                                  |
|------------------------------------------|-----------------------------------------------------|
| `Rashba_func()` (the summed `rashba` wave) | `rashba_model.build_rashba_bands()` → `rashba`     |
| `Rashba_func2()` (`rashba1`, `rashba2`)  | `rashba_model.build_rashba_bands()` → `rashba1`, `rashba2` |
| `gauss(x, x0, width)`                    | `rashba_model.gauss(x, x0, width)`                  |
| `Display; AppendToGraph rashba`          | `WaterfallApp._draw_band_map()` (left-hand plot)    |
| "waterfall control" panel (start/end/amp/step) | `WaterfallApp` control frame (Tkinter `Entry` widgets) |
| `Plot_EDCs_br(w1, w2)`                   | `WaterfallApp.plot_edcs()`                          |
| `ButtonProc` ("Plot EDCs" button)        | `WaterfallApp.on_plot_edcs()`                       |
| `EDCw[][curpos]` column extraction       | `rashba_model.extract_edc()`                        |
| Red / blue trace colouring               | `WaterfallApp.plot_edcs()`, `red_blue_mode = True`  |
| (no direct Igor equivalent shown)        | `WaterfallApp.on_red_blue()` — toggles between fixed red/blue and a green→blue gradient (closer to the plain, single-wave `Plot_EDCs` routine also present in the Igor file) |
| Image line profile (`Graph18_Prof:rashba_Prof1`) | `rashba_model.extract_mdc()` + `WaterfallApp.plot_mdc()` |
| (no direct Igor equivalent shown)        | `WaterfallApp.on_apply_zoom()` / `on_reset_zoom()` — crops the band-map view to a chosen K||/energy window, so the bands sit centred instead of surrounded by black space |

One thing worth flagging honestly: the Igor code you shared never
shows a `SetScale` command for the `rashba` wave, so the exact axis
calibration wasn't in the text file. The Python version's energy axis
(0–2.9 eV, 461 points) and momentum axis (0 to −1.1 Å⁻¹, 413 points)
were chosen to reproduce the axis ranges and band position visible in
your screenshot — and the resulting figure lines up with it almost
point-for-point. If you have the real `SetScale` values from your Igor
experiment file, just edit `E_MIN`, `E_MAX`, `K_MIN`, `K_MAX` at the
top of `rashba_model.py` to match exactly.

## Files

```
rashba_project/
├── rashba_model.py     # physics only: builds the numpy arrays, no plotting
├── waterfall_app.py     # Tkinter GUI: band map + waterfall control panel
├── requirements.txt
├── images/               # example output figures, referenced below
└── README.md
```

`rashba_model.py` has no GUI or plotting code in it at all — it just
builds numpy arrays — so you can also import it directly in a plain
script or a Jupyter notebook if you ever want the data without the GUI.

## Results

### Band map

The simulated ARPES band map, equivalent to `Graph18:rashba`. Two
spin-split parabolic bands, vertex at K|| ≈ −0.74 Å⁻¹, E ≈ 1.4–1.6 eV.
By default the app now zooms straight to the region around the bands,
so they sit centred in the plot instead of being surrounded by a lot
of empty black space — use the **band map zoom** controls (K|| min/max,
E min/max, plus **Apply Zoom** / **Reset View**) to crop the view
further or go back to the full range:

![Rashba band map, zoomed on the bands](images/band_map_zoomed.png)

### EDC waterfall (default values)

With the default control-panel values from your Igor screenshot
(`start=-1.04`, `end=-0.41`, `step=0.03`, `amp=0.03`), 22 EDCs are cut
from the band map and stacked at their momentum position. The two
spin branches (red/blue) visibly cross and swap relative intensity as
K|| sweeps across the splitting — the signature look of a Rashba
waterfall:

![EDC waterfall, default parameters](images/waterfall_default.png)

### MDC profile

A single horizontal cut through the band map at E = 1.80 eV,
equivalent to the `rashba_Prof1` image line profile. Because each
branch is a full parabola in k, this fixed-energy cut crosses each
branch twice, giving four peaks arranged as two pairs:

![MDC profile at 1.80 eV](images/mdc_profile.png)

Cutting at a deeper energy (2.00 eV, further from the band bottom)
spreads all four peaks further apart, since each parabola is being cut
further from its vertex:

![MDC profile comparison at two energies](images/mdc_energy_comparison.png)

### Same data, different parameters — a direct comparison

All three panels below come from the exact same underlying band data.
Only the waterfall control values differ:

![Effect of start/end/step/amp on the waterfall](images/param_comparison.png)

- **Left (default, step=0.03):** 22 densely-packed EDCs. The crossing
  pattern between the two branches is clearly visible.
- **Middle (step=0.10):** only 7 curves from the same momentum range.
  Same underlying physics, but sampled so coarsely that the crossing
  structure is barely visible — a real example of how too large a step
  can hide the interesting part of the data.
- **Right (narrow k-range, fine step, amp=0.06):** zoomed into a
  narrow window right at the crossing point, with the amplitude scaled
  up. Tightly packed, tall, overlapping curves — a completely different
  visual result from the same model, just by changing four numbers.

This is the point of separating `rashba_model.py` (the physics) from
`waterfall_app.py` (the display): the same `build_rashba_bands()` /
`extract_edc()` / `extract_mdc()` functions can be sliced, stepped, and
scaled however you like — in the GUI, in a notebook, or in a batch
script — without ever touching the underlying model.

## Running it in Thonny

1. Open Thonny.
2. Install the two dependencies: **Tools → Manage packages...**, then
   search for and install `numpy` and `matplotlib`. (`tkinter` ships
   with Python already — you don't need to install it separately. On
   some Linux installs it's a separate OS package: `sudo apt install
   python3-tk`.)
3. Open `waterfall_app.py` in Thonny.
4. Press **Run** (F5).

Three panels should appear side by side:

- **Left panel** — a **band map zoom** control box (K|| min/max, E
  min/max, plus **Apply Zoom** / **Reset View**) sitting above the
  simulated Rashba band map, equivalent to `Graph18:rashba`: a black
  background with the two parabolic bands glowing white, split apart
  near their vertex, zoomed by default so the bands sit centred.
- **Middle panel** — the "waterfall control" box (start value, end
  value, amp factor, step, plus the **RedBlue** and **Plot EDCs**
  buttons) sitting above the waterfall plot, equivalent to
  `Rash_wf_br`.
- **Right panel** — the "MDC profile control" box (a single **energy
  cut** field plus a **Plot MDC** button) sitting above a red intensity
  vs K|| curve, equivalent to the `rashba_Prof1` image line profile.
  With the default energy (1.80 eV) it reproduces the same four-peak
  shape shown in your screenshot.

## Using the controls

- **K|| min / K|| max, E min / E max (band map zoom)** — crops the
  view of the band map to that momentum/energy window. The data itself
  never changes, only what part of it is visible, so this is free to
  play with. **Apply Zoom** redraws with the current fields; **Reset
  View** puts the numbers back to the full array range (0 to −1.1 Å⁻¹,
  0 to 2.9 eV) and redraws. The app opens already zoomed to
  `(-0.30, -1.10)` / `(0.90, 2.90)` so the bands are centred by default.
- **start value / end value** — the momentum (K||) range to cut EDCs
  from, in 1/Å. Defaults: `-1.04` to `-0.41`, matching your screenshot.
- **step** — momentum spacing between successive EDCs (1/Å). Smaller
  step = more, more tightly packed curves.
- **amp factor** — how much each EDC's intensity is scaled before
  being added on top of its momentum baseline. Larger = taller peaks,
  more overlap between neighbouring curves.
- **Plot EDCs** — recomputes and redraws the waterfall using whatever
  is currently in the four fields (equivalent to Igor's `ButtonProc` →
  `Plot_EDCs_br`).
- **RedBlue** — toggles the colour scheme between fixed red (band 1) /
  blue (band 2), and a green-to-blue gradient by curve index.
- **energy cut (eV)** — the fixed binding energy for the MDC profile.
  Values closer to the band bottom (`e0 = 1.4` eV) bring the two inner
  peaks together and eventually merge all four into two; values deeper
  below it spread all four peaks further apart.
- **Plot MDC** — recomputes and redraws the MDC profile using whatever
  is currently in the energy field.
