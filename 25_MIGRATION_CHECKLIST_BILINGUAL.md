# 25 Migration Checklist / 迁移 Checklist

Status: `MIGRATION_AUTHORIZATION_GATE`

Every new decoder must answer these questions before training.

任何新 decoder 在训练前都必须回答以下问题。

## Decoder Identity / Decoder 身份

- What is `K`?
- `K` 是什么？
- What does one hypothesis mean?
- 一个 hypothesis 表示什么？
- Are hypotheses `persistent_slot`, `stochastic_sample`, or `codebook_entry`?
- hypotheses 是 `persistent_slot`、`stochastic_sample` 还是 `codebook_entry`？
- Which budget is potentially wasted: parameters, slots, sampling, probability
  mass, inference compute, or gradient information?
- 可能被浪费的是 parameters、slots、sampling、probability mass、inference
  compute 还是 gradient information？

## Tensor Contract / Tensor 契约

- Are candidates exposed as `[B,K,T,D]` or actions as `[B,K,H,D_a]`?
- candidates 是否以 `[B,K,T,D]`，或 actions 以 `[B,K,H,D_a]` 暴露？
- If internal tensors are `[B*K,...]`, where are they unflattened?
- 如果内部 tensor 是 `[B*K,...]`，在哪里恢复成 `[B,K,...]`？
- Can any relation computation mix different condition batches?
- relation computation 是否可能混合不同 condition batch？
- Are padding masks and variable horizons explicit?
- padding mask 与 variable horizon 是否明确？

## Action Manifold / Action 流形

- What is the valid action metric?
- 有效 action metric 是什么？
- How are scales normalized?
- scale 如何 normalization？
- How are angles wrapped?
- angle 如何 wrap？
- Does SE(2), quaternion, or mixed discrete/continuous structure require a
  special metric?
- SE(2)、quaternion 或离散/连续混合结构是否需要特殊 metric？

## Outcome Representation / Outcome representation

- What is the frozen consequence encoder?
- frozen consequence encoder 是什么？
- Is it frozen at parameter level?
- 参数层面是否 frozen？
- Does the input gradient survive?
- input gradient 是否保留？
- Is the representation validated against task outcomes?
- representation 是否与 task outcome 做过验证？
- Is the teacher target independent of the features being evaluated?
- teacher target 是否独立于被评估 feature？

## Decoder Path / Decoder 路径

- Does the decoder expose final actions/trajectories, clean estimates, velocity,
  or noise?
- decoder 暴露的是 final actions/trajectories、clean estimates、velocity 还是
  noise？
- Can `K` hypotheses be generated differentiably?
- `K` 个 hypotheses 是否可微生成？
- What is the memory/runtime cost of the path?
- 路径的 memory/runtime cost 是什么？
- Is a proxy-to-endpoint agreement test available?
- 是否有 proxy-to-endpoint agreement test？

## Objective / Objective

- What base loss should receive any released modeling freedom?
- 释放的建模自由度应由哪个 base loss 使用？
- Does the regularizer preserve relevant support?
- regularizer 是否保持 relevant support？
- Can the loss cause mode collapse?
- loss 是否可能造成 mode collapse？
- Is the loss decoder-aware rather than copied from Drive-JEPA?
- loss 是否 decoder-aware，而不是从 Drive-JEPA 直接复制？

## Evaluation / Evaluation

- What is the primary task metric?
- primary task metric 是什么？
- What are the predeclared safety and coverage budgets?
- 预注册的 safety 与 coverage budget 是什么？
- Are baseline, AMC-v1, and TA-AMC matched in initialization, data, steps,
  optimizer, compute, and seed?
- baseline、AMC-v1、TA-AMC 是否在 initialization、data、steps、optimizer、
  compute、seed 上匹配？
- What evidence would falsify the claimed mechanism?
- 什么证据会证伪当前机制 claim？

## Authorization / 授权

If any answer is missing:

如果有任何一项无法回答：

```text
MIGRATION_NOT_YET_AUTHORIZED
```

If all answers are present, only Level 0-1 may begin without a separate
training authorization.

即使全部回答完毕，也只能先开始 Level 0-1；训练仍需单独授权。

