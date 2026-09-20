from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class AffinityMoments:
    """Cardinality-normalized consequence-topology statistics."""

    mu1: torch.Tensor
    mu2: torch.Tensor
    rho: torch.Tensor
    k_eff_legacy: torch.Tensor
    k_eff_density: torch.Tensor
    edge_eff: torch.Tensor
    pair_count: int


def _check_latents(h: torch.Tensor) -> None:
    if h.ndim != 3:
        raise ValueError(f"expected h[B,K,D], got shape {tuple(h.shape)}")
    if h.shape[1] < 2:
        raise ValueError("K must be at least 2 for pair topology")


def pairwise_squared_distances(h: torch.Tensor) -> torch.Tensor:
    """Return q_ij = ||h_i - h_j||^2 for h[B,K,D]."""

    _check_latents(h)
    delta = h[:, :, None, :] - h[:, None, :, :]
    return (delta * delta).sum(dim=-1)


def affinity_from_latents(h: torch.Tensor, tau_h: float) -> torch.Tensor:
    """Return S_ij = exp(-q_ij / tau_h^2) from consequence latents."""

    if tau_h <= 0:
        raise ValueError("tau_h must be positive")
    q = pairwise_squared_distances(h)
    return torch.exp(-q / (tau_h * tau_h))


def upper_triangular_values(x: torch.Tensor) -> torch.Tensor:
    """Extract i<j entries from x[B,K,K] as x_pairs[B,M]."""

    if x.ndim != 3 or x.shape[1] != x.shape[2]:
        raise ValueError(f"expected x[B,K,K], got shape {tuple(x.shape)}")
    k = x.shape[1]
    i, j = torch.triu_indices(k, k, offset=1, device=x.device)
    return x[:, i, j]


def effective_capacity_ref(mu1: torch.Tensor, k_ref: int) -> torch.Tensor:
    """Map pair redundancy density to a reference sample/proposal cardinality."""

    if k_ref < 2:
        raise ValueError("k_ref must be at least 2")
    return k_ref / (1.0 + (k_ref - 1.0) * mu1)


def pair_moments_from_affinity(S: torch.Tensor, eps: float = 1e-12) -> AffinityMoments:
    """Compute pair moments and legacy-equivalent K_eff from affinity S[B,K,K].

    Let w_ij = S_ij^2 for i<j and M = K choose 2. Then

        mu1 = M^{-1} sum w_ij
        mu2 = M^{-1} sum w_ij^2
        K_eff = K / [1 + (K-1) mu1]
        rho = mu1^2 / mu2 = E_eff / M

    The K_eff identity is equivalent to K^2 / tr(S^2) when S_ii = 1.
    """

    if S.ndim != 3 or S.shape[1] != S.shape[2]:
        raise ValueError(f"expected S[B,K,K], got shape {tuple(S.shape)}")
    k = S.shape[1]
    if k < 2:
        raise ValueError("K must be at least 2")

    pairs = upper_triangular_values(S)
    w = pairs * pairs
    mu1 = w.mean(dim=-1)
    mu2 = (w * w).mean(dim=-1)
    pair_count = k * (k - 1) // 2

    k_eff_density = effective_capacity_ref(mu1, k)
    tr_s2 = (S * S).sum(dim=(-1, -2))
    k_eff_legacy = (k * k) / tr_s2

    A = w.sum(dim=-1)
    B = (w * w).sum(dim=-1)
    edge_eff = (A * A) / (B + eps)
    rho = (mu1 * mu1) / (mu2 + eps)

    return AffinityMoments(
        mu1=mu1,
        mu2=mu2,
        rho=rho,
        k_eff_legacy=k_eff_legacy,
        k_eff_density=k_eff_density,
        edge_eff=edge_eff,
        pair_count=pair_count,
    )


def topology_log_rho_grad_q(q_pairs: torch.Tensor, tau_h: float, eps: float = 1e-12) -> torch.Tensor:
    """Analytic d log(rho) / d q_e for edge distances q_e.

    For w_e = exp(-2 q_e / tau_h^2), p_e = w_e / sum w, and
    r_e = w_e^2 / sum w^2:

        d log rho / d q_e = 4 / tau_h^2 * (r_e - p_e).
    """

    if q_pairs.ndim != 2:
        raise ValueError(f"expected q_pairs[B,M], got shape {tuple(q_pairs.shape)}")
    if tau_h <= 0:
        raise ValueError("tau_h must be positive")

    w = torch.exp(-2.0 * q_pairs / (tau_h * tau_h))
    p = w / (w.sum(dim=-1, keepdim=True) + eps)
    w2 = w * w
    r = w2 / (w2.sum(dim=-1, keepdim=True) + eps)
    return (4.0 / (tau_h * tau_h)) * (r - p)
