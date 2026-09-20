"""AMC-RTT v1 generator-agnostic math core.

This package is intentionally standalone. It does not import Drive-JEPA code and
does not assume whether hypotheses came from fixed slots, diffusion samples, or
flow-matching particles.
"""

from .core import (
    AffinityMoments,
    affinity_from_latents,
    effective_capacity_ref,
    pair_moments_from_affinity,
    pairwise_squared_distances,
    topology_log_rho_grad_q,
    upper_triangular_values,
)
from .adapters import (
    CleanHypotheses,
    DiffusionCleanEndpointAdapter,
    FlowMatchingCleanEndpointAdapter,
    HypothesisMetadata,
    assert_same_time_cross_hypothesis,
)

__all__ = [
    "AffinityMoments",
    "CleanHypotheses",
    "DiffusionCleanEndpointAdapter",
    "FlowMatchingCleanEndpointAdapter",
    "HypothesisMetadata",
    "affinity_from_latents",
    "assert_same_time_cross_hypothesis",
    "effective_capacity_ref",
    "pair_moments_from_affinity",
    "pairwise_squared_distances",
    "topology_log_rho_grad_q",
    "upper_triangular_values",
]
