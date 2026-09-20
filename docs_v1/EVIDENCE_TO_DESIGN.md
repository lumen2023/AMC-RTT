# Evidence To Design After A32 / A32 后证据到设计映射

Status: `MAINLINE_REFRAMED_AFTER_A32`

## One-Sentence Correction / 一句话纠偏

A32 does not invalidate multimodal de-redundancy. It invalidates the narrower
claim that the current Drive-JEPA final-layer base loss already provides dense
all-pair optimizer credit that AMC-RTT can simply decorrelate.

A32 没有否定多模态去冗余。它否定的是更窄的说法：当前 Drive-JEPA final-layer
base loss 已经提供 dense all-pair optimizer credit，AMC-RTT 只需去相关即可。

## Latest Evidence / 最新证据

| item | finding | design consequence |
| --- | --- | --- |
| A18 | $K_{\rm eff}$ reduction controls total squared affinity mass and can diffuse over many edges | scalar $K_{\rm eff}$ alone is not enough |
| A19 | $S^4$ / topology-concentrated fields reduce diffuse cross-mode contraction in read-only simulation | topology-aware credit is the deployable direction |
| A20 | $L_K+\alpha L_{\rm topo}$ has a clean non-oracle mathematical design | preserve this core as the main route |
| A26 | selected topology-activated cohort shows conditional matched-development signal, but no independent confirmation | keep the mechanism, do not overclaim |
| A30 | all-layer fold reconnects final-layer gradients under small batches | base loss contract bug must be separated from AMC |
| A31 | repaired final-proposal all-pair gradient redundancy is not supported | stop optimizer-credit redundancy framing |
| A32 | active gradient rows match WTA winner set; median active rows $=5/32$ | base loss is sparse WTA specialization; AMC-RTT should regulate whole-set topology |

## Mainline Now / 当前主线

$$
\boxed{
\text{base WTA supervision}
\Rightarrow
\text{sparse winner specialization}
}
$$

and separately:

$$
\boxed{
\text{AMC-RTT}
\Rightarrow
\text{whole-set consequence-topology regularization}
}
$$

Do not merge these two roles. The base loss covers known targets through sparse
winner credit. AMC-RTT shapes the full generated set so finite multimodal
capacity is not repeatedly spent on consequence-equivalent hypotheses.

不要混淆这两个角色。base loss 通过稀疏 winner credit 覆盖已知 target；
AMC-RTT 塑造整组 generated set，使有限多模态容量不反复花在后果等价的 hypotheses
上。

## Serious Corrections / 必须严肃纠正的错误

### Error 1: "A32 means AMC motivation is false"

This is wrong. A32 shows that final trajectory credit is sparse because the loss
has a winner-take-min structure. It says little about whether the inactive
non-winner hypotheses are consequence-redundant or whether whole-set topology is
useful.

### Error 2: "Gradient redundancy remains the central object"

This is now wrong for the Drive-JEPA final proposal layer under A31/A32. The
central object must be consequence topology:

$$
\{\tau_i\}_{i=1}^K
\xrightarrow{\Phi_{\rm AC}}
\{h_i\}_{i=1}^K
\xrightarrow{\text{pair moments}}
(\mu_1,\mu_2,\rho,K_{\rm eff}^{\rm ref}).
$$

### Error 3: "DM/FM can reuse Drive-JEPA loss unchanged"

This is wrong because $K$ has different semantics. Static Drive-JEPA has
persistent slots. DM/FM often have stochastic samples or particles. The shared
object is the clean hypothesis set, not the native noise/score/velocity.

## Current Progress / 当前进度

Done in v1:

- generator-independent math core implemented;
- $K_{\rm eff}$ pair-density identity tested;
- $\rho=\mu_1^2/\mu_2$ topology identity tested;
- analytic $\partial\log\rho/\partial q_e$ tested against autograd;
- DM epsilon/x0/v clean endpoint adapters tested;
- FM linear endpoint adapter tested;
- same-time/cross-hypothesis invariant tested.

Next:

1. Drive-JEPA static replay parity against legacy persisted records;
2. DM contract smoke on a real or toy diffusion policy;
3. FM contract smoke on a real or toy flow-matching policy;
4. only then consider tiny training.
