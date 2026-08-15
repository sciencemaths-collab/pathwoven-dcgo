import numpy as np

from pathwoven_dcgo.benchmarks import get_benchmark, sphere, rastrigin, ackley, michalewicz


def test_sphere_minimum():
    assert sphere(np.zeros(3)) == 0.0


def test_rastrigin_minimum():
    assert abs(rastrigin(np.zeros(4))) < 1e-12


def test_ackley_minimum():
    assert abs(ackley(np.zeros(3))) < 1e-10


def test_michalewicz_returns_finite_value():
    value = michalewicz(np.array([2.2, 1.57]))
    assert np.isfinite(value)


def test_get_benchmark_bounds():
    bench = get_benchmark("michalewicz")
    lower, upper = bench.bounds(5)
    assert lower.shape == (5,)
    assert upper.shape == (5,)
    assert np.all(upper > lower)
