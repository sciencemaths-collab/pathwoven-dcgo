import pytest

from pathwoven_dcgo.benchmarks import get_benchmark
from pathwoven_dcgo.experiment import _ensure_length, run_benchmark
from pathwoven_dcgo.stats import summarize


def test_ensure_length_pads_short_series():
    assert _ensure_length([3.0], 4) == [3.0, 3.0, 3.0, 3.0]


def test_ensure_length_handles_empty_series():
    padded = _ensure_length([], 3)
    assert len(padded) == 3


def test_run_benchmark_shapes():
    results = run_benchmark(get_benchmark("sphere"), dimensions=2, runs=2, iterations=5, seed=7)
    assert len(results) == 3
    for result in results:
        assert len(result.values) == 2
        assert len(result.convergence) == 2
        assert len(result.convergence[0]) == 5


def test_stats_rejects_empty_samples():
    with pytest.raises(ValueError):
        summarize({"bad": []})
