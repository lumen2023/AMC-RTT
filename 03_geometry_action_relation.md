# 03 Geometry Action Relation

Status: `SUPPORTED_DIAGNOSTIC_WITH_LIMITED_COMPRESSION`

The Drive-JEPA A2 line compared raw geometry, raw action features, and frozen
AC-JEPA latent readouts for relation prediction.

## Feature Families

Geometry:

```text
trajectory ADE/FDE
endpoint distance
trajectory L2
```

Raw action:

```text
SE(2) adjacent actions
normalized action sequences
action L2
```

Frozen AC-JEPA latent:

```text
Z = [K,H,P,D]
pooled Z or per-horizon distances
```

Drive-JEPA action conversion uses adjacent SE(2) deltas:

```text
trajectory [8,3]
origin pose [0,0,0]
relative_se2_action(pose_i, pose_j) -> [dx_local, dy_local, dyaw]
actions [8,3]
```

The action normalization is train-split statistics:

```text
actions_norm = (actions - mean) / std
```

## Evidence Boundary

A2.7 supports that `G+A+Z/H` improves relation prediction beyond `G+A` in
full pair support and wider geometry bins. It does not prove set-level
compression.

A2.8 shows risk-calibrated Safe Cover did not convert that relation gain into a
strict matched-safety retained-K compression pass:

```text
primary budget: identity cover
set-level compression: NOT_SUPPORTED
```

## Correct Claim

Supported:

```text
frozen latent relation readout contains incremental consequence information
```

Not supported:

```text
post-hoc learned cover compresses the proposal set under strict matched safety
```

