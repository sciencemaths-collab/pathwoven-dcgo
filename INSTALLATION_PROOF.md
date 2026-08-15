# Installation Proof

The package was installed and tested in the ChatGPT sandbox after patching package exports.

## Install command used

```bash
python -m pip install -e . --no-deps --no-build-isolation
```

The no-build-isolation flag was required because the sandbox could not fetch isolated build dependencies from the internet, even though local build tooling was available.

## Test result

```text
12 passed
```

## Michalewicz smoke benchmark

```text
Simulated Annealing: n=3 mean=-1.60627
Particle Swarm Optimization: n=3 mean=-3.89602
PathWoven Inside DCGO: n=3 mean=-4.04754
```

This smoke benchmark is not a universal superiority claim. It is a first validation that the implementation runs and can outperform the included baselines under a small fixed test budget.
