# 07 AMC Training Regularizer

Status: `SUPPORTED_FOR_DRIVE_JEPA_EFFECTIVE_CALIBRATION`

AMC-v1 matches the student candidate set's effective multimodality to a frozen
teacher candidate set.

## Student

$$
Z_{\mathrm{pred}}=F_{\mathrm{frozen}}(c,Y_{\mathrm{pred}}),
\qquad
S_{\mathrm{pred}}=\operatorname{similarity}(Z_{\mathrm{pred}}),
\qquad
K_{\mathrm{pred}}=K_{\mathrm{eff}}(S_{\mathrm{pred}}).
$$

## Teacher

$$
Z_{\mathrm{teacher}}=F_{\mathrm{frozen}}(c,T_{\mathrm{teacher}}),
\qquad
S_{\mathrm{teacher}}=\operatorname{similarity}(Z_{\mathrm{teacher}}),
\qquad
K_{\mathrm{teacher}}=K_{\mathrm{eff}}(S_{\mathrm{teacher}}).
$$

Teacher values are stop-gradient targets:

$$
\operatorname{stopgrad}\!\left(\log K_{\mathrm{teacher}}\right).
$$

## Loss

$$
L_{\mathrm{AMC}}
=
\left[
\log K_{\mathrm{pred}}
-
\operatorname{stopgrad}(\log K_{\mathrm{teacher}})
\right]^2,
\qquad
L_{\mathrm{total}}
=
L_{\mathrm{task}}+\lambda L_{\mathrm{AMC}}.
$$

The teacher source is a pluggable interface:

```text
TeacherCandidateProvider(context) -> T_teacher
```

AMC itself does not define where teacher multimodality comes from.

## Drive-JEPA Evidence

Validated path:

- A3.2: real frozen AC-JEPA gradient smoke passed.
- A3.3: tiny AMC training path passed with original Drive-JEPA losses intact.
- A3.4: teacher target validity preflight passed.
- A3.5: Phase-II AMC training completed; `K_eff_pred` moved toward teacher.
- A3.6: longer validation found a good early window but possible collapse at
  the long endpoint.
- A3.7: coverage-aware AMC stabilized mean coverage under the tested rule.

A3.5 summary:

```text
K_eff_pred: 2.043266 -> 1.790320
abs_log_gap: 0.280503 -> 0.244442
teacher_coverage_2m: 0.981250 -> 0.993750
score: 0.972387 -> 0.969782
```

A3.7 summary:

```text
K_eff_pred: 2.0982 -> 1.7535
abs_log_gap: 0.2475 -> 0.2003
coverage@2m: 0.9812 -> 0.9812
score: 0.9582 -> 0.9525
```

## Gradient Ratio

Small `lambda` does not imply small optimization influence. Track:

$$
\rho
=
\frac{\lVert \lambda\nabla L_{\mathrm{AMC}}\rVert}
{\lVert\nabla L_{\mathrm{task}}\rVert}.
$$

or the corresponding auxiliary/base ratio when coverage terms are included.

## Correct Claim

Supported:

```text
effective multimodality calibration / redundancy-aware consolidation
```

Not supported:

```text
proposal cardinality reduction
planning quality improvement
mode-preserving compression solved
```
