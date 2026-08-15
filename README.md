# PathWoven-DCGO

**PathWoven-DCGO** is a geometry-guided hybrid optimization framework for hard nonconvex search. It combines pizza-slice geometric decomposition, Particle Swarm Optimization inside local sectors, and Simulated Annealing-style global refinement.

The repository is designed as a research reference for rugged benchmark functions such as Michalewicz, Rastrigin, Rosenbrock, Ackley, and Sphere.

> Status: reference implementation with tests and a benchmark harness. Do not claim universal superiority without repeated runs across dimensions, seeds, budgets, and statistical tests.

## Architecture

![PathWoven-DCGO architecture](docs/assets/pathwoven_architecture.svg)

## Benchmark snapshot

The packaged smoke benchmark below compares Simulated Annealing, Particle Swarm Optimization, and PathWoven Inside DCGO on Michalewicz. The plotted score is `-best objective`, so higher is better.

![PathWoven-DCGO benchmark snapshot](docs/assets/smoke_benchmark.svg)

Smoke result from the installed package:

| Method | Runs | Mean best objective | Score shown above |
|---|---:|---:|---:|
| Simulated Annealing | 3 | -1.60627 | 1.606 |
| Particle Swarm Optimization | 3 | -3.89602 | 3.896 |
| PathWoven Inside DCGO | 3 | -4.04754 | 4.048 |

For serious claims, run the full benchmark matrix with more seeds, dimensions, and iteration budgets.

## Core idea

```text
problem landscape -> circular domain mapping -> pizza-slice sectors -> rectangular PathWoven windows
                 -> PSO flock search inside each sector -> SA global refinement -> best solution x*
```

The pizza intuition is the same geometry behind the circle-area identity:

```text
circle -> thin slices -> rectangular strip
area ≈ (πr) · r = πr²
```

In optimization, this becomes:

```text
curved / rugged domain -> sector windows -> coordinated local search
```

## GitHub-safe formulas

The README avoids unsupported Markdown math macros, so it renders cleanly on GitHub.

```text
Normalize candidate:
z = 2 * (x - lower) / (upper - lower) - 1

Radial-angle membership:
r = norm(z, 2)
theta = atan2(z2, z1)

PSO update inside sector k:
v_i(t+1) = w*v_i(t) + c1*r1*(p_i - x_i) + c2*r2*(g_k - x_i) + c3*r3*(g - x_i)
x_i(t+1) = x_i(t) + v_i(t+1)

Annealed acceptance:
P_accept = exp(-delta_E / T)
T_next = alpha * T
```

## Install

```bash
python -m pip install -e . --no-build-isolation
```

For normal online environments:

```bash
pip install -e .[dev]
```

## Test

```bash
pytest -q
```

Expected local validation from the first packaged version:

```text
12 passed
```

## Run a benchmark

```bash
python examples/run_benchmark.py --function michalewicz --dimensions 5 --runs 10 --iterations 300
```

The benchmark compares:

- Simulated Annealing
- Particle Swarm Optimization
- PathWoven Inside DCGO

## Repository layout

```text
src/pathwoven_dcgo/
  algorithms.py    # SA, PSO, PathWoven-DCGO
  benchmarks.py    # objective functions
  experiment.py    # benchmark orchestration
  stats.py         # robust sample summaries
  plotting.py      # convergence plotting

tests/             # unit tests
examples/          # benchmark CLI
docs/              # formal algorithm specification
```

## Why this fixes the earlier plotting/statistics issue

The benchmark harness pads convergence logs to a uniform length before plotting and rejects empty statistical samples before summarization. That prevents errors like:

```text
ValueError: x and y must have same first dimension
RuntimeWarning: Mean of empty slice
```

## License

MIT
