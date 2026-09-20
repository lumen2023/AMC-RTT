# 00 Problem And Universal Interface

Status: `SUPPORTED_DESIGN_BOUNDARY`

## Problem

Many modern policies and trajectory decoders output a fixed or overcomplete
candidate set:

```text
Y = {y_1, ..., y_K}
```

But:

```text
K_generated = K
K_effective <= K
```

The toolkit studies how much of the candidate set represents genuinely distinct
task-relevant futures and how much is redundant modeling freedom.

## Universal Generator

Every decoder is reduced to:

```text
xi_k ~ p0
y_k = G_theta(c, xi_k)
Y = stack_k y_k
```

`G_theta` may be:

- proposal decoder;
- diffusion decoder;
- flow-matching decoder;
- autoregressive sampler;
- mixture model;
- query-based decoder.

AMC-RTT does not study where multimodality comes from. It studies the effective
structure of the decoded candidates.

## Tensor Contract

Required:

```text
context: C
decoded candidates: Y in R^[B,K,T,D_y]
```

Optional:

```text
actions: A in R^[B,K,H,D_a]
teacher candidates: T_teacher in R^[B,M,T,D_y]
```

Frozen consequence representation:

```text
Z = F_frozen(C, A or Y)
```

Pairwise dissimilarity and similarity:

```text
D in R^[B,K,K]
S in R^[B,K,K]
```

`S_ij` should be high when two candidates are consequence-redundant under the
chosen frozen evaluator.

## Decoder-Agnostic Rule

The redundancy module must not depend on:

- diffusion noise values;
- flow-matching initial noise;
- proposal query identity;
- sampling seed identity;
- teacher-source implementation details.

Those variables may be useful for debugging, but the generic AMC interface
starts after candidates are decoded.

## Three Reusable Interfaces

```text
CandidateDecoderAdapter.decode_candidates(context, num_candidates) -> Y
TaskRepresentationAdapter.to_actions(context, Y) -> A
FrozenConsequenceEncoder.encode(context, A or Y) -> Z
```

Once `Z` is available, the rest of the pipeline is shared:

```text
SimilarityMetric(Z) -> D, S
EffectiveMultimodalityEstimator(S) -> K_eff
RedundancyRegularizer(K_eff_pred, K_eff_teacher) -> L_red
RedundancyDiagnostics(Y, Z, S, teachers) -> report
```

