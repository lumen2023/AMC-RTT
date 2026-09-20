# 28 Positive Math Proof And Literature / 正面数学证明与文献锚点

Status: `PROOF_COMPANION__POSITIVE_ROUTE`

This file fixes two presentation issues in the public package:

1. formulas should render as GitHub/MathJax math, not as plain code blocks;
2. every strong idea should be backed by either a derivation under explicit
   assumptions or an authoritative paper anchor.

本文件修复公开包中的两个表达问题：

1. 公式应使用 GitHub/MathJax 可渲染数学式，而不是普通 code block；
2. 每个强观点都必须有明确假设下的推导，或有权威论文作为依据。

## Formula Rendering Policy / 公式渲染规范

Use inline math for symbols, for example `$K_{\mathrm{eff}}$`.

符号使用 inline math，例如 `$K_{\mathrm{eff}}$`。

Use display math for equations, written directly in Markdown:

成行公式使用 display math：

$$
\mathbb{E}[U_K]
=
\sum_{m=1}^{M}\left[1-(1-p_m)^K\right].
$$

Use fenced code blocks only for commands, paths, status tags, or ASCII
pipelines. Do not put mathematical claims inside fenced code blocks if the file
is meant for GitHub or a website.

code block 只用于命令、路径、状态标签或 ASCII 流程图。面向 GitHub/网站的数学
claim 不应放进 fenced code block。

## Proof Map / 证明地图

| result | positive conclusion | proof type | main anchors |
| --- | --- | --- | --- |
| finite-$K$ semantic coverage | balancing probability mass improves expected unique mode coverage | theorem | majorization theory; diffusion/FM sample semantics |
| gradient multiplicity bias | de-redundancy can move shared gradients toward semantic weights | proposition | GradNorm, PCGrad as gradient-credit motivation |
| correlated-gradient ESS | decorrelating duplicate gradients increases independent optimization information | theorem | Kish-style design effect; gradient covariance diagnostics |
| Fisher/logdet volume | independent directions carry larger local information volume than repeated directions | proposition | D-optimal/logdet information geometry |
| complex-scene update share | reducing repeated easy gradients increases hard-direction share under normalized/clipped updates | conditional theorem | clipped/normalized update analysis; multitask gradient work |
| fixed-slot Jacobian rank | duplicate slot sensitivities lower output degrees of freedom | proposition | effective rank; set uniqueness analogy from DETR |
| decoder transfer | interface transfers, while loss semantics are decoder-aware | theorem plus protocol | Drive-JEPA, Diffusion Policy, Flow Matching, VQ-BeT |

## Search-Verified Literature Discipline / 检索核验纪律

The literature role in this package is deliberately narrow. A paper can anchor
a mathematical object, a decoder family, or an optimization phenomenon; it does
not by itself prove AMC-RTT. Every AMC-RTT-specific claim below is therefore
written as one of three objects:

1. an algebraic theorem under explicit assumptions;
2. a local proposition whose boundary is stated beside it;
3. an empirical proof obligation that must be measured before the claim is
   upgraded.

本包对文献的使用是克制的：论文可以锚定数学对象、decoder family 或优化现象，
但不能自动证明 AMC-RTT。因此下面所有 AMC-RTT 专属结论只按三类表达：

1. 明确假设下的代数定理；
2. 带边界条件的局部命题；
3. 必须实测后才能升级的经验证明义务。

Public anchors checked for this revision include Drive-JEPA for the motivating
driving planner, DETR for set prediction with uniqueness pressure, Diffusion
Policy for multimodal action diffusion, Flow Matching for vector-field
probability transport, VQ-BeT for latent-action capacity, GradNorm and PCGrad
for shared-gradient balancing/conflict, Roy--Vetterli effective rank,
Marshall--Olkin--Arnold majorization, Kish design effect / effective sample
size, and D-optimal/logdet design references.

本次修订核验的公开锚点包括：Drive-JEPA 的驾驶 planner 背景，DETR 的 set
prediction 与唯一性压力，Diffusion Policy 的多模态动作 diffusion，Flow
Matching 的 vector-field probability transport，VQ-BeT 的 latent-action
capacity，GradNorm 与 PCGrad 的共享梯度平衡/冲突，Roy--Vetterli effective
rank，Marshall--Olkin--Arnold majorization，Kish design effect / effective
sample size，以及 D-optimal/logdet design 参考。

## 1. Finite-$K$ Coverage Theorem / 有限 $K$ 覆盖定理

