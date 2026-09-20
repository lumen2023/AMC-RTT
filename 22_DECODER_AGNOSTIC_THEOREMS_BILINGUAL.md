# 22 Decoder-Agnostic Theorems / Decoder-Agnostic 定理

Status: `THEORY_WITH_DECODER_BOUNDARIES`

The word “decoder-agnostic” applies to the interface and evidence protocol, not
to every mathematical loss or capacity interpretation.

“decoder-agnostic” 只适用于接口与证据协议，不适用于所有数学 loss 或容量解释。

## The Portable Core / 可迁移核心

The following composition is decoder-agnostic:

以下组合是 decoder-agnostic 的：

```text
decode
-> canonicalize [B,K,...]
-> task/action adapter
-> frozen consequence embedding
-> relation [B,K,K]
-> statistics
-> decoder-aware regularization policy
```

The final policy is decoder-aware because the meaning of `K` changes.

最后的 policy 必须 decoder-aware，因为 `K` 的含义会变化。

## Result Classification / 结论分类

| statement | label | scope |
| --- | --- | --- |
| finite-K coverage formula | `THEOREM` | IID semantic samples |
| multiplicity bias formula | `PROPOSITION` | equal slot/sample averaging |
| correlated-gradient `r_eff` | `THEOREM` | exchangeable covariance |
| Fisher volume comparison | `PROPOSITION` | local equal-energy vectors |
| complex-scene update share | `CONDITIONAL_RESULT` | normalized/clipped orthogonal update |
| slot Jacobian rank argument | `PROPOSITION` | persistent-slot decoder |
| TA-AMC improves task score | `EMPIRICAL_HYPOTHESIS` | requires matched experiment |
| MoE specialization analogy | `ANALOGY` | not direct action redundancy evidence |

## Decoder-Specific Meaning / Decoder-specific 含义

### Drive-JEPA / Drive-JEPA

Persistent proposals make slot/query freedom and output-Jacobian rank meaningful.

持久 proposals 使 slot/query freedom 与 output-Jacobian rank 具有明确意义。

### Diffusion / Diffusion

The main object is the conditional probability distribution and finite sample
coverage. A contraction loss can increase dominant-mode probability mass.

核心对象是 conditional probability distribution 与有限样本覆盖。contraction
loss 可能增加 dominant-mode probability mass。

### Flow Matching / Flow Matching

The main object is the probability transport induced by the vector field and
ODE flow map. Endpoint gradients can modify the full field.

核心对象是 vector field 与 ODE flow map 诱导的 probability transport。endpoint
gradient 可能改变整个 vector field。

## Counterexample To Universal Loss Reuse / 通用 loss 复用反例

Take two semantic modes with probabilities $p=(0.9,0.1)$ and $K=8$. If a
regularizer makes the distribution more concentrated toward $p'=(1,0)$, then:

考虑两个 semantic modes，概率 $p=(0.9,0.1)$，$K=8$。如果 regularizer 把
分布进一步集中到 $p'=(1,0)$：

$$
\mathbb{E}[U_8](p)
=
\left[1-(0.1)^8\right]
+
\left[1-(0.9)^8\right],
\qquad
\mathbb{E}[U_8](p')=1.
$$

The second mode becomes impossible, even though pairwise sample similarity may
look “cleaner”. Thus a lower redundancy statistic can be worse semantic sample
efficiency.

第二个 mode 会变得不可能，尽管 pairwise sample similarity 可能看起来更“干净”。
因此更低的 redundancy statistic 可能对应更差的 semantic sample efficiency。

## Applicability Matrix / 适用性矩阵

| result | Drive-JEPA | Diffusion | Flow Matching |
| --- | --- | --- | --- |
| finite-K coverage | conditional semantic audit | primary | primary |
| multiplicity bias | persistent slot weighting | MC sample weighting | base-noise weighting |
| gradient ESS | shared planner gradients | stochastic gradient budget | vector-field gradient budget |
| Fisher volume | slot/output Jacobian | local sample-gradient information | local flow sensitivity |
| complex-scene share | requires optimizer audit | requires sampler/training audit | requires ODE/optimizer audit |
| `K_eff` loss sign | candidate only, bounded | unsafe by default | unsafe by default |

## Final Theorem Boundary / 最终定理边界

No theorem in this package proves:

本包没有任何定理证明：

$$
\text{redundancy reduction}
\Rightarrow
\text{capacity efficiency}
\Rightarrow
\text{task improvement}.
$$

The package provides conditions, mechanisms, counterexamples, and experiments
that can either support or falsify those arrows.

本包提供条件、机制、反例与实验，使这些箭头能够被支持或证伪。
