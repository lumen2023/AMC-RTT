"""Framework-neutral interfaces for AMC-RTT v1.0.

This file is intentionally standalone. It defines Protocols and lightweight
dataclasses only; it does not import Drive-JEPA, AC-JEPA, torch, numpy, or any
project module. Concrete projects should adapt these interfaces to their own
tensor framework.

The API deliberately separates decoder semantics, canonicalization, relation
metrics, redundancy statistics, and regularization policy. A common
``K_eff`` statistic must not silently imply a common loss for persistent slots,
stochastic samples, and codebook entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


TensorLike = Any


class SampleSemantics(str, Enum):
    """Meaning of the K axis for capacity claims."""

    PERSISTENT_SLOT = "persistent_slot"
    STOCHASTIC_SAMPLE = "stochastic_sample"
    CODEBOOK_ENTRY = "codebook_entry"


class DecoderFamily(str, Enum):
    """Decoder family used for transfer-risk bookkeeping."""

    PROPOSAL = "proposal"
    DIFFUSION = "diffusion"
    FLOW_MATCHING = "flow_matching"
    AUTOREGRESSIVE = "autoregressive"
    MIXTURE = "mixture"
    QUERY = "query"
    OTHER = "other"


@dataclass(frozen=True)
class TensorContract:
    """Canonical semantic contract.

    The actual runtime tensor may be flattened internally, but redundancy
    computation must receive the explicit ``[B,K,...]`` structure.
    """

    batch_axis: str = "B"
    candidate_axis: str = "K"
    horizon_axis: str = "H"
    action_axis: str = "D_a"
    latent_horizon_axis: str = "H_z"
    latent_axis: str = "D_z"
    affinity_shape: tuple[str, ...] = ("B", "K", "K")


@dataclass(frozen=True)
class DecoderSemantics:
    """Decoder and sample semantics carried with every candidate set."""

    family: DecoderFamily
    sample_semantics: SampleSemantics
    persistent_identity: bool
    candidate_count: int | None = None
    notes: str = ""


@dataclass(frozen=True)
class CandidateBatch:
    """Decoded multimodal candidates.

    Expected semantic shape:
        candidates: [B,K,T,D_y]
        actions: optional [B,K,H,D_a]
    """

    context: Mapping[str, Any]
    candidates: TensorLike
    actions: TensorLike | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    semantics: DecoderSemantics | None = None
    valid_mask: TensorLike | None = None
    delta_t: TensorLike | None = None
    action_scaling: Mapping[str, Any] | None = None


DecodedSet = CandidateBatch


@dataclass(frozen=True)
class RelationMatrices:
    """Pairwise distance and similarity matrices."""

    distances: TensorLike
    similarities: TensorLike
    tau: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EffectiveMultimodality:
    """Effective multimodality estimate and companion diagnostics."""

    k_eff: TensorLike
    affinity_mass: TensorLike | None = None
    edge_participation: TensorLike | None = None
    row_effective_neighbors: TensorLike | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RegularizerOutput:
    """Auxiliary redundancy loss and guard metrics."""

    loss: TensorLike
    metrics: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DiagnosticsReport:
    """No-training or post-training redundancy diagnostics."""

    rows: Sequence[Mapping[str, Any]]
    summary: Mapping[str, Any]
    status: str


class DecoderAdapter(Protocol):
    """Decoder boundary before any redundancy computation."""

    def decode_multimodal(
        self,
        context: Mapping[str, Any],
        num_candidates: int,
    ) -> CandidateBatch:
        """Decode candidates and preserve explicit [B,K,...] semantics."""

    def canonicalize(self, decoded: TensorLike, batch_size: int, num_candidates: int) -> CandidateBatch:
        """Restore [B,K,...] after any internal [B*K,...] flattening."""


class CandidateDecoderAdapter(Protocol):
    """Decode K candidates from a context."""

    def decode_candidates(self, context: Mapping[str, Any], num_candidates: int) -> CandidateBatch:
        """Return candidates with semantic shape [B,K,T,D_y]."""


class TaskRepresentationAdapter(Protocol):
    """Convert decoded candidates to the representation expected by the task evaluator."""

    def to_actions(self, batch: CandidateBatch) -> CandidateBatch:
        """Attach or replace `batch.actions` without detaching candidate gradients."""


class TaskOutcomeEvaluator(Protocol):
    """Optional task score or cost provider for diagnostic relations."""

    def evaluate(self, batch: CandidateBatch) -> TensorLike:
        """Return task score/cost for candidates, usually [B,K]."""


class FrozenConsequenceEncoder(Protocol):
    """Frozen task-aware encoder.

    Implementations must freeze parameters while preserving gradients with
    respect to candidate actions or trajectories when used in training.
    """

    def encode(self, batch: CandidateBatch) -> TensorLike:
        """Return consequence latents, commonly [B,K,...]."""


class SimilarityMetric(Protocol):
    """Pairwise distance and similarity computation."""

    def pairwise(self, latents: TensorLike, tau: float | None = None) -> RelationMatrices:
        """Return distances and similarities with shape [B,K,K]."""


class RelationMetric(Protocol):
    """Explicit relation stage, separated from decoder and statistics."""

    def compute_relation(
        self,
        latents: TensorLike,
        valid_mask: TensorLike | None = None,
        tau: float | None = None,
    ) -> RelationMatrices:
        """Compute pairwise relations within each condition batch only."""


class EffectiveMultimodalityEstimator(Protocol):
    """Estimate effective candidate-set cardinality from a similarity matrix."""

    def estimate(self, relations: RelationMatrices) -> EffectiveMultimodality:
        """Return K_eff and topology companion statistics."""


class RedundancyStatistic(Protocol):
    """Compute scalar and topology statistics without choosing a loss."""

    def compute_statistics(self, relations: RelationMatrices) -> EffectiveMultimodality:
        """Return K_eff, rho, and companion diagnostics."""


class TeacherCandidateProvider(Protocol):
    """Provide teacher/reference candidates for AMC targets."""

    def get_teacher_candidates(self, context: Mapping[str, Any]) -> CandidateBatch:
        """Return teacher candidates with semantic shape [B,M,T,D_y]."""


class CoverageConstraint(Protocol):
    """Optional coverage/collapse stabilizer."""

    def loss(self, student: CandidateBatch, teacher: CandidateBatch | None = None) -> RegularizerOutput:
        """Return a coverage-preservation loss and metrics."""


class RedundancyRegularizer(Protocol):
    """Compute the redundancy auxiliary loss."""

    def loss(
        self,
        student: EffectiveMultimodality,
        teacher: EffectiveMultimodality | None = None,
    ) -> RegularizerOutput:
        """Return AMC or topology-aware AMC loss."""


class RegularizationPolicy(Protocol):
    """Decoder-aware policy that maps statistics to a training loss."""

    def compute_regularizer(
        self,
        student: EffectiveMultimodality,
        teacher: EffectiveMultimodality | None,
        semantics: DecoderSemantics,
    ) -> RegularizerOutput:
        """Choose a loss only after decoder/sample semantics are known."""


class RedundancyDiagnostics(Protocol):
    """No-training and post-training audits."""

    def run(
        self,
        batch: CandidateBatch,
        relations: RelationMatrices,
        effective: EffectiveMultimodality,
        teacher: CandidateBatch | None = None,
    ) -> DiagnosticsReport:
        """Return topology, coverage, and claim-boundary diagnostics."""


def required_adapter_methods() -> tuple[str, ...]:
    """Minimal methods a new project usually implements."""

    return (
        "DecoderAdapter.decode_multimodal",
        "DecoderAdapter.canonicalize",
        "TaskRepresentationAdapter.to_actions",
        "FrozenConsequenceEncoder.encode",
    )


def _shape_of(value: TensorLike) -> tuple[int, ...]:
    """Return a concrete shape without depending on a tensor framework."""

    shape = getattr(value, "shape", None)
    if shape is None:
        raise TypeError("value must expose a .shape attribute")
    return tuple(int(dim) for dim in shape)


def validate_canonical_batch(batch: CandidateBatch) -> tuple[int, int, int, int]:
    """Validate the minimum canonical candidate contract.

    Returns ``(B, K, T, D)`` for candidates. This intentionally checks only
    structural invariants; domain-specific manifolds need a task adapter.
    """

    candidate_shape = _shape_of(batch.candidates)
    if len(candidate_shape) != 4:
        raise ValueError(f"candidates must have shape [B,K,T,D], got {candidate_shape}")
    batch_size, candidate_count, horizon, feature_dim = candidate_shape
    if batch_size <= 0 or candidate_count <= 0 or horizon <= 0 or feature_dim <= 0:
        raise ValueError(f"candidate dimensions must be positive, got {candidate_shape}")

    if batch.actions is not None:
        action_shape = _shape_of(batch.actions)
        if len(action_shape) != 4 or action_shape[:2] != (batch_size, candidate_count):
            raise ValueError(
                "actions must have shape [B,K,H,D_a] with the same B,K as candidates; "
                f"got {action_shape} versus {candidate_shape}"
            )

    if batch.valid_mask is not None:
        mask_shape = _shape_of(batch.valid_mask)
        if mask_shape[:2] != (batch_size, candidate_count):
            raise ValueError(
                "valid_mask must begin with [B,K] and cannot mix conditions; "
                f"got {mask_shape} versus {candidate_shape}"
            )

    if batch.semantics is not None and batch.semantics.candidate_count is not None:
        if batch.semantics.candidate_count != candidate_count:
            raise ValueError(
                "semantics.candidate_count disagrees with candidate tensor: "
                f"{batch.semantics.candidate_count} versus {candidate_count}"
            )
    return candidate_shape


def canonicalize_flat_candidates(
    flat_candidates: TensorLike,
    batch_size: int,
    candidate_count: int,
) -> TensorLike:
    """Restore ``[B,K,...]`` from ``[B*K,...]``.

    This helper is deliberately explicit because treating ``B*K`` as one
    condition is the most dangerous cross-scene affinity failure.
    """

    flat_shape = _shape_of(flat_candidates)
    if len(flat_shape) < 2:
        raise ValueError(f"flat candidates must have rank >=2, got {flat_shape}")
    expected = int(batch_size) * int(candidate_count)
    if flat_shape[0] != expected:
        raise ValueError(
            f"leading dimension {flat_shape[0]} does not equal B*K={expected}; "
            "refusing to mix candidate sets across conditions"
        )
    reshape = getattr(flat_candidates, "reshape", None)
    if reshape is None:
        raise TypeError("flat_candidates must expose reshape")
    return reshape(int(batch_size), int(candidate_count), *flat_shape[1:])


def validate_relation_shape(relations: RelationMatrices, batch_size: int, candidate_count: int) -> None:
    """Reject relation matrices that could mix different condition batches."""

    expected = (int(batch_size), int(candidate_count), int(candidate_count))
    distance_shape = _shape_of(relations.distances)
    similarity_shape = _shape_of(relations.similarities)
    if distance_shape != expected or similarity_shape != expected:
        raise ValueError(
            "relation matrices must have shape [B,K,K] for the same condition batch; "
            f"got distances={distance_shape}, similarities={similarity_shape}, expected={expected}"
        )
