# 3-Hour Autonomous Codex Directive / 3 小时自主科研指令

Status: `READY_FOR_LONG_HORIZON_AUTONOMY`

## Mission / 任务

Upgrade AMC-RTT into a generator-agnostic consequence-topology regularization
research package without modifying any file outside `AMC-RTT_v1.0/`.

把 AMC-RTT 升级为 generator-agnostic consequence-topology regularization 研究包，
同时不修改 `AMC-RTT_v1.0/` 之外任何文件。

## Mainline / 主线

$$
\boxed{
\text{fixed-K / multi-sample generator}
\rightarrow
\text{clean future hypotheses}
\rightarrow
\text{frozen consequence topology}
\rightarrow
\text{selective redundancy regularization}
\rightarrow
\text{preserved effective multimodality}
}
$$

A30-A32 mandatory framing:

$$
\boxed{
\text{base WTA loss handles sparse target coverage, while AMC-RTT handles
whole-set consequence topology.}
}
$$

Forbidden framing:

```text
AMC-RTT = optimizer-credit redundancy correction
```

## Phase 0: Isolation And Evidence Audit / 0:00-0:20

1. Locate `AMC-RTT_v1.0/`.
2. Generate `UPSTREAM_LOCK_BEFORE.json` with sha256 for tracked files outside
   `AMC-RTT_v1.0/`.
3. Only write under `AMC-RTT_v1.0/**`.
4. Read A18, A19, A20, A26, A30, A31, A32.
5. Update `docs_v1/EVIDENCE_TO_DESIGN.md`.

Stop only on:

```text
ISOLATION_VIOLATION
data corruption risk
AC-JEPA unexpectedly trainable
```

## Phase 1: Generator-Independent Math Core / 0:20-0:50

Implement or verify:

$$
q_{ij}=\lVert h_i-h_j\rVert^2,
\qquad
S_{ij}=\exp\left(-\frac{q_{ij}}{\tau_h^2}\right),
\qquad
w_{ij}=S_{ij}^2.
$$

Pair moments:

$$
\mu_1=\frac{1}{M}\sum_{i<j}w_{ij},
\qquad
\mu_2=\frac{1}{M}\sum_{i<j}w_{ij}^2.
$$

Required identities:

$$
K_{\rm eff}
=
\frac{K}{1+(K-1)\mu_1},
\qquad
\rho
=
\frac{\mu_1^2}{\mu_2}.
$$

Gradient identity:

$$
\frac{\partial\log\rho}{\partial q_e}
=
\frac{4}{\tau_h^2}(r_e-p_e).
$$

Gate:

```text
pytest -q tests_v1
```

Expected:

```text
8 passed
```

## Phase 2: Generator Adapter Contract / 0:50-1:15

Define:

```text
GeneratorAdapter.to_clean_hypotheses(...)
```

Output:

```text
clean_trajectory: [B,K,T,D]
metadata:
  hypothesis_id
  generator_family
  sample_source
  generation_time
  anchor_id(optional)
  noise_seed(optional)
```

Hard invariant:

$$
\boxed{
\text{same generative time}+\text{different hypotheses}
}
$$

Reject:

```text
diffusion steps as modes
flow integration steps as modes
```

## Phase 3: Diffusion Adapter / 1:15-1:45

For:

$$
x_t=\alpha_t x_0+\sigma_t\epsilon,
$$

support:

$$
\hat x_0
=
\frac{x_t-\sigma_t\hat\epsilon_\theta}{\alpha_t}
\quad\text{for epsilon prediction},
$$

$$
\hat x_0=\hat x_{0,\theta}
\quad\text{for x0 prediction},
$$

and under $\alpha_t^2+\sigma_t^2=1$:

$$
\hat x_0
=
\alpha_t x_t-\sigma_t\hat v_\theta
\quad\text{for v prediction}.
$$

Record:

$$
\left\lVert
\frac{\partial \hat x_0}{\partial \hat\epsilon_\theta}
\right\rVert
=
\frac{\sigma_t}{\alpha_t}.
$$

Decision:

- if finite and same-time invariant passes: `DM_CONTRACT_PASS`;
- otherwise: `AMC_RTT_DM_ADAPTER_BLOCKED`.

## Phase 4: Flow-Matching Adapter / 1:45-2:10

For linear path:

$$
x_t=(1-t)x_0+t x_1,
\qquad
u=x_1-x_0.
$$

Clean endpoint:

$$
\hat x_1=x_t+(1-t)v_\theta.
$$

Oracle proof:

$$
v_\theta=u
\Rightarrow
\hat x_1=x_1.
$$

Gradient scale:

$$
\frac{\partial \hat x_1}{\partial v_\theta}=(1-t)I.
$$

Decision:

- if endpoint reconstruction and gradient finite: `FM_CONTRACT_PASS`;
- otherwise: `AMC_RTT_FM_ADAPTER_BLOCKED`.

## Phase 5: Static Replay / 2:10-2:35

Use persisted Drive-JEPA/TA-AMC records read-only.

Gate:

| item | threshold |
| --- | --- |
| legacy $K_{\rm eff}$ parity | $<10^{-6}$ |
| $\rho$ parity | $<10^{-6}$ |
| topology analytic/autograd gradient | $<10^{-6}$ |
| AC-JEPA parameter grads | exactly zero |

If this fails:

```text
BACKWARD_COMPATIBILITY_FAIL
```

Stop DM/FM work and repair core parity first.

## Phase 6: Tiny Smoke Branch / 2:35-2:55

Only if static replay, DM contract, and FM contract pass:

1. detect a local real DM/FM model;
2. otherwise use a tiny synthetic 2D trajectory model;
3. run AMC off vs AMC-RTT;
4. check finite losses and bounded gradient ratio;
5. do not claim task improvement.

## Phase 7: Closeout / 2:55-3:00

Generate:

- `UPSTREAM_LOCK_AFTER.json`;
- `UPSTREAM_IMMUTABILITY_REPORT.md`;
- test report;
- updated `AUTONOMOUS_STATE.yaml`.

Final scientific question:

$$
\boxed{
\text{Can the same consequence-topology regularizer operate over clean
hypothesis sets from static, diffusion, and flow-matching generators without
changing mathematical meaning?}
}
$$

## Branch Decisions / 分支裁决

| case | verdict | next action |
| --- | --- | --- |
| static + DM + FM contract pass | `AMC_RTT_V1_GENERATOR_AGNOSTIC_CORE_PASS` | freeze math core; next real tiny training |
| static pass, DM fail | `AMC_RTT_DM_ADAPTER_BLOCKED` | localize prediction convention/time conditioning |
| static pass, FM fail | `AMC_RTT_FM_ADAPTER_BLOCKED` | localize path convention/endpoint reconstruction |
| static replay fail | `BACKWARD_COMPATIBILITY_FAIL` | stop DM/FM; repair core parity |
| contracts pass but native loss conflicts | `GENERATOR_ADAPTER_VALID__OPTIMIZATION_CONFLICT` | study time window/schedule |
