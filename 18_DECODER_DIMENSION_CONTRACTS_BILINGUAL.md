# 18 Decoder Dimension Contracts / Decoder 维度契约

Status: `API_SAFETY_CONTRACT`

## Canonical Shapes / 规范形状

Every adapter must expose candidates in explicit condition and candidate axes:

每个 adapter 都必须显式保留 condition 与 candidate 轴：

```text
actions        A: [B,K,H,D_a]
valid_mask         [B,K,H] or broadcast-compatible
context            [B,C] or [B,N_ctx,D_ctx]
outcome_latent Z:  [B,K,H_z,D_z] or [B,K,D_z]
affinity       S:  [B,K,K]
K_eff              [B]
rho                [B]
scores/logits      [B,K] (optional)
```

`B` is the condition batch, `K` is a proposal or stochastic-sample axis, `H`
is action horizon, and `D_a` is action dimension.

`B` 是 condition batch，`K` 是 proposal 或 stochastic-sample 轴，`H` 是
action horizon，`D_a` 是 action dimension。

## Sample Semantics / 样本语义

Every candidate set must declare one:

每个 candidate set 必须声明一种语义：

```text
persistent_slot
stochastic_sample
codebook_entry
```

This declaration changes the capacity claim:

该声明会改变 capacity claim：

| semantics | allowed interpretation |
| --- | --- |
| `persistent_slot` | slot/query/output Jacobian freedom may be discussed |
| `stochastic_sample` | finite sample budget, probability mass, and Monte-Carlo information |
| `codebook_entry` | discrete code capacity, duplicate/dead entry risk |

## Flattening Rule / Flatten 规则

Internal implementations may use:

内部实现可以使用：

```text
[B*K,H,D_a]
```

but must restore:

但在 redundancy computation 前必须恢复：

```text
[B,K,H,D_a]
```

before computing pairwise relations. Mixing candidates across different
conditions is a hard schema failure, not a minor implementation detail.

把不同 condition 的 candidate 混在一起计算 pairwise relation 是硬性 schema
failure，而不是小的实现细节。

## Masks And Time / Mask 与时间

Adapters must specify:

adapter 必须明确：

- variable horizon and padding mask;
- variable horizon 与 padding mask；
- `delta_t` or time-step spacing;
- `delta_t` 或时间步间隔；
- whether padded values are excluded from distances;
- padding 是否从 distance 中排除；
- whether candidate validity is `[B,K]` or per-step `[B,K,H]`.
- candidate validity 是 `[B,K]` 还是逐步 `[B,K,H]`。

## Action Manifold / Action 流形

Do not flatten heterogeneous actions and assume Euclidean distance is meaningful.

禁止直接 flatten 异构 action 并默认 Euclidean distance 有意义。

Required domain decisions:

必须先做领域决定：

- continuous channels: scaling and normalization;
- continuous channel：scaling 与 normalization；
- angles: wrap or represent with sine/cosine;
- 角度：wrap 或使用 sine/cosine；
- SE(2): use local-frame composition and periodic yaw;
- SE(2)：使用 local-frame composition 与周期 yaw；
- quaternions: identify antipodal equivalence `q ~ -q`;
- quaternion：处理 antipodal equivalence `q ~ -q`；
- discrete gripper/control channels: use a mixed metric or separate relation;
- 离散 gripper/control channel：使用 mixed metric 或独立 relation；
- action scaling: record train-split statistics and inverse-transform policy.
- action scaling：记录 train-split statistics 与 inverse-transform policy。

Drive-JEPA uses adjacent SE(2) actions `[dx_local,dy_local,dyaw]` and wraps yaw
to `[-pi,pi]`; see
`navsim_v1/navsim/agents/branch_drive/acwm/se2_action_utils.py:14-68`.

Drive-JEPA 使用相邻 SE(2) actions `[dx_local,dy_local,dyaw]`，并把 yaw wrap
到 `[-pi,pi]`；见
`navsim_v1/navsim/agents/branch_drive/acwm/se2_action_utils.py:14-68`。

## AC-JEPA Concrete Contract / AC-JEPA 具体契约

The current raw latent is:

当前 raw latent 是：

```text
Z = [K,H,P,D] = [candidate, rollout horizon, patch tokens, latent channels]
```

The current source documents `P=512` patch tokens and `D=256` latent channels;
the A3.2 smoke measured `[8,2,512,256]`. This is a Drive-JEPA contract, not a
universal latent shape.

当前源码文档记录 `P=512` patch tokens、`D=256` latent channels；A3.2 smoke
实测 `[8,2,512,256]`。这是 Drive-JEPA 契约，不是通用 latent shape。

## Validation Checklist / 校验清单

An adapter is not authorized until:

adapter 在以下项目完成前不得授权：

1. candidate shape is `[B,K,...]`;
2. candidate shape 是 `[B,K,...]`；
3. relation shape is `[B,K,K]`;
4. relation shape 是 `[B,K,K]`；
5. no cross-condition pair is computed;
6. 不计算跨 condition pair；
7. masks and time spacing are explicit;
8. mask 与时间间隔明确；
9. action metric matches the domain manifold;
10. action metric 与领域流形一致；
11. sample semantics is declared;
12. sample semantics 已声明；
13. gradient smoke has finite candidate gradients and zero frozen-evaluator parameter gradients.
14. gradient smoke 中 candidate gradients 有限非零且 frozen-evaluator 参数梯度为零。

