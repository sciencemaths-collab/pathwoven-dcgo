from __future__ import annotations

import argparse
from pathlib import Path

from pathwoven_dcgo.benchmarks import get_benchmark
from pathwoven_dcgo.experiment import run_benchmark
from pathwoven_dcgo.plotting import plot_convergence
from pathwoven_dcgo.stats import summarize


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PathWoven-DCGO benchmarks.")
    parser.add_argument("--function", default="michalewicz", choices=["sphere", "rastrigin", "rosenbrock", "ackley", "michalewicz"])
    parser.add_argument("--dimensions", type=int, default=5)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--plot", default="benchmark_convergence.png")
    args = parser.parse_args()

    benchmark = get_benchmark(args.function)
    results = run_benchmark(
        benchmark,
        dimensions=args.dimensions,
        runs=args.runs,
        iterations=args.iterations,
        seed=args.seed,
    )

    samples = {result.algorithm: result.values for result in results}
    summary = summarize(samples)
    for name, stats in summary.items():
        print(f"{name}: n={int(stats['n'])} mean={stats['mean']:.6g} std={stats['std']:.6g} min={stats['min']:.6g}")

    path = plot_convergence(results, iterations=args.iterations, output_path=Path(args.plot))
    print(f"Saved convergence plot to {path}")


if __name__ == "__main__":
    main()
