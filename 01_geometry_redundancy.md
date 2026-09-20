# 01 Geometry Redundancy

Status: `DIAGNOSTIC_ONLY`

Geometry is the simplest and most portable redundancy baseline. It should be
implemented in every transfer task before using task-aware consequence latents.

## Distances

Candidate trajectory `y_i` has shape `[T,D]`. Candidate action `a_i` has shape
`[H,D_a]`.

Common distances:

```text
ADE(i,j) = mean_t || y_i[t,:2] - y_j[t,:2] ||_2
FDE(i,j) = || y_i[T,:2] - y_j[T,:2] ||_2
endpoint(i,j) = FDE(i,j)
max_point(i,j) = max_t || y_i[t,:2] - y_j[t,:2] ||_2
trajectory_L2(i,j) = || flatten(y_i - y_j) ||_2
action_L2(i,j) = || flatten(a_i - a_j) ||_2
```

Generic threshold relation:

```text
R_G(i,j) = 1[d_G(i,j) <= epsilon]
```

## Interpretation

Geometry is a baseline, not the final consequence redundancy definition.

The Drive-JEPA evidence says local geometric similarity explains only a limited
part of consequence redundancy. A2.6 localized much of the oracle compression
headroom outside the very local geometry region, and A2.7 showed AC-JEPA latent
readouts add consequence information beyond geometry plus raw action features.

## Use In Transfer

Run geometry first to establish:

- raw duplicate rate;
- endpoint overlap;
- local versus wide-support redundancy;
- whether the task is already solved by a simple metric.

Proceed to task-aware consequence metrics only after documenting the geometry
baseline. Do not present geometry-only success as AMC success unless the task
itself defines redundancy purely geometrically.

