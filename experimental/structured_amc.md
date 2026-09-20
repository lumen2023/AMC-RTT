# Structured AMC

Status: `EXPERIMENTAL_DESIGN_ONLY`

Structured AMC addresses the A18 limitation: scalar `K_eff` matching controls
the amount of affinity mass but not its topology.

## Notation

For student proposals:

```text
S_ij = exp(-q_ij / tau^2)
q_ij = d_ij^2
w_ij = S_ij^2
A = sum_{i<j} w_ij
B = sum_{i<j} w_ij^2
K_eff = K^2 / (K + 2A)
E_eff = A^2 / B
rho = E_eff / C(K,2)
```

For teacher candidates:

```text
K_T = K_eff(teacher)
rho_T = E_eff(teacher) / C(M,2)
```

Both are stop-gradient targets.

## Candidate Loss

```text
L_K = (log K_eff(pred) - stopgrad(log K_T))^2

L_topo =
  [log rho_pred - stopgrad(log rho_T + m_rho)]_+^2

L_TA_AMC = L_K + alpha * L_topo
```

The hinge avoids forcing over-concentration when the student is already no more
diffuse than the teacher target.

## Gradient Intuition

For:

```text
p_ij = w_ij / A
r_ij = w_ij^2 / B
zeta = log rho_pred - stopgrad(log rho_T + m_rho)
```

when `zeta > 0`:

```text
d log rho_pred / d q_ij = 4 / tau^2 * (r_ij - p_ij)
d L_topo / d q_ij = 8 * zeta / tau^2 * (r_ij - p_ij)
```

High-mass edges are strengthened; low-mass diffuse edges are weakened.

## Required Preflight

Before any training:

- teacher `rho_T` finite;
- teacher topology non-degenerate;
- not a pure teacher-count artifact;
- teacher source/hash matches previous AMC pipeline;
- same trajectory-to-action encoding for student and teacher;
- frozen evaluator params remain frozen;
- topology gradient is not collinear with AMC-v1 gradient;
- no oracle labels are used in the deployable loss.

## Claim Boundary

Supported by A18-A20:

```text
topology-aware credit assignment is mathematically distinct from K_eff matching
```

Not supported:

```text
TA-AMC improves planning
TA-AMC is ready for full training
```

