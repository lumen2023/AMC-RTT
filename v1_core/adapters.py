from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch


@dataclass(frozen=True)
class HypothesisMetadata:
    """Metadata required to keep hypothesis and generative-time axes separate."""

    hypothesis_id: str
    generator_family: str
    sample_source: str
    generation_time: float | int | str
    anchor_id: str | None = None
    noise_seed: int | None = None


@dataclass(frozen=True)
class CleanHypotheses:
    """Canonical clean hypothesis set.

    `trajectory` must be [B,K,T,D]. The topology core only compares the K axis
    within the same batch condition and at the same generation-time convention.
    """

    trajectory: torch.Tensor
    metadata: tuple[HypothesisMetadata, ...]


def _check_clean_shape(x: torch.Tensor) -> None:
    if x.ndim != 4:
        raise ValueError(f"expected clean trajectory [B,K,T,D], got {tuple(x.shape)}")
    if x.shape[1] < 2:
        raise ValueError("K must be at least 2")


def assert_same_time_cross_hypothesis(clean: CleanHypotheses) -> None:
    """Reject accidental use of generative-time steps as semantic hypotheses."""

    _check_clean_shape(clean.trajectory)
    if len(clean.metadata) != clean.trajectory.shape[1]:
        raise ValueError(
            f"metadata length {len(clean.metadata)} must equal K={clean.trajectory.shape[1]}"
        )
    times = {m.generation_time for m in clean.metadata}
    if len(times) != 1:
        raise ValueError(
            "AMC topology requires same generative time across hypotheses; "
            f"got generation_time values {sorted(map(str, times))}"
        )


class DiffusionCleanEndpointAdapter:
    """Map diffusion native predictions to clean trajectory hypotheses."""

    def __init__(self, prediction_type: str) -> None:
        allowed = {"epsilon", "x0", "v"}
        if prediction_type not in allowed:
            raise ValueError(f"prediction_type must be one of {sorted(allowed)}")
        self.prediction_type = prediction_type

    def to_clean_hypotheses(
        self,
        x_t: torch.Tensor,
        prediction: torch.Tensor,
        *,
        alpha_t: torch.Tensor | float,
        sigma_t: torch.Tensor | float,
        metadata: tuple[HypothesisMetadata, ...],
    ) -> CleanHypotheses:
        _check_clean_shape(x_t)
        if prediction.shape != x_t.shape:
            raise ValueError("prediction must have the same shape as x_t")

        alpha = torch.as_tensor(alpha_t, dtype=x_t.dtype, device=x_t.device)
        sigma = torch.as_tensor(sigma_t, dtype=x_t.dtype, device=x_t.device)

        if self.prediction_type == "epsilon":
            clean = (x_t - sigma * prediction) / alpha
        elif self.prediction_type == "x0":
            clean = prediction
        else:
            # Common v-prediction convention with alpha^2 + sigma^2 = 1:
            # v = alpha * epsilon - sigma * x0, hence x0 = alpha*x_t - sigma*v.
            clean = alpha * x_t - sigma * prediction

        out = CleanHypotheses(trajectory=clean, metadata=metadata)
        assert_same_time_cross_hypothesis(out)
        return out

    def conditioning_ratio(
        self,
        *,
        alpha_t: torch.Tensor | float,
        sigma_t: torch.Tensor | float,
    ) -> torch.Tensor:
        """Return |d x0_hat / d eps_hat| for epsilon prediction."""

        alpha = torch.as_tensor(alpha_t)
        sigma = torch.as_tensor(sigma_t)
        return torch.abs(sigma / alpha)


class FlowMatchingCleanEndpointAdapter:
    """Map flow-matching native velocity predictions to clean endpoints."""

    def __init__(self, path_convention: str = "linear_x0_to_x1") -> None:
        if path_convention != "linear_x0_to_x1":
            raise ValueError(
                "v1 supports only path_convention='linear_x0_to_x1'; "
                "other conventions must implement an explicit endpoint adapter"
            )
        self.path_convention = path_convention

    def to_clean_hypotheses(
        self,
        x_t: torch.Tensor,
        v_hat: torch.Tensor,
        *,
        t: torch.Tensor | float,
        metadata: tuple[HypothesisMetadata, ...],
        extra: dict[str, Any] | None = None,
    ) -> CleanHypotheses:
        _check_clean_shape(x_t)
        if v_hat.shape != x_t.shape:
            raise ValueError("v_hat must have the same shape as x_t")
        t_tensor = torch.as_tensor(t, dtype=x_t.dtype, device=x_t.device)
        clean = x_t + (1.0 - t_tensor) * v_hat
        out = CleanHypotheses(trajectory=clean, metadata=metadata)
        assert_same_time_cross_hypothesis(out)
        return out

    def gradient_scale(self, *, t: torch.Tensor | float) -> torch.Tensor:
        """Return |d x1_hat / d v_hat| = |1-t| for the linear path."""

        return torch.abs(1.0 - torch.as_tensor(t))
