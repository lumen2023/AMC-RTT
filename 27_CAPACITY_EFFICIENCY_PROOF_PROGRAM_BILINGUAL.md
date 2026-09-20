# 27 Capacity-Efficiency Proof Program / 容量效率证明程序

Status: `FUTURE_PROOF_OBLIGATION`

The objective is not to force a proof. The objective is to build a falsifiable
causal chain.

目标不是强行得到证明，而是建立一条可证伪的因果链。

## H1: Structured AMC Lowers Redundant Gradient Correlation

### Hypothesis / 假设

TA-AMC lowers gradient redundancy relative to AMC-v1.

TA-AMC 相比 AMC-v1 降低梯度冗余。

### Measurements / 测量

```text
pair gradient cosine
effective gradient sample size
gradient covariance effective rank
cross-mode contraction mass
edge participation
```

### Gate / 门控

The improvement must be measured in parameter or representation gradient space,
not only in pair-affinity space.

改进必须在 parameter 或 representation gradient space 中测量，不能只在
pair-affinity space 中测量。

## H2: Structured AMC Raises Local Information Volume

### Hypothesis / 假设

TA-AMC raises a predeclared local information proxy:

TA-AMC 提升预注册的局部信息 proxy：

```text
erank(G_grad)
or
log det(I + lambda F_hat)
```

### Measurements / 测量

- Jacobian sketches;
- Jacobian sketches；
- low-rank Fisher approximation;
- low-rank Fisher approximation；
- Hutchinson/logdet estimator with fixed seeds;
- 使用固定 seeds 的 Hutchinson/logdet estimator；
- compute-normalized information per update.
- 按 compute normalization 的每次更新信息量。

### Counter-risk / 反风险

Higher rank can reflect irrelevant or noisy directions. Pair with task-relevant
projection and held-out task metrics.

更高 rank 可能只是无关或噪声方向。必须配合 task-relevant projection 与
held-out task metrics。

## H3: TA-AMC Reduces Easy-Scene Dominance

### Hypothesis / 假设

After defining difficulty before final evaluation, TA-AMC reduces the share of
shared updates dominated by easy/redundant scenes.

在 final evaluation 前预定义 difficulty 后，TA-AMC 降低 easy/redundant scenes
对 shared updates 的支配。

### Measurements / 测量

```text
per-scene gradient norm
gradient cosine by difficulty pair
normalized contribution share
easy / medium / hard batch contribution
```

### Required Optimizer Audit / 必须的 optimizer audit

Check:

检查：

- Adam/AdamW state;
- Adam/AdamW state；
- gradient clipping;
- gradient clipping；
- batch reduction;
- batch reduction；
- gradient accumulation;
- gradient accumulation；
- mixed precision scaling.
- mixed precision scaling。

The conditional complex-scene theorem is not enough without this audit.

没有这个 audit，complex-scene conditional theorem 不足以支持结论。

## H4: Hard Scenes Receive More Effective Updates

### Hypothesis / 假设

TA-AMC increases the projection of the total update onto hard-scene gradient
directions while preserving easy-scene task performance.

TA-AMC 提高总更新在 hard-scene gradient directions 上的投影，同时保持
easy-scene task performance。

### Measurements / 测量

```text
<Delta theta, g_hard / ||g_hard||>
hard-scene update share
task score by difficulty
coverage by difficulty
```

Compare:

比较：

```text
baseline vs AMC-v1 vs TA-AMC
```

## H5: Task Learning Improves

### Hypothesis / 假设

Only after H1-H4 pass should task-level benefit be tested as a causal endpoint.

只有 H1-H4 通过后，才应把 task-level benefit 作为因果终点测试。

Primary metrics:

主指标：

- trajectory loss;
- trajectory loss；
- score / best_score;
- score / best_score；
- PDMS / EPDMS or actual task metric;
- PDMS / EPDMS 或项目真实 task metric；
- safety/coverage constraints.
- safety/coverage constraints。

## Upgrade Gate / 升级门控

Upgrade to:

只有在以下条件同时成立时，才能升级为：

```text
CAPACITY_EFFICIENCY_SUPPORTED
```

only if:

```text
redundancy structure improves
AND optimization information improves
AND hard/complex-scene update share improves
AND matched task metric improves
```

Otherwise:

否则：

```text
MECHANISM_SUPPORTED__TASK_GAIN_NOT_YET_SUPPORTED
```

## What Would Falsify The Story? / 什么会证伪故事？

The story is weakened or falsified if:

以下结果会削弱或证伪当前故事：

- TA-AMC changes affinity topology but not parameter-space gradients;
- TA-AMC 改变 affinity topology 但不改变 parameter-space gradients；
- gradient information proxy rises but task performance falls consistently;
- gradient information proxy 上升但 task performance 持续下降；
- hard-scene share rises only because easy-scene learning collapses;
- hard-scene share 上升只是因为 easy-scene learning collapse；
- the effect disappears after matching compute and optimizer state;
- 匹配 compute 与 optimizer state 后效果消失；
- the effect is caused by teacher leakage or post hoc difficulty labels.
- 效果由 teacher leakage 或事后 difficulty labels 造成。

