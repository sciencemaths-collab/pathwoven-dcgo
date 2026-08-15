"""Statistical helpers that avoid empty-array traps."""

from __future__ import annotations

from itertools import combinations
from typing import Iterable

import numpy as np


def validate_samples(samples: dict[str, Iterable[float]]) -> dict[str, np.ndarray]:
    cleaned: dict[str, np.ndarray] = {}
    for name, values in samples.items():
        arr = np.asarray(list(values), dtype=float)
        arr = arr[np.isfinite(arr)]
        if arr.size < 2:
            raise ValueError(f"'{name}' needs at least two finite values for statistical comparison")
        cleaned[name] = arr
    return cleaned


def summarize(samples: dict[str, Iterable[float]]) -> dict[str, dict[str, float]]:
    cleaned = validate_samples(samples)
    return {
        name: {
            "n": float(arr.size),
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr, ddof=1)),
            "min": float(np.min(arr)),
            "median": float(np.median(arr)),
        }
        for name, arr in cleaned.items()
    }


def pairwise_effects(samples: dict[str, Iterable[float]]) -> dict[tuple[str, str], float]:
    """Return simple mean differences a-b. Use scipy externally for exact p-values if desired."""

    cleaned = validate_samples(samples)
    return {(a, b): float(np.mean(cleaned[a]) - np.mean(cleaned[b])) for a, b in combinations(cleaned, 2)}
