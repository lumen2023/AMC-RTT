# 19 Drive-JEPA Golden Path / Drive-JEPA 金标准路径

Status: `SUPPORTED_IMPLEMENTATION_EVIDENCE`

This file is a read-only source map. The referenced project files are not
modified by AMC-RTT.

本文件是只读源码地图。AMC-RTT 不修改这些被引用的项目文件。

## Entry Points / 入口

Primary AMC training entry:

主要 AMC training 入口：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_5_phase2_amc_training.py:505
```

Coverage-aware extension:

coverage-aware 扩展：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_7_phase4_coverage_aware_amc.py:569
```

Real frozen gradient smoke:

真实冻结梯度 smoke：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_2_real_ac_jepa_gradient_smoke.py:230
```

## Source And Checkpoint / 数据源与 checkpoint

A3.5 records:

A3.5 记录：

- C0 AC-JEPA model summary and checkpoint key: `a3_5...py:96-103`;
- C0 AC-JEPA model summary 与 checkpoint key：`a3_5...py:96-103`；
- Drive-JEPA checkpoint default:
  `a3_5...py:71-73`;
- Drive-JEPA checkpoint 默认路径：
  `a3_5...py:71-73`；
- A3.4 teacher validity summary:
  `a3_5...py:94-100`;
- A3.4 teacher validity summary：
  `a3_5...py:94-100`。

The exact external artifact paths are provenance, not portable API. A transfer
implementation must replace them with project-local configuration.

这些外部 artifact 路径只是 provenance，不是可迁移 API。迁移实现必须用新项目
自己的配置替换它们。

## Planner Decoder And Proposal Tensor / Planner decoder 与 proposal tensor

The planner receives feature tensors through:

planner 通过以下路径接收 feature tensors：

```text
DriveJEPAAgent.forward(features)
-> DriveJEPAModel
-> pred["proposals"]
```

Source:

源码：

```text
navsim_v1/navsim/agents/drive_jepa_perception_based/drive_jepa_agent.py:115-116
navsim_v1/navsim/agents/drive_jepa_perception_based/drive_jepa_agent.py:308-315
```

The A3.3 contract checks:

A3.3 契约检查：

```text
pred["proposals"]: [B,32,8,3]
```

where `32` is the proposal count, `8` is the trajectory horizon, and `3` is
the local pose/action representation `[x,y,yaw]` before adjacent-action
conversion.

其中 `32` 是 proposal 数量，`8` 是 trajectory horizon，`3` 是相邻 action
转换前的 local pose/action 表示 `[x,y,yaw]`。

## Trajectory To Action / trajectory 到 action

The real conversion is:

真实转换为：

```text
trajectory [8,3]
-> implicit origin [0,0,0]
-> relative_se2_action
-> actions [8,3]
```

Source:

源码：

```text
navsim_v1/navsim/agents/branch_drive/acwm/se2_action_utils.py:14-34
navsim_v1/navsim/agents/branch_drive/acwm/se2_action_utils.py:55-68
```

The torch training path mirrors it in:

训练时的 torch 路径在：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_3_tiny_amc_pilot.py:198-222
```

Train-split normalization is:

train-split normalization 是：

$$
\operatorname{actions}_{\mathrm{norm}}
=
\frac{\operatorname{actions}-\operatorname{mean}}
{\operatorname{std}}.
$$

Source:

源码：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/action_stats.py:64-70
```

## AC-JEPA Frozen Evaluator / 冻结 AC-JEPA evaluator

Raw AC-JEPA latent:

AC-JEPA raw latent：

```text
pred = rollout_from_prefix(...)
pred shape = [K,H,P,D]
```

The current source documents `[K,H,P,D]` as candidate, rollout horizon, patch
tokens, and latent channels:

当前源码将 `[K,H,P,D]` 解释为 candidate、rollout horizon、patch tokens 与
latent channels：

```text
navsim_v1/navsim/agents/branch_drive/acwm/partition/types.py:20-32
```

A3.2 measured `[8,2,512,256]`.

A3.2 实测 `[8,2,512,256]`。

Student branch:

student branch：

```text
freeze_module(model)
...
model.rollout_from_prefix(..., stop_gradient=False)
```

Source:

源码：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_2_real_ac_jepa_gradient_smoke.py:163-180
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_2_real_ac_jepa_gradient_smoke.py:239-253
```

The student path must not use `torch.no_grad()` around the AC-JEPA forward,
because the gradient must travel:

student path 不能在 AC-JEPA forward 外层使用 `torch.no_grad()`，因为梯度必须
沿着以下路径传播：

```text
proposal/action
-> AC-JEPA
-> redundancy scalar
-> planner parameters
```

Teacher branch:

teacher branch：

```text
@torch.no_grad()
teacher_log_keff(...)
rollout_from_prefix(..., stop_gradient=True)
```

Source:

源码：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_3_tiny_amc_pilot.py:254-273
```

## Relation And K_eff / Relation 与 K_eff

Pairwise latent distance:

pairwise latent distance：

`pairwise_mse_by_horizon(latent)` first averages over rollout horizons, then:

$$
S_{ij}
=
\exp\!\left(-\frac{\operatorname{mse}_{ij}}{\tau^2}\right),
\qquad
\operatorname{diag}(S)=1,
\qquad
S=\frac{1}{2}(S+S^\top).
$$

Source:

源码：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_2_real_ac_jepa_gradient_smoke.py:186-227
```

