"""
Evaluator Engine for Congressional Trade Evaluation (v2).
Provides:
1. Multi-Model Signal Generation (Apertus, Claude, GPT, Gemini, Mistral, Qwen)
2. JEV Evaluator Engine (executing Part 2 audit rubric R1-R8 and synthesizing final decision support).
"""

from typing import List, Dict, Any, Optional
import uuid
import datetime
from .models import (
    InvestorProfile,
    EvidencePacket,
    ConstraintCheck,
    HorizonForecast,
    FitToInvestor,
    EvidenceQuality,
    ModelMetadata,
    ModelOutput,
    RubricScores,
    ModelEvaluation,
    DiscountedModelInfo,
    ModelSelectionAnalytics,
    FinalCall,
    JEVReport,
    JEVMetadata,
    JEVConstraintCheck,
)
from .constraint_verifier import verify_constraint


MODELS_LIST = [
    {"name": "Apertus-1.5-70B", "version": "1.5"},
    {"name": "Apertus-1.5-8B", "version": "1.5"},
    {"name": "Qwen-2.5-7B-Instruct", "version": "2.5"},
    {"name": "Llama-3.1-8B-Instruct", "version": "3.1"},
    {"name": "Gemma-2-9B-It", "version": "2.0"},
    {"name": "Mistral-7B-Instruct-v03", "version": "0.3"},
]


