# AMC-RTT v1.0 Manifest / 文件清单

This manifest records purpose, claim level, evidence source, and migration role.

本 manifest 记录每个文件的目的、claim level、证据来源与迁移角色。

| file | purpose / 目的 | claim level | source/evidence / 来源 | migration role / 迁移角色 |
| --- | --- | --- | --- | --- |
| `README.md` | package entry and claim boundary / 包入口与 claim boundary | governance | A2-A20, current guard | orientation |
| `README_EN.md` | English GitHub-facing entry / 英文入口 | governance | README, evidence anchor | orientation |
| `README_CN.md` | Chinese GitHub-facing entry / 中文入口 | governance | README, evidence anchor | orientation |
| `evidence/DRIVE_JEPA_93_95_ANCHOR.md` | standalone 93.95 evidence anchor / 独立高分证据锚点 | engineering evidence | AMC-Drive score summary, NAVSIM main results, source hooks | motivation |
| `NON_DESTRUCTIVE_GUARD.md` | write/runtime safety / 写入与运行安全 | governance | repository instructions | all |
| `00_problem_and_universal_interface.md` | universal problem and tensors / 通用问题与 tensor | design | decoder abstraction | all |
| `01_geometry_redundancy.md` | geometry baseline / 几何 baseline | diagnostic | A2.6-A2.7 | all |
| `02_geometry_plus_task_score_epdms.md` | geometry + outcome diagnostic / 几何+结果 | diagnostic | Drive outcome path | task-specific |
| `03_geometry_action_relation.md` | G/A/Z relation evidence / G/A/Z relation | supported diagnostic | A2.4, A2.7, A2.8 | all |
| `04_frozen_consequence_encoder.md` | frozen differentiable evaluator / 冻结 evaluator | supported gradient path | A3.2 | all |
| `05_acjepa_interface_and_tensor_contract.md` | real AC-JEPA contract / 真实 AC-JEPA 契约 | supported Drive scope | source code, A3.2 | Drive-JEPA |
| `06_spectral_effective_multimodality.md` | `S`, `K_eff`, topology limitation | supported with limit | A3.2, A18 | all |
| `07_amc_training_regularizer.md` | AMC-v1 objective / AMC-v1 目标 | supported bounded | A3.3-A3.6 | Drive baseline |
| `08_coverage_preserving_amc.md` | optional coverage stabilizer / coverage 稳定器 | supported stabilization | A3.7 | task-specific |
| `09_topology_and_collapse_diagnostics.md` | topology/collapse library / topology 与 collapse | diagnostic | A18-A19 | all |
| `10_diffusion_decoder_adapter.md` | diffusion interface / diffusion 接口 | transfer hypothesis | diffusion path | diffusion |
| `11_flow_matching_decoder_adapter.md` | FM interface / FM 接口 | transfer hypothesis | ODE path | flow matching |
| `12_transfer_validation_protocol.md` | Level 0-4 gates / Level 0-4 门控 | required protocol | package policy | all |
| `13_failure_modes_and_negative_results.md` | legacy diagnostic guard / 旧版诊断护栏 | claim safety | A2.8, A3.6, A15-A20 | all |
| `14_drive_jepa_evidence_map.md` | original evidence map / 原证据图 | evidence index | A2-A20 | Drive-JEPA |
| `15_MAINLINE_AND_ICLR_STORY_BILINGUAL.md` | main narrative / 主线故事 | synthesis | A2-A20 | paper framing |
| `16_REDUNDANCY_CAPACITY_THEORY_BILINGUAL.md` | finite-K, bias, Jacobian theory | theorem/proposition | explicit assumptions | all |
| `17_GRADIENT_SNR_INFORMATION_THEORY_BILINGUAL.md` | SNR, Fisher, hard-scene theory | theorem/conditional | explicit assumptions, A18-A19 | all |
| `18_DECODER_DIMENSION_CONTRACTS_BILINGUAL.md` | canonical tensor safety | API contract | source shape audit | all |
| `19_DRIVE_JEPA_GOLDEN_PATH_BILINGUAL.md` | source-level golden path | supported implementation evidence | real file:function:line | Drive-JEPA |
| `20_DIFFUSION_MIGRATION_MATH_BILINGUAL.md` | diffusion proxy/endpoint math | transfer hypothesis | diffusion equations | diffusion |
| `21_FLOW_MATCHING_MIGRATION_MATH_BILINGUAL.md` | FM ODE sensitivity math | transfer hypothesis | ODE equations | flow matching |
| `22_DECODER_AGNOSTIC_THEOREMS_BILINGUAL.md` | theorem applicability matrix | theory boundary | 16-21 | all |
| `23_EVIDENCE_CLAIM_MATRIX_BILINGUAL.md` | supported/not/future matrix | governance | A2-A20 | all |
| `24_FAILURE_MODES_AND_SAFETY_GATES_BILINGUAL.md` | stop conditions / stop 条件 | safety gates | known failures | all |
| `25_MIGRATION_CHECKLIST_BILINGUAL.md` | pre-authorization questions | authorization gate | API + theory | all |
| `26_ICLR_EXPERIMENT_PROGRAM_BILINGUAL.md` | staged experiment plan | no training authorization | protocol design | all |
| `27_CAPACITY_EFFICIENCY_PROOF_PROGRAM_BILINGUAL.md` | H1-H5 causal program | future proof obligation | theory + A18-A20 | all |
| `28_POSITIVE_MATH_PROOF_AND_LITERATURE_BILINGUAL.md` | positive derivation companion and literature anchors / 正面推导与文献锚点 | theorem/proposition/literature | derivations + primary papers | all |
| `interfaces/redundancy_api.py` | hardened standalone API | implementation scaffold | canonical contracts | all |
| `figures/fig1_high_score_anchor.svg` | Drive-JEPA-based 93.95 achievement anchor | engineering evidence visualization | AMC-Drive score summary, NAVSIM main results | motivation |
| `figures/fig2_keff_intuition.svg` | `K_generated` vs `K_eff` intuition | mathematical visualization | `S`, `K_eff` equations | all |
| `figures/fig3_credit_assignment.svg` | scalar-vs-topology credit warning | diagnostic visualization | A18-A20 | all |
| `figures/fig4_decoder_transfer_pipeline.svg` | decoder-agnostic migration pipeline | protocol visualization | API contract, Level 0-4 gates | all |
| `figures/specs/*.json` | deterministic FigureSpec sources | reproducibility | local renderer | all |
| `.gitignore` | standalone repository hygiene | governance | package policy | all |
| `experimental/structured_amc.md` | TA-AMC candidate | experimental | A19-A20 | Drive first |
| `experimental/pair_credit_assignment.md` | pair credit diagnostics | experimental diagnostic | A18-A19 | all |
| `skill/SKILL.md` | reusable workflow | protocol | package rules | all |
| `configs/*.yaml` | domain templates | documentation-only | adapter contracts | Drive/DM/FM |
| `references.bib` | verified literature anchors | bibliography | primary sources | all |

## Highlighted Engineering Anchor / 高分工程锚点

```text
Drive-JEPA-based AMC / de-redundancy lineage:
NAVSIM v1 local submission rescore PDMS = 0.939443730121 ~= 93.95
```

This is recorded as engineering evidence for the Drive-JEPA-based path, while
the cross-decoder theorem/package verdict remains bounded below.

该结果是 Drive-JEPA-based 路线的工程证据；跨 decoder 理论包的最终边界仍以下方
verdict 为准。

## Package Verdict / 包裁决

```text
MECHANISM_SUPPORTED__CAPACITY_EFFICIENCY_PROOF_ACTIVE
```
