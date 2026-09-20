# Next Decisions And Experiments / 下一步决策与实验

Status: `NEXT_STEP_STATIC_REPLAY_THEN_DM_FM_CONTRACT`

## Current Progress / 当前进度

AMC-RTT v1 has a tested synthetic math and adapter core:

```text
tests_v1: 8 passed
```

This does not prove task improvement. It proves the package now has a clean
generator-independent mathematical contract that can be tested without touching
Drive-JEPA code.

## Immediate Decision / 最近需要做出的决策

Choose the next branch:

1. `STATIC_REPLAY_FIRST` - recommended.
2. `REAL_DM_CONTRACT` - only after static replay parity.
3. `REAL_FM_CONTRACT` - only after static replay parity.
4. `TOY_DM_FM_SMOKE` - allowed if real DM/FM models are absent.

Recommended decision:

$$
\boxed{
\text{STATIC\_REPLAY\_FIRST}
}
$$

Reason: if the new core cannot reproduce legacy $K_{\rm eff}$, $\rho$, and
topology gradient on Drive-JEPA persisted records, then DM/FM success would be
scientifically meaningless.

## Experiment E00: Math Contract / 数学契约

Already passed synthetically:

- $K_{\rm eff}=K/[1+(K-1)\mu_1]$ parity;
- $\rho=\mu_1^2/\mu_2=E_{\rm eff}/M$ parity;
- analytic $\partial\log\rho/\partial q_e$ parity with autograd;
- DM epsilon/v endpoint reconstruction;
- FM linear endpoint reconstruction;
- same-time invariant.

## Experiment E01: Drive-JEPA Static Replay

Goal:

$$
\boxed{
\text{new v1 core reproduces legacy Drive-JEPA topology numbers}
}
$$

Inputs:

- persisted consequence latents or pair distances from A18/A19/A20/A26;
- no training;
- no AC-JEPA update;
- read-only wrapper import if needed.

Gates:

| metric | gate |
| --- | --- |
| legacy $K_{\rm eff}$ parity | max abs error $<10^{-6}$ |
| $\rho$ parity | max abs error $<10^{-6}$ |
| topology analytic/autograd gradient | max abs error $<10^{-6}$ |
| AC-JEPA parameter grads | exactly zero |

Fail action: stop DM/FM work and fix parity.

## Experiment E02: Diffusion Contract

Goal:

$$
\boxed{
\text{DM native state}
\rightarrow
\hat x_0
\rightarrow
\text{AMC-RTT core}
\quad\text{has finite gradients}
}
$$

Minimal gates:

- prediction type explicitly declared: `epsilon`, `x0`, or `v`;
- no topology on raw noise/score/epsilon vectors;
- same-time, cross-hypothesis metadata valid;
- finite $L_{\rm cap}$ and $L_{\rm topo}$;
- bounded AMC/native gradient ratio inside a configured SNR/time window.

Fail action: localize convention/time-scale issue; do not redesign AMC core.

## Experiment E03: Flow-Matching Contract

Goal:

$$
\boxed{
\text{FM native state}
\rightarrow
\hat x_1
\rightarrow
\text{AMC-RTT core}
\quad\text{has finite gradients}
}
$$

Minimal gates:

- `path_convention` explicit;
- endpoint reconstruction verified for oracle velocity;
- no topology on raw velocity vectors;
- gradient scale $(1-t)$ recorded;
- finite AMC/native gradient ratio.

Fail action: localize path convention/integration; do not redesign AMC core.

## What Not To Do Next / 下一步不要做什么

- Do not run long AMC training from A31/A32.
- Do not revive optimizer-credit redundancy as the main claim.
- Do not directly train on DiffusionDrive/FM before static replay parity.
- Do not treat $K_{\rm eff}$ reduction as capacity improvement by itself.
- Do not add semantic teacher guards back into the default core before
  independent confirmation.

## Plain-Language Next Goal / 通俗下一步目标

The next goal is not "make the score go up tomorrow." The next goal is:

> prove that AMC-RTT has one stable mathematical core, and only the clean-endpoint
> adapter changes across Drive-JEPA, diffusion, and flow matching.

中文：

> 下一步不是马上追分，而是证明 AMC-RTT 有一个稳定数学核心；跨 Drive-JEPA、
> Diffusion、Flow Matching 时只换 clean-endpoint adapter。
