# 06 Spectral Effective Multimodality

Status: `SUPPORTED_WITH_TOPOLOGY_LIMITATION`

## Similarity

Given pairwise distances:

$$
d_{ij}\ge 0.
$$

construct:

$$
S_{ij}=\exp\!\left[-\left(\frac{d_{ij}}{\tau}\right)^2\right],
\qquad
S_{ii}=1,
\qquad
S=\frac{1}{2}(S+S^\top).
$$

In the AC-JEPA implementation, `d_ij^2` is the mean per-horizon latent MSE and
the code writes:

$$
S_{ij}=\exp\!\left(-\frac{\operatorname{mse}_{ij}}{\tau^2}\right).
$$

`tau` must be calibrated on training/calibration data or inherited from frozen
experiment provenance. Avoid tuning `tau` on held-out evaluation data.

## Effective Rank

The spectral effective multimodality is the participation-ratio effective rank:

$$
K_{\mathrm{eff}}(S)
=
\frac{(\operatorname{tr}S)^2}{\operatorname{tr}(S^2)}.
$$

Since `diag(S)=1`:

$$
\operatorname{tr}S=K,
\qquad
\operatorname{tr}(S^2)
=
K+2\sum_{i<j}S_{ij}^2.
$$

so:

$$
K_{\mathrm{eff}}
=
\frac{K^2}{K+2\sum_{i<j}S_{ij}^2}.
$$

## Sanity Cases

Identical candidates:

$$
S_{ij}=1\ \text{for all }i,j
\quad\Rightarrow\quad
K_{\mathrm{eff}}=1.
$$

Independent candidates:

$$
S=I
\quad\Rightarrow\quad
K_{\mathrm{eff}}=K.
$$

Ideal `M` equal-size blocks with within-block similarity near one and
cross-block similarity near zero:

$$
K_{\mathrm{eff}}\approx M.
$$

## Important Limitation

`K_eff` controls total squared affinity mass:

$$
\sum_{i<j}S_{ij}^2.
$$

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
