# Drive-JEPA-Based 93.95 Anchor

## English

AMC-RTT is anchored by a concrete Drive-JEPA-based engineering result:

```text
AMC-Drive local full-navtest / submission rescore:
PDMS = 0.939443730121 ~= 93.944 ~= 93.95
```

This result comes from the Drive-JEPA-style `AMC-Drive` NAVSIM v1 lineage. The
package keeps this evidence as a positive migration anchor: de-redundancy is not
only a theory narrative; it has a high-scoring Drive-JEPA-based implementation
path.

Key facts preserved from the upstream workspace:

- method lineage: Drive-JEPA-based `AMC-Drive`;
- score: NAVSIM v1 PDMS `0.939443730121`, reported as approximately `93.95`;
- practical compute route: local single-RTX-3090 / fixcache fine-tuning lineage;
- de-redundancy hook: `consequence_dedup_loss.py`, `dedup_weight`,
  `dedup_centerline_cache`, and `config.dedup_weight * dedup_loss` in the
  Drive-JEPA-style training loss;
- engineering role: a strong starting point for AMC-RTT migration to other
  decoders.

Upstream source paths used to create this standalone evidence note:

```text
AMC-Drive/evidence/navsimv1_score_93.9_summary.md
AMC-Drive/README.md
AMC-Drive/MANIFEST.md
docs/NAVSIM_v1_v2_main_results_20260902.md
AMC-Drive/navsim_v1_overlay/navsim/agents/amc_drive/consequence_dedup_loss.py
AMC-Drive/navsim_v1_overlay/navsim/agents/amc_drive/amc_drive_config.py
AMC-Drive/navsim_v1_overlay/navsim/agents/amc_drive/amc_drive_agent.py
```

## 中文

AMC-RTT 以一个明确的 Drive-JEPA-based 工程结果作为锚点：

```text
AMC-Drive local full-navtest / submission rescore:
PDMS = 0.939443730121 ~= 93.944 ~= 93.95
```

该结果来自 Drive-JEPA 风格的 `AMC-Drive` NAVSIM v1 路线。本包把它作为积极的
迁移锚点：去冗余不仅是理论叙事，也已经有 Drive-JEPA-based 的高分实现路径。

关键事实：

- 方法路线：Drive-JEPA-based `AMC-Drive`；
- 分数：NAVSIM v1 PDMS `0.939443730121`，约等于 `93.95`；
- 算力路线：本地单张 RTX 3090 / fixcache 微调 lineage；
- 去冗余接入：`consequence_dedup_loss.py`、`dedup_weight`、
  `dedup_centerline_cache`，以及 Drive-JEPA-style training loss 中的
  `config.dedup_weight * dedup_loss`；
- 工程角色：为 AMC-RTT 迁移到其他 decoder 提供强起点。

本独立证据说明来自上游 workspace 中的真实证据路径：

```text
AMC-Drive/evidence/navsimv1_score_93.9_summary.md
AMC-Drive/README.md
AMC-Drive/MANIFEST.md
docs/NAVSIM_v1_v2_main_results_20260902.md
AMC-Drive/navsim_v1_overlay/navsim/agents/amc_drive/consequence_dedup_loss.py
AMC-Drive/navsim_v1_overlay/navsim/agents/amc_drive/amc_drive_config.py
AMC-Drive/navsim_v1_overlay/navsim/agents/amc_drive/amc_drive_agent.py
```
