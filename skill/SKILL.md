# Redundancy-Aware Multimodal Generation Transfer

Use this skill when a model outputs multiple trajectories, actions, futures, or
plans and the user suspects redundant hypotheses in a fixed-K or stochastic
multimodal decoder.

Applicable decoders:

- proposal decoder;
- diffusion decoder;
- flow-matching decoder;
- autoregressive sampler;
- mixture model;
- query-based decoder.

Do not use this skill to claim universal generality before external
diffusion/flow-matching validation.

## Step 1: Identify Candidate Tensor

Input:

```text
context c
candidates Y [B,K,T,D]
optional actions A [B,K,H,D_a]
```

Output:

```text
CandidateBatch
```

Pass gate:

```text
shape and candidate semantics are known
```

Fail gate:

```text
K dimension is ambiguous or candidate identities are mixed with batch/time
```

Next action: fix the adapter before computing redundancy.

## Step 2: Geometry Baseline

Math:

```text
d_G(i,j) = ADE/FDE/action_L2/trajectory_L2
R_G(i,j) = 1[d_G(i,j) <= epsilon]
```

Output:

```text
geometry redundancy table
```

Pass gate:

```text
geometry duplicate structure is measurable
```

Fail gate:

```text
candidate units or coordinate frames are inconsistent
```

## Step 3: Optional Geometry Plus Outcome Diagnostic

Input:

```text
task score J(y,c)
```

Math:

```text
GeometryOutcomeRelation = geometry closeness + outcome similarity
```

Pass gate:

```text
task score is held fixed and not tuned on test data
```

Fail gate:

```text
score is unavailable, unstable, or training-leaky
```

Next action: skip to frozen consequence encoder if available.

## Step 4: Build Frozen Consequence Encoder Adapter

Input:

```text
context
candidates or actions
```

Output:

```text
Z = F_frozen(context, candidates/actions)
```

Pass gate:

```text
frozen evaluator parameter grads are zero
candidate/action grads are preserved when training is intended
```

Fail gate:

```text
input gradients are detached or evaluator parameters receive grads
```

## Step 5: Gradient Smoke

Math:

```text
Z -> S -> K_eff -> scalar backward
```

Pass gate:

```text
finite scalar
finite nonzero candidate gradients
zero frozen-evaluator parameter gradients
```

Fail gate:

```text
NaN, OOM, zero candidate grad, nonzero frozen parameter grad
```

## Step 6: Build Similarity And K_eff

Math:

```text
S_ij = exp(-(d_ij/tau)^2)
K_eff = (tr S)^2 / tr(S^2)
```

Output:

```text
K_eff
affinity mass
edge participation
row effective neighbor count
```

Pass gate:

```text
tau provenance is fixed and diagnostics are finite
```

Fail gate:

```text
tau tuned on held-out data or K_eff reported alone
```

## Step 7: No-Training Redundancy Audit

Output:

```text
geometry metrics
latent metrics
topology metrics
coverage/task metrics
known failure flags
```

Pass gate:

```text
redundancy is real and not a tensor/schema artifact
```

## Step 8: Tiny AMC Training

Math:

```text
L_AMC = (log K_eff_pred - stopgrad(log K_eff_teacher))^2
L_total = L_task + lambda * L_AMC
```

Pass gate:

```text
base loss finite
K_eff can move
coverage not catastrophic
frozen evaluator remains frozen
```

Fail gate:

```text
collapse, NaN/OOM, frozen-boundary violation, base loss explosion
```

## Step 9: Coverage, Collapse, And Topology Gates

Required metrics:

```text
coverage
task score
within/cross affinity
edge participation
row effective neighbors
same/different mode contraction if labels exist
```

Pass gate:

```text
K_eff movement is not caused by diffuse false-merge smoothing
```

## Step 10: Matched Baseline

Compare:

```text
baseline
baseline + AMC
```

Keep everything else matched.

Pass gate:

```text
redundancy improves without violating task/coverage gates
```

## Step 11: Task-Performance Claim

Only claim task improvement after external task metrics improve under matched
baseline evaluation.

## Adapter Templates

Proposal decoder:

```text
proposal_decoder(context) -> Y [B,K,T,D]
to_actions(Y) -> A
F_frozen(context,A) -> Z
```

Diffusion decoder:

```text
epsilon_k ~ N(0,I)
DiffusionDecode(context, epsilon_k) -> y_k
Y -> shared AMC pipeline
```

Flow-matching decoder:

```text
x0_k ~ p0
integrate dx/dt = v_theta(x,t,context)
y_k = x_k(1)
Y -> shared AMC pipeline
```

## Claim Guard

Always check:

- redundancy is not confused with diversity;
- `K_eff` decrease is not claimed as performance improvement;
- diagnostic targets are not presented as deployed methods;
- teacher-side leakage is not counted as model support;
- A14 rich-support interpretation is marked superseded by A15-A17;
- cross-decoder generality is not claimed before DM/FM validation.

