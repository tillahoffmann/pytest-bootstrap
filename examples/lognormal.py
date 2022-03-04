from matplotlib import pyplot as plt
import numpy as np
import pytest
from pytest_bootstrap import bootstrap_test, BootstrapTestError, result_hist


def lognormal_expectation(mu, sigma):
    """
    Evaluate the expectation of a log normal random variable.
    """
    return np.exp(mu + sigma ** 2 / 2)


def lognormal_expectation_wrong(mu, sigma):
    """
    Evaluate the expectation of a log normal random variable but with a bug.
    """
    return np.exp(mu + sigma ** 2)


# Define parameters.
mu = -1
sigma = 1
# Draw a random sample to compare with.
x = np.exp(np.random.normal(mu, sigma, 1000))
# Check the correct implementation.
reference = lognormal_expectation(mu, sigma)
result = bootstrap_test(x, np.mean, reference)
# Verify the wrong one raises an error.
with pytest.raises(BootstrapTestError):
    reference_wrong = lognormal_expectation_wrong(mu, sigma)
    bootstrap_test(x, np.mean, reference_wrong)
# Show a visualisation of the bootstrap test.
fig, ax = plt.subplots()
result_hist(result)
ax.axvline(reference_wrong, color='C3', label='incorrect reference')
ax.set_xlabel('Bootstrapped mean')
ax.set_ylabel('Density')
ax.legend(fontsize='small')
fig.tight_layout()
