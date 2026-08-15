"""Benchmark objective functions."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Callable

import numpy as np

Array = np.ndarray
Objective = Callable[[Array], float]


@dataclass(frozen=True)
class Benchmark:
    name: str
    objective: Objective
    lower: float
    upper: float
    known_minimum: float | None = None
    description: str = ""

    def bounds(self, dimensions: int) -> tuple[Array, Array]:
        return np.full(dimensions, self.lower, dtype=float), np.full(dimensions, self.upper, dtype=float)


def sphere(x: Array) -> float:
    return float(np.sum(np.asarray(x, dtype=float) ** 2))


def rastrigin(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    return float(10 * x.size + np.sum(x**2 - 10 * np.cos(2 * np.pi * x)))


def rosenbrock(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    return float(np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2))


def ackley(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    d = x.size
    sum_sq = np.sum(x**2)
    sum_cos = np.sum(np.cos(2 * np.pi * x))
    return float(-20 * np.exp(-0.2 * np.sqrt(sum_sq / d)) - np.exp(sum_cos / d) + 20 + np.e)


def michalewicz(x: Array, m: int = 10) -> float:
    """Michalewicz minimization function on the conventional [0, pi]^d domain."""

    x = np.asarray(x, dtype=float)
    i = np.arange(1, x.size + 1, dtype=float)
    return float(-np.sum(np.sin(x) * np.sin(i * x**2 / pi) ** (2 * m)))


_BENCHMARKS: dict[str, Benchmark] = {
    "sphere": Benchmark("sphere", sphere, -5.12, 5.12, 0.0, "Convex sanity-check objective."),
    "rastrigin": Benchmark("rastrigin", rastrigin, -5.12, 5.12, 0.0, "Highly multimodal separable objective."),
    "rosenbrock": Benchmark("rosenbrock", rosenbrock, -2.048, 2.048, 0.0, "Curved valley objective."),
    "ackley": Benchmark("ackley", ackley, -32.768, 32.768, 0.0, "Rugged objective with broad outer basin."),
    "michalewicz": Benchmark("michalewicz", michalewicz, 0.0, pi, None, "Deceptive multimodal objective."),
}


def get_benchmark(name: str) -> Benchmark:
    key = name.lower().strip()
    try:
        return _BENCHMARKS[key]
    except KeyError as exc:
        options = ", ".join(sorted(_BENCHMARKS))
        raise ValueError(f"Unknown benchmark '{name}'. Available: {options}") from exc
