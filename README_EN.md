# AMC-RTT v1.0

AMC-RTT is a theory, implementation, transfer, and evidence package for
redundancy-aware multimodal generation. Its central principle is simple:

Do not let a finite multimodal decoder spend its modeling, sampling, and
optimization budget repeatedly representing the same future.

## High-Score Anchor

On top of Drive-JEPA, the AMC-Drive de-redundancy implementation reaches:

```text
NAVSIM v1 PDMS = 0.939443730121 ~= 93.944 ~= 93.95
```

This is a local single-RTX-3090 / fixcache fine-tuning lineage. See
[evidence/DRIVE_JEPA_93_95_ANCHOR.md](evidence/DRIVE_JEPA_93_95_ANCHOR.md).

![Drive-JEPA high-score anchor](figures/fig1_high_score_anchor.svg)

## Why Redundancy Matters

Modern multimodal decoders often expose a fixed budget:

$$
K_{\mathrm{generated}} = K,
\qquad
K_{\mathrm{effective}} \le K .
$$

The goal is to convert generated multimodality into effective multimodality by
reducing repeated hypotheses while preserving useful semantic support.

![K generated versus K effective](figures/fig2_keff_intuition.svg)

## Core Mechanism

$$
\text{multimodal redundancy}
\Rightarrow
\text{repeated modeling/sampling/optimization freedom}
\Rightarrow
\text{redundancy-aware credit assignment}
\Rightarrow
\text{better effective capacity allocation}
\Rightarrow
\text{better task learning}.
$$

The strongest proof route combines:

$$
\text{gradient redundancy}\downarrow
\quad\land\quad
\operatorname{erank}(G_{\mathrm{grad}})\uparrow
\ \text{or}\
\log\det(I+\lambda F)\uparrow
\quad\land\quad
\text{hard-scene update share}\uparrow
\quad\land\quad
\text{task score}\uparrow .
$$

Detailed derivations and literature anchors are in
[28_POSITIVE_MATH_PROOF_AND_LITERATURE_BILINGUAL.md](28_POSITIVE_MATH_PROOF_AND_LITERATURE_BILINGUAL.md).

## Proof Backbone

The positive argument is not a slogan. It is a chain of local results with
explicit assumptions:

1. finite-$K$ coverage:

$$
\mathbb{E}[U_K]
=
\sum_{m=1}^{M}\left[1-(1-p_m)^K\right];
$$

2. correlated-gradient effective sample size:

$$
r_{\mathrm{eff}}
=
\frac{r}{1+(r-1)\rho_g};
$$

3. local information volume:

$$
\log(1+\lambda r a^2)
<
r\log(1+\lambda a^2)
\qquad(r>1);
$$

4. normalized/clipped hard-direction share:

$$
\left|
\left\langle
\Delta\theta,
\frac{v}{\lVert v\rVert}
\right\rangle
\right|
=
\eta G
\frac{\lVert v\rVert}
{\sqrt{r^2\lVert u\rVert^2+\lVert v\rVert^2}}.
$$

The first three are mathematical mechanisms; the task-score step remains an
empirical proof obligation. That boundary is intentional.

## Decoder Transfer

AMC-RTT is decoder-agnostic at the interface level and decoder-aware at the
optimization level:

```text
decode
-> canonicalize [B,K,...]
-> task/action adapter
-> frozen consequence encoder
-> relation S[B,K,K]
-> statistics
-> decoder-aware regularization policy
-> Level 0-4 validation protocol
```

![Decoder-agnostic migration pipeline](figures/fig4_decoder_transfer_pipeline.svg)

Diffusion and Flow Matching are promising extensions when the regularizer is
support-preserving and sample-efficiency aware.

## Mathematical Figures

- [fig1_high_score_anchor.svg](figures/fig1_high_score_anchor.svg)
- [fig2_keff_intuition.svg](figures/fig2_keff_intuition.svg)
- [fig3_credit_assignment.svg](figures/fig3_credit_assignment.svg)
- [fig4_decoder_transfer_pipeline.svg](figures/fig4_decoder_transfer_pipeline.svg)

The editable FigureSpec sources are in [figures/specs](figures/specs).

## Entry Points

- [README.md](README.md): bilingual main README.
- [README_CN.md](README_CN.md): Chinese README.
- [MANIFEST.md](MANIFEST.md): file map and claim levels.
- [interfaces/redundancy_api.py](interfaces/redundancy_api.py): standalone
  decoder-agnostic API.
- [27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md](27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md):
  proof program for capacity efficiency and task improvement.
- [28_POSITIVE_MATH_PROOF_AND_LITERATURE_BILINGUAL.md](28_POSITIVE_MATH_PROOF_AND_LITERATURE_BILINGUAL.md):
  rendered derivations and authoritative literature anchors.

## Current Status

Current status: `MECHANISM_SUPPORTED__CAPACITY_EFFICIENCY_PROOF_ACTIVE`.

The Drive-JEPA high-score anchor and mechanism evidence make AMC-RTT ready for
active transfer. The proof program defines the efficient path from mechanism
evidence to capacity-efficiency and task-score evidence.