### Statement / 命题

Assume a condition has $M$ semantic modes with probabilities
$p_1,\ldots,p_M$ and $\sum_m p_m=1$. Draw $K$ IID hypotheses. Let $U_K$ be the
number of unique semantic modes observed.

假设一个 condition 有 $M$ 个 semantic modes，概率为 $p_1,\ldots,p_M$ 且
$\sum_m p_m=1$。采样 $K$ 个 IID hypotheses，令 $U_K$ 为实际覆盖到的 unique
semantic modes 数量。

Then:

于是：

$$
\mathbb{E}[U_K]
=
\sum_{m=1}^{M}\left[1-(1-p_m)^K\right],
\qquad
\mathbb{E}[R_K]
=
K-\mathbb{E}[U_K].
$$

The miss probability of mode $m$ is:

mode $m$ 被完全漏掉的概率为：

$$
\Pr[m\ \text{missed}]
=
(1-p_m)^K.
$$

### Derivation / 推导

Define an indicator:

定义 indicator：

$$
I_m
=
\mathbf{1}\{\text{mode }m\text{ appears at least once among }K\text{ draws}\}.
$$

Then:

于是：

$$
U_K=\sum_{m=1}^{M} I_m.
$$

For a fixed $m$, the probability that no sample belongs to mode $m$ is
$(1-p_m)^K$. Therefore:

对固定 $m$，没有任何样本属于 mode $m$ 的概率是 $(1-p_m)^K$。因此：

$$
\mathbb{E}[I_m]
=
\Pr[I_m=1]
=
1-(1-p_m)^K.
$$

By linearity of expectation:

由期望线性性：

$$
\mathbb{E}[U_K]
=
\sum_m \mathbb{E}[I_m]
=
\sum_m \left[1-(1-p_m)^K\right].
$$

### Positive De-Redundancy Direction / 正向去冗余方向

Let

令

$$
F(p)=\sum_{m=1}^{M} f(p_m),
\qquad
f(p)=1-(1-p)^K.
$$

For $K\ge 2$:

当 $K\ge2$：

$$
f''(p)
=
-K(K-1)(1-p)^{K-2}
\le 0.
$$

So $F$ is symmetric and concave on the probability simplex; therefore it is
Schur-concave. A more balanced distribution gives larger expected unique
coverage.

所以 $F$ 在概率单纯形上是 symmetric concave，因此是 Schur-concave。更均衡的
概率分布带来更大的期望 unique coverage。

More concretely, suppose $p_a>p_b$ and move a small probability mass
$\epsilon>0$ from overrepresented mode $a$ to underrepresented mode $b$:

更直接地，若 $p_a>p_b$，把一个很小的概率质量 $\epsilon>0$ 从过度表示的
mode $a$ 移到欠表示的 mode $b$：

$$
p'_a=p_a-\epsilon,\qquad p'_b=p_b+\epsilon.
$$

The first-order change is:

一阶变化为：

$$
\left.\frac{d}{d\epsilon}
\left[
f(p_a-\epsilon)+f(p_b+\epsilon)
\right]\right|_{\epsilon=0}
=
-f'(p_a)+f'(p_b).
$$

Since

因为

$$
f'(p)=K(1-p)^{K-1},
$$

and $p_a>p_b$ implies $f'(p_a)<f'(p_b)$, the derivative is positive:

且 $p_a>p_b$ 推出 $f'(p_a)<f'(p_b)$，所以导数为正：

$$
-f'(p_a)+f'(p_b)>0.
$$

Thus support-preserving de-redundancy that moves probability mass from repeated
dominant behavior toward undercovered behavior strictly increases expected
finite-$K$ semantic coverage locally.

因此，只要去冗余是 support-preserving，并把概率质量从重复的 dominant behavior
移向 undercovered behavior，它就会在局部严格提高有限 $K$ 的期望语义覆盖。

### Literature Anchor / 文献锚点

This theorem is elementary probability plus Schur-concavity. It is the cleanest
bridge to stochastic decoders: Diffusion Policy models a multimodal conditional
action distribution, while Flow Matching models probability transport through a
velocity field. For fixed set prediction, DETR motivates uniqueness through
bipartite matching.

该定理是基础概率加 Schur-concavity。它是迁移到 stochastic decoder 的最干净桥：
Diffusion Policy 建模多模态条件动作分布，Flow Matching 建模由 velocity field
诱导的概率传输；而 fixed set prediction 中 DETR 通过 bipartite matching 强化
预测集合唯一性。

