"""
waterfall_app.py
=================
Tkinter GUI that reproduces the Igor Pro workflow from the procedure
file: it shows the simulated Rashba band map (Graph18:rashba) and a
"waterfall control" panel with Start value / End value / amp factor /
step fields plus "Plot EDCs" and "RedBlue" buttons, just like the
original Igor panel.

Run this file directly (e.g. open it in Thonny and press Run / F5).

Igor -> Python map
------------------
Rashba_func()      -> rashba_model.build_rashba_bands() (the `rashba` array)
Rashba_func2()     -> rashba_model.build_rashba_bands() (the `rashba1`/`rashba2` arrays)
Plot_EDCs_br()     -> WaterfallApp.plot_edcs()
ButtonProc()       -> WaterfallApp.on_plot_edcs()   ("Plot EDCs" button)
(RedBlue button)   -> WaterfallApp.on_red_blue()    (toggles the colour mode)
waveselect() /
Menu "waterfall
 plot"             -> not needed: there is only one dataset here, so no
                      wave-picker dialog is required.
Image line profile
("rashba_Prof1")   -> WaterfallApp.plot_mdc()       (a horizontal cut through
                      the band map at one fixed energy, i.e. a Momentum
                      Distribution Curve)
"""

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from rashba_model import build_rashba_bands, extract_edc, extract_mdc, DK


class WaterfallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rashba model - Python version of the Igor Pro project")

        # Colour mode toggled by the "RedBlue" button:
        #   True  -> band 1 always red, band 2 always blue (like the Igor
        #            Plot_EDCs_br routine)
        #   False -> gradient colouring by curve index (like the plain
        #            Plot_EDCs routine, green -> blue)
        self.red_blue_mode = True

        # Build the physics model once; it never needs to change unless
        # you edit the parameters at the top of rashba_model.py.
        self.E, self.k, self.rashba, self.rashba1, self.rashba2 = build_rashba_bands()

        self._build_layout()
        self.on_apply_zoom()      # draw the band map already zoomed in on the bands
        self.plot_edcs()  # draw an initial waterfall with the default values
        self.plot_mdc()   # draw an initial MDC profile with the default value

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self):
        # Left: band map (equivalent to "Graph18:rashba")
        left = ttk.Frame(self.root, padding=8)
        left.grid(row=0, column=0, sticky="nsew")

        zoom_control = ttk.LabelFrame(left, text="band map zoom", padding=10)
        zoom_control.pack(fill="x", pady=(0, 8))

        # Defaults zoom in on the region where the bands actually sit,
        # instead of the full 0..-1.1 / 0..2.9 array range, so the bands
        # land centred in the plot instead of surrounded by black space.
        self.k_min_var = tk.StringVar(value="-0.30")
        self.k_max_var = tk.StringVar(value="-1.10")
        self.e_min_var = tk.StringVar(value="0.90")
        self.e_max_var = tk.StringVar(value="2.90")

        self._add_field(zoom_control, "K|| min (1/Å)", self.k_min_var, 0)
        self._add_field(zoom_control, "K|| max (1/Å)", self.k_max_var, 1)
        self._add_field(zoom_control, "E min (eV)", self.e_min_var, 2)
        self._add_field(zoom_control, "E max (eV)", self.e_max_var, 3)

        zoom_btn_frame = ttk.Frame(zoom_control)
        zoom_btn_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        ttk.Button(zoom_btn_frame, text="Apply Zoom", command=self.on_apply_zoom).pack(
            side="left", expand=True, fill="x", padx=(0, 4)
        )
        ttk.Button(zoom_btn_frame, text="Reset View", command=self.on_reset_zoom).pack(
            side="left", expand=True, fill="x", padx=(4, 0)
        )

        self.map_fig = Figure(figsize=(5, 5), dpi=100)
        self.map_ax = self.map_fig.add_subplot(111)
        self.map_canvas = FigureCanvasTkAgg(self.map_fig, master=left)
        self.map_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Right: waterfall control panel (equivalent to the "waterfall
        # control" floating panel) stacked above the waterfall plot
        # (equivalent to "Rash_wf_br").
        right = ttk.Frame(self.root, padding=8)
        right.grid(row=0, column=1, sticky="nsew")

        control = ttk.LabelFrame(right, text="waterfall control", padding=10)
        control.pack(fill="x", pady=(0, 8))

        self.start_var = tk.StringVar(value="-1.04")
        self.end_var = tk.StringVar(value="-0.41")
        self.amp_var = tk.StringVar(value="0.03")
        self.step_var = tk.StringVar(value="0.03")

        self._add_field(control, "start value", self.start_var, 0)
        self._add_field(control, "end value", self.end_var, 1)
        self._add_field(control, "amp factor", self.amp_var, 2)
        self._add_field(control, "step", self.step_var, 3)

        btn_frame = ttk.Frame(control)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        ttk.Button(btn_frame, text="RedBlue", command=self.on_red_blue).pack(
            side="left", expand=True, fill="x", padx=(0, 4)
        )
        ttk.Button(btn_frame, text="Plot EDCs", command=self.on_plot_edcs).pack(
            side="left", expand=True, fill="x", padx=(4, 0)
        )

        self.wf_fig = Figure(figsize=(5, 6), dpi=100)
        self.wf_ax = self.wf_fig.add_subplot(111)
        self.wf_canvas = FigureCanvasTkAgg(self.wf_fig, master=right)
        self.wf_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Third column: MDC control (equivalent to the "rashba_Prof1"
        # image line profile) - a single fixed-energy horizontal cut
        # through the band map, plotted as intensity vs K||.
        far_right = ttk.Frame(self.root, padding=8)
        far_right.grid(row=0, column=2, sticky="nsew")

        mdc_control = ttk.LabelFrame(far_right, text="MDC profile control", padding=10)
        mdc_control.pack(fill="x", pady=(0, 8))

        self.energy_var = tk.StringVar(value="1.80")
        self._add_field(mdc_control, "energy cut (eV)", self.energy_var, 0)

        ttk.Button(mdc_control, text="Plot MDC", command=self.on_plot_mdc).grid(
            row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew"
        )

        self.mdc_fig = Figure(figsize=(5, 6), dpi=100)
        self.mdc_ax = self.mdc_fig.add_subplot(111)
        self.mdc_canvas = FigureCanvasTkAgg(self.mdc_fig, master=far_right)
        self.mdc_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)

    @staticmethod
    def _add_field(parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(parent, textvariable=var, width=10).grid(
            row=row, column=1, sticky="e", pady=3, padx=(10, 0)
        )

    # ------------------------------------------------------------------
    # Plot 1: the Rashba band map ("Graph18:rashba" equivalent)
    # ------------------------------------------------------------------
    def _draw_band_map(self, k_min=None, k_max=None, e_min=None, e_max=None):
        ax = self.map_ax
        ax.clear()
        ax.imshow(
            self.rashba,
            extent=[self.k[0], self.k[-1], self.E[-1], self.E[0]],
            aspect="auto",
            cmap="gray",
            origin="upper",
        )
        ax.set_xlabel("K|| (1/Å)")
        ax.set_ylabel("Electron Binding Energy [eV]")
        ax.set_title(f"Rashba model for {DK:.3f} Å$^{{-1}}$ splitting")

        # Zoom is just a view crop - set_xlim/set_ylim don't touch the
        # underlying data, they only change what part of it is visible.
        if k_min is not None and k_max is not None:
            ax.set_xlim(k_min, k_max)
        if e_min is not None and e_max is not None:
            ax.set_ylim(e_max, e_min)  # inverted so low energy stays on top

        self.map_fig.tight_layout()
        self.map_canvas.draw()

    # ------------------------------------------------------------------
    # Plot 2: the EDC waterfall ("Rash_wf_br" / Plot_EDCs_br equivalent)
    # ------------------------------------------------------------------
    def _read_controls(self):
        """Parse and validate the four control-panel fields."""
        try:
            startval = float(self.start_var.get())
            endval = float(self.end_var.get())
            amp = float(self.amp_var.get())
            step = float(self.step_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Start value, end value, amp factor and step "
                "must all be numbers."
            )
            return None
        if step <= 0:
            messagebox.showerror("Invalid input", "Step must be greater than 0.")
            return None
        return startval, endval, amp, step

    def plot_edcs(self):
        """Equivalent of Igor's Plot_EDCs_br(rashba1, rashba2)."""
        values = self._read_controls()
        if values is None:
            return
        startval, endval, amp, step = values

        num = int(np.floor(abs(endval - startval) / step)) + 1

        ax = self.wf_ax
        ax.clear()

        for j in range(num):
            kv = startval + j * step
            edc1, k1 = extract_edc(self.E, self.k, self.rashba1, kv)
            edc2, k2 = extract_edc(self.E, self.k, self.rashba2, kv)

            if self.red_blue_mode:
                color1, color2 = "red", "blue"
            else:
                # gradient colouring, mirrors Igor's
                # rgb=(0, 65535*(1-j/num), 65535*j/num) green->blue fade
                frac = j / max(num - 1, 1)
                color1 = (0, 1 - frac, frac)
                color2 = (0, 1 - frac, frac)

            ax.plot(self.E, k1 + amp * edc1, color=color1, lw=1)
            ax.plot(self.E, k2 + amp * edc2, color=color2, lw=1)

        ax.set_xlabel("Electron Binding Energy [eV]")
        ax.set_ylabel("K|| (1/Å)")
        ax.invert_xaxis()
        ax.set_title(f"{num} EDCs, step={step:g}, amp={amp:g}")
        self.wf_fig.tight_layout()
        self.wf_canvas.draw()

    # ------------------------------------------------------------------
    # Plot 3: the MDC profile ("rashba_Prof1" equivalent)
    # ------------------------------------------------------------------
    def plot_mdc(self):
        """
        Equivalent of drawing an image line profile across the band map
        at one fixed binding energy - a Momentum Distribution Curve
        (MDC). Because each Rashba branch is a full parabola in k, a
        cut above the band bottom crosses each branch twice, giving the
        characteristic four-peak curve.
        """
        try:
            energy_value = float(self.energy_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Energy cut must be a number.")
            return

        mdc, actual_E = extract_mdc(self.E, self.k, self.rashba, energy_value)

        ax = self.mdc_ax
        ax.clear()
        ax.plot(self.k, mdc, color="red", lw=2)
        ax.set_xlim(self.k[0] + 0.05, self.k[-1] - 0.1)
        ax.set_xlabel("K|| (1/Å)")
        ax.set_ylabel("Photoemission Intensity (a.u.)")
        ax.set_title("Rashba model")
        ax.text(
            0.05, 0.92, f"E = {actual_E:.2f} eV",
            transform=ax.transAxes, fontsize=10, va="top",
        )
        self.mdc_fig.tight_layout()
        self.mdc_canvas.draw()

    # ------------------------------------------------------------------
    # Button callbacks
    # ------------------------------------------------------------------
    def on_plot_edcs(self):
        self.plot_edcs()

    def on_red_blue(self):
        self.red_blue_mode = not self.red_blue_mode
        self.plot_edcs()

    def on_plot_mdc(self):
        self.plot_mdc()

    def on_apply_zoom(self):
        try:
            k_min = float(self.k_min_var.get())
            k_max = float(self.k_max_var.get())
            e_min = float(self.e_min_var.get())
            e_max = float(self.e_max_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid input", "K|| min/max and E min/max must all be numbers."
            )
            return
        self._draw_band_map(k_min=k_min, k_max=k_max, e_min=e_min, e_max=e_max)

    def on_reset_zoom(self):
        """Go back to showing the full array range, no cropping."""
        self.k_min_var.set(f"{self.k[0]:.2f}")
        self.k_max_var.set(f"{self.k[-1]:.2f}")
        self.e_min_var.set(f"{self.E[0]:.2f}")
        self.e_max_var.set(f"{self.E[-1]:.2f}")
        self._draw_band_map(
            k_min=self.k[0], k_max=self.k[-1], e_min=self.E[0], e_max=self.E[-1]
        )


def main():
    root = tk.Tk()
    app = WaterfallApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
