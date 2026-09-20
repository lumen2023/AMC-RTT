# 10 Diffusion Decoder Adapter

Status: `TRANSFER_HYPOTHESIS`

Diffusion decoders can be adapted because they ultimately emit candidate
trajectories or actions.

## Candidate Generation

For the same context `c`, sample `K` independent noise seeds:

```text
epsilon_1, ..., epsilon_K ~ N(0,I)
y_k = DiffusionDecode_theta(c, epsilon_k)
Y = stack_k y_k
```

Then use the shared pipeline:

```text
Y
-> task/action adapter
-> frozen consequence encoder
-> S
-> K_eff
-> AMC loss
```

## Mode A: Faithful Endpoint Mode

Run the full differentiable denoising chain to final clean candidates:

```text
epsilon_k -> denoising solver -> y_k
```

Advantages:

- closest to actual generated outputs;
- easiest to interpret.

Costs:

- high memory;
- high compute;
- solver differentiability concerns in some implementations.

## Mode B: Predicted-Clean Proxy Mode

At a sampled diffusion timestep, use predicted clean trajectory estimates:

```text
x0_hat_theta(x_t, t, c)
```

This is only `TRANSFER_HYPOTHESIS`. It must be validated against full endpoint
redundancy before training claims.

## Loss Composition

Do not replace the diffusion objective:

```text
L_total = L_diffusion + lambda * L_AMC
```

## Required Validation

Before claiming diffusion transfer:

1. Level 0 no-training redundancy audit.
2. Level 1 gradient smoke: decoder gradients nonzero, frozen evaluator grads
   zero.
3. Level 2 tiny optimization changes redundancy metrics without catastrophic
   coverage loss.
4. Matched baseline training.
5. External task validation.

