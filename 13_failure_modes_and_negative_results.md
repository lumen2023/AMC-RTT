# 13 Failure Modes And Negative Results

Status: `REQUIRED_CLAIM_GUARD`

Negative results are part of the method. They prevent the transfer toolkit from
over-claiming.

## Known Boundaries

Geometry-only is insufficient:

```text
local geometric similarity explains only limited consequence redundancy
```

Safe Cover compression is not supported:

```text
A2.8 strict matched safety -> identity cover
set-level compression -> NOT_SUPPORTED
```

Large or long AMC can risk collapse:

```text
A3.6 long endpoint marked possible mode collapse by coverage gate
```

Naive mode-preserving AMC is not supported:

```text
MP-AMC remained diagnostic/control, not a validated fix
```

Scalar calibration is insufficient:

```text
calibration does not imply the scalar contains the needed relation topology
```

A14 rich-support interpretation is superseded:

```text
A15 shows A14 gain is deconfounded by teacher-side target variables
```

Teacher margin gain is target-side self-dependency:

```text
hard assignment + margin/uncertainty almost reconstruct the soft target Q
```

Multi-horizon AC-JEPA support fails the primary gate:

```text
M5_acjepa_horizon_mse - M0_affinity
Delta R2 = -0.0168
95% CI = [-0.0290, -0.0045]
```

`K_eff` decrease is not performance improvement:

$K_{\mathrm{eff}}$ only controls total affinity mass; topology and task score
must be checked separately.

Planning quality improvement is not supported:

```text
A3.7 score drops slightly despite stable coverage
```

## Teacher-Side Leakage Guard

The soft relation target:

$$
\pi_i(m)
=
\frac{
\exp\!\left[-\operatorname{ADE}(\tau_i,p_m)/T\right]
}{
\sum_\ell
\exp\!\left[-\operatorname{ADE}(\tau_i,p_\ell)/T\right]
},
\qquad
Q_{ij}
=
\sum_m\pi_i(m)\pi_j(m).
$$

is a deterministic function of teacher-ADE vectors. Features derived from the
same vectors, such as hard assignment, margin, entropy, nearest ADE, or
second-nearest ADE, are target-side information.

Do not count their predictive power as frozen model-side consequence support.

## Final Rule

Never convert a `DIAGNOSTIC_ONLY` pass into a method claim without a matched
training or task-validation gate.
