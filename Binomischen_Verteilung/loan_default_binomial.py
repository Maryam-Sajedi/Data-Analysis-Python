"""
If we have 200 bank loans, each with an 8% independent chance of default,
what's the probability that exactly 20 of them default?
"""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Parameters
n_loans = 200       # number of loans (trials)
p_default = 0.08    # probability each loan defaults

# 1. What's the expected number of defaults?
expected_defaults = n_loans * p_default
print(f"Expected number of defaults: {expected_defaults}")

# 2. What's the probability of EXACTLY 20 defaults?
prob_exactly_20 = stats.binom.pmf(20, n_loans, p_default)  # probability of exactly k successes
print(f"P(exactly 20 defaults): {prob_exactly_20:.4f}")

# 3. What's the probability of MORE THAN 25 defaults? (risk question)
prob_more_than_25 = 1 - stats.binom.cdf(25, n_loans, p_default)  # cdf = cumulative probability of k or fewer successes
print(f"P(more than 25 defaults): {prob_more_than_25:.4f}")

# 4. What's a "reasonable range" of defaults? (90% confidence interval)
lower = stats.binom.ppf(0.05, n_loans, p_default)
upper = stats.binom.ppf(0.95, n_loans, p_default)
print(f"90% of the time, defaults will fall between {lower} and {upper}")

# Plot the full Binomial distribution:
x = np.arange(0, 40)
probabilities = stats.binom.pmf(x, n_loans, p_default)

plt.figure(figsize=(10, 5))
plt.bar(x, probabilities, color='steelblue')
plt.axvline(expected_defaults, color='red', linestyle='--', label=f'Expected ({expected_defaults:.0f})')
plt.xlabel('Number of Defaults')
plt.ylabel('Probability')
plt.title('Binomial Distribution: Loan Defaults out of 200 Loans (p=8%)')
plt.legend()
plt.show()

# Is 35 defaults surprising, given our assumption of p=8%?
observed_defaults = 35
prob_35_or_more = 1 - stats.binom.cdf(observed_defaults - 1, n_loans, p_default)
print(f"P(35 or more defaults | true rate is 8%): {prob_35_or_more:.5f}")

if prob_35_or_more < 0.05:
    print("This is unlikely under our 8% assumption — the true default rate may be higher.")
else:
    print("This is within normal variation — no strong evidence the 8% assumption is wrong.")
