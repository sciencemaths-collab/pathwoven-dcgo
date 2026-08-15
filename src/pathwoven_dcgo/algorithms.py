"""Reference algorithms for PathWoven-DCGO experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

Array = np.ndarray
Objective = Callable[[Array], float]


@dataclass
class OptimizationResult:
    """Returned by every optimizer."""

    best_x: Array
    best_value: float
    convergence: list[float]
    metadata: dict[str, float | int | str]


def _clip(x: Array, lower: Array, upper: Array) -> Array:
    return np.minimum(np.maximum(x, lower), upper)


def _rng(seed: int | None) -> np.random.Generator:
    return np.random.default_rng(seed)


class SimulatedAnnealing:
    """Small, robust simulated annealing baseline."""

    def __init__(self, *, initial_temperature: float = 1.0, cooling: float = 0.985, step_scale: float = 0.15):
        self.initial_temperature = initial_temperature
        self.cooling = cooling
        self.step_scale = step_scale

    def minimize(self, objective: Objective, lower: Array, upper: Array, *, iterations: int, seed: int | None = None) -> OptimizationResult:
        rng = _rng(seed)
        span = upper - lower
        x = rng.uniform(lower, upper)
        fx = objective(x)
        best_x = x.copy()
        best_value = fx
        convergence: list[float] = []
        temperature = self.initial_temperature

        for _ in range(iterations):
            proposal = _clip(x + rng.normal(0.0, self.step_scale, size=x.size) * span, lower, upper)
            fp = objective(proposal)
            delta = fp - fx
            if delta <= 0 or rng.random() < np.exp(-delta / max(temperature, 1e-12)):
                x, fx = proposal, fp
            if fx < best_value:
                best_x, best_value = x.copy(), fx
            convergence.append(float(best_value))
            temperature *= self.cooling

        return OptimizationResult(best_x, float(best_value), convergence, {"algorithm": "simulated_annealing"})


class ParticleSwarmOptimizer:
    """Particle swarm optimization baseline."""

    def __init__(self, *, particles: int = 36, inertia: float = 0.72, cognitive: float = 1.49, social: float = 1.49):
        self.particles = particles
        self.inertia = inertia
        self.cognitive = cognitive
        self.social = social

    def minimize(self, objective: Objective, lower: Array, upper: Array, *, iterations: int, seed: int | None = None) -> OptimizationResult:
        rng = _rng(seed)
        dim = lower.size
        span = upper - lower
        x = rng.uniform(lower, upper, size=(self.particles, dim))
        v = rng.normal(0.0, 0.05, size=(self.particles, dim)) * span
        pbest = x.copy()
        pbest_values = np.array([objective(row) for row in pbest])
        g_idx = int(np.argmin(pbest_values))
        gbest = pbest[g_idx].copy()
        gbest_value = float(pbest_values[g_idx])
        convergence: list[float] = []

        for _ in range(iterations):
            r1 = rng.random(size=(self.particles, dim))
            r2 = rng.random(size=(self.particles, dim))
            v = self.inertia * v + self.cognitive * r1 * (pbest - x) + self.social * r2 * (gbest - x)
            x = _clip(x + v, lower, upper)
            values = np.array([objective(row) for row in x])
            improved = values < pbest_values
            pbest[improved] = x[improved]
            pbest_values[improved] = values[improved]
            g_idx = int(np.argmin(pbest_values))
            if pbest_values[g_idx] < gbest_value:
                gbest = pbest[g_idx].copy()
                gbest_value = float(pbest_values[g_idx])
            convergence.append(gbest_value)

        return OptimizationResult(gbest, float(gbest_value), convergence, {"algorithm": "pso", "particles": self.particles})


class PathWovenDCGO:
    """Geometry-guided DCGO variant with PSO-in-sector search and SA sector refinement."""

    def __init__(
        self,
        *,
        sectors: int = 12,
        particles_per_sector: int = 8,
        inertia: float = 0.68,
        cognitive: float = 1.35,
        social: float = 1.65,
        global_social: float = 0.35,
        initial_temperature: float = 1.0,
        cooling: float = 0.985,
        boundary_jitter: float = 0.03,
    ):
        if sectors < 2:
            raise ValueError("sectors must be >= 2")
        if particles_per_sector < 2:
            raise ValueError("particles_per_sector must be >= 2")
        self.sectors = sectors
        self.particles_per_sector = particles_per_sector
        self.inertia = inertia
        self.cognitive = cognitive
        self.social = social
        self.global_social = global_social
        self.initial_temperature = initial_temperature
        self.cooling = cooling
        self.boundary_jitter = boundary_jitter

    def minimize(self, objective: Objective, lower: Array, upper: Array, *, iterations: int, seed: int | None = None) -> OptimizationResult:
        rng = _rng(seed)
        dim = lower.size
        count = self.sectors * self.particles_per_sector
        span = upper - lower
        x = rng.uniform(lower, upper, size=(count, dim))
        v = rng.normal(0.0, 0.04, size=(count, dim)) * span
        sector_ids = np.repeat(np.arange(self.sectors), self.particles_per_sector)

        pbest = x.copy()
        pbest_values = np.array([objective(row) for row in pbest])
        sector_best = pbest.copy()
        sector_best_values = np.full(self.sectors, np.inf)
        global_idx = int(np.argmin(pbest_values))
        global_best = pbest[global_idx].copy()
        global_best_value = float(pbest_values[global_idx])
        convergence: list[float] = []
        temperature = self.initial_temperature

        for _ in range(iterations):
            for k in range(self.sectors):
                members = np.where(sector_ids == k)[0]
                if members.size == 0:
                    continue
                local_idx = members[int(np.argmin(pbest_values[members]))]
                candidate_value = float(pbest_values[local_idx])
                if candidate_value < sector_best_values[k]:
                    sector_best[k] = pbest[local_idx].copy()
                    sector_best_values[k] = candidate_value

            r1 = rng.random(size=(count, dim))
            r2 = rng.random(size=(count, dim))
            r3 = rng.random(size=(count, dim))
            local_targets = sector_best[sector_ids]
            v = (
                self.inertia * v
                + self.cognitive * r1 * (pbest - x)
                + self.social * r2 * (local_targets - x)
                + self.global_social * r3 * (global_best - x)
            )

            jitter = rng.normal(0.0, self.boundary_jitter * temperature, size=(count, dim)) * span
            x_next = _clip(x + v + jitter, lower, upper)
            values = np.array([objective(row) for row in x_next])
            current_values = np.array([objective(row) for row in x])
            delta = values - current_values
            accept = (delta <= 0) | (rng.random(count) < np.exp(-delta / max(temperature, 1e-12)))
            x[accept] = x_next[accept]

            accepted_values = np.array([objective(row) for row in x])
            improved = accepted_values < pbest_values
            pbest[improved] = x[improved]
            pbest_values[improved] = accepted_values[improved]

            global_idx = int(np.argmin(pbest_values))
            if pbest_values[global_idx] < global_best_value:
                global_best = pbest[global_idx].copy()
                global_best_value = float(pbest_values[global_idx])

            if dim >= 2:
                z = 2 * (x - lower) / np.where(span == 0, 1, span) - 1
                theta = np.arctan2(z[:, 1], z[:, 0])
                theta = (theta + 2 * np.pi) % (2 * np.pi)
                sector_ids = np.minimum((theta / (2 * np.pi) * self.sectors).astype(int), self.sectors - 1)

            convergence.append(global_best_value)
            temperature *= self.cooling

        return OptimizationResult(
            global_best,
            float(global_best_value),
            convergence,
            {
                "algorithm": "pathwoven_dcgo",
                "sectors": self.sectors,
                "particles_per_sector": self.particles_per_sector,
            },
        )
