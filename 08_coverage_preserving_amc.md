# 08 Coverage Preserving AMC

Status: `SUPPORTED_STABILIZATION__NOT_PLANNING_IMPROVEMENT`

A3.7 adds a coverage-decrease hinge on top of AMC. This is an optional
stabilizer, not the core AMC definition.

## Soft Teacher Coverage

Given predicted proposals and teacher trajectories:

$$
\operatorname{ADE}(m,i)
=
\operatorname{mean}_t
\left\|
\operatorname{teacher}_m[t,:2]
-
\operatorname{proposal}_i[t,:2]
\right\|_2,
$$

$$
\operatorname{softmin}_m
=
-T_{\min}
\log\sum_i
\exp\!\left(
-\frac{\operatorname{ADE}(m,i)}{T_{\min}}
\right),
$$

$$
C_{\mathrm{soft}}
=
\operatorname{mean}_m
\sigma\!\left(
\frac{\operatorname{threshold}_m-\operatorname{softmin}_m}
{T_{\sigma}}
\right).
$$

The Drive-JEPA default threshold in A3.7 was coverage@2m.

## Loss

$$
L_{\mathrm{total}}
=
L_{\mathrm{original}}
+
\lambda L_{\mathrm{AMC}}
+
\beta L_{\mathrm{coverage}},
$$

$$
L_{\mathrm{AMC}}
=
\left[
\log K_{\mathrm{eff,pred}}
-
\operatorname{stopgrad}(\log K_{\mathrm{eff,teacher}})
\right]^2,
$$

$$
L_{\mathrm{coverage}}
=
\operatorname{ReLU}
\left[
\operatorname{stopgrad}(C_{\mathrm{soft,baseline}})
-
C_{\mathrm{soft,pred}}
\right]^2.
$$

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
