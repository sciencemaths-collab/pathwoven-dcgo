# PathWoven-DCGO

**PathWoven-DCGO** is a geometry-guided hybrid optimization framework for hard nonconvex search. It combines pizza-slice geometric decomposition, Particle Swarm Optimization inside local sectors, and Simulated Annealing-style global refinement.

The algorithm is designed as a research reference for rugged benchmark functions such as Michalewicz, Rastrigin, Rosenbrock, Ackley, and Sphere.

> Status: reference implementation with tests and a benchmark harness. Do not claim universal superiority without repeated runs across dimensions, seeds, budgets, and statistical tests.

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

## Equations

Normalize a candidate vector:

```math
z = 2\frac{x-l}{u-l} - 1
```

Map to radial-angle sector membership:

```math
r = \lVert z \rVert_2, \quad \theta = \operatorname{atan2}(z_2,z_1)
```

PSO local search inside each sector:

```math
v_i(t+1)=\omega v_i(t)+c_1\rho_1(p_i-x_i)+c_2\rho_2(g_k-x_i)+c_3\rho_3(g-x_i)
```

```math
x_i(t+1)=x_i(t)+v_i(t+1)
```

Annealed acceptance:

```math
P=\exp(-\Delta E/T), \quad T_{t+1}=\alpha T_t
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
