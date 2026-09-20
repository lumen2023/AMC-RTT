# 11 Flow Matching Decoder Adapter

Status: `TRANSFER_HYPOTHESIS`

Flow matching decoders can be adapted through endpoint candidates.

## Candidate Generation

For each candidate:

```text
x0_k ~ p0
dx/dt = v_theta(x,t,c)
y_k = x_k(1)
Y = stack_k y_k
```

Then use the same redundancy pipeline:

```text
Y
-> task/action adapter
-> frozen consequence encoder
-> S
-> K_eff
-> AMC
```

## Mode A: Differentiable Endpoint Integration

Integrate the ODE with gradients through the solver:

```text
x0_k -> ODE solver -> y_k
```

This is the faithful mode and should be the first validation target if memory
allows.

## Mode B: Endpoint Estimate Or Short-Solver Proxy

Use an endpoint estimate or a reduced-step solver during training.

Status:

```text
EXPERIMENTAL
```

It can only become a method after showing high agreement with full endpoint
redundancy relations.

## Loss Composition

Do not alter the conditional path definition:

```text
L_total = L_flow_matching + lambda * L_AMC
```

## Validation Rule

Flow-matching transfer is not supported until the Level 0-4 validation protocol
passes on at least one FM task.

