# 09 Topology And Collapse Diagnostics

Status: `SUPPORTED_DIAGNOSTIC_LIBRARY`

Scalar `K_eff` must be paired with topology and collapse diagnostics.

## Core Diagnostics

Affinity groups:

```text
within_affinity
cross_affinity
affinity_margin = within_affinity - cross_affinity
distance_margin
edge_density
connected_components
component_compactness
```

Coverage and mode preservation:

```text
oracle cover diagnostic
coverage@threshold
teacher modes covered
active teacher modes
collapse risk index (CRI)
```

Topology concentration:

```text
w_ij = S_ij^2
A = sum_{i<j} w_ij
B = sum_{i<j} w_ij^2
E_eff = A^2 / B
rho = E_eff / C(K,2)
```

Row-local concentration:

```text
row_mass_i = sum_{j != i} w_ij
row_neff_i = row_mass_i^2 / sum_{j != i} w_ij^2
```

## Selective Consolidation Versus Diffuse Smoothing

Selective consolidation should:

- concentrate contraction on high-confidence redundant neighborhoods;
- reduce diffuse cross-mode contraction;
- preserve or improve coverage;
- avoid broad increases in weak cross-pair affinity.

Diffuse smoothing tends to:

- lower `K_eff`;
- raise total affinity mass;
- increase edge participation;
- increase cross-mode contraction mass;
- create false-merge risk.

## Drive-JEPA Evidence

A18 found:

```text
K_eff_pred decreases
affinity mass A increases
edge participation E_eff increases
row effective neighbor count increases
different-teacher diagnostic gradient mass increases
```

This supports diffuse smoothing, not selective consolidation.

A19 found topology-aware gradient fields can reduce different-hard-teacher
contraction mass relative to AMC-v1 in read-only simulation.

## Rule

Never report `K_eff` alone as evidence of capacity efficiency or diversity
improvement.

