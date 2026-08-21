#!/usr/bin/env python3
"""
Binomische Formeln - calculator and expander:

1. (a + b)^2 = a^2 + 2ab + b^2
2. (a - b)^2 = a^2 - 2ab + b^2
3. (a + b)(a - b) = a^2 - b^2

Run without arguments for an interactive prompt, or pass a and b:
    python binomische_formeln.py 3 5
"""

import sys


def fmt(x: float) -> str:
    """Print 4 instead of 4.0, but keep real decimals."""
    return f"{x:g}"


def first(a: float, b: float) -> tuple[str, float]:
    """(a + b)^2 = a^2 + 2ab + b^2"""
    result = (a + b) ** 2
    steps = (
        f"({fmt(a)} + {fmt(b)})^2 = "
        f"{fmt(a)}^2 + 2*{fmt(a)}*{fmt(b)} + {fmt(b)}^2 = "
        f"{fmt(a**2)} + {fmt(2 * a * b)} + {fmt(b**2)} = {fmt(result)}"
    )
    return steps, result


def second(a: float, b: float) -> tuple[str, float]:
    """(a - b)^2 = a^2 - 2ab + b^2"""
    result = (a - b) ** 2
    steps = (
        f"({fmt(a)} - {fmt(b)})^2 = "
        f"{fmt(a)}^2 - 2*{fmt(a)}*{fmt(b)} + {fmt(b)}^2 = "
        f"{fmt(a**2)} - {fmt(2 * a * b)} + {fmt(b**2)} = {fmt(result)}"
    )
    return steps, result


def third(a: float, b: float) -> tuple[str, float]:
    """(a + b)(a - b) = a^2 - b^2"""
    result = (a + b) * (a - b)
    steps = (
        f"({fmt(a)} + {fmt(b)}) * ({fmt(a)} - {fmt(b)}) = "
        f"{fmt(a)}^2 - {fmt(b)}^2 = "
        f"{fmt(a**2)} - {fmt(b**2)} = {fmt(result)}"
    )
    return steps, result


FORMULAS = {
    1: ("1. Binomische Formel", first),
    2: ("2. Binomische Formel", second),
    3: ("3. Binomische Formel", third),
}


def show_all(a: float, b: float) -> None:
    for number, (name, func) in FORMULAS.items():
        steps, _ = func(a, b)
        print(f"{name}:")
        print(f"{steps}\n")


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 2:
        a, b = float(args[0]), float(args[1])
    else:
        try:
            a = float(input("a = "))
            b = float(input("b = "))
        except ValueError:
            print("Please enter numbers only.")
            return
        except (EOFError, KeyboardInterrupt):
            print()
            return 
    print()
    show_all(a, b)


if __name__ == "__main__":
    main()
