"""
Pydantic schemas for Congressional Trade Evaluation (v2).
Implements schemas for Evidence Packets, Investor Profiles, Model Outputs, and JEV Reports.
"""

from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Part 0: Investor Profile Schemas
# ---------------------------------------------------------------------------

class InvestorProfile(BaseModel):
    investor_id: Literal["A", "B", "C", "D"]
    investor_name: str
    hard_constraint: str
    risk_appetite: Literal["Conservative", "Moderate", "Aggressive"]
    target_horizon: Literal["3M", "6M", "9M"]
    max_single_position_pct: float


# ---------------------------------------------------------------------------
# Part 1: Evidence Packet Schemas
# ---------------------------------------------------------------------------

class PoliticianInfo(BaseModel):
    name: str
    party: Optional[str] = None
    chamber: Optional[str] = None
    state_district: Optional[str] = None
    committees: List[str] = Field(default_factory=list)


class AssetInfo(BaseModel):
    ticker: Optional[str] = None
    asset_name: Optional[str] = None
    asset_type: Optional[str] = None


class TradeInfo(BaseModel):
    transaction_type: Optional[str] = None
    owner: Optional[str] = None
    amount_range: Optional[str] = None
    amount_min_usd: Optional[float] = None
    amount_max_usd: Optional[float] = None
    price_per_share: Optional[float] = None


class TimingInfo(BaseModel):
    transaction_date: str
    filing_date: str
    days_to_disclosure: int


class SourceInfo(BaseModel):
    source_url: Optional[str] = None
    data_origin: Optional[str] = None


class EvidencePacket(BaseModel):
    trade_id: str
    politician: PoliticianInfo
    asset: AssetInfo
    trade: TradeInfo
    timing: TimingInfo
    source: SourceInfo
    data_quality_flags: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Part 1: Model Output Schemas
# ---------------------------------------------------------------------------

class ModelMetadata(BaseModel):
    model_name: str
    model_version: str
    prompt_version: str = "v2"
    evaluation_timestamp: str
    trade_id: str
    investor_id: Literal["A", "B", "C", "D"]


class ConstraintCheck(BaseModel):
    resolved_ticker: Optional[str] = None
    issuer_sector: Optional[str] = None
    issuer_listing: Optional[str] = None
    passes: Optional[bool] = None
    borderline: bool = False
    explanation: str


class HorizonForecast(BaseModel):
    direction: Literal["BULLISH", "NEUTRAL", "BEARISH"]
    expected_alpha_vs_spy_pct: float


class FitToInvestor(BaseModel):
    risk_fit: Optional[Literal["GOOD", "PARTIAL", "POOR"]] = None
    horizon_fit: Optional[Literal["GOOD", "PARTIAL", "POOR"]] = None
    suggested_allocation_pct: float = 0.0


class EvidenceQuality(BaseModel):
    conviction_bracket: Literal["HIGH", "MEDIUM", "LOW"]
    timing_freshness: Literal["FRESH (<15d)", "MODERATE (15-30d)", "STALE (>30d)"]


class ModelOutput(BaseModel):
    metadata: ModelMetadata
    constraint_check: ConstraintCheck
    signal: Literal["BUY", "HOLD", "SELL", "ABSTAIN"]
    abstain_reason: Optional[
        Literal[
            "CONSTRAINT_FAIL",
            "CONSTRAINT_UNVERIFIABLE",
            "STALE_DISCLOSURE",
            "LOW_CONVICTION",
            "INSUFFICIENT_EVIDENCE",
            "CONFLICTING_EVIDENCE",
        ]
    ] = None
    probability: float = 0.0
    optimal_horizon: Optional[Literal["3M", "6M", "9M"]] = None
    horizon_forecasts: Optional[Dict[str, HorizonForecast]] = None
    fit_to_investor: Optional[FitToInvestor] = None
    evidence_quality: Optional[EvidenceQuality] = None
    rationale: str
    cited_evidence: List[str] = Field(default_factory=list)
    key_assumptions: List[str] = Field(default_factory=list)
    risks_and_uncertainties: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Part 2: JEV Output Schemas
# ---------------------------------------------------------------------------

class JEVMetadata(BaseModel):
    report_id: str
    trade_id: str
    investor_id: Literal["A", "B", "C", "D"]
    jev_version: str
    rubric_version: str = "v2"
    timestamp: str


class JEVConstraintCheck(BaseModel):
    passes: Optional[bool] = None
    borderline: bool = False
    explanation: str


class RubricScores(BaseModel):
    R1_constraint_accuracy: int = Field(ge=0, le=5)
    R2_traceability: int = Field(ge=0, le=5)
    R3_timing_awareness: int = Field(ge=0, le=5)
    R4_instrument_rigor: int = Field(ge=0, le=5)
    R5_investor_fit: int = Field(ge=0, le=5)
    R6_uncertainty_handling: int = Field(ge=0, le=5)
    R7_internal_consistency: int = Field(ge=0, le=5)
    R8_time_boundary_hygiene: int = Field(ge=0, le=5)


class ModelEvaluation(BaseModel):
    model_id: str
    model_signal: Optional[Literal["BUY", "HOLD", "SELL", "ABSTAIN"]] = None
    status: Literal["SELECTED", "WEIGHTED", "DISCOUNTED", "UNAVAILABLE", "INVALID_OUTPUT"]
    weight_assigned: float = 0.0
    rubric_scores: RubricScores
    strengths: List[str] = Field(default_factory=list)
    flaws: List[str] = Field(default_factory=list)
    critique: str


class DiscountedModelInfo(BaseModel):
    model_id: str
    reason: str


class ModelSelectionAnalytics(BaseModel):
    selected_models: List[str] = Field(default_factory=list)
    discounted_models: List[DiscountedModelInfo] = Field(default_factory=list)
    selection_rationale: str
    consensus_summary: str
    dissent_summary: str
    constraint_disagreement: str


class FinalCall(BaseModel):
    signal: Literal["BUY", "HOLD", "SELL", "ABSTAIN"]
    abstain_reason: Optional[
        Literal[
            "CONSTRAINT_FAIL",
            "CONSTRAINT_UNVERIFIABLE",
            "STALE_DISCLOSURE",
            "LOW_CONVICTION",
            "INSUFFICIENT_EVIDENCE",
            "CONFLICTING_EVIDENCE",
            "EXCESSIVE_DISAGREEMENT",
        ]
    ] = None
    horizon: Optional[Literal["3M", "6M", "9M"]] = None
    final_rationale: str
    key_evidence: List[str] = Field(default_factory=list)
    key_risks: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    what_would_change_the_call: List[str] = Field(default_factory=list)


class JEVReport(BaseModel):
    metadata: JEVMetadata
    jev_constraint_check: JEVConstraintCheck
    model_evaluations: List[ModelEvaluation]
    model_selection_analytics: ModelSelectionAnalytics
    final_call: FinalCall
    investor_message: str