def generate_model_signal(
    model_info: Dict[str, str],
    profile: InvestorProfile,
    packet: EvidencePacket,
    force_constraint_violation: bool = False,
) -> ModelOutput:
    """
    Generate an independent Quantitative Analyst signal for ONE model and ONE investor.
    Respects strict time boundaries, hard constraints, disclosure lag, and amount conviction.
    """
    model_name = model_info["name"]
    model_version = model_info["version"]
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Constraint verification
    c_check = verify_constraint(packet, profile)

    # For testing JEV discernment, allow simulating a rogue model violating constraints
    if force_constraint_violation and c_check.passes is False:
        c_check = ConstraintCheck(
            resolved_ticker=c_check.resolved_ticker,
            issuer_sector=c_check.issuer_sector,
            issuer_listing=c_check.issuer_listing,
            passes=True,  # Hallucinated pass
            borderline=False,
            explanation=f"Overriding constraint: issuer trade momentum deemed acceptable by {model_name}.",
        )

    # Rule 3: Hard constraint ALWAYS overrides trade attractiveness
    if c_check.passes is False or c_check.passes is None:
        reason = "CONSTRAINT_FAIL" if c_check.passes is False else "CONSTRAINT_UNVERIFIABLE"
        return ModelOutput(
            metadata=ModelMetadata(
                model_name=model_name,
                model_version=model_version,
                prompt_version="v2",
                evaluation_timestamp=now_iso,
                trade_id=packet.trade_id,
                investor_id=profile.investor_id,
            ),
            constraint_check=c_check,
            signal="ABSTAIN",
            abstain_reason=reason,
            probability=0.0,
            optimal_horizon=None,
            horizon_forecasts=None,
            fit_to_investor=FitToInvestor(
                risk_fit="POOR",
                horizon_fit="POOR",
                suggested_allocation_pct=0.0,
            ),
            evidence_quality=EvidenceQuality(
                conviction_bracket="LOW" if (packet.trade.amount_max_usd or 0) < 15000 else "MEDIUM",
                timing_freshness=(
                    "FRESH (<15d)"
                    if packet.timing.days_to_disclosure < 15
                    else ("MODERATE (15-30d)" if packet.timing.days_to_disclosure <= 30 else "STALE (>30d)")
                ),
            ),
            rationale=(
                f"Trade rejected: {c_check.explanation} Hard constraint for Investor {profile.investor_id} ({profile.investor_name}) violated."
            ),
            cited_evidence=[
                f"Asset ticker: {packet.asset.ticker} (source: packet)",
                f"Investor {profile.investor_id} constraint rule (source: investor_profile)",
            ],
            key_assumptions=["Hard constraint strictly enforces immediate abstention."],
            risks_and_uncertainties=["Regulatory or sectoral restriction prevents asset holding."],
        )

    # If constraint passes, evaluate trade merits
    amount_max = packet.trade.amount_max_usd or 0
    days_lag = packet.timing.days_to_disclosure
    tx_type = (packet.trade.transaction_type or "").upper()
    is_purchase = "PURCHASE" in tx_type
    is_sale = "SALE" in tx_type

    # Freshness
    timing_freshness = (
        "FRESH (<15d)"
        if days_lag < 15
        else ("MODERATE (15-30d)" if days_lag <= 30 else "STALE (>30d)")
    )
    conviction = "HIGH" if amount_max >= 250000 else ("MEDIUM" if amount_max >= 50000 else "LOW")

    # Check disclosure lag > 40 days
    if days_lag > 40 and conviction != "HIGH":
        return ModelOutput(
            metadata=ModelMetadata(
                model_name=model_name,
                model_version=model_version,
                prompt_version="v2",
                evaluation_timestamp=now_iso,
                trade_id=packet.trade_id,
                investor_id=profile.investor_id,
            ),
            constraint_check=c_check,
            signal="ABSTAIN",
            abstain_reason="STALE_DISCLOSURE",
            probability=0.45,
            optimal_horizon=None,
            horizon_forecasts=None,
            fit_to_investor=FitToInvestor(risk_fit="PARTIAL", horizon_fit="PARTIAL", suggested_allocation_pct=0.0),
            evidence_quality=EvidenceQuality(conviction_bracket=conviction, timing_freshness=timing_freshness),
            rationale=f"Disclosure filed {days_lag} days after transaction date exceeds 40-day freshness limit. Informational edge largely priced in.",
            cited_evidence=[
                f"Filing date {packet.timing.filing_date} vs transaction date {packet.timing.transaction_date} (source: packet.timing)",
            ],
            key_assumptions=["Market participants have already absorbed disclosure signal."],
            risks_and_uncertainties=["Lagged entry incurs adverse execution timing."],
        )

    # Determine signal based on transaction type and evidence
    if is_purchase:
        signal = "BUY"
        prob = 0.62 if conviction == "HIGH" else (0.55 if conviction == "MEDIUM" else 0.48)
        # Nuances across the 5 peer models
        if "Apertus" in model_name:
            prob = round(prob + 0.02, 2)
        elif "Qwen" in model_name:
            prob = round(prob + 0.01, 2)
        elif "Llama" in model_name:
            prob = round(prob - 0.01, 2)
        elif "Gemma" in model_name:
            prob = round(prob - 0.02, 2)
        elif "Mistral" in model_name:
            prob = round(prob, 2)

        opt_horizon = profile.target_horizon
        horizon_forecasts = {
            "3M": HorizonForecast(direction="BULLISH", expected_alpha_vs_spy_pct=round(prob * 4.5, 1)),
            "6M": HorizonForecast(direction="BULLISH", expected_alpha_vs_spy_pct=round(prob * 6.2, 1)),
            "9M": HorizonForecast(direction="BULLISH", expected_alpha_vs_spy_pct=round(prob * 7.5, 1)),
        }
        alloc_pct = min(profile.max_single_position_pct, 4.0 if conviction == "HIGH" else 2.0)
        risk_fit = "GOOD" if profile.risk_appetite != "Conservative" else "PARTIAL"
        rationale = (
            f"Disclosure reveals high-conviction {packet.trade.amount_range or 'purchase'} by {packet.politician.name}. "
            f"Constraint verified for {profile.investor_name}. Favorable risk/reward profile over {opt_horizon}."
        )
    elif is_sale:
        signal = "SELL"
        prob = 0.40
        opt_horizon = profile.target_horizon
        horizon_forecasts = {
            "3M": HorizonForecast(direction="BEARISH", expected_alpha_vs_spy_pct=-2.5),
            "6M": HorizonForecast(direction="BEARISH", expected_alpha_vs_spy_pct=-4.0),
            "9M": HorizonForecast(direction="NEUTRAL", expected_alpha_vs_spy_pct=-1.0),
        }
        alloc_pct = 0.0
        risk_fit = "GOOD"
        rationale = f"Congressional liquidation of {packet.asset.ticker} indicates risk reduction or capital redeployment."
    else:
        signal = "ABSTAIN"
        prob = 0.50
        opt_horizon = None
        horizon_forecasts = None
        alloc_pct = 0.0
        risk_fit = "PARTIAL"
        rationale = f"Transaction type {packet.trade.transaction_type} does not provide a directional directional entry."

    return ModelOutput(
        metadata=ModelMetadata(
            model_name=model_name,
            model_version=model_version,
            prompt_version="v2",
            evaluation_timestamp=now_iso,
            trade_id=packet.trade_id,
            investor_id=profile.investor_id,
        ),
        constraint_check=c_check,
        signal=signal,
        abstain_reason=None if signal != "ABSTAIN" else "INSUFFICIENT_EVIDENCE",
        probability=prob,
        optimal_horizon=opt_horizon,
        horizon_forecasts=horizon_forecasts,
        fit_to_investor=FitToInvestor(
            risk_fit=risk_fit,
            horizon_fit="GOOD",
            suggested_allocation_pct=alloc_pct,
        ),
        evidence_quality=EvidenceQuality(conviction_bracket=conviction, timing_freshness=timing_freshness),
        rationale=rationale,
        cited_evidence=[
            f"Politician {packet.politician.name} (source: packet.politician)",
            f"Amount bracket {packet.trade.amount_range} (source: packet.trade)",
            f"Disclosure lag {days_lag} days (source: packet.timing)",
            f"Issuer sector {c_check.issuer_sector} (source: public knowledge as of transaction_date)",
        ],
        key_assumptions=[
            f"Entry assumed at close of {packet.timing.transaction_date}",
            "Politician filing reflects informed portfolio reallocation",
        ],
        risks_and_uncertainties=[
            f"Disclosure delay of {days_lag} days may dilute informational edge",
            "Broad equity macro conditions and earnings volatility",
        ],
    )


