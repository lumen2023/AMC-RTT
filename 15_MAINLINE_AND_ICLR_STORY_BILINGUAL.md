# 15 Mainline And ICLR Story / 主线与 ICLR 故事

Status: `MAINLINE_SYNTHESIS`

## Core Thesis / 核心主张

**Do not let a finite multimodal decoder spend its modeling, sampling, and
optimization budget repeatedly representing the same future.**

**不要让有限的多模态 decoder 把建模、采样和优化预算反复花在同一个未来上。**

The scientific chain is:

科学链条是：

```text
multimodal redundancy
-> redundant modeling / sampling / optimization freedom
-> redundancy-aware gradient credit assignment
-> better effective capacity allocation
-> better task learning
```

The first two links are structural or conditional claims. The last two are
future proof obligations.

前两个箭头是结构性或条件性结论；后两个箭头是尚未完成的 future proof
obligations。

## Research Question / 研究问题

Fixed candidate count, persistent decoder slots, codebook size, and stochastic
sample count are not interchangeable. The package asks:

固定候选数、持久 decoder slot、codebook 大小和随机样本数不能混为一谈。本包
要回答：

1. What does one hypothesis consume?
2. 一个 hypothesis 消耗的到底是什么？
3. Can a frozen consequence evaluator identify semantic redundancy?
4. 冻结 consequence evaluator 能否识别语义冗余？
5. Does the redundancy gradient allocate credit selectively?
6. 冗余梯度是否选择性地分配 credit？
7. Does that allocation improve optimization information and task learning?
8. 这种分配是否最终改善优化信息与任务学习？

## ICLR Ladder / ICLR 理论梯子

1. `K_generated != K_effective`.
2. `K_generated != K_effective`。
3. Existing multimodal objectives may over-segment or repeatedly represent
   nearby behavior modes.
4. 现有多模态目标可能过度分割行为模式，或重复表示相邻行为模式。
5. A frozen action-conditioned predictive representation gives a
   consequence-level relation.
6. 冻结的 action-conditioned predictive representation 提供 consequence-level
   relation。
7. Scalar effective-rank matching has a provable amount-versus-topology gap.
8. 标量 effective-rank matching 存在可证明的“总量—拓扑”缺口。
9. A18 observes the predicted diffuse-smoothing failure.
10. A18 观察到了理论预测的 diffuse smoothing failure。
11. A19 provides read-only evidence that topology-concentrated fields change
    pair credit in the desired direction.
12. A19 提供只读证据，表明 topology-concentrated field 能按预期改变 pair credit。
13. The causal task-learning link remains open.
14. 因果的 task-learning 链条仍然开放。

## Current Supported Story / 当前已支持故事

Supported:

已支持：

- consequence-level redundancy exists beyond simple local geometry;
- consequence-level redundancy 不仅是简单局部几何相似；
- frozen AC-JEPA can carry a redundancy scalar gradient to candidate actions;
- 冻结 AC-JEPA 能将 redundancy scalar 梯度传给 candidate actions；
- AMC-v1 changes effective multimodality under the tested Drive-JEPA protocol;
- 在测试的 Drive-JEPA 协议下，AMC-v1 能改变 effective multimodality；
- A18-A20 identify topology-aware credit assignment as the next mechanism test.
- A18-A20 将 topology-aware credit assignment 确定为下一步机制测试。

Not supported:

尚不支持：

- capacity efficiency has already improved;
- 容量效率已经提升；
- planning quality has already improved;
- planning quality 已经提升；
- proposal cardinality has decreased;
- proposal cardinality 已经减少；
- the same AMC loss is valid for stochastic DM/FM samples.
- 同一个 AMC loss 对随机 DM/FM samples 直接有效。

## Negative Results As Contribution / 把负结果写成贡献

A18 is not merely a failed tuning run. It is a mechanism result:

A18 不只是一次调参失败，而是一个机制结果：

```text
K_eff down
affinity mass up
edge participation up
task score not improved
```

This pattern is consistent with diffuse smoothing. It motivates TA-AMC as a
falsifiable credit-assignment correction, not as a pre-claimed winning method.

这一模式与 diffuse smoothing 一致。它支持把 TA-AMC 作为可证伪的
credit-assignment 修正方向，而不是预先宣称已经成功的方法。

## Decoder-Agnostic Boundary / decoder-agnostic 边界

The portable object is:

可迁移的对象是：

```text
decode candidates
-> canonicalize [B,K,...]
-> frozen consequence representation
-> relation
-> statistics
-> decoder-aware policy
```

The portable object is not a promise that:

可迁移对象不意味着以下承诺成立：

```text
one loss sign
one capacity interpretation
one metric
one sampler path
```

## Falsifiable End State / 可证伪终点

The strongest eventual evidence would show, under matched compute:

在计算量匹配的条件下，最强的最终证据应同时显示：

```text
gradient redundancy down
gradient effective rank up or logdet proxy up
hard/complex-scene update share up
task score up
```

Until all four are observed with predeclared gates, the package must use:

在四项都按预注册门控观察到之前，本包必须使用：

```text
MECHANISM_SUPPORTED__TASK_GAIN_NOT_YET_SUPPORTED
```

