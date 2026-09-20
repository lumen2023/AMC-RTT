# 24 Failure Modes And Safety Gates / 失败模式与安全门控

Status: `CLAIM_SAFETY`

## Failure Modes / 失败模式

### F1: Geometry Is Mistaken For Consequence / 把几何当成 consequence

Geometry-only can miss task-equivalent or task-different futures. A2.7 supports
incremental frozen-latent relation information, while A2.8 shows that relation
information does not automatically yield safe set compression.

仅靠 geometry 可能漏掉 task-equivalent 或 task-different futures。A2.7 支持
frozen-latent relation 的增量信息，但 A2.8 表明 relation information 不会自动
转化为安全的 set compression。

### F2: Teacher Leakage / teacher 泄漏

The soft target:

$$
\pi_i(m)
=
\operatorname{softmax}_m\!\left(
-\frac{\operatorname{ADE}(\tau_i,p_m)}{T}
\right),
\qquad
Q_{ij}
=
\sum_m \pi_i(m)\pi_j(m).
$$

is constructed from teacher-ADE vectors. Hard teacher assignment, margin,
entropy, nearest ADE, and second-nearest ADE can predict `Q` by construction.
Their predictive power is target-side self-dependency, not independent
representation support.

该 soft target 来源于 teacher-ADE vectors。hard assignment、margin、entropy、
nearest ADE、second-nearest ADE 天然可以预测 `Q`。它们的预测能力是 target-side
self-dependency，不是独立 representation support。

### F3: `K_eff` Is Treated As Topology / 把 `K_eff` 当成 topology

$$
K_{\mathrm{eff}}
=
\frac{K^2}{K+2\sum_{i<j}S_{ij}^2}.
$$

controls total affinity mass but not its allocation across edges. Report edge
participation, row effective neighbors, and cross-mode mass with `K_eff`.

它控制 affinity 总量，但不控制总量如何分配到 edge。必须与 edge participation、
row effective neighbors、cross-mode mass 一起报告。

### F4: Diffuse Smoothing / diffuse smoothing

`K_eff down` with affinity mass and edge participation up is consistent with
many weak pairs becoming similar. This can increase false merges and gradient
correlation.

`K_eff` 下降但 affinity mass 与 edge participation 上升，说明可能是大量弱 pair
同时变得相似，从而增加 false merge 与 gradient correlation。

### F5: Mode Collapse In Stochastic Decoders / 随机 decoder mode collapse

Attraction among diffusion/FM samples can concentrate probability mass and lower:

Diffusion/FM sample attraction 可能集中概率质量并降低：

$$
\mathbb{E}[U_K]
=
\sum_m\left[1-(1-p_m)^K\right].
$$

### F6: Proxy/Endpoint Mismatch / proxy 与 endpoint 不一致

One-step diffusion `x0_hat` or short FM solver may not preserve final endpoint
relations. Proxy agreement must be measured before proxy training claims.

Diffusion 单步 `x0_hat` 或 FM 短 solver 可能不保持 final endpoint relation。
必须先测 proxy agreement。

### F7: Collapse Hidden By Mean Coverage / 被平均 coverage 隐藏的 collapse

Mean coverage can stay constant while individual hard scenes lose modes. Report
scene-level tails and hard-scene coverage, not only the mean.

平均 coverage 不变时，个别 hard scenes 仍可能丢 mode。必须报告 scene-level tail
与 hard-scene coverage，而不只是均值。

## Safety Gates / 安全门控

### Gate G0: Schema

```text
[B,K,...] candidates
[B,K,K] relations
no cross-condition pairs
```

### Gate G1: Frozen Boundary

```text
candidate gradient finite and nonzero
frozen evaluator parameter gradients exactly zero
```

### Gate G2: Numerical

```text
loss finite
K_eff finite
tau finite and provenance fixed
no NaN/OOM
```

### Gate G3: Topology

```text
edge participation
row effective neighbors
same/different mode contraction
```

must be recorded before claiming selective consolidation.

### Gate G4: Coverage

Predeclare:

预注册：

- mean coverage budget;
- 平均 coverage budget；
- per-scene tail budget;
- per-scene tail budget；
- hard/complex-scene mode coverage gate.
- hard/complex-scene mode coverage gate。

### Gate G5: Task

Require matched held-out task metrics:

要求 matched held-out task metrics：

```text
trajectory loss
score / best_score
PDMS / EPDMS or the actual task metric
```

## Stop Conditions / 停止条件

Stop the migration or pilot if:

出现以下任一情况必须停止迁移或 pilot：

- frozen parameter gradients are nonzero;
- frozen parameter gradients 非零；
- cross-condition affinity is detected;
- 检测到跨 condition affinity；
- `K_eff` improves only while hard-scene coverage collapses;
- `K_eff` 改善但 hard-scene coverage collapse；
- proxy relation fails endpoint agreement;
- proxy relation 不满足 endpoint agreement；
- task score gate is missing but a task-improvement claim is attempted.
- 缺少 task score gate 却试图声称 task improvement。
