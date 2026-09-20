# 04 Frozen Consequence Encoder

Status: `SUPPORTED_FOR_GRADIENT_PATH`

The central reusable interface is a frozen task-aware consequence encoder:

```python
class FrozenConsequenceEncoder:
    def encode(self, context, candidate_actions):
        ...
```

## Freeze Boundary

Frozen parameters do not mean detached inputs.

Correct:

```text
z_i = F_phi(c, a_i)
phi frozen
d z_i / d a_i may be nonzero
d L / d phi = 0
```

Incorrect:

```text
detach(candidate_actions) before F_phi
```

The encoder parameters must have:

```text
requires_grad = False
parameter_grad_count = 0
```

while candidate actions or decoded candidates may still receive gradients.

## Drive-JEPA Evidence

A3.2 real AC-JEPA gradient smoke validated:

```text
candidate action input
-> frozen C0 AC-JEPA rollout_from_prefix(..., stop_gradient=False)
-> predictive latent geometry
-> spectral effective-rank scalar
-> backward to candidate action input
```

Observed example:

```text
candidates: 8
rollout steps: 2
pred shape: [8,2,512,256]
K_eff: 2.6866
tau: 0.198094
action grad mean abs: 0.0273527
action grad max abs: 0.972636
AC-JEPA param grads: 0
```

This supports the real gradient path only. It does not by itself prove planner
improvement, compression, or teacher target validity.

## Transfer Rule

For a new decoder:

1. Freeze the consequence encoder.
2. Keep gradients from the redundancy scalar back to decoded candidates.
3. Verify parameter gradients remain zero.
4. Verify candidate gradients are finite and nonzero.
5. Only then run a tiny optimization.

