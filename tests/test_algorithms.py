import numpy as np

from pathwoven_dcgo.algorithms import ParticleSwarmOptimizer, SimulatedAnnealing, PathWovenDCGO
from pathwoven_dcgo.benchmarks import get_benchmark


def run_optimizer(optimizer):
    bench = get_benchmark("sphere")
    lower, upper = bench.bounds(3)
    result = optimizer.minimize(bench.objective, lower, upper, iterations=25, seed=42)
    assert np.isfinite(result.best_value)
    assert len(result.convergence) == 25
    assert result.best_x.shape == (3,)
    assert np.all(result.best_x >= lower)
    assert np.all(result.best_x <= upper)


def test_simulated_annealing_runs():
    run_optimizer(SimulatedAnnealing())


def test_pso_runs():
    run_optimizer(ParticleSwarmOptimizer(particles=10))


def test_pathwoven_dcgo_runs():
    run_optimizer(PathWovenDCGO(sectors=4, particles_per_sector=4))
