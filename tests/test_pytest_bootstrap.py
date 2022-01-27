import numpy as np
import pytest
import pytest_bootstrap
from scipy import stats


def test_mean_success():
    x = np.random.normal(0, 1, 100)
    pytest_bootstrap.bootstrap_test(x, np.mean, 0)


def test_mean_fail():
    x = np.random.normal(0, 1, 100)
    with pytest.raises(pytest_bootstrap.BootstrapTestError):
        pytest_bootstrap.bootstrap_test(x, np.mean, 1)


def test_success_due_to_small_sample():
    x = np.random.normal(0, 1, 10)
    # This test passes despite the reference value being wrong because the sample is small.
    pytest_bootstrap.bootstrap_test(x, np.mean, .1)


def test_calibration():
    num_runs = 200
    num_failures = 0
    xs = np.random.normal(0, 1, (num_runs, 100))
    alpha = .3
    for x in xs:
        try:
            pytest_bootstrap.bootstrap_test(x, np.mean, 0, alpha=alpha)
        except pytest_bootstrap.BootstrapTestError:
            num_failures += 1
    # Use Fisher's exact test to check the number of failures is as expected.
    pvalue = stats.binom_test(num_failures, num_runs, alpha)
    assert pvalue > 0.01, 'poor calibration'


def test_small_sample_warning():
    with pytest.warns(UserWarning):
        pytest_bootstrap.bootstrap_test(np.random.normal(0, 1, 10), np.mean, 0, alpha=1e-9)


def test_variance_success():
    x = np.random.normal(0, 1, 1000)
    pytest_bootstrap.bootstrap_test(x, np.var, 1)


def test_variance_fail():
    x = np.random.normal(0, 1, 1000)
    with pytest.raises(pytest_bootstrap.BootstrapTestError):
        pytest_bootstrap.bootstrap_test(x, np.var, 1.5)
