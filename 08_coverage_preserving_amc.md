# 08 Coverage Preserving AMC

Status: `SUPPORTED_STABILIZATION__NOT_PLANNING_IMPROVEMENT`

A3.7 adds a coverage-decrease hinge on top of AMC. This is an optional
stabilizer, not the core AMC definition.

## Soft Teacher Coverage

Given predicted proposals and teacher trajectories:

```text
ADE(m,i) = mean_t || teacher_m[t,:2] - proposal_i[t,:2] ||_2
soft_min_m = -temp_min * logsumexp_i(-ADE(m,i) / temp_min)
C_soft = mean_m sigmoid((threshold_m - soft_min_m) / temp_sigmoid)
```

The Drive-JEPA default threshold in A3.7 was coverage@2m.

## Loss

```text
L_total = L_original + lambda * L_AMC + beta * L_coverage
L_AMC = (log K_eff_pred - stopgrad(log K_eff_teacher))^2
L_coverage = relu(stopgrad(C_soft_baseline) - C_soft_pred)^2
```

The hinge only penalizes predicted coverage dropping below the baseline
surrogate.

## Evidence

A3.7:

```text
lambda = 0.25
beta = 0.1
steps = 500
hard failures = []
AC-JEPA parameter grads = 0
```

Mean deltas:

```text
K_eff_pred: -0.3447
abs log-gap: -0.0472
coverage@2m: +0.0000
within-mode latent dispersion: -15.87
score: -0.0058
```

## Transfer Examples

For robotics or control, coverage constraints may use:

- teacher action support;
- goal success support;
- demonstration support;
- reachable contact states;
- safety envelope coverage.

## Correct Claim

Supported:

```text
coverage-stable effective multimodality calibration
```

Not supported:

```text
task-performance improvement
strict per-scene coverage monotonicity
proposal cardinality reduction
```

