"""PathWoven-DCGO optimization package."""

from .algorithms import OptimizationResult, ParticleSwarmOptimizer, SimulatedAnnealing, PathWovenDCGO
from .benchmarks import get_benchmark
from .experiment import ExperimentResult, run_benchmark

__version__ = "0.1.0"

__all__ = [
    "OptimizationResult",
    "ParticleSwarmOptimizer",
    "SimulatedAnnealing",
    "PathWovenDCGO",
    "ExperimentResult",
    "get_benchmark",
    "run_benchmark",
    "__version__",
]
