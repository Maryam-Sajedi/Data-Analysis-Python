"""
simulate_led.py
================
Main script: solves the LED circuit's operating point, prints the
results, and generates all result plots (diode I-V curve with load
line, and a supply-voltage sweep) into the images/ folder.

Run this file directly (e.g. open it in Thonny and press Run / F5).
"""

import os

import numpy as np
import matplotlib.pyplot as plt

from led_model import (
    V_SUPPLY, R_RESISTOR, VT, IDS,
    diode_current, solve_operating_point, sweep_supply_voltage,
)

IMAGES_DIR = "images"


def print_operating_point(point):
    print("LED circuit operating point")
    print("-" * 32)
    print(f"Supply voltage       : {point['v_supply']:.3f} V")
    print(f"LED forward voltage   : {point['v_diode']:.4f} V")
    print(f"LED forward current   : {point['i_diode'] * 1e3:.3f} mA")
    print(f"Resistor voltage      : {point['v_resistor']:.4f} V")
    print(f"Resistor current      : {point['i_resistor'] * 1e3:.3f} mA")
    print(f"LED power dissipation : {point['p_diode'] * 1e3:.3f} mW")
    print(f"Resistor power        : {point['p_resistor'] * 1e3:.3f} mW")


def plot_iv_with_load_line(point, path):
    """
    Classic load-line analysis: the diode's own exponential I-V curve,
    the resistor's straight load line (I = (V_supply - V) / R), and
    their intersection, which is the operating point found above.
    """
    v = np.linspace(0, V_SUPPLY, 500)
    i_diode_curve = diode_current(v) * 1e3          # mA
    i_load_line = (V_SUPPLY - v) / R_RESISTOR * 1e3  # mA

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(v, i_diode_curve, color="red", lw=2, label="LED I-V curve")
    ax.plot(v, i_load_line, color="blue", lw=2, linestyle="--",
            label=f"Load line ({R_RESISTOR:g} \u03a9)")
    ax.plot(point["v_diode"], point["i_diode"] * 1e3, "ko", ms=8, zorder=5,
            label="Operating point")
    ax.annotate(
        f"({point['v_diode']:.3f} V, {point['i_diode']*1e3:.2f} mA)",
        xy=(point["v_diode"], point["i_diode"] * 1e3),
        xytext=(point["v_diode"] + 0.3, point["i_diode"] * 1e3 - 5),
        fontsize=9,
    )
    ax.set_xlabel("Voltage across LED (V)")
    ax.set_ylabel("Current (mA)")
    ax.set_title("LED I-V curve and resistor load line")
    ax.set_xlim(0, V_SUPPLY)
    ax.set_ylim(0, max(i_load_line) * 1.05)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_supply_sweep(path):
    """
    Sweep the supply voltage from 0 to 5 V and show how the LED
    current and LED voltage each respond - useful for seeing how
    sharply the diode "turns on".
    """
    v_supply, v_diode, i_diode = sweep_supply_voltage(0.0, V_SUPPLY, 300)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(v_supply, i_diode * 1e3, color="red", lw=2)
    ax1.set_xlabel("Supply voltage (V)")
    ax1.set_ylabel("LED current (mA)")
    ax1.set_title("LED current vs. supply voltage")
    ax1.grid(alpha=0.3)

    ax2.plot(v_supply, v_diode, color="darkorange", lw=2)
    ax2.set_xlabel("Supply voltage (V)")
    ax2.set_ylabel("LED forward voltage (V)")
    ax2.set_title("LED voltage vs. supply voltage")
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)

    point = solve_operating_point()
    print_operating_point(point)

    iv_path = os.path.join(IMAGES_DIR, "led_iv_load_line.png")
    sweep_path = os.path.join(IMAGES_DIR, "led_supply_sweep.png")

    plot_iv_with_load_line(point, iv_path)
    plot_supply_sweep(sweep_path)

    print()
    print(f"Saved: {iv_path}")
    print(f"Saved: {sweep_path}")


if __name__ == "__main__":
    main()
