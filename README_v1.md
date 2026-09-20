# AMC-RTT v1 Upgrade: Generator-Agnostic Consequence-Topology Regularization

Status: `V1_CORE_CONTRACT_PASS__DOCS_AND_TESTS_READY`

This v1 layer upgrades AMC-RTT from a Drive-JEPA-specific AMC package into a
generator-agnostic consequence-topology regularization package.

中文：v1 层把 AMC-RTT 从 Drive-JEPA 上的一套 AMC 实现，升级为
generator-agnostic consequence-topology regularization 包。

## Current Situation / 当前状况

The newest A30-A32 evidence corrects the mainline:

- A30: the repaired `all_layer_fold` contract reconnects final-layer trajectory
  gradients under small batches.
- A31: after that repair, all-pair optimizer-gradient redundancy is still not
  supported.
- A32: the reason is sparse winner-take-min credit: median active proposals are
  `5/32`, max active proposals are `5/32`, and active rows match the human/pseudo
  winner set at `100%`.

Correct interpretation:

$$
\boxed{
\text{WTA/base loss specializes sparse winners, while AMC-RTT regularizes the
whole-set consequence topology.}
}
$$

This means AMC-RTT should no longer be framed as direct optimizer-credit
redundancy reduction. The current mainline is:

$$
\boxed{
\text{clean hypothesis set}
\rightarrow
\text{frozen AC-JEPA consequence space}
\rightarrow
\text{pair moments and topology}
\rightarrow
\text{selective regularization}
}
$$

## What Was Added / 新增内容

- `v1_core/core.py`: pure generator-independent math core.
- `v1_core/adapters.py`: clean-endpoint adapters for diffusion and flow
  matching.
- `tests_v1/`: synthetic contract tests for math identities, gradients, and
  generator-axis invariants.
- `docs_v1/`: evidence-to-design map, theory, DM/FM adaptation, next decisions,
  and the 3-hour autonomous Codex directive.

Validation:

```text
pytest -q tests_v1
8 passed
```

## Hard Invariant / 硬不变量

AMC-RTT topology is always computed over:

$$
\boxed{
\text{same generative time} + \text{different hypotheses}
}
$$

It must never treat diffusion denoising steps or flow integration steps as
semantic modes.

## Key Math / 关键数学

For consequence latents $h_i=\Phi_{\rm AC}(c,\tau_i)$:

$$
q_{ij}=\lVert h_i-h_j\rVert^2,
\qquad
S_{ij}=\exp\left(-\frac{q_{ij}}{\tau_h^2}\right),
\qquad
w_{ij}=S_{ij}^2.
$$

Let $M=\binom{K}{2}$:

$$
\mu_1=\frac{1}{M}\sum_{i<j}w_{ij},
\qquad
\mu_2=\frac{1}{M}\sum_{i<j}w_{ij}^2.
$$

Then:

$$
\boxed{
K_{\rm eff}
=
\frac{K}{1+(K-1)\mu_1}
}
$$

and:

$$
\boxed{
\rho
=
\frac{\mu_1^2}{\mu_2}
=
\frac{E_{\rm eff}}{\binom K2}.
}
$$

The topology gradient is:

$$
\boxed{
\frac{\partial\log\rho}{\partial q_e}
=
\frac{4}{\tau_h^2}(r_e-p_e),
\quad
p_e=\frac{w_e}{\sum_u w_u},
\quad
r_e=\frac{w_e^2}{\sum_u w_u^2}.
}
$$

This is the selective credit rule: high-mass edges consolidate; low-mass diffuse
edges release.

## Near-Term Goal / 下一步目标

Do not run a new Drive-JEPA/DM/FM training campaign yet. The next target is:

$$
\boxed{
\text{prove that one AMC-RTT core operates unchanged on static, diffusion, and
flow-matching clean hypothesis sets.}
}
$$

Only after static replay, DM contract, and FM contract all pass should real
DiffusionDrive/FM tiny training be considered.