The effective rank is:

有效秩为：

$$
K_{\mathrm{eff}}
=
\frac{(\operatorname{tr}S)^2}{\operatorname{tr}(S^2)}.
$$

The A3.4 tau provenance is passed into A3.5 and reused for student and teacher
readouts; it must not be tuned on held-out evaluation data.

A3.4 的 tau provenance 被传入 A3.5，并用于 student 与 teacher readout；不能在
held-out evaluation data 上重新调 tau。

## AMC Insertion Point / AMC 插入点

The A3.5 student loss is:

A3.5 student loss：

$$
L_{\mathrm{AMC}}
=
\left[
\log K_{\mathrm{eff,pred}}
-
\operatorname{stopgrad}(\log K_{\mathrm{eff,teacher}})
\right]^2,
\qquad
L_{\mathrm{total}}
=
L_{\mathrm{base}}+\lambda(t)L_{\mathrm{AMC}}.
$$

Here `L_base` is produced by `agent.compute_loss(...)`.

Source:

源码：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_5_phase2_amc_training.py:583-602
```

The original Drive-JEPA loss remains assembled in:

原始 Drive-JEPA loss 仍在：

```text
navsim_v1/navsim/agents/drive_jepa_perception_based/drive_jepa_agent.py:308-383
```

including trajectory, score, agent, BEV, and existing dedup terms configured by
the project.

包括 trajectory、score、agent、BEV 以及项目配置的已有 dedup terms。

## Optimizer And Clip / 优化器与裁剪

The planner optimizer is Adam with a smaller backbone learning rate:

planner optimizer 是 Adam，backbone 使用更小 learning rate：

```text
navsim_v1/navsim/agents/drive_jepa_perception_based/drive_jepa_agent.py:395-400
```

The AMC scripts explicitly clip trainable planner gradients:

AMC scripts 对可训练 planner 梯度显式裁剪：

```text
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_5_phase2_amc_training.py:606-613
navsim_v1/navsim/agents/branch_drive/acwm/training/a3_7_phase4_coverage_aware_amc.py:316-323
```

This makes the normalized-update complex-scene theorem plausible as a mechanism
test, but not automatically proven for Adam's full stateful dynamics.

这使 normalized-update complex-scene theorem 成为合理的机制测试，但不能自动
证明 Adam 的完整 stateful dynamics 满足该结论。

## Score / PDMS Evaluation / Score 与 PDMS evaluation

During training, `compute_score` detaches proposals before the external score
path, while the planner losses use returned score targets and prediction losses:

训练期间，`compute_score` 在外部 score path 前 detach proposals，而 planner
loss 使用返回的 score targets 与 prediction losses：

```text
drive_jepa_agent.py:118-159
drive_jepa_agent.py:161-202
```

The score backend is:

score backend 是：

```text
navsim_v1/navsim/agents/drive_jepa_perception_based/score_module/compute_navsim_score.py:24-123
```

The evaluation shell invokes the NAVSIM PDM scoring path:

evaluation shell 调用 NAVSIM PDM scoring path：

```text
navsim_v2/scripts/evaluation/eval_drive_jepa_perception_based.sh:20
```

## Call Graph / 调用图

```text
A3.5 main
  -> load teacher/source summaries
  -> make_drive_jepa_agent
  -> agent.forward
       -> DriveJEPAModel
       -> pred["proposals"] [B,32,8,3]
  -> agent.compute_loss
       -> compute_score / trajectory_loss_anchors / score_loss / existing terms
  -> pred_log_keff
       -> trajectory_to_actions_torch
       -> normalize_actions
       -> frozen AC-JEPA rollout_from_prefix(stop_gradient=False)
       -> pairwise_mse_by_horizon
       -> effective_rank_from_rollout
  -> teacher_log_keff
       -> teacher trajectories
       -> action conversion
       -> frozen AC-JEPA rollout_from_prefix(stop_gradient=True)
  -> L_total = L_base + lambda * L_AMC
  -> backward
  -> frozen AC-JEPA parameter-grad audit
  -> clip_grad_norm_
  -> Adam optimizer.step
  -> held-out evaluation / score / coverage / dispersion
```

## Golden-Path Claim Boundary / 金标准路径边界

Supported:

已支持：

- real frozen AC-JEPA gradient path;
- 真实冻结 AC-JEPA gradient path；
- effective multimodality calibration under the tested Drive-JEPA protocol;
- 在测试 Drive-JEPA 协议下的 effective multimodality calibration；
- zero AC-JEPA parameter gradients in the audited path.
- 审计路径中 AC-JEPA parameter gradients 为零。

Not supported:

尚不支持：

- universal outcome validity of AC-JEPA distance;
- AC-JEPA distance 的 universal outcome validity；
- proposal cardinality reduction;
- proposal cardinality reduction；
- planning improvement;
- planning improvement；
- direct reuse of this loss for stochastic DM/FM samples.
- 将此 loss 直接复用到 stochastic DM/FM samples。
