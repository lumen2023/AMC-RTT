import torch

from v1_core import (
    affinity_from_latents,
    effective_capacity_ref,
    pair_moments_from_affinity,
    topology_log_rho_grad_q,
)


def test_k_eff_pair_density_identity() -> None:
    torch.manual_seed(20260920)
    h = torch.randn(3, 7, 5, dtype=torch.float64)
    S = affinity_from_latents(h, tau_h=0.73)
    moments = pair_moments_from_affinity(S)
    err = (moments.k_eff_legacy - moments.k_eff_density).abs().max().item()
    assert err < 1e-10, err


def test_reference_capacity_uses_pair_density_not_bank_cardinality() -> None:
    mu1 = torch.tensor([0.0, 0.25, 1.0], dtype=torch.float64)
    k_ref = effective_capacity_ref(mu1, 32)
    expected = 32.0 / (1.0 + 31.0 * mu1)
    assert torch.allclose(k_ref, expected)
    assert k_ref[0].item() == 32.0
    assert abs(k_ref[-1].item() - 1.0) < 1e-12


def test_rho_matches_edge_eff_normalized() -> None:
    torch.manual_seed(7)
    h = torch.randn(2, 6, 4, dtype=torch.float64)
    S = affinity_from_latents(h, tau_h=1.1)
    moments = pair_moments_from_affinity(S, eps=0.0)
    rho_from_edge_eff = moments.edge_eff / moments.pair_count
    assert torch.allclose(moments.rho, rho_from_edge_eff, atol=1e-12, rtol=1e-12)


def test_topology_log_rho_gradient_matches_autograd() -> None:
    torch.manual_seed(19)
    tau_h = 0.83
    q = torch.rand(4, 10, dtype=torch.float64, requires_grad=True)
    w = torch.exp(-2.0 * q / (tau_h * tau_h))
    mu1 = w.mean(dim=-1)
    mu2 = (w * w).mean(dim=-1)
    log_rho = torch.log(mu1 * mu1 / mu2).sum()
    (grad_auto,) = torch.autograd.grad(log_rho, q)
    grad_formula = topology_log_rho_grad_q(q.detach(), tau_h=tau_h, eps=0.0)
    assert torch.allclose(grad_auto, grad_formula, atol=1e-10, rtol=1e-10)