- Diffusion Policy: Chi et al., RSS 2023 / IJRR, arXiv:2303.04137.
- Flow Matching: Lipman et al., ICLR 2023, arXiv:2210.02747.
- DETR: Carion et al., ECCV 2020, arXiv:2005.12872.

## 2. Gradient Multiplicity Bias / 梯度重复偏置

### Statement / 命题

Assume semantic mode $m$ is represented by $r_m$ hypotheses and
$\sum_m r_m=K$. Each hypothesis in mode $m$ has expected shared-parameter
gradient $\mu_m$. If the loss averages hypotheses equally:

假设 semantic mode $m$ 由 $r_m$ 个 hypotheses 表示，且 $\sum_m r_m=K$。mode
$m$ 中每个 hypothesis 对共享参数的期望梯度为 $\mu_m$。若 loss 对 hypotheses
等权平均：

$$
\mathbb{E}[g]
=
\sum_{m=1}^{M}
\frac{r_m}{K}\mu_m.
$$

If the desired semantic gradient weighting is $\pi_m$, then:

若理想 semantic gradient weighting 是 $\pi_m$，则：

$$
g^\star
=
\sum_{m=1}^{M}\pi_m\mu_m,
\qquad
b
=
\mathbb{E}[g]-g^\star
=
\sum_m
\left(
\frac{r_m}{K}-\pi_m
\right)\mu_m.
$$

### Positive De-Redundancy Direction / 正向去冗余方向

Assume $\{\mu_m\}$ are orthonormal and define:

假设 $\{\mu_m\}$ 正交归一，并定义：

$$
\alpha_m=\frac{r_m}{K}-\pi_m.
$$

Then:

则：

$$
\lVert b\rVert^2
=
\sum_m \alpha_m^2.
$$

Suppose mode $a$ is overrepresented and mode $b$ is underrepresented:

若 mode $a$ 过度表示、mode $b$ 欠表示：

$$
\alpha_a>0,\qquad \alpha_b<0.
$$

Move a small weight $\delta>0$ from $a$ to $b$:

把一个小权重 $\delta>0$ 从 $a$ 移到 $b$：

$$
\alpha'_a=\alpha_a-\delta,
\qquad
\alpha'_b=\alpha_b+\delta.
$$

The squared-bias change is:

squared bias 的变化为：

$$
\Delta
=
(\alpha_a-\delta)^2+(\alpha_b+\delta)^2
-\alpha_a^2-\alpha_b^2
=
-2\delta(\alpha_a-\alpha_b)+2\delta^2.
$$

If

若

$$
0<\delta<\alpha_a-\alpha_b,
$$

then $\Delta<0$. Thus a small transfer from overrepresented to underrepresented
semantic modes reduces gradient weighting bias.

则 $\Delta<0$。因此，从过度表示 mode 向欠表示 mode 的小幅转移，会降低 shared
gradient weighting bias。

### Literature Anchor / 文献锚点

GradNorm and PCGrad do not prove AMC-RTT, but they are authoritative evidence
that gradient magnitude, balancing, and conflict matter in shared networks.

GradNorm 与 PCGrad 不是 AMC-RTT 的直接证明，但它们权威支持一个关键事实：
共享网络中的梯度幅值、平衡与冲突会实质影响优化。

- GradNorm: Chen et al., ICML 2018, PMLR.
- PCGrad / Gradient Surgery: Yu et al., NeurIPS 2020.

## 3. Correlated-Gradient Effective Sample Size / 相关梯度有效样本数

### Statement And Derivation / 命题与推导

Let $g_i=\mu+\epsilon_i$ for $i=1,\ldots,r$, with

令 $g_i=\mu+\epsilon_i$，其中

$$
\operatorname{Var}(\epsilon_i)=\sigma^2,
\qquad
\operatorname{Cov}(\epsilon_i,\epsilon_j)=\rho_g\sigma^2
\quad(i\ne j).
$$

For $\bar g=\frac{1}{r}\sum_i g_i$:

对 $\bar g=\frac{1}{r}\sum_i g_i$：

$$
\operatorname{Var}(\bar g)
=
\operatorname{Var}\left(
\frac{1}{r}\sum_i \epsilon_i
\right)
=
\frac{1}{r^2}
\left[
r\sigma^2+r(r-1)\rho_g\sigma^2
\right].
$$

Therefore:

因此：

