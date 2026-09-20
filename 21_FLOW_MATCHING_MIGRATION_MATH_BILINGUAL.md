# 21 Flow Matching Migration Math / Flow Matching 迁移数学

Status: `TRANSFER_HYPOTHESIS__ODE_SENSITIVITY`

## Endpoint Generator / Endpoint generator

Flow Matching uses a learned vector field:

Flow Matching 学习 vector field：

```text
dx_t / dt = v_theta(x_t,t,c)
```

For `K` base samples:

对于 `K` 个 base samples：

```text
x_0^(k) ~ p0
x_1^(k) = Phi_theta(x_0^(k), c)
```

where `Phi_theta` is the numerical ODE flow map.

其中 `Phi_theta` 是数值 ODE flow map。

The canonical endpoint tensor is:

endpoint canonical tensor：

```text
[B,K,H,A]
```

## Parameter Sensitivity / 参数敏感度

Let:

令：

```text
S_t = d x_t / d theta
```

Differentiating the ODE:

对 ODE 求导：

```text
d S_t / dt
 = [d v_theta / d x] S_t
   + d v_theta / d theta
```

Therefore a terminal redundancy loss affects the entire velocity field through
the ODE dynamics, not just a final decoder head.

因此 terminal redundancy loss 会通过 ODE dynamics 作用于整个 velocity field，
而不是只作用于最终 decoder head。

## Solver Modes / Solver 模式

### Direct Backpropagation / 直接反传

Differentiate through the full numerical solver.

通过完整数值 solver 反传。

Record:

记录：

- solver steps;
- solver steps；
- memory and checkpointing;
- memory 与 checkpointing；
- gradient stiffness;
- gradient stiffness；
- endpoint discretization error.
- endpoint discretization error。

### Adjoint / Adjoint 反传

Adjoint can reduce activation storage but introduces its own numerical
approximation and backward-solver behavior. It must be audited rather than
treated as mathematically identical to direct backpropagation.

Adjoint 可以降低 activation storage，但有自己的数值近似与 backward-solver
行为。不能默认它与 direct backpropagation 完全等价。

### Truncated Or Checkpointed Solver / 截断或 checkpointed solver

This is a transfer proxy. Its relation to the full endpoint must be measured on
scene/sample units before training claims.

这是 transfer proxy。必须在 scene/sample 单位上测量其与 full endpoint 的关系，
之后才能形成训练结论。

## Linear-Path Proxy / Linear-flow path proxy

For a linear path:

对于 linear path：

```text
x_t = (1-t)x_0 + t x_1
u_t = x_1 - x_0
```

if the implementation predicts `u_t` with the same orientation, one can form:

如果实现以相同 orientation 预测 `u_t`，可以构造：

```text
x1_hat = x_t + (1-t) v_theta(x_t,t,c)
```

This proxy is valid only for the stated path orientation and parameterization.
Some implementations reverse the time endpoints; the adapter must read the
actual implementation instead of assuming `t=0` is noise.

该 proxy 只在指定 path orientation 与 parameterization 下成立。不同实现可能反转
time endpoints；adapter 必须读取真实实现，不能假设 `t=0` 一定是 noise。

## Proxy Agreement Gate / Proxy 一致性门控

Before using a proxy relation:

使用 proxy relation 前必须验证：

```text
Corr(proxy pair relation, full endpoint pair relation)
Corr(proxy K_eff, full endpoint K_eff)
scene-level rank correlation
mode-coverage agreement
```

The minimum gate should be predeclared on calibration data and evaluated on
held-out scenes.

最小门控应在 calibration data 上预注册，并在 held-out scenes 上评估。

## Why FM Is Not Fixed-Slot AMC / 为什么 FM 不是 fixed-slot AMC

FM samples are trajectories through a learned vector field. Pair attraction at
the endpoint can alter the vector field globally through the sensitivity ODE.
This can change probability transport, not merely consolidate persistent
queries.

FM samples 是穿过 learned vector field 的 trajectories。endpoint pair attraction
会通过 sensitivity ODE 全局改变 vector field，改变 probability transport，而不
只是合并持久 query。

## Claim Boundary / 结论边界

```text
SUPPORTED:
    endpoint candidates can enter the shared relation API.
TRANSFER_HYPOTHESIS:
    differentiable endpoint or proxy feedback can train FM decoders.
NOT_SUPPORTED:
    fixed-slot capacity language or unchanged AMC-v1 loss transfers automatically.
```