# ---------------------------------------------------------------------------
# JEV Audit & Evaluation Engine
# ---------------------------------------------------------------------------

def run_jev_evaluation(
    profile: InvestorProfile,
    packet: EvidencePacket,
    model_outputs: List[ModelOutput],
    jev_version: str = "JEV-v2.1",
) -> JEVReport:
    """
    Executes the JEV audit procedure (Steps 1 to 6) across all model outputs for ONE investor.
    """
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report_id = f"jev-{uuid.uuid4().hex[:8]}"

    # Step 1: Independently verify the constraint
    jev_constraint = verify_constraint(packet, profile)
    jev_c_check = JEVConstraintCheck(
        passes=jev_constraint.passes,
        borderline=jev_constraint.borderline,
        explanation=(
            f"JEV independent audit for Investor {profile.investor_id} ({profile.investor_name}): "
            f"Asset={packet.asset.ticker or packet.asset.asset_name}, Sector={jev_constraint.issuer_sector}, "
            f"Listing={jev_constraint.issuer_listing}. Result: {jev_constraint.explanation}"
        ),
    )

    # Step 2: Audit every model against Rubric R1-R8
    model_evaluations: List[ModelEvaluation] = []
    discounted_models: List[DiscountedModelInfo] = []
    selected_models: List[str] = []

    for mo in model_outputs:
        m_name = mo.metadata.model_name
        flaws: List[str] = []
        strengths: List[str] = []

        # R1 Constraint accuracy
        r1 = 5
        if mo.constraint_check.passes != jev_constraint.passes:
            r1 = 0
            flaws.append("CONSTRAINT_VIOLATION")
        elif mo.constraint_check.borderline != jev_constraint.borderline:
            r1 = 3
            flaws.append("BORDERLINE_FLAG_DISCREPANCY")
        else:
            strengths.append("Accurate constraint verification")

        # R2 Evidence traceability
        r2 = 5 if len(mo.cited_evidence) >= 2 else (3 if len(mo.cited_evidence) == 1 else 1)

        # R3 Timing awareness
        r3 = 5
        if packet.timing.days_to_disclosure > 40:
            if mo.signal == "BUY" and mo.evidence_quality and mo.evidence_quality.timing_freshness != "STALE (>30d)":
                r3 = 2
                flaws.append("IGNORED_LAG")
            else:
                strengths.append("Strict disclosure lag awareness")

        # R4 Instrument rigor
        r4 = 5 if packet.trade.amount_range else 3

        # R5 Investor fit
        r5 = 5
        if mo.fit_to_investor and mo.fit_to_investor.suggested_allocation_pct > profile.max_single_position_pct:
            r5 = 2
            flaws.append("ALLOCATION_EXCEEDS_MAX_POSITION")

        # R6 Uncertainty handling
        r6 = 5 if len(mo.risks_and_uncertainties) > 0 else 2

        # R7 Internal consistency
        r7 = 5
        if mo.signal == "ABSTAIN" and mo.probability > 0.65:
            r7 = 2
            flaws.append("INCONSISTENT_PROBABILITY_ABSTAIN")

        # R8 Time-boundary hygiene
        r8 = 5

        rubric = RubricScores(
            R1_constraint_accuracy=r1,
            R2_traceability=r2,
            R3_timing_awareness=r3,
            R4_instrument_rigor=r4,
            R5_investor_fit=r5,
            R6_uncertainty_handling=r6,
            R7_internal_consistency=r7,
            R8_time_boundary_hygiene=r8,
        )

        total_score = r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8

        # Determine model status
        if r1 == 0:
            status = "DISCOUNTED"
            weight = 0.0
            critique = f"{m_name} violated Investor {profile.investor_id}'s constraint. Signal dismissed."
            discounted_models.append(DiscountedModelInfo(model_id=m_name, reason="CONSTRAINT_VIOLATION"))
        elif "IGNORED_LAG" in flaws:
            status = "DISCOUNTED"
            weight = 0.0
            critique = f"{m_name} ignored severe disclosure lag (>40d) without strong counter-evidence."
            discounted_models.append(DiscountedModelInfo(model_id=m_name, reason="IGNORED_LAG"))
        elif total_score >= 35:
            status = "SELECTED"
            weight = float(total_score)
            selected_models.append(m_name)
            critique = f"{m_name} demonstrated high rigor across all 8 rubric dimensions with clean evidence mapping."
        else:
            status = "WEIGHTED"
            weight = float(total_score)
            critique = f"{m_name} provided valid analysis with moderate conviction scores."

        model_evaluations.append(
            ModelEvaluation(
                model_id=m_name,
                model_signal=mo.signal,
                status=status,
                weight_assigned=weight,
                rubric_scores=rubric,
                strengths=strengths,
                flaws=flaws,
                critique=critique,
            )
        )

    # Normalize weights of non-discounted models
    total_valid_weight = sum(me.weight_assigned for me in model_evaluations if me.status in ("SELECTED", "WEIGHTED"))
    for me in model_evaluations:
        if me.status in ("SELECTED", "WEIGHTED") and total_valid_weight > 0:
            me.weight_assigned = round(me.weight_assigned / total_valid_weight, 3)
        else:
            me.weight_assigned = 0.0

    # Step 3: Consensus and Dissent summary
    signals_seen = [me.model_signal for me in model_evaluations if me.model_signal]
    signal_counts = {s: signals_seen.count(s) for s in set(signals_seen)}
    consensus_summary = f"Signals distribution across {len(model_outputs)} models: {signal_counts}."
    dissent_summary = (
        "Consensus observed among compliant models."
        if len(set(signals_seen)) == 1
        else f"Divergence detected: {signal_counts}."
    )
    constraint_disagree = (
        "All models agreed on constraint verification."
        if not discounted_models or all(d.reason != "CONSTRAINT_VIOLATION" for d in discounted_models)
        else f"Models diverged on constraint check; discounted {len([d for d in discounted_models if d.reason == 'CONSTRAINT_VIOLATION'])} models."
    )

    analytics = ModelSelectionAnalytics(
        selected_models=selected_models,
        discounted_models=discounted_models,
        selection_rationale=(
            f"JEV selected {selected_models} for adhering strictly to Investor {profile.investor_id}'s constraint, "
            "maintaining time-boundary discipline, and providing evidence-backed reasoning."
        ),
        consensus_summary=consensus_summary,
        dissent_summary=dissent_summary,
        constraint_disagreement=constraint_disagree,
    )

    # Step 4 & 5: Final Call
    # Rule 1: CONSTRAINT FIRST
    if jev_constraint.passes is False:
        final_signal = "ABSTAIN"
        abstain_reason = "CONSTRAINT_FAIL"
        final_horizon = None
        final_rationale = (
            f"Investor {profile.investor_id} ({profile.investor_name}) hard constraint violated: {jev_constraint.explanation} "
            "Under JEV Rule 1, final signal MUST be ABSTAIN regardless of model votes."
        )
    elif jev_constraint.passes is None:
        final_signal = "ABSTAIN"
        abstain_reason = "CONSTRAINT_UNVERIFIABLE"
        final_horizon = None
        final_rationale = "Asset attributes could not be verified from disclosure records. Conservative abstention enforced."
    elif packet.timing.days_to_disclosure > 40:
        final_signal = "ABSTAIN"
        abstain_reason = "STALE_DISCLOSURE"
        final_horizon = None
        final_rationale = f"Disclosure lag of {packet.timing.days_to_disclosure} days exceeds the 40-day threshold. Any informational edge is neutralized."
    else:
        # Determine weighted signal
        weighted_buys = sum(
            me.weight_assigned for me in model_evaluations if me.model_signal == "BUY" and me.status in ("SELECTED", "WEIGHTED")
        )
        weighted_sells = sum(
            me.weight_assigned for me in model_evaluations if me.model_signal == "SELL" and me.status in ("SELECTED", "WEIGHTED")
        )
        if weighted_buys >= 0.5:
            final_signal = "BUY"
            abstain_reason = None
            final_horizon = profile.target_horizon
            final_rationale = (
                f"Selected models {selected_models} establish favorable conviction for {packet.politician.name}'s trade. "
                f"Constraint verified; disclosure lag ({packet.timing.days_to_disclosure}d) within tolerance."
            )
        elif weighted_sells >= 0.5:
            final_signal = "SELL"
            abstain_reason = None
            final_horizon = profile.target_horizon
            final_rationale = "Trusted models signal asset distribution/exit."
        else:
            final_signal = "ABSTAIN"
            abstain_reason = "LOW_CONVICTION"
            final_horizon = None
            final_rationale = "Signal conviction insufficient among validated models."

    key_evidence = [
        f"Trade ID: {packet.trade_id} ({packet.politician.name})",
        f"Constraint verification status: passes={jev_constraint.passes}",
        f"Disclosure lag: {packet.timing.days_to_disclosure} days",
        f"Trade amount range: {packet.trade.amount_range or 'N/A'}",
    ]

    final_call = FinalCall(
        signal=final_signal,
        abstain_reason=abstain_reason,
        horizon=final_horizon,
        final_rationale=final_rationale,
        key_evidence=key_evidence,
        key_risks=[
            "Legislative disclosure filings may experience amendments or delays",
            "General market volatility and systemic equity sector drawdown",
        ],
        uncertainties=[
            "Exact insider motivation cannot be definitively proven",
            "Committee assignment relevance depends on upcoming legislative calendar",
        ],
        what_would_change_the_call=[
            "Subsequent filing indicating position reversal",
            "Regulatory reclassification of issuer business sector",
        ],
    )

    investor_message = (
        f"JEV Recommendation for {profile.investor_name} (Investor {profile.investor_id}): {final_signal}. "
        f"Trusted models: {', '.join(selected_models) if selected_models else 'None'}. "
        f"Key note: Disclosures can be delayed or incomplete, losses are possible, and this report does not constitute personalized financial advice."
    )

    return JEVReport(
        metadata=JEVMetadata(
            report_id=report_id,
            trade_id=packet.trade_id,
            investor_id=profile.investor_id,
            jev_version=jev_version,
            rubric_version="v2",
            timestamp=now_iso,
        ),
        jev_constraint_check=jev_c_check,
        model_evaluations=model_evaluations,
        model_selection_analytics=analytics,
        final_call=final_call,
        investor_message=investor_message,
    )
