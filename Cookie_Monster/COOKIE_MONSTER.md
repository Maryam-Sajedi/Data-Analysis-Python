# Cookie Monster Weight Predictor

Cookie Monster's birthday is in 2 weeks, and the local municipality wants to send a postcard with its exact weight on it. This Python script predicts that weight.

The fixed rules of the original puzzle no longer hold exactly. So instead of calculating a single "correct" answer, the script runs a **Monte Carlo simulation**. It plays out the next 14 days 100,000 times with random variation and reports the most likely weight together with a range.

## The problem

- Cookie Monster eats about **10 kg of cookies a day**. The original rule was that every 10 kg eaten makes it **5 kg heavier**.
- **Grandma Cookie Monster** brings **15 kg of cookies** when she visits. She only visits when she's in a good mood, and **no more than twice a week**.
- Grandma is in a good mood when her likes outweigh her dislikes on that day:

  | Likes 👍 | Dislikes 👎 |
  |---------|------------|
  | 🌞 Sunny and not too warm (< 28 ℃) | 👀 Her neighbour looking out of the window when she leaves |
  | 🚃 Taking tram 1 | 🚃 Taking tram 3 |

- On average she is in a good mood **3 days a week**.

### Observed data

| Day | Cookies eaten (kg) | Neighbour looking | Temp. (℃) | Tram 1 working | Lake temp. (℃) | Evgeny teaching ML | Weight start (kg) | Weight end (kg) |
|-----|------|-----|----|---|------|---|-------|-------|
| 1   | 15   | Yes | 25 | 1 | 15   | 1 | 100.0 | 114.3 |
| 2   | 10   | No  | 23 | 0 | 15.5 | 0 | 114.3 | 120.7 |
| 3   | 40   | Yes | 29 | 1 | 15.3 | 1 | 120.7 | 135.4 |

In the code, this table is stored as a dictionary called `OBSERVATIONS`. Each column name is a key, and its value is the list of numbers for days 1–3:

```python
OBSERVATIONS = {
    "cookies_eaten": [15, 10, 40],
    "weight_end": [114.3, 120.7, 135.4],
    ...
}
```

## How the model works

1. **Weight gain.** The model is `gain = beta × cookies eaten + noise`. The old rule (`beta = 0.5`) is the starting assumption, and the three observed days adjust it using Bayesian linear regression. The result is about **0.46 ± 0.10 kg gained per kg of cookies**, with around 5 kg of random variation per day.
2. **Grandma's mood.** Following her likes and dislikes, she can only be in a good mood when tram 1 is running. She is then in a good mood unless the neighbour is looking *and* the weather isn't sunny and mild:

   ```
   P(good mood) = P(tram 1) × (1 − (1 − P(sunny & mild)) × P(neighbour looking))
   ```

   The chances of tram 1 running and the neighbour looking are estimated from the observed days. The chance of sunny, mild weather isn't in the data, so it is set so that she is in a good mood about 3 days a week on average.
3. **Visits.** Grandma visits on good-mood days, at most twice a week.
4. **Cookies eaten.** 10 kg a day, plus 15 kg on days Grandma visits, plus some random variation.

### Assumptions

- If tram 1 isn't running, Grandma takes tram 3.
- The weather (sunny or not) isn't in the data, so it is worked out from the "3 good-mood days a week" average.
- Lake temperature and whether Evgeny is teaching are stored in the data, but the model doesn't use them. With only three days of data, their effect can't be told apart from noise.

## Requirements

- Python 3.8 or newer
- [NumPy](https://numpy.org/)

```bash
python3 -m pip install numpy
```

## Usage

```bash
python3 cookie_monster.py
```

Example output:

```
Start weight (end of day 3): 135.4 kg
Fitted gain rate: 0.463 ± 0.100 kg per kg of cookies (daily noise ~5.0 kg)
Grandma visits in 14 days: 3.6 on average

Predicted weight after 14 days:
  mean   225.3 kg
  median 224.8 kg
  90% interval 168.5 – 283.9 kg

For the postcard: ~225 kg (an 'exact' number isn't possible under uncertainty)
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--days` | `14` | Number of days until the birthday |
| `--sims` | `100000` | Number of simulated runs (more runs give more stable results but take longer) |
| `--cookie-noise` | `5.0` | How much the daily cookie intake varies (standard deviation, in kg) |
| `--seed` | `42` | Random seed, so results can be repeated exactly |

Example:

```bash
python3 cookie_monster.py --days 14 --sims 200000 --cookie-noise 3
```

## Result

The prediction for the postcard is **about 225 kg**, with a 90% chance that the true weight is between **168 and 284 kg**. The range is wide because there are only three days of data to learn from.
