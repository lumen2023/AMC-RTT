# DM/FM Adaptation / Diffusion 与 Flow Matching 适配

Status: `CLEAN_ENDPOINT_ADAPTERS_TESTED_SYNTHETICALLY`

## 1. Shared Principle / 共享原则

AMC-RTT is generator-agnostic only after clean hypotheses exist:

$$
\boxed{
\text{native state}
\rightarrow
\text{clean trajectory hypothesis}
\rightarrow
\Phi_{\rm AC}
\rightarrow
S_{ij}.
}
$$

It is wrong to compare native diffusion noise, score, or flow velocity vectors
directly as multimodal consequence redundancy.

## 2. Hard Axis Invariant / 轴不变量

Hypothesis axis:

$$
i=1,\ldots,K.
$$

Generative-time axis:

$$
t.
$$

AMC-RTT computes topology across different hypotheses at the same generative
time:

$$
\boxed{
S_{ij}(t),\quad i\ne j,\quad t\text{ fixed}.
}
$$

It must not compute $S(t_1,t_2)$ and call that multimodal redundancy.

## 3. Diffusion Adapter / Diffusion 适配

Assume:

$$
x_t=\alpha_t x_0+\sigma_t\epsilon.
$$

### epsilon prediction

If the model predicts $\hat\epsilon_\theta$:

$$
\boxed{
\hat x_0
=
\frac{x_t-\sigma_t\hat\epsilon_\theta}{\alpha_t}.
}
$$

Gradient scale:

$$
\frac{\partial \hat x_0}{\partial\hat\epsilon_\theta}
=
-\frac{\sigma_t}{\alpha_t}I.
$$

So high-noise regions with $\alpha_t\to0$ can amplify AMC gradients. v1 does
not invent a complex schedule; it requires a configured SNR/time window and
records the AMC/native gradient ratio.

### x0 prediction

If the model directly predicts $\hat x_0$, the adapter returns $\hat x_0$.

### v prediction

Under the common convention $\alpha_t^2+\sigma_t^2=1$ and
$v=\alpha_t\epsilon-\sigma_t x_0$:

$$
\boxed{
\hat x_0
=
\alpha_t x_t-\sigma_t\hat v_\theta.
}
$$

### Anchor diffusion metadata

Anchor/truncated diffusion planners must preserve:

```text
hypothesis_id
anchor_id
noise_seed
generation_time
```

Without this metadata, repeated samples from one anchor can be mistaken for
independent semantic modes.

## 4. Flow-Matching Adapter / Flow Matching 适配

For a linear conditional flow path:

$$
x_t=(1-t)x_0+t x_1,
\qquad
u=x_1-x_0.
$$

If the model predicts $v_\theta(x_t,t,c)$, v1 uses:

$$
\boxed{
\hat x_1
=
x_t+(1-t)v_\theta(x_t,t,c).
}
$$

Under the oracle field $v_\theta=u$:

$$
x_t+(1-t)(x_1-x_0)
=(1-t)x_0+t x_1+(1-t)x_1-(1-t)x_0
=x_1.
$$

Gradient scale:

$$
\boxed{
\frac{\partial \hat x_1}{\partial v_\theta}
=(1-t)I.
}
$$

This differs from epsilon-DM: near the endpoint, FM gradients naturally shrink.
Therefore DM/FM can share the consequence-topology objective but not the same
native-time weighting rule.

## 5. Decision Rules / 决策规则

| case | decision |
| --- | --- |
| static replay parity fails | stop DM/FM work; fix core parity |
| DM adapter fails | localize prediction convention/time conditioning; keep AMC core fixed |
| FM adapter fails | localize path convention/endpoint reconstruction; keep AMC core fixed |
| DM/FM adapters pass but native loss conflicts | study time window/schedule, not a new topology objective |

## 6. Authoritative Anchors / 权威依据

- Diffusion Policy supports action diffusion for high-dimensional multimodal
  control.
- DiffusionDrive motivates truncated / anchor-based diffusion for autonomous
  driving planners.
- Flow Matching establishes the vector-field probability-path formulation.
- Streaming Flow Policy supports flow-matching policies over action trajectories.

The shared conclusion is not that one loss can be blindly reused. The shared
conclusion is:

$$
\boxed{
\text{different generators need different clean-endpoint adapters, then the
same consequence-topology core can apply.}
}
$$
