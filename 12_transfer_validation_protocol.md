# 12 Transfer Validation Protocol

Status: `REQUIRED_PROTOCOL`

Use this protocol before claiming AMC-RTT works in a new decoder family.

## Level 0: No-Training Redundancy Audit

Inputs:

```text
context batch
candidate tensor [B,K,T,D]
optional teacher candidates
optional frozen evaluator
```

Report:

- geometry redundancy;
- latent redundancy;
- `K_eff`;
- topology diagnostics;
- coverage;
- task score.

Pass gate:

```text
redundancy is measurable and not a schema artifact
```

## Level 1: Gradient Smoke

Verify:

```text
grad decoder candidates != 0
grad frozen evaluator parameters == 0
loss finite
no NaN/OOM/schema mismatch
```

Fail action: stop and fix adapter or freeze boundary.

## Level 2: Tiny Optimization

Run a tiny, bounded optimization.

Pass gate:

```text
redundancy metric can move
base loss finite
coverage not catastrophic
frozen evaluator remains frozen
```

## Level 3: Matched Baseline Training

Compare:

```text
baseline
baseline + AMC
```

Keep architecture, data, schedule, and randomization matched except the
redundancy term.

## Level 4: External Task Validation

The final gate is task performance:

```text
success / reward / planning score / safety / held-out task metric
```

Do not claim success from `K_eff` movement alone.

## Cross-Decoder Generality

Required before writing `cross-decoder generality supported`:

```text
1 Drive-JEPA / driving validation
1 diffusion decoder validation
1 flow-matching decoder validation
```

Before that, write:

```text
decoder-agnostic design / transfer hypothesis
```

