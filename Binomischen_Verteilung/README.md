# Loan Default Risk — Binomial Distribution Exercise

A small Python exercise that uses the **binomial distribution** to model default risk across a portfolio of bank loans. This simulates a typical question a risk/quant analyst or consultant might be asked: *"Given our assumed default rate, is what we're observing normal — or a red flag?"*

## The question

> If we have 200 bank loans, each with an 8% independent chance of default, what's the probability that exactly 20 of them default?

This is a classic **binomial** setup:
- a **fixed number of trials** (200 loans)
- each trial has the **same probability** of "success" (default = 8%)
- trials are **independent** of each other (one loan defaulting doesn't affect another)

## Requirements

```bash
pip install numpy scipy matplotlib
```

Tested in [Thonny](https://thonny.org/), but runs in any standard Python 3 environment.

## What the script does

### 1. Expected number of defaults

```python
expected_defaults = n_loans * p_default
```

For a binomial distribution, the expected value (mean) is simply `n × p`. With 200 loans at an 8% default rate, we expect **16 defaults** on average.

### 2. Probability of exactly 20 defaults — `pmf`

```python
prob_exactly_20 = stats.binom.pmf(20, n_loans, p_default)
```

`pmf` = **Probability Mass Function**. It returns the probability of *exactly* `k` successes out of `n` trials. Here it answers: "What's the chance *exactly* 20 out of 200 loans default?"

### 3. Probability of more than 25 defaults — `cdf`

```python
prob_more_than_25 = 1 - stats.binom.cdf(25, n_loans, p_default)
```

`cdf` = **Cumulative Distribution Function**. It returns the probability of `k` *or fewer* successes. So `cdf(25, ...)` gives P(25 or fewer defaults), and `1 - cdf(25, ...)` gives everything above that: P(more than 25 defaults). This is the kind of tail-risk question a bank would actually ask: "How likely is it that things go worse than expected?"

### 4. A "reasonable range" of outcomes — `ppf`

```python
lower = stats.binom.ppf(0.05, n_loans, p_default)
upper = stats.binom.ppf(0.95, n_loans, p_default)
```

`ppf` = **Percent Point Function** (the inverse of `cdf`). Instead of "given a number of defaults, what's the probability," it answers "given a probability, what's the number of defaults." Here it finds the 5th and 95th percentiles, giving a **90% confidence range** — the band of outcomes considered "normal" under the 8% assumption.

### 5. Visualizing the distribution

```python
x = np.arange(0, 40)
probabilities = stats.binom.pmf(x, n_loans, p_default)
plt.bar(x, probabilities, ...)
```

Plots the full probability distribution of possible default counts (0 to 39), with a red dashed line marking the expected value (16). This shows the classic bell-like shape of a binomial distribution when `n` is large.

### 6. Testing whether an observed result is surprising

```python
observed_defaults = 35
prob_35_or_more = 1 - stats.binom.cdf(observed_defaults - 1, n_loans, p_default)
```

This is the most "consultant-style" part of the script: given the model's assumption (8% default rate), how likely is it that we'd observe **35 or more** defaults just by chance?

- We subtract 1 (`observed_defaults - 1`) before calling `cdf` so that 35 itself is *included* in "35 or more."
- If this probability is very low (the script uses a **5% threshold**, a standard statistical convention), it suggests the 8% assumption may no longer hold — the true default rate might be higher than modeled, and the risk model may need recalibration.

## Example output

```
Expected number of defaults: 16.0
P(exactly 20 defaults): 0.0532
P(more than 25 defaults): 0.0161
90% of the time, defaults will fall between 9.0 and 23.0
P(35 or more defaults | true rate is 8%): 0.00016
This is unlikely under our 8% assumption — the true default rate may be higher.
```

*(Exact numbers may vary slightly depending on the scipy version.)*

## Key takeaway

This script demonstrates a real risk-analysis workflow: define an assumption (default rate), understand its expected behavior, define what "normal" variation looks like, and then test whether real-world observations still fit that assumption — or whether the model needs to be revisited.

## Function quick reference

| Function | Question it answers | Input → Output |
|---|---|---|
| `binom.pmf(k, n, p)` | What's the probability of *exactly* k defaults? | number → probability |
| `binom.cdf(k, n, p)` | What's the probability of k *or fewer* defaults? | number → probability |
| `binom.ppf(q, n, p)` | What number of defaults corresponds to probability q? | probability → number |
