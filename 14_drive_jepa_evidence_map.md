# 14 Drive-JEPA Evidence Map

Status: `EVIDENCE_INDEX`

This map separates supported methods, diagnostics, failures, and superseded
interpretations.

| item | status | supported claim | unsupported claim |
| --- | --- | --- | --- |
| A2.4 local information audit | `SUPPORTED_DIAGNOSTIC` | frozen latent adds local relation information | set-level compression |
| A2.7 full-support relation audit | `SUPPORTED_DIAGNOSTIC` | `G+A+Z/H` improves relation prediction beyond `G+A` | deployable compression |
| A2.8 risk-calibrated Safe Cover | `LIMITED_OR_FAILED` | exact selector shows oracle headroom and learned relation bottleneck | strict matched-safety K reduction |
| A3.2 real AC-JEPA gradient smoke | `SUPPORTED` | frozen AC-JEPA can pass nonzero gradients to candidate actions while params stay frozen | planner improvement |
| A3.3 tiny AMC pilot | `SUPPORTED_SMOKE` | original planner loss plus tiny AMC path runs | mature objective |
| A3.4 teacher target validity | `SUPPORTED_PREFLIGHT` | teacher `K_eff` finite, non-degenerate, not count-only | teacher relation target is perfect |
| A3.5 Phase-II AMC | `SUPPORTED_BOUNDED` | `K_eff_pred` moves toward teacher | proposal count reduction |
| A3.6 long horizon | `LIMITED` | useful early window; long endpoint can trigger collapse gate | unlimited stable training |
| A3.7 coverage-aware AMC | `SUPPORTED_STABILIZATION` | stable mean coverage with lower `K_eff` | task score improvement |
| A3.8-A4.1 structure diagnostics | `DIAGNOSTIC_ONLY` | redundancy structure and collapse risk can be measured | direct fix |
| A5-A9 mode/boundary audits | `DIAGNOSTIC_ONLY` | false merge and teacher-boundary issues are real | representation fix authorized |
| A10-A13 calibration audits | `DIAGNOSTIC_ONLY` | calibration and scalar reliability can be separated | calibrated scalar is sufficient |
| A14 rich support audit | `SUPERSEDED_INTERPRETATION` | mixed features can predict target variance | rich AC-JEPA support proved |
| A15 support deconfounding | `SUPPORTED_NEGATIVE` | teacher margin explains much of A14 gain | multi-horizon AC-JEPA support gate passes |
| A16 self-dependency audit | `SUPPORTED_NEGATIVE` | target-side teacher-ADE features reconstruct `Q` | target prediction proves model support |
| A17 relation target decision | `DECISION` | teacher relation target needs redesign/audit | planner training authorized |
| A18 credit assignment audit | `SUPPORTED_DIAGNOSTIC` | AMC-v1 creates diffuse smoothing | capacity efficiency proved |
| A19 structured gradient simulation | `SUPPORTED_READONLY_DESIGN` | topology-aware fields look promising in simulation | deployable objective validated |
| A20 topology-aware design memo | `DESIGN_ONLY` | `K_eff` amount and topology are distinct constraints | TA-AMC improves planning |

## Current Mainline Boundary

As of A17-A20:

```text
do not launch planner training from A14/A15 teacher-relation reconstruction
do not claim rich AC-JEPA relation support
do not claim universal decoder transfer
```

Authorized direction:

```text
read-only target audit / topology-aware objective preflight
external DM/FM Level 0-2 transfer validation
```

