# AMC-RTT v1.0

AMC-RTT is a theory, implementation, transfer, and evidence package for
redundancy-aware multimodal generation. Its central principle is simple:

```text
Do not let a finite multimodal decoder spend its modeling, sampling, and
optimization budget repeatedly representing the same future.
```

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

```text
K_generated = K
K_effective <= K
```

The goal is to convert generated multimodality into effective multimodality by
reducing repeated hypotheses while preserving useful semantic support.

![K generated versus K effective](figures/fig2_keff_intuition.svg)

## Core Mechanism

```text
multimodal redundancy
-> redundant modeling / sampling / optimization freedom
-> redundancy-aware gradient credit assignment
-> better effective capacity allocation
-> better task learning
```

The strongest proof route combines:

```text
gradient redundancy down
AND gradient effective rank or logdet up
AND hard-scene update share up
AND task score up
=> CAPACITY_EFFICIENCY_SUPPORTED
```

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

## Current Status

```text
MECHANISM_SUPPORTED__CAPACITY_EFFICIENCY_PROOF_ACTIVE
```

The Drive-JEPA high-score anchor and mechanism evidence make AMC-RTT ready for
active transfer. The proof program defines the efficient path from mechanism
evidence to capacity-efficiency and task-score evidence.
