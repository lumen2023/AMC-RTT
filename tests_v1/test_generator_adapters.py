import pytest
import torch

from v1_core import (
    DiffusionCleanEndpointAdapter,
    FlowMatchingCleanEndpointAdapter,
    HypothesisMetadata,
    assert_same_time_cross_hypothesis,
)


def _metadata(k: int, generation_time: float = 0.5):
    return tuple(
        HypothesisMetadata(
            hypothesis_id=f"h{i}",
            generator_family="synthetic",
            sample_source="unit_test",
            generation_time=generation_time,
            noise_seed=i,
        )
        for i in range(k)
    )


def test_diffusion_epsilon_clean_reconstruction_and_gradient_scale() -> None:
    torch.manual_seed(1)
    x0 = torch.randn(2, 4, 3, 2, dtype=torch.float64)
    eps = torch.randn_like(x0)
    alpha = torch.tensor(0.8, dtype=torch.float64)
    sigma = torch.tensor(0.6, dtype=torch.float64)
    x_t = alpha * x0 + sigma * eps

    eps_hat = eps.clone().detach().requires_grad_(True)
    adapter = DiffusionCleanEndpointAdapter("epsilon")
    out = adapter.to_clean_hypotheses(
        x_t,
        eps_hat,
        alpha_t=alpha,
        sigma_t=sigma,
        metadata=_metadata(4, generation_time=0.25),
    )
    assert torch.allclose(out.trajectory, x0, atol=1e-12, rtol=1e-12)

    scalar = out.trajectory[0, 0, 0, 0]
    (grad,) = torch.autograd.grad(scalar, eps_hat)
    assert abs(grad[0, 0, 0, 0].item() + (sigma / alpha).item()) < 1e-12
    assert abs(adapter.conditioning_ratio(alpha_t=alpha, sigma_t=sigma).item() - 0.75) < 1e-12


def test_diffusion_v_prediction_clean_reconstruction() -> None:
    torch.manual_seed(2)
    x0 = torch.randn(1, 5, 2, 3, dtype=torch.float64)
    eps = torch.randn_like(x0)
    alpha = torch.tensor(0.6, dtype=torch.float64)
    sigma = torch.tensor(0.8, dtype=torch.float64)
    x_t = alpha * x0 + sigma * eps
    v = alpha * eps - sigma * x0

    adapter = DiffusionCleanEndpointAdapter("v")
    out = adapter.to_clean_hypotheses(
        x_t,
        v,
        alpha_t=alpha,
        sigma_t=sigma,
        metadata=_metadata(5, generation_time="snr_window_mid"),
    )
    assert torch.allclose(out.trajectory, x0, atol=1e-12, rtol=1e-12)


def test_flow_matching_endpoint_projection_and_gradient_scale() -> None:
    torch.manual_seed(3)
    x_base = torch.randn(2, 3, 4, 2, dtype=torch.float64)
    x_data = torch.randn_like(x_base)
    t = torch.tensor(0.35, dtype=torch.float64)
    x_t = (1.0 - t) * x_base + t * x_data
    u = (x_data - x_base).detach().requires_grad_(True)

    adapter = FlowMatchingCleanEndpointAdapter()
    out = adapter.to_clean_hypotheses(
        x_t,
        u,
        t=t,
        metadata=_metadata(3, generation_time=0.35),
    )
    assert torch.allclose(out.trajectory, x_data, atol=1e-12, rtol=1e-12)

    scalar = out.trajectory[0, 0, 0, 0]
    (grad,) = torch.autograd.grad(scalar, u)
    assert abs(grad[0, 0, 0, 0].item() - (1.0 - t).item()) < 1e-12
    assert abs(adapter.gradient_scale(t=t).item() - (1.0 - t).item()) < 1e-12


def test_same_time_invariant_rejects_time_axis_as_hypothesis_axis() -> None:
    x = torch.zeros(1, 3, 2, 2)
    adapter = DiffusionCleanEndpointAdapter("x0")
    bad_meta = (
        HypothesisMetadata("h0", "diffusion", "unit", generation_time=0),
        HypothesisMetadata("h1", "diffusion", "unit", generation_time=1),
        HypothesisMetadata("h2", "diffusion", "unit", generation_time=2),
    )
    with pytest.raises(ValueError, match="same generative time"):
        out = adapter.to_clean_hypotheses(x, x, alpha_t=1.0, sigma_t=0.0, metadata=bad_meta)
        assert_same_time_cross_hypothesis(out)