$$
\operatorname{Var}(\bar g)
=
\frac{\sigma^2}{r}
\left[
1+(r-1)\rho_g
\right].
$$

Define $r_{\mathrm{eff}}$ by matching the independent-sample variance
$\sigma^2/r_{\mathrm{eff}}$:

用独立样本方差 $\sigma^2/r_{\mathrm{eff}}$ 来定义有效样本数：

$$
\frac{\sigma^2}{r_{\mathrm{eff}}}
=
\frac{\sigma^2}{r}
\left[
1+(r-1)\rho_g
\right],
\qquad
r_{\mathrm{eff}}
=
\frac{r}{1+(r-1)\rho_g}.
$$

Since

因为

$$
\frac{\partial r_{\mathrm{eff}}}{\partial \rho_g}
=
-
\frac{r(r-1)}
{\left[1+(r-1)\rho_g\right]^2}
<0
\quad(r>1),
$$

decorrelating redundant gradients strictly increases effective independent
optimization information under the exchangeable covariance model.

在 exchangeable covariance 模型下，降低冗余梯度相关性会严格提高有效独立优化信息量。

### Literature Anchor / 文献锚点

This is the same algebraic structure as design-effect / effective-sample-size
arguments in survey sampling and correlated Monte Carlo diagnostics. AMC-RTT
uses it as a gradient diagnostic, not as a claim about raw dataset size.

这与 survey sampling 和 correlated Monte Carlo diagnostics 中的 design effect /
effective sample size 具有相同代数结构。AMC-RTT 把它用作 gradient diagnostic，
不是原始数据量 claim。

## 4. Fisher / Logdet Information Volume / Fisher 与 Logdet 信息体积

### Statement / 命题

Let local gradient or score vectors be $v_i$ and define:

令局部梯度或 score vectors 为 $v_i$，定义：

$$
F=\sum_i v_i v_i^\top,
\qquad
V(F)=\log\det(I+\lambda F),
\qquad
\lambda>0.
$$

For $r$ duplicate directions $v_i=a u$, $\lVert u\rVert=1$:

若 $r$ 个方向完全重复，$v_i=a u$ 且 $\lVert u\rVert=1$：

$$
F_{\mathrm{dup}}
=
r a^2 u u^\top.
$$

The eigenvalues of $F_{\mathrm{dup}}$ are $r a^2,0,\ldots,0$, so:

$F_{\mathrm{dup}}$ 的特征值为 $r a^2,0,\ldots,0$，所以：

$$
V_{\mathrm{dup}}
=
\log(1+\lambda r a^2).
$$

For $r$ orthogonal equal-norm directions $v_i=a u_i$, with
$u_i^\top u_j=0$ for $i\ne j$:

若 $r$ 个等范数方向正交，$v_i=a u_i$ 且 $u_i^\top u_j=0$：

$$
F_{\mathrm{orth}}
=
a^2\sum_{i=1}^{r} u_i u_i^\top,
$$

whose nonzero eigenvalues are all $a^2$. Thus:

其非零特征值均为 $a^2$，因此：

$$
V_{\mathrm{orth}}
=
r\log(1+\lambda a^2).
$$

Let $x=\lambda a^2>0$. For $r>1$:

令 $x=\lambda a^2>0$。当 $r>1$：

$$
(1+x)^r
=
1+rx+\sum_{k=2}^{r}{r\choose k}x^k
>
1+rx.
$$

Taking logs:

取对数：

$$
r\log(1+x)
>
\log(1+rx).
$$

Therefore:

因此：

$$
V_{\mathrm{orth}}>V_{\mathrm{dup}}.
$$

### Positive De-Redundancy Direction / 正向去冗余方向

Under a fixed gradient-energy budget, replacing repeated directions with
independent task-relevant directions increases local information volume. This is
the mathematical backbone for measuring $\log\det(I+\lambda F)$ or effective
gradient rank before/after structured AMC.

在固定 gradient-energy 预算下，把重复方向替换为独立且任务相关的方向，会提高局部
信息体积。这正是 structured AMC 前后测量 $\log\det(I+\lambda F)$ 或 gradient
effective rank 的数学依据。

### Literature Anchor / 文献锚点

Effective rank is a standard way to summarize dimensionality from a spectrum
(Roy and Vetterli, 2007). Log-determinant information volume is standard in
D-optimal experimental design and information geometry.

effective rank 是用谱总结有效维度的标准工具（Roy and Vetterli, 2007）。
log-determinant 信息体积在 D-optimal design 与信息几何中是标准对象。

