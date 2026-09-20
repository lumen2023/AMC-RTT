# 16 Redundancy Capacity Theory / 冗余与容量理论

Status: `THEORETICAL_FOUNDATION`

This file separates mathematical results from empirical hypotheses. A result
label applies only under the assumptions written beside it.

本文件严格区分数学结果与经验假设。每个结论标签只在其列出的假设下成立。

## 16.1 Finite-K Semantic Coverage

### THEOREM 1 / 定理 1

Assume a condition has `M` semantic modes with probabilities
`p_1,...,p_M`, and `K` samples are IID semantic labels.

假设一个 condition 有 `M` 个 semantic modes，概率为 `p_1,...,p_M`，并且
`K` 个样本的 semantic labels IID。

Let `U_K` be the number of unique modes observed:

令 `U_K` 表示实际覆盖到的 unique modes 数量：

```text
E[U_K] = sum_m [1 - (1-p_m)^K]
E[R_K] = K - E[U_K]
P(mode m is missed) = (1-p_m)^K
```

### Derivation / 推导

Let `I_m` indicate that mode `m` appears at least once. Then:

令 `I_m` 表示 mode `m` 至少出现一次，则：

```text
U_K = sum_m I_m
E[I_m] = 1 - P(no sample has mode m)
       = 1 - (1-p_m)^K
```

Linearity of expectation gives the result without requiring independence between
the indicators.

利用期望线性性即可得到结果，不需要不同 `I_m` 之间相互独立。

### Schur-Concavity / Schur 凹性

For `K >= 2`:

当 `K >= 2`：

```text
f(p) = 1 - (1-p)^K
f''(p) = -K(K-1)(1-p)^(K-2) <= 0
```

Thus `sum_m f(p_m)` is symmetric concave, hence Schur-concave on the probability
simplex. More concentrated mode mass lowers expected unique coverage at fixed
`K`, while a more balanced distribution raises it.

因此 `sum_m f(p_m)` 在概率单纯形上是 symmetric concave、也就是
Schur-concave。固定 `K` 时，概率质量越集中，期望 unique coverage 越低；
概率越均衡，期望 unique coverage 越高。

### Counterexample / 反例

This theorem does not apply if:

该定理不适用于：

- samples are not IID;
- 样本不是 IID；
- the semantic partition is wrong or merges distinct modes;
- semantic partition 本身错误或把不同 mode 合并；
- the decoder is intentionally conditional on a coverage policy;
- decoder 有意遵循一个 coverage policy；
- `K_eff` is used as a proxy without a valid semantic evaluator.
- 没有有效 semantic evaluator 却直接使用 `K_eff` proxy。

### Applicability / 适用性

| system | interpretation |
| --- | --- |
| Drive-JEPA | conditional only if persistent proposal outputs can be mapped to semantic modes |
| Diffusion | directly relevant to finite stochastic sample coverage |
| Flow Matching | relevant to finite base-noise sample coverage |

## 16.2 Gradient Multiplicity Bias

### PROPOSITION 2 / 命题 2

Assume mode `m` is represented by `r_m` hypotheses, `sum_m r_m = K`, and each
hypothesis has expected shared-parameter gradient `mu_m`. If the loss averages
slot/sample contributions equally:

假设 mode `m` 被 `r_m` 个 hypotheses 表示，`sum_m r_m=K`，且每个 hypothesis
对共享参数的期望梯度是 `mu_m`。如果 loss 对 slot/sample 等权平均：

```text
E[g] = sum_m (r_m / K) mu_m
```

For a desired semantic weighting `pi_m`:

若理想 semantic weighting 是 `pi_m`：

```text
g* = sum_m pi_m mu_m
b  = E[g] - g*
   = sum_m (r_m/K - pi_m) mu_m
```

### Assumptions / 假设

- equal contribution weights;
- 等权贡献；
- a meaningful semantic partition;
- 有意义的 semantic partition；
- `mu_m` is stable over the local update;
- 局部更新内 `mu_m` 稳定。

If the `mu_m` are linearly independent, `b=0` requires
`r_m/K = pi_m` for every mode.

如果 `mu_m` 线性独立，则 `b=0` 要求每个 mode 都满足
`r_m/K = pi_m`。

### Counterexample / 反例

If all `mu_m` are equal, duplication changes the count but not the expected
gradient direction. Therefore the proposition is about semantic weighting bias,
not a universal claim that every duplicate changes optimization.

如果所有 `mu_m` 都相同，重复数量会改变计数但不改变期望梯度方向。因此该命题
描述的是 semantic weighting bias，不是“任何重复都会改变优化”的普遍定理。

### Applicability / 适用性

| system | correct reading |
| --- | --- |
| Drive-JEPA | persistent proposals can alter shared planner gradient weighting |
| Diffusion | sample averaging can bias Monte-Carlo gradient estimates toward dominant modes |
| Flow Matching | base-noise samples can bias vector-field updates toward repeatedly observed regions |

## 16.3 Persistent-Slot Jacobian Rank

### PROPOSITION 3 / 命题 3

For a fixed-slot decoder with outputs `y_k(theta)`, define:

对于 fixed-slot decoder 的输出 `y_k(theta)`，定义：

```text
J_k = d y_k / d theta
J = [J_1; ...; J_K]
```

If several slot Jacobians are identical, the row-space of `J` contains fewer
independent output directions than `K` distinct Jacobians. A spectral effective
rank of `J J^T` therefore decreases or stays unchanged.

如果多个 slot Jacobian 相同，`J` 的 row-space 中独立输出方向少于 `K` 个不同
Jacobian。于是 `J J^T` 的谱有效秩下降或不变。

### Counterexample / 反例

Similar outputs do not imply similar Jacobians. Two slots may currently produce
nearby trajectories while retaining different local sensitivity. Output
redundancy is therefore not by itself proof of parameter or slot redundancy.

相似输出不等于相似 Jacobian。两个 slot 当前可能产生接近轨迹，但局部 sensitivity
仍然不同。因此输出冗余本身不能证明参数或 slot 冗余。

### Applicability / 适用性

This argument is appropriate for persistent-slot Drive-JEPA, but not as a direct
claim that diffusion/FM parameters are wasted by duplicate samples. For
diffusion/FM, use finite sample coverage, probability mass, and gradient
Monte-Carlo information instead.

该论证适用于持久 slot 的 Drive-JEPA，但不能直接说 diffusion/FM 参数因重复样本
而浪费。对 diffusion/FM 应转而研究有限样本覆盖、概率质量和 gradient
Monte-Carlo information。

## Summary / 总结

The theory establishes mechanisms under assumptions. It does not establish the
causal chain to task improvement. That requires the experiment program in
[27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md](27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md).

这些理论在明确假设下建立机制，但没有建立到 task improvement 的因果链。后者需要
[27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md](27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md)
中的实验程序。

