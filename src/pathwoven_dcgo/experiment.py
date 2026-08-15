"""Benchmark orchestration for PathWoven-DCGO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .algorithms import OptimizationResult, ParticleSwarmOptimizer, SimulatedAnnealing, PathWovenDCGO
from .benchmarks import Benchmark


@dataclass
class ExperimentResult:
    algorithm: str
    values: list[float]
    convergence: list[list[float]]

    @property
    def mean(self) -> float:
        return float(np.mean(self.values))

    @property
    def std(self) -> float:
        return float(np.std(self.values, ddof=1)) if len(self.values) > 1 else 0.0


def run_benchmark(
    benchmark: Benchmark,
    *,
    dimensions: int,
    runs: int,
    iterations: int,
    seed: int = 1234,
) -> list[ExperimentResult]:
    """Run a repeated benchmark across baseline and PathWoven methods."""

    lower, upper = benchmark.bounds(dimensions)
    optimizers: dict[str, Callable[[int], OptimizationResult]] = {
        "Simulated Annealing": lambda s: SimulatedAnnealing().minimize(
            benchmark.objective, lower, upper, iterations=iterations, seed=s
        ),
        "Particle Swarm Optimization": lambda s: ParticleSwarmOptimizer().minimize(
            benchmark.objective, lower, upper, iterations=iterations, seed=s
        ),
        "PathWoven Inside DCGO": lambda s: PathWovenDCGO().minimize(
            benchmark.objective, lower, upper, iterations=iterations, seed=s
        ),
    }
    rng = np.random.default_rng(seed)
    results: list[ExperimentResult] = []

    for name, runner in optimizers.items():
        values: list[float] = []
        convergence: list[list[float]] = []
        for _ in range(runs):
            result = runner(int(rng.integers(0, 2**31 - 1)))
            values.append(result.best_value)
            convergence.append(_ensure_length(result.convergence, iterations))
        results.append(ExperimentResult(name, values, convergence))

    return results


def _ensure_length(series: list[float], expected: int) -> list[float]:
    """Pad convergence logs so plotting never sees x/y length mismatch."""

    if len(series) == expected:
        return list(series)
    if not series:
        return [float("nan")] * expected
    if len(series) < expected:
        return list(series) + [series[-1]] * (expected - len(series))
    return list(series[:expected])