- Roy and Vetterli, EUSIPCO 2007, "The Effective Rank".

## 5. Complex-Scene Update Share / 复杂场景更新份额

### Conditional Theorem / 条件定理

Let a batch gradient decompose into repeated easy-scene direction and
rare/complex direction:

令 batch gradient 分解为重复 easy-scene 方向和 rare/complex 方向：

$$
g=ru+v,
\qquad
u^\top v=0,
\qquad
u\ne0,\ v\ne0.
$$

Assume normalized or clipped update:

假设使用 normalized 或 clipped update：

$$
\Delta\theta
=
-\eta G\frac{g}{\lVert g\rVert}.
$$

The magnitude of the update projected onto the complex direction is:

更新投影到复杂方向的幅值为：

$$
\phi(r)
=
\left|
\left\langle
\Delta\theta,
\frac{v}{\lVert v\rVert}
\right\rangle
\right|
=
\eta G
\frac{\lVert v\rVert}
{\sqrt{r^2\lVert u\rVert^2+\lVert v\rVert^2}}.
$$

Differentiate:

求导：

$$
\phi'(r)
=
-
\eta G\lVert v\rVert
\frac{r\lVert u\rVert^2}
{\left(r^2\lVert u\rVert^2+\lVert v\rVert^2\right)^{3/2}}
<0
\quad(r>0).
$$

Thus reducing redundant easy-scene multiplicity $r$ strictly increases the
normalized update share available to the complex direction.

因此，降低重复 easy-scene multiplicity $r$，会严格提高 normalized update 中复杂方向
获得的份额。

### Interpretation / 解释

This is a conditional theorem, not a blanket claim about every optimizer. It is
directly relevant when gradient clipping, normalization, or bounded update norms
are active. For Adam/AdamW, AMC-RTT should measure the realized projection and
optimizer-state effect.

这是条件定理，不是对所有 optimizer 的无条件 claim。当 gradient clipping、
normalization 或 bounded update norm 存在时，它直接相关。对 Adam/AdamW，
AMC-RTT 需要实测 realized projection 与 optimizer-state effect。

## 6. Fixed-Slot Jacobian Rank / 固定 Slot Jacobian 秩

### Proposition / 命题

For a persistent-slot decoder, let the output of slot $k$ be $y_k(\theta)$ and
define:

对于 persistent-slot decoder，令 slot $k$ 的输出为 $y_k(\theta)$，定义：

$$
J_k
=
\frac{\partial y_k}{\partial \theta},
\qquad
J
=
\begin{bmatrix}
J_1\\
\vdots\\
J_K
\end{bmatrix}.
$$

If $J_a=J_b$ for two slots, then row block $b$ adds no new row-space direction
beyond row block $a$:

若两个 slots 满足 $J_a=J_b$，则 row block $b$ 不会在 $J_a$ 之外增加新的
row-space 方向：

$$
\operatorname{rank}(J)
\le
K-1
\quad
\text{at the slot-block level}.
$$

For near-duplicate Jacobians, the small singular values of $J$ shrink, lowering
spectral effective rank:

对于近似重复的 Jacobian，$J$ 的小奇异值会缩小，从而降低谱有效秩：

$$
\operatorname{erank}(J J^\top)
=
\exp\left(
-
\sum_i
\tilde\lambda_i
\log \tilde\lambda_i
\right),
\qquad
\tilde\lambda_i
=
\frac{\lambda_i}{\sum_j \lambda_j}.
$$

### Positive De-Redundancy Direction / 正向去冗余方向

For Drive-JEPA-style persistent proposals, de-redundancy is valuable when it
creates distinct slot sensitivities, not merely different endpoint coordinates.
The measurement target should be output relation plus Jacobian/effective-rank
evidence.

对 Drive-JEPA 风格 persistent proposals，去冗余真正有价值的条件是产生不同 slot
sensitivity，而不仅仅是不同 endpoint 坐标。应同时测量 output relation 与
Jacobian/effective-rank 证据。

## 7. Decoder Transfer Theorem / Decoder 迁移定理

### Interface Theorem / 接口定理

If a decoder can expose $K$ differentiable hypotheses for each condition, and
an adapter maps them into a canonical action/outcome tensor, then AMC-RTT can
construct a decoder-agnostic relation:

如果 decoder 能为每个 condition 暴露 $K$ 个可微 hypotheses，并且 adapter 能把它们
映射到 canonical action/outcome tensor，那么 AMC-RTT 可以构造 decoder-agnostic
relation：

