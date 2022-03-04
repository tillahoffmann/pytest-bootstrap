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


@pytest.mark.parametrize('vector_statistic, multiple_hypothesis_correction', [
    # Standard scalar test.
    (False, False),
    # Vector test with Bonferroni correction.
    (True, 'bonferroni'),
    # Vector test without multiple hypothesis correction; this test is miscalibrated.
    (True, False),
], ids=['scalar', 'vector-without-correction', 'vector-bonferroni'])
def test_calibration(vector_statistic: bool, multiple_hypothesis_correction: str):
    alpha = .3  # Significance level. We expect `alpha` tests to fail.
    num_runs = 200  # Number of independent tests to run.
    num_failures = 0

    if vector_statistic:
        sample_shape = (num_runs, 100, 5)
    else:
        sample_shape = (num_runs, 100)
    xs = np.random.normal(0, 1, sample_shape)
    for x in xs:
        try:
            pytest_bootstrap.bootstrap_test(
                x, lambda x: np.mean(x, axis=0), 0, alpha=alpha,
                multiple_hypothesis_correction=multiple_hypothesis_correction,
            )
        except pytest_bootstrap.BootstrapTestError:
            num_failures += 1

    # Use Fisher's exact test to check the number of failures is as expected.
    pvalue = stats.binom_test(num_failures, num_runs, alpha)
    if vector_statistic and not multiple_hypothesis_correction:
        assert pvalue < 0.01, 'expected miscalibrated test without multiple hypothesis ' \
            f'correction; p-value {pvalue}'
    else:
        assert pvalue > 0.01, f'expected {num_runs * alpha} failures but got {num_failures}; '\
            'p-value = {pvalue}'


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


def test_invalid_dimensions():
    with pytest.raises(ValueError):
        x = np.random.normal(0, 1, (100, 3, 4))
        pytest_bootstrap.bootstrap_test(x, lambda x: np.mean(x, axis=0), 0)


def test_unsupported_multiple_hypothesis_correction():
    with pytest.raises(NotImplementedError):
        x = np.random.normal(0, 1, (100, 3))
        pytest_bootstrap.bootstrap_test(x, lambda x: np.mean(x, axis=0), 0,
                                        multiple_hypothesis_correction='some-method')


def test_tolerance():
    x = 2.9 * np.ones(10)
    with pytest.raises(pytest_bootstrap.BootstrapTestError):
        pytest_bootstrap.bootstrap_test(x, np.mean, 3)

    # Absolute tolerance.
    with pytest.raises(pytest_bootstrap.BootstrapTestError):
        pytest_bootstrap.bootstrap_test(x, np.mean, 2, atol=0.099)
    pytest_bootstrap.bootstrap_test(x, np.mean, 3, atol=0.11)

    # Relative tolerance.
    with pytest.raises(pytest_bootstrap.BootstrapTestError):
        pytest_bootstrap.bootstrap_test(x, np.mean, 3, rtol=0.033)
    pytest_bootstrap.bootstrap_test(x, np.mean, 3, rtol=0.034)


def test_on_fail_warn():
    x = 2.9 * np.ones(10)
    with pytest.warns(UserWarning, match='the reference value'):
        result = pytest_bootstrap.bootstrap_test(x, np.mean, 3, on_fail='warn')
    assert result['upper'] < 3


def test_on_fail_invalid():
    x = 2.9 * np.ones(10)
    with pytest.raises(ValueError):
        pytest_bootstrap.bootstrap_test(x, np.mean, 3, on_fail='invalid')
