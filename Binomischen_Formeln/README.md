# Binomische Formeln — Calculator

A small command-line program that applies the three binomial formulas to a pair
of numbers and prints the full working, not just the final answer.

---

## Goals

- Compute all three *binomische Formeln* for any two numbers `a` and `b`.
- Show every intermediate step, so the output can be checked by hand or used
  for learning rather than just trusted.
- Work in two modes: command-line arguments for quick use, interactive prompts
  for running from an IDE.
- Fail readably — wrong input produces a sentence, not a traceback.
- Depend on nothing outside the standard library.

## The formulas

| # | Formula | Expansion |
|---|---------|-----------|
| 1 | `(a + b)²` | `a² + 2ab + b²` |
| 2 | `(a - b)²` | `a² - 2ab + b²` |
| 3 | `(a + b)(a - b)` | `a² - b²` |

## Tools

- **Python 3.9+** — required for the built-in generic annotations
  (`tuple[str, float]`). On Python 3.8, add `from __future__ import annotations`
  as the first line of code.
- No build step, no virtual environment, no installation.

## Libraries

| Library | Type | Used for |
|---------|------|----------|
| `sys` | standard library | Reading `sys.argv` to accept `a` and `b` from the command line |

No third-party packages. Formatting uses f-strings with the `:g` format code so
that `9.0` prints as `9` while genuine decimals such as `2.5` are preserved.

## Usage

Pass both values as arguments:

```bash
python binomische_formeln.py 3 5
```

Or run with no arguments and enter them when prompted:

```bash
python binomische_formeln.py
a = 3
b = 5
```

## Results

Output for `a = 3`, `b = 5`:

```
1. Binomische Formel:
   (3 + 5)^2 = 3^2 + 2*3*5 + 5^2 = 9 + 30 + 25 = 64

2. Binomische Formel:
   (3 - 5)^2 = 3^2 - 2*3*5 + 5^2 = 9 - 30 + 25 = 4

3. Binomische Formel:
   (3 + 5) * (3 - 5) = 3^2 - 5^2 = 9 - 25 = -16
```

Decimal and negative inputs work as expected; `python binomische_formeln.py 2.5 -1`
is valid.

## Structure

| Component | Purpose |
|-----------|---------|
| `fmt(x)` | Formats numbers for display, dropping trailing `.0` |
| `first(a, b)` | 1st formula — returns the working as a string plus the numeric result |
| `second(a, b)` | 2nd formula — same contract |
| `third(a, b)` | 3rd formula — same contract |
| `FORMULAS` | Dictionary mapping `1, 2, 3` to a label and the matching function |
| `show_all(a, b)` | Iterates over `FORMULAS` and prints each result |
| `main()` | Collects input from arguments or prompts, handles input errors |

The three formula functions contain no printing and no input handling, so they
can be imported and tested independently:

```python
from binomische_formeln import first
steps, value = first(3, 5)   # value == 64
```

## Error handling

| Situation | Behaviour |
|-----------|-----------|
| Non-numeric input at the prompt | Prints `Please enter numbers only.` and exits |
| Ctrl+C or end of input | Exits quietly on a clean new line |
| Wrong number of arguments | Falls back to the interactive prompt |

## Possible extensions

- Symbolic expansion with variables, e.g. `(3x + 2)² → 9x² + 12x + 4`, which
  would require `sympy`.
- Factoring in the other direction: recognising `a² - b²` and returning
  `(a + b)(a - b)`.
- Unicode superscripts (`a²`) in the output instead of `a^2`.
