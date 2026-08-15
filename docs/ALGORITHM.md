# PathWoven-DCGO Algorithm Specification

## 1. Purpose

PathWoven-DCGO is a hybrid optimization technique for hard nonconvex objective functions. It is inspired by the geometric transformation used to explain the circle-area identity `A = pi*r^2`: slice a circular domain into thin sectors, then rearrange the sectors into a nearly rectangular structure.

In this optimizer, the same geometric idea decomposes a rugged search region into tractable local windows. Particle Swarm Optimization performs coordinated search inside each window, while a Simulated Annealing controller manages exploration, sector refinement, and cross-sector transitions.

## 2. Conceptual modules

### 2.1 Problem landscape

The optimizer accepts an objective function `f(x)`, lower and upper bounds, an iteration budget, a sector count, and particles per sector.

```text
minimize f(x), where x is inside the bounded domain [lower, upper]^d
```

### 2.2 Circular domain mapping

The search domain is normalized:

```text
z = 2 * (x - lower) / (upper - lower) - 1
```

The first two normalized coordinates define angular sector membership:

```text
theta = atan2(z2, z1)
```

For higher-dimensional problems, this angular projection acts as a coordination layer, not a full dimensionality reduction.

### 2.3 Pizza-slice decomposition

The angular domain is partitioned into `K` sectors:

```text
S_k = [2*pi*k/K, 2*pi*(k+1)/K)
```

Each sector receives a sub-swarm.

### 2.4 PathWoven rearrangement

A sector is treated as a local rectangular search window:

```text
circle -> slices -> rectangular strip
```

This does not claim the objective becomes convex. It creates a disciplined structure for parallel local exploration.

### 2.5 PSO local search

For particle `i`:

```text
v_i(t+1) = w*v_i(t) + c1*r1*(p_i - x_i) + c2*r2*(g_k - x_i) + c3*r3*(g - x_i)
x_i(t+1) = x_i(t) + v_i(t+1)
```

where `p_i` is particle best, `g_k` is sector best, and `g` is global best.

### 2.6 Annealed refinement

The SA controller accepts exploratory moves with:

```text
P_accept = exp(-delta_E / T)
```

The temperature decreases according to:

```text
T_next = alpha * T
```

This lets the optimizer behave like a wide-search flock early and a disciplined local solver late.

### 2.7 DCGO coordination layer

The DCGO layer acts above the local swarms. Its role is to:

- rank promising sectors,
- propagate strong information across local windows,
- retain best-path candidates,
- permit adaptive updates to sector emphasis.

This makes the algorithm more than a simple PSO-in-a-box scheme; it becomes a coordinated hybrid search architecture.

## 3. Pseudocode

```text
Input: objective f, bounds [lower, upper], sectors K, particles per sector M, iterations T
Initialize K x M particles across domain
Assign particles to angular sectors
Evaluate objective values
Store particle, sector, and global bests

for t = 1..T:
    for each sector k:
        update sector best g_k

    for each particle i in sector k:
        compute PSO velocity using particle best, sector best, and global best
        propose candidate position
        add annealed PathWoven jitter proportional to temperature
        accept candidate if better or by exp(-delta/T)
        update particle best

    update global best
    recompute sector membership from radial-angle projection
    cool temperature
    record convergence

return best solution, best objective value, convergence trace, metadata
```

## 4. Benchmark plan

| Function | Dimensions | Runs | Iterations | Purpose |
|---|---:|---:|---:|---|
| Sphere | 2, 5, 10 | 30 | 300 | sanity check |
| Rastrigin | 2, 5, 10 | 30 | 500 | multimodal stress test |
| Rosenbrock | 2, 5, 10 | 30 | 1000 | curved valley behavior |
| Ackley | 2, 5, 10 | 30 | 500 | rugged global basin |
| Michalewicz | 2, 5, 10 | 30 | 1000 | deceptive landscape |

## 5. Application domains

PathWoven-DCGO is suitable wherever the search problem is high-cost, rugged, constrained, or transition-oriented. Representative targets include:

- robotics and motion planning,
- logistics and scheduling,
- manufacturing and assembly planning,
- network reconfiguration,
- legal or compliance workflow optimization,
- scientific transition-path problems in physics, chemistry, and computational science.

## 6. Validation rules

A serious performance claim requires identical budgets, run counts, seeds, dimensions, and statistical summaries. The repository includes guardrails that reject empty statistical samples and pad convergence traces to avoid plotting shape mismatches.

For an academic presentation, the recommended evidence stack is:

1. matched benchmark budgets,
2. repeated seeds,
3. convergence traces,
4. summary tables of final best values,
5. ANOVA or equivalent omnibus testing,
6. pairwise post-hoc comparisons where justified.