$$
A\in\mathbb{R}^{B\times K\times H\times D_a}
\quad\Rightarrow\quad
Z\in\mathbb{R}^{B\times K\times D_z}
\quad\Rightarrow\quad
S\in\mathbb{R}^{B\times K\times K}.
$$

This proves interface portability, not identical loss semantics.

这证明的是接口可迁移，不是相同 loss semantics。

### Positive Migration Rule / 正向迁移规则

For persistent-slot decoders, regularization can target slot freedom, output
Jacobian rank, and shared-gradient allocation.

对于 persistent-slot decoder，regularization 可以指向 slot freedom、output
Jacobian rank 与 shared-gradient allocation。

For stochastic diffusion/FM decoders, the positive theorem is the finite-$K$
coverage result: the loss should move probability mass away from repeated
dominant behaviors toward undercovered task-relevant behaviors, while preserving
support.

对于 stochastic diffusion/FM decoder，正向定理是 finite-$K$ coverage：loss 应把
概率质量从重复 dominant behavior 移向 undercovered task-relevant behavior，并保持
support。

### Literature Anchor / 文献锚点

- Drive-JEPA defines the motivating persistent-proposal autonomous-driving
  lineage.
- Diffusion Policy shows action diffusion as a multimodal continuous action
  decoder.
- Flow Matching provides the ODE/vector-field generative setting.
- VQ-BeT shows that action code capacity and latent action discretization are
  central in behavior generation.
- Forecasting WTA/GMM work directly motivates the problem that hard assignment
  can over-split or destabilize mode structure.

中文：

- Drive-JEPA 给出了 motivating persistent-proposal 自动驾驶路线；
- Diffusion Policy 展示了多模态连续动作 diffusion decoder；
- Flow Matching 提供 ODE/vector-field 生成设置；
- VQ-BeT 说明行为生成中的 action code capacity 与 latent action 离散化很关键；
- Forecasting WTA/GMM 工作直接支持 hard assignment 可能造成 mode 结构不稳定或过分割。

## 8. Reference Anchors / 权威文献锚点

The package cites authoritative papers in [references.bib](references.bib). The
most relevant public anchors are:

本包的权威文献记录在 [references.bib](references.bib)。最相关公开锚点如下：

- Drive-JEPA: <https://arxiv.org/abs/2601.22032>
- Rethinking WTA/GMM Forecasting: <https://arxiv.org/abs/2606.26424>
- DETR: <https://arxiv.org/abs/2005.12872>
- Diffusion Policy: <https://arxiv.org/abs/2303.04137>
- Flow Matching: <https://openreview.net/forum?id=PqvMRDCJT9t>
- VQ-BeT / Behavior Generation with Latent Actions: <https://proceedings.mlr.press/v235/lee24y.html>
- Effective Rank: <https://eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a5p-h05.pdf>
- GradNorm: <https://proceedings.mlr.press/v80/chen18a.html>
- PCGrad: <https://papers.nips.cc/paper/2020/hash/3fe78a8acf5fda99de95303940a2420c-Abstract.html>
- Calibration: <https://proceedings.mlr.press/v70/guo17a.html>

## 9. Claim Discipline / Claim 纪律

The positive mathematical route is strong:

正向数学路线是强的：

$$
\text{redundancy}
\Rightarrow
\text{coverage loss / gradient bias / lower ESS / lower information volume}
$$

under explicit assumptions. Therefore structured de-redundancy has a rigorous
mechanism target:

在明确假设下，冗余会导致覆盖损失、梯度偏置、有效样本数下降和信息体积下降。
因此 structured de-redundancy 有严格机制目标：

$$
\text{reduce repeated mass and correlated gradient directions}
\Rightarrow
\text{increase effective coverage and optimization information}.
$$

The final task-score step should be pursued as a proof program:

最终 task-score 步骤应作为证明程序推进：

$$
\text{gradient redundancy}\downarrow
\quad\land\quad
\operatorname{erank}(G_{\mathrm{grad}})\uparrow
\quad\land\quad
\text{hard-scene update share}\uparrow
\quad\land\quad
\text{task score}\uparrow.
$$

This framing is positive and mathematically honest: it gives future migration
models a clear route to prove success instead of asking them to accept an
unsupported slogan.

这种表述既正面又数学诚实：它给后续迁移模型一条清晰的证明成功路线，而不是要求它们
接受没有支撑的口号。
