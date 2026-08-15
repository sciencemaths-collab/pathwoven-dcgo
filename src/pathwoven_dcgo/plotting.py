"""Plotting utilities for convergence traces."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .experiment import ExperimentResult


def plot_convergence(results: list[ExperimentResult], *, iterations: int, output_path: str | Path) -> Path:
    """Plot mean convergence with robust length handling."""

    x = np.arange(1, iterations + 1)
    fig, ax = plt.subplots(figsize=(8, 5))
    curves: list[tuple[str, np.ndarray]] = []
    global_min = np.inf
    for result in results:
        matrix = np.asarray(result.convergence, dtype=float)
        if matrix.ndim != 2 or matrix.shape[1] != iterations:
            raise ValueError(f"Convergence for {result.algorithm} must be runs x {iterations}; got {matrix.shape}")
        y = np.nanmean(matrix, axis=0)
        curves.append((result.algorithm, y))
        finite = y[np.isfinite(y)]
        if finite.size:
            global_min = min(global_min, float(np.min(finite)))

    shift = 0.0 if global_min > 0 else abs(global_min) + 1e-12
    for name, y in curves:
        ax.plot(x, y + shift, label=name)
    ax.set_yscale("log")
    ax.set_xlabel("Iteration")
    ylabel = "Best objective value" if shift == 0.0 else "Best objective value + positive shift"
    ax.set_ylabel(ylabel)
    ax.set_title("Optimization convergence")
    ax.legend()
    ax.grid(True, which="both", linewidth=0.3)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path
