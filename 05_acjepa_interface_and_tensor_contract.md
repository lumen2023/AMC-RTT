# 05 AC-JEPA Interface And Tensor Contract

Status: `SUPPORTED_FOR_DRIVE_JEPA_ADAPTER_SCOPE`

This contract is extracted from the current Drive-JEPA / AC-JEPA code path, not
from shape guessing.

## Raw Latent Layout

The raw AC-JEPA candidate-specific future latent is:

```text
Z = [K,H,P,D]
```

Meaning:

```text
K = number of candidate proposals, typically 32
H = rollout horizons / rollout steps
P = patch tokens per frame, documented as 16*32 = 512
D = latent channel dimension, documented as 256
```

Source files:

```text
navsim_v1/navsim/agents/branch_drive/acwm/partition/types.py
navsim_v1/navsim/agents/branch_drive/acwm/partition/raw_latents.py
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_2_real_ac_jepa_gradient_smoke.py
```

A3.2 measured:

```text
pred shape = [8,2,512,256]
```

where `K=8`, `H=2`, `P=512`, `D=256`.

## Candidate To Action Path

Drive-JEPA proposal:

```text
proposal trajectory: [K,8,3]
```

Action conversion:

```text
trajectory_to_actions(trajectory [8,3]) -> actions [8,3]
```

The trajectory is interpreted relative to the ego-frame origin:

```text
origin = [0,0,0]
pose sequence = concat(origin, trajectory)
relative_se2_action(pose_i, pose_{i+1}) -> [dx_local, dy_local, dyaw]
```

Normalization:

```text
actions_norm = normalize_actions(actions, dataset.action_stats, stride_steps=1)
```

The A3.3 tiny pilot requires stride-1 action encoding.

## Rollout Interface

Current adapter call:

```python
pred = ac_model.rollout_from_prefix(
    z_context,
    actions_normalized[:, :steps],
    proprio,
    prefix_t=0,
    steps=steps,
    stop_gradient=False,
)
```

Tensor meanings:

| name | meaning | shape | gradient |
| --- | --- | --- | --- |
| `z0` | context latent for one scene | `[P,D]` | detached context |
| `z_context` | repeated prefix context | `[K,1,P,D]` | no decoder gradient needed |
| `actions_normalized` | candidate SE(2) actions | `[K,8,3]` | requires grad for student candidates |
| `proprio` | zero proprio placeholder in AMC path | `[K,H,8]` | no grad required |
| `pred` | predicted future latent | `[K,H,P,D]` | carries candidate gradient |

## Pairwise Distance Path

The implemented A3.2 distance flattens tokens and channels per horizon:

```text
flat = pred.float().flatten(2)      # [K,H,P*D]
d_h(i,j) = mean squared distance at horizon h
d(i,j) = mean_h d_h(i,j)
S_ij = exp(-d(i,j) / tau^2)
diag(S) = 1
S = 0.5 * (S + S^T)
```

When `tau` is estimated in A3.2 smoke, it is the detached median off-diagonal
L2 distance. Later AMC training uses the frozen tau from the A3.4 provenance.

## Minimal Adapter Pseudocode

```python
def encode_acjepa(context_z0, proposals, dataset, ac_model, tau, rollout_steps):
    actions = normalized_actions_from_trajectories(
        proposals, dataset.action_stats, dataset.wm_stride_steps
    )
    latent = rollout_latents_grad(
        ac_model=ac_model,
        z0=context_z0,
        actions_normalized=actions,
        chunk_size=4,
        rollout_steps=rollout_steps,
        stop_gradient=False,
    )
    return latent
```

Boundary: this adapter is supported for the Drive-JEPA C0 AC-JEPA path. It is
not evidence that AC-JEPA multi-horizon support alone recovers the teacher
relation target after A15-A17.

