# 17 Gradient SNR And Information Theory / 梯度 SNR 与信息理论

Status: `THEORETICAL_AND_EMPIRICAL_PROGRAM`

## 17.1 Correlated-Gradient Effective Sample Size

### THEOREM 4 / 定理 4

Assume `r` gradient contributions:

假设有 `r` 个梯度贡献：

```text
g_i = mu + epsilon_i
Var(epsilon_i) = sigma^2
Corr(epsilon_i, epsilon_j) = rho_g, i != j
```

For the sample mean:

样本均值的方差为：

```text
Var(mean_i g_i)
 = sigma^2/r * [1 + (r-1)rho_g]
```

Define:

定义有效独立样本数：

```text
r_eff = r / [1 + (r-1)rho_g]
```

When `rho_g -> 1`, `r_eff -> 1`. When `rho_g=0`, `r_eff=r`.

当 `rho_g -> 1` 时，`r_eff -> 1`；当 `rho_g=0` 时，`r_eff=r`。

### Derivation / 推导

Expand:

展开：

```text
Var(mean g)
 = 1/r^2 [r sigma^2 + r(r-1)rho_g sigma^2]
```

which simplifies to the stated expression.

### Counterexample / 反例

The scalar correlation model fails for non-exchangeable covariance, anisotropic
noise, adaptive optimizers, or gradients with strong mean drift. The result is
then a diagnostic approximation, not an exact effective sample count.

当 covariance 非 exchangeable、噪声各向异性、optimizer 自适应，或梯度均值显著
漂移时，标量 correlation 模型会失效。此时它只是诊断近似，不是精确样本数。

## 17.2 Fisher / Information-Volume Comparison

### PROPOSITION 5 / 命题 5

Let local gradient vectors be `v_i` and use:

令局部梯度向量为 `v_i`，定义：

```text
F = sum_i v_i v_i^T
V(F) = log det(I + lambda F)
```

For `r` duplicate vectors `v_i = a u`, with `||u||=1`:

对于 `r` 个相同方向 `v_i=a u`：

```text
V_duplicate = log(1 + lambda r a^2)
```

For `r` orthogonal equal-norm vectors:

对于 `r` 个等范数正交方向：

```text
V_orthogonal = r log(1 + lambda a^2)
```

Since `(1+x)^r > 1+rx` for `r>1,x>0`:

由于 `r>1,x>0` 时 `(1+x)^r > 1+rx`：

```text
V_orthogonal > V_duplicate
```

This is a local information-volume result, not a global generalization theorem.

这是局部信息体积结果，不是全局 generalization theorem。

### Counterexample / 反例

Orthogonal gradients may point toward irrelevant or conflicting task directions.
Higher local information volume does not guarantee a better objective or better
generalization.

正交梯度可能指向无关或冲突的任务方向。更高的局部信息体积不保证 objective 更好
或 generalization 更好。

## 17.3 Complex-Scene Gradient Share

### CONDITIONAL RESULT 6 / 条件结果 6

Let:

令：

```text
g = r u + v
u perpendicular to v
Delta theta = -eta G g / ||g||
```

Here `r u` is repeated easy-scene direction and `v` is a rare/complex-scene
direction. The normalized update component along `v` is:

其中 `r u` 是重复 easy-scene 方向，`v` 是 rare/complex-scene 方向。沿 `v`
的 normalized update 分量为：

```text
|<Delta theta, v/||v||>|
 = eta G ||v|| / sqrt(r^2 ||u||^2 + ||v||^2)
```

For nonzero `u,v`, this expression is strictly decreasing in `r`.

当 `u,v` 非零时，该表达式关于 `r` 严格递减。

### Important Boundary / 重要边界

This result assumes normalized or clipped update behavior and orthogonality.
The current Drive-JEPA AMC scripts use Adam through
`drive_jepa_agent.py:395-400` and explicit `clip_grad_norm_` in
`a3_5_phase2_amc_training.py:606-613` and
`a3_7_phase4_coverage_aware_amc.py:316-323`. Adam's coordinate-wise state and
scene batching mean the theorem is a mechanism hypothesis, not a direct proof
about the full Drive-JEPA optimizer.

该结果假设 normalized 或 clipped update 以及方向正交。当前 Drive-JEPA AMC
脚本在 `drive_jepa_agent.py:395-400` 使用 Adam，并在
`a3_5_phase2_amc_training.py:606-613` 与
`a3_7_phase4_coverage_aware_amc.py:316-323` 使用显式
`clip_grad_norm_`。但 Adam 的 coordinate-wise state 和 scene batching 意味着：
该定理是机制假设，不是对完整 Drive-JEPA optimizer 的直接证明。

### Required Measurement / 必须测量

Before upgrading this result:

在升级该结论前必须测量：

- per-scene gradient norm;
- 每个 scene 的 gradient norm；
- pairwise gradient cosine;
- 梯度两两 cosine；
- easy/medium/hard contribution share;
- easy/medium/hard contribution share；
- projection of total update onto hard-scene gradients;
- 总更新投影到 hard-scene gradients 的份额；
- Adam state and clipping statistics.
- Adam state 与 clipping 统计。

## 17.4 Link To A18-A19 / 与 A18-A19 的连接

A18 reports `K_eff down` together with affinity mass and edge participation up.
That pattern is compatible with more pairwise contraction pressure and potentially
more correlated redundancy gradients. A19's `S^4`-focused simulation reallocates
positive credit toward stronger edges, but it does not yet measure parameter-space
gradient SNR or task learning.

A18 报告了 `K_eff` 下降，同时 affinity mass 与 edge participation 上升。该
模式与更多 pairwise contraction pressure、以及潜在更高的冗余梯度相关性一致。
A19 的 `S^4`-focused simulation 把正向 credit 重新分配给更强 edge，但尚未测量
parameter-space gradient SNR 或 task learning。

## Claim Level / 结论等级

```text
THEOREM / PROPOSITION:
    exact under written covariance or update assumptions.
CONDITIONAL_RESULT:
    mechanism applies only when optimizer/update conditions hold.
EMPIRICAL_HYPOTHESIS:
    TA-AMC improves gradient SNR, information volume, and hard-scene share.
NOT_YET_SUPPORTED:
    these improvements cause better planning or task score.
```

