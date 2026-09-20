# Pair Credit Assignment

Status: `EXPERIMENTAL_DIAGNOSTIC`

Pair credit assignment asks which candidate pairs receive contraction or
repulsion pressure from a redundancy objective.

## AMC-v1 Pair Weight

When:

```text
delta_K = log K_eff(pred) - stopgrad(log K_teacher)
```

and `delta_K > 0`, AMC-v1 contraction mass is proportional to:

```text
w_ij = S_ij^2
p_ij = w_ij / sum_{a<b} w_ab
```

This means all currently similar pairs get contraction pressure, including
cross-mode pairs if the metric already gives them nontrivial affinity.

## Diagnostic Fields

A19 compared:

```text
AMC-v1 K: p_ij proportional to S^2
K + 0.5 logE: blend of S^2 and S^4
S^4 focused: concentrated on stronger edges
signed concentration: can repel weak diffuse edges
high-conf abstain: diagnostic only
soft-same weighted: diagnostic only
hard-same high-conf oracle: diagnostic only
```

Teacher-relation fields are not deployable methods. They are upper-bound
diagnostics for the direction a mode-aware credit allocator would take.

## A19 Readout

Relative to AMC-v1, the `S^4` focused field:

```text
reduced different-hard-teacher contraction mass
reduced edge participation
increased top-edge concentration
```

This supports topology-aware design but does not authorize training.

## Transfer Use

For a new decoder, build the pair-credit table:

```text
i, j
distance
affinity
credit mass
teacher same/different if available
confidence bin if available
coverage impact if available
```

Then check whether the objective contracts many weak cross-pairs or a few
high-confidence redundant neighborhoods.

