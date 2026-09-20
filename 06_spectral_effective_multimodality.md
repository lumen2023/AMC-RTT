# 06 Spectral Effective Multimodality

Status: `SUPPORTED_WITH_TOPOLOGY_LIMITATION`

## Similarity

Given pairwise distances:

```text
d_ij >= 0
```

construct:

```text
S_ij = exp(-(d_ij / tau)^2)
S_ii = 1
S = 0.5 * (S + S^T)
```

In the AC-JEPA implementation, `d_ij^2` is the mean per-horizon latent MSE and
the code writes:

```text
S_ij = exp(-mse_ij / tau^2)
```

`tau` must be calibrated on training/calibration data or inherited from frozen
experiment provenance. Avoid tuning `tau` on held-out evaluation data.

## Effective Rank

The spectral effective multimodality is the participation-ratio effective rank:

```text
K_eff(S) = (tr S)^2 / tr(S^2)
```

Since `diag(S)=1`:

```text
tr S = K
tr(S^2) = K + 2 * sum_{i<j} S_ij^2
```

so:

```text
K_eff = K^2 / (K + 2 * sum_{i<j} S_ij^2)
```

## Sanity Cases

Identical candidates:

```text
S_ij = 1 for all i,j
K_eff = 1
```

Independent candidates:

```text
S = I
K_eff = K
```

Ideal `M` equal-size blocks with within-block similarity near one and
cross-block similarity near zero:

```text
K_eff approximately M
```

## Important Limitation

`K_eff` controls total squared affinity mass:

```text
sum_{i<j} S_ij^2
```

It does not uniquely determine redundancy topology. A few strong local
redundant neighborhoods and many moderate cross-pair similarities can produce
similar `K_eff`.

A18 confirmed this limitation for AMC-v1: `K_eff_pred` decreased while affinity
mass and edge participation increased, supporting diffuse smoothing rather than
selective local consolidation.

## Required Companion Diagnostics

Always report `K_eff` with:

- affinity mass;
- edge participation ratio;
- row effective neighbor count;
- same/different teacher contraction mass when teacher labels are available;
- coverage and task score.

