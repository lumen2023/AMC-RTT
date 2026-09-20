# 26 ICLR Experiment Program / ICLR 实验程序

Status: `NO_TRAINING_AUTHORIZED_BY_THIS_DOCUMENT`

This is a staged program, not an authorization to launch new model training.

这是分阶段程序，不是启动新模型训练的授权。

## Phase A: Mechanism Audit / 阶段 A：机制审计

### A0: Schema And Provenance

Record:

记录：

- decoder family;
- decoder family；
- sample semantics;
- sample semantics；
- canonical shapes;
- canonical shapes；
- checkpoint/config/source hashes;
- checkpoint/config/source hashes；
- tau and normalization provenance.
- tau 与 normalization provenance。

Gate: no schema ambiguity.

门控：不存在 schema ambiguity。

### A1: No-Training Relation

Compare:

比较：

```text
geometry
geometry + task score
frozen consequence relation
```

Report relation quality, topology, coverage, and task-score association.

报告 relation quality、topology、coverage 与 task-score association。

## Phase B: Gradient Mechanism / 阶段 B：梯度机制

### B0: Frozen Gradient Smoke

Require:

要求：

```text
candidate gradient finite and nonzero
frozen evaluator parameter grad count = 0
```

### B1: Pair Credit Audit

Measure whether the candidate loss concentrates credit on strong/local
redundant relations or spreads it over weak cross-mode pairs.

测量 candidate loss 是把 credit 集中到强/局部冗余 relation，还是扩散到弱
cross-mode pairs。

## Phase C: Matched Optimization / 阶段 C：匹配优化

Compare exactly:

严格比较：

```text
baseline
AMC-v1
TA-AMC
```

Match:

匹配：

```text
initialization
data order
steps
optimizer
learning-rate schedule
compute budget
seed set
```

## Phase D: Task And Difficulty / 阶段 D：任务与难度

Predeclare scene difficulty before reading final results. Candidate difficulty
signals:

在读取最终结果前预注册 scene difficulty。候选 difficulty signals：

- scenario tags;
- scenario tags；
- teacher-mode complexity;
- teacher-mode complexity；
- agent count or interaction count;
- agent count 或 interaction count；
- base loss strata;
- base loss strata；
- collision/intervention burden.
- collision/intervention burden。

Avoid using a post hoc score that directly leaks the target task metric.

避免使用直接泄漏 target task metric 的事后指标。

Report:

报告：

```text
easy / medium / hard redundancy
gradient norm
gradient cosine
gradient effective rank
hard-scene update share
task score by difficulty
overall task score
```

## Phase E: Cross-Decoder Transfer / 阶段 E：跨 decoder 迁移

Minimum external set:

最小外部集合：

```text
Drive-JEPA / driving
one diffusion action decoder
one flow-matching action or trajectory decoder
```

Before all three pass Level 0-4, write:

在三者都通过 Level 0-4 前，只能写：

```text
decoder-agnostic design / transfer hypothesis
```

## Upgrade Rules / 升级规则

```text
MECHANISM_SUPPORTED:
    relation and gradient mechanism pass, task gate incomplete.

CAPACITY_EFFICIENCY_SUPPORTED:
    redundancy structure improves,
    optimization information improves,
    and matched task metric improves.

CROSS_DECODER_GENERALITY_SUPPORTED:
    the above gates pass on Drive-JEPA, diffusion, and flow matching.
```

No single scalar `K_eff` result can trigger an upgrade.

任何单独的 `K_eff` 结果都不能触发 claim upgrade。

