# 20 Diffusion Migration Math / Diffusion 迁移数学

Status: `TRANSFER_HYPOTHESIS__DECODER_SPECIFIC_GRADIENTS`

## Semantic Difference / 语义差异

Diffusion Policy-style models learn a conditional action distribution. `K`
usually means Monte-Carlo samples from the same condition, not persistent
decoder slots.

Diffusion Policy 类模型学习 conditional action distribution。`K` 通常表示
同一 condition 下的 Monte-Carlo samples，而不是持久 decoder slots。

Therefore the correct budget language is:

因此正确的 budget 语言是：

```text
probability mass
finite sample budget
Monte-Carlo gradient budget
inference latency
semantic mode coverage
```

not automatically:

而不是自动地说：

```text
persistent slot parameters are wasted
```

## One-Step Clean Estimate / 单步 clean estimate

For a forward process:

对于 forward process：

$$
x_t = \alpha_t x_0 + \sigma_t \epsilon.
$$

under epsilon prediction:

在 epsilon prediction 下：

$$
\hat{x}_{0,\theta}(x_t,t,c)
=
\frac{x_t-\sigma_t\epsilon_\theta(x_t,t,c)}{\alpha_t}.
$$

For `K` independent noises under one condition:

同一 condition 下使用 `K` 个独立噪声：

$$
\epsilon^{(1)},\ldots,\epsilon^{(K)}
\mapsto
\hat{x}_0^{(1)},\ldots,\hat{x}_0^{(K)}
\mapsto
A\in\mathbb{R}^{B\times K\times H\times D_a}.
$$

If `L_R` is applied to clean-action estimates:

如果 redundancy loss 作用于 clean-action estimates：

$$
\frac{\partial L_R}{\partial \theta}
=
\sum_{k=1}^{K}
\frac{\partial L_R}{\partial \hat{x}_0^{(k)}}
\left(-\frac{\sigma_t}{\alpha_t}\right)
\frac{\partial \epsilon_\theta^{(k)}}{\partial \theta}.
$$

This is a pathwise gradient only under the schedule and parameterization
assumptions above.

该 pathwise gradient 只在上述 schedule 与 parameterization 假设下成立。

## Three Migration Levels / 三个迁移等级

### Level 1: One-Step Proxy / Level 1：单步 proxy

Use `x0_hat` at sampled timesteps.

在采样 timestep 使用 `x0_hat`。

Measure:

测量：

- correlation with final-sample pair relation;
- 与 final-sample pair relation 的 correlation；
- bias across timestep;
- timestep 造成的 bias；
- gradient variance and memory.
- gradient variance 与 memory。

Status: `EXPERIMENTAL`.

状态：`EXPERIMENTAL`。

### Level 2: Truncated Differentiable Sampler / Level 2：截断可微 sampler

Backpropagate through a short suffix or a checkpointed subset of denoising
steps.

通过短 suffix 或 checkpointed denoising steps 反传。

Record:

记录：

```text
memory
runtime
gradient variance
proxy-to-endpoint relation bias
```

### Level 3: Full Differentiable Sampler / Level 3：完整可微 sampler

Backpropagate through:

通过以下完整路径反传：

$$
x_T \to x_{T-1}\to\cdots\to x_0.
$$

Costs include `O(T)` activation memory, Jacobian products, possible
exploding/vanishing gradients, and stochastic-path variance.

代价包括 `O(T)` activation memory、Jacobian product、可能的梯度爆炸/消失和
stochastic-path variance。

## Why AMC-v1 Cannot Be Copied / 为什么不能直接复制 AMC-v1

Attractive pairwise redundancy loss can increase concentration in
`p_theta(mode)`. By Theorem 1:

pairwise attraction 可能增加 `p_theta(mode)` 的集中程度。根据定理 1：

$$
\mathbb{E}[U_K]
=
\sum_m \left[1-(1-p_m)^K\right].
$$

concentration can lower finite-K unique semantic coverage. Thus a lower
latent-distance or lower `K_eff` score may indicate mode collapse rather than
better sample efficiency.

概率集中会降低有限 K 下的 unique semantic coverage。因此 latent distance 或
`K_eff` 下降可能意味着 mode collapse，而不是更高的 sample efficiency。

## Required Diffusion Gate / 必须通过的 Diffusion 门控

Do not define semantic redundancy directly on raw epsilon or velocity output
unless a domain proof justifies it. Use clean actions or final decoded
trajectories, then validate:

除非有领域证明，否则不要直接在 raw epsilon 或 velocity output 上定义 semantic
redundancy。应使用 clean actions 或最终 decoded trajectories，并验证：

1. proxy relation agrees with final endpoint relation;
2. proxy relation 与 final endpoint relation 一致；
3. coverage does not decrease beyond a predeclared budget;
4. coverage 不超过预注册预算地下降；
5. task loss remains finite;
6. task loss 保持有限；
7. decoder gradients are nonzero and frozen evaluator gradients are zero;
8. decoder gradients 非零且 frozen evaluator gradients 为零；
9. increasing `K_eff`-matching pressure does not simply collapse mode mass.
10. 增强 `K_eff` matching pressure 不会简单造成 mode mass collapse。

## Claim Boundary / 结论边界

```text
SUPPORTED:
    interface-level candidate extraction principle.
TRANSFER_HYPOTHESIS:
    one-step or endpoint redundancy feedback for diffusion.
NOT_SUPPORTED:
    unchanged Drive-JEPA AMC-v1 loss is automatically valid for diffusion.
```
