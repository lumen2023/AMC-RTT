# AMC-RTT v1 Theory / v1 理论

Status: `MATH_CORE_TESTED_SYNTHETICALLY`

## 1. Generator-Agnostic Object / 生成器无关对象

Let a generator produce $K$ clean future hypotheses under condition $c$:

$$
\mathcal{T}(c)=\{\tau_1,\ldots,\tau_K\}.
$$

A frozen consequence encoder maps each hypothesis to:

$$
h_i=\Phi_{\rm AC}(c,\tau_i).
$$

AMC-RTT v1 begins only after this map. This is the architectural boundary:

$$
\boxed{
\text{native generator state}
\rightarrow
\text{clean trajectory hypothesis}
\rightarrow
\Phi_{\rm AC}
\rightarrow
\text{consequence topology}.
}
$$

## 2. Pair Moments / Pair 矩

Define:

$$
q_{ij}=\lVert h_i-h_j\rVert^2,
\qquad
S_{ij}=\exp\left(-\frac{q_{ij}}{\tau_h^2}\right),
\qquad
w_{ij}=S_{ij}^2.
$$

For $M=\binom K2$:

$$
\mu_1=\frac{1}{M}\sum_{i<j}w_{ij},
\qquad
\mu_2=\frac{1}{M}\sum_{i<j}w_{ij}^2.
$$

Interpretation:

- $\mu_1$: pairwise redundancy density;
- $\mu_2$: second moment of redundancy mass;
- $\rho=\mu_1^2/\mu_2$: redundancy concentration.

## 3. Effective Capacity Identity / 有效容量恒等式

Legacy:

$$
K_{\rm eff}
=
\frac{K^2}{\operatorname{tr}(S^2)}.
$$

Because $S_{ii}=1$:

$$
\operatorname{tr}(S^2)
=
\sum_{i,j}S_{ij}^2
=
K+2\sum_{i<j}w_{ij}.
$$

Using $\sum_{i<j}w_{ij}=M\mu_1$ and $2M=K(K-1)$:

$$
\operatorname{tr}(S^2)
=
K+K(K-1)\mu_1
=
K\left[1+(K-1)\mu_1\right].
$$

Therefore:

$$
\boxed{
K_{\rm eff}
=
\frac{K}{1+(K-1)\mu_1}.
}
$$

This identity is tested in `tests_v1/test_math_contract.py`.

## 4. Reference Capacity / Reference 容量

For DM/FM, a training bank may use $K_{\rm bank}=8$ while Drive-JEPA uses
$K=32$. Directly comparing $K_{\rm eff}^{(8)}$ and $K_{\rm eff}^{(32)}$ mixes
cardinality with redundancy density.

Use a reference cardinality:

$$
\boxed{
K_{\rm eff}^{\rm ref}
=
\frac{K_{\rm ref}}{1+(K_{\rm ref}-1)\hat\mu_1}.
}
$$

Important boundary:

$$
\hat\mu_1
=
\frac{1}{\binom{K_{\rm bank}}2}
\sum_{i<j}w_{ij}
$$

is a natural pair-average estimator. After the nonlinear map
$f(\hat\mu_1)=K_{\rm eff}^{\rm ref}$, v1 calls it a sample/reference estimator,
not an unbiased estimator.

## 5. Topology Concentration / 拓扑集中度

Legacy edge effective count:

$$
E_{\rm eff}
=
\frac{\left(\sum_{i<j}w_{ij}\right)^2}
{\sum_{i<j}w_{ij}^2}.
$$

Normalize by $M=\binom K2$:

$$
\rho
=
\frac{E_{\rm eff}}{M}
=
\frac{(M\mu_1)^2}{M(M\mu_2)}
=
\boxed{\frac{\mu_1^2}{\mu_2}}.
$$

Thus $\rho$ is cardinality-normalized edge-mass concentration.

## 6. Selective Topology Gradient / 选择性拓扑梯度

Let:

$$
A=\sum_e w_e,\qquad B=\sum_e w_e^2,\qquad
\rho=\frac{A^2}{BM}.
$$

Then:

$$
\log\rho=2\log A-\log B-\log M.
$$

Since:

$$
w_e=\exp\left(-\frac{2q_e}{\tau_h^2}\right),
\qquad
\frac{\partial w_e}{\partial q_e}
=
-\frac{2}{\tau_h^2}w_e,
$$

we get:

$$
\frac{\partial\log A}{\partial q_e}
=
-\frac{2}{\tau_h^2}\frac{w_e}{A}
=
-\frac{2}{\tau_h^2}p_e,
$$

and:

$$
\frac{\partial\log B}{\partial q_e}
=
\frac{1}{B}2w_e\frac{\partial w_e}{\partial q_e}
=
-\frac{4}{\tau_h^2}\frac{w_e^2}{B}
=
-\frac{4}{\tau_h^2}r_e.
$$

Therefore:

$$
\boxed{
\frac{\partial\log\rho}{\partial q_e}
=
\frac{4}{\tau_h^2}(r_e-p_e).
}
$$

If $r_e>p_e$, gradient descent on a positive topology penalty decreases $q_e$,
consolidating a strong edge. If $r_e<p_e$, gradient descent increases $q_e$,
releasing diffuse weak edges. This is the formal reason topology-aware AMC is
more selective than scalar $K_{\rm eff}$ matching.

## 7. Literature Anchors / 文献锚点

- DETR shows that set prediction often needs uniqueness constraints through
  bipartite matching.
- The WTA/GMM forecasting line supports the observation that hard assignment can
  over-split or destabilize nearby modes.
- Effective rank provides the spectral language for effective dimensionality.
- GradNorm and PCGrad support the need to reason about gradient magnitudes and
  conflicts, while A31/A32 show that this is not the current central object for
  Drive-JEPA final-layer AMC-RTT.
