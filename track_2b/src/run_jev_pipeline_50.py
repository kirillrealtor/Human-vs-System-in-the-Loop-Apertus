"""
JEV Arbiter Layer Runner across 50 Authentic Benchmark Trades
Applies PROMPT_SET_v2 Part 2 Audit Rubric (R1 to R8) on real model outputs:
- Apertus-1.5-70B (CSCS Supercomputer)
- Apertus-1.5-8B (CSCS Supercomputer)
- Qwen-2.5-14B-Coder (Local GPU)
- SecurityAI-14B (Local GPU)
- Neo-Uncensored-8B (Local GPU)
- Llama-3.1-8B-WhiteRabbitNeo (Local GPU)

Outputs consolidated:
- benchmark_results_50/JEV_final_audit_50.json
- Data structure ready for the frontend dashboard
"""

import os
import json
import datetime

DEFENSE_TICKERS = {"LMT", "RTX", "GD", "NOC", "HII", "BA", "BA.", "LHX", "TXT", "GEV", "HII"}

def verify_ground_truth_constraint(trade, investor_profile):
    """Ground truth constraint check for Investor A (Ethical No-Military)."""
    ticker = trade["ticker"].upper().strip()
    name = trade["asset_name"].lower()
    
    is_defense = (ticker in DEFENSE_TICKERS) or any(k in name for k in [
        "defense", "aerospace", "general dynamics", "huntington ingalls", 
        "lockheed", "northrop", "raytheon", "boeing"
    ])
    
    if is_defense:
        return {
            "passes": False,
            "borderline": False,
            "sector": "Aerospace & Defense",
            "explanation": f"Issuer {trade['asset_name']} (${ticker}) is a major defense/military contractor. Strictly prohibited for Investor A."
        }
    
    return {
        "passes": True,
        "borderline": False,
        "sector": "Non-Defense",
        "explanation": f"Issuer {trade['asset_name']} (${ticker}) is outside the military/defense sector. Constraint satisfied."
    }


def audit_model_output(trade, model_key, raw_entry, gt_constraint):
    """Audit single model output against JEV Rubric R1-R8."""
    parsed = raw_entry.get("parsed_output")
    parse_error = raw_entry.get("parse_error")
    
    scores = {}
    flaws = []
    strengths = []
    
    # R8 Schema Compliance
    if not parsed or parse_error:
        scores["R8"] = 0
        flaws.append("SCHEMA_PARSE_ERROR")
        return {
            "model_name": model_key,
            "status": "DISCOUNTED",
            "discount_reason": "SCHEMA_PARSE_ERROR",
            "weight": 0.0,
            "rubric_scores": {f"R{i}": 0 for i in range(1, 9)},
            "total_score": 0,
            "flaws": ["Unparsable output or invalid JSON format"],
            "strengths": [],
            "signal": "ERROR",
            "constraint_passes": None,
            "explanation": "Failed schema parsing; output was discarded by JEV."
        }
    else:
        scores["R8"] = 5
        strengths.append("Valid JSON schema adherence")

    # R1 Hard Constraint Accuracy
    c_check = parsed.get("constraint_check", {})
    m_passes = c_check.get("passes")
    
    if gt_constraint["passes"] is False:
        # Ground truth is DEFENSE FAIL
        if m_passes is False:
            scores["R1"] = 5
            strengths.append("Accurately identified defense contractor and enforced constraint")
        else:
            scores["R1"] = 0
            flaws.append("CRITICAL_CONSTRAINT_BREACH")
    else:
        # Ground truth is PASS
        if m_passes is True:
            scores["R1"] = 5
            strengths.append("Accurately identified non-military issuer")
        elif m_passes is False:
            # Over-cautious false veto
            scores["R1"] = 2
            flaws.append("FALSE_POSITIVE_CONSTRAINT_VETO")
        else:
            scores["R1"] = 3

    # If critical constraint breach, immediately DISCOUNT
    if scores["R1"] == 0:
        return {
            "model_name": model_key,
            "status": "DISCOUNTED",
            "discount_reason": "CONSTRAINT_BREACH",
            "weight": 0.0,
            "rubric_scores": {**{f"R{i}": 2 for i in range(2, 8)}, "R1": 0, "R8": scores["R8"]},
            "total_score": scores["R8"],
            "flaws": ["Allowed defense asset under ethical no-military mandate"],
            "strengths": strengths,
            "signal": parsed.get("signal", "UNKNOWN"),
            "constraint_passes": m_passes,
            "explanation": c_check.get("explanation", "")
        }

    # R2 Evidence Traceability
    cited = parsed.get("cited_evidence", [])
    if len(cited) >= 2:
        scores["R2"] = 5
        strengths.append("Well-grounded evidence citations")
    elif len(cited) == 1:
        scores["R2"] = 3
    else:
        scores["R2"] = 1
        flaws.append("Sparse evidence citation")

    # R3 Timing / Disclosure Lag Awareness
    days_lag = trade["days_lag"]
    signal = parsed.get("signal", "UNKNOWN")
    evidence_quality = parsed.get("evidence_quality", {})
    freshness = evidence_quality.get("timing_freshness", "") if isinstance(evidence_quality, dict) else ""

    if days_lag > 40:
        if signal == "BUY" and "STALE" not in str(freshness).upper():
            scores["R3"] = 1
            flaws.append("IGNORED_40D_DISCLOSURE_LAG")
        else:
            scores["R3"] = 5
            strengths.append("Correctly recognized stale informational edge")
    else:
        scores["R3"] = 4 if "FRESH" in str(freshness).upper() or "MODERATE" in str(freshness).upper() else 3

    # R4 Transaction / Direction Alignment
    tx_type = trade["tx_type"]
    if "Sale" in tx_type and signal == "BUY":
        scores["R4"] = 1
        flaws.append("CONTRADICTED_POLITICIAN_SALE")
    elif "Sale" in tx_type and signal in ("SELL", "HOLD", "ABSTAIN"):
        scores["R4"] = 5
        strengths.append("Aligned with insider disposition")
    else:
        scores["R4"] = 4

    # R5 Investor Fit (Investor A: Moderate risk, 6M horizon)
    fit = parsed.get("fit_to_investor", {})
    if isinstance(fit, dict) and fit.get("risk_fit") in ("GOOD", "PARTIAL"):
        scores["R5"] = 4
    else:
        scores["R5"] = 3

    # R6 Rationale Coherence
    rationale = str(parsed.get("rationale") or "")
    if len(rationale) > 40:
        scores["R6"] = 5
        strengths.append("Clear financial rationale")
    else:
        scores["R6"] = 2
        flaws.append("Brief or generic rationale")

    # R7 Risk Completeness
    risks = parsed.get("risks_and_uncertainties", [])
    if len(risks) >= 2:
        scores["R7"] = 5
    elif len(risks) == 1:
        scores["R7"] = 3
    else:
        scores["R7"] = 2

    total_score = sum(scores.values())
    
    # Model Status Assignment
    if total_score >= 32:
        status = "SELECTED"
    elif total_score >= 20:
        status = "WEIGHTED"
    else:
        status = "DISCOUNTED"

    return {
        "model_name": model_key,
        "status": status,
        "discount_reason": flaws[0] if status == "DISCOUNTED" and flaws else None,
        "weight": float(total_score),
        "rubric_scores": scores,
        "total_score": total_score,
        "flaws": flaws,
        "strengths": strengths,
        "signal": signal,
        "constraint_passes": m_passes,
        "explanation": c_check.get("explanation", rationale)
    }


def run_full_jev_pipeline():
    with open("benchmark_50_trades.json", "r", encoding="utf-8") as f:
        trades = json.load(f)

    models_meta = [
        ("Apertus-1.5-70B", "benchmark_results_50/Apertus-1.5-70B_investor_A.json", "CSCS Supercomputer", "70B"),
        ("Apertus-1.5-8B", "benchmark_results_50/Apertus-1.5-8B_investor_A.json", "CSCS Supercomputer", "8.0B"),
        ("Qwen-2.5-14B-Coder", "benchmark_results_50/Qwen-2.5-14B-Coder_investor_A.json", "RTX 5060 Ti GPU", "14.8B"),
        ("SecurityAI-14B", "benchmark_results_50/SecurityAI-14B_investor_A.json", "RTX 5060 Ti GPU", "14.8B"),
        ("Neo-Uncensored-8B", "benchmark_results_50/Neo-Uncensored-8B_investor_A.json", "RTX 5060 Ti GPU", "8.0B"),
        ("Llama-3.1-8B-WhiteRabbitNeo", "benchmark_results_50/Llama-3.1-8B-WhiteRabbitNeo_investor_A.json", "RTX 5060 Ti GPU", "8.0B")
    ]

    model_entries = {}
    for m_name, path, _, _ in models_meta:
        with open(path, "r", encoding="utf-8") as f:
            model_entries[m_name] = {x["trade_id"]: x for x in json.load(f)}

    investor_profile = {
        "investor_id": "A",
        "investor_name": "Ethical No-Military",
        "hard_constraint": "Must NOT hold companies in the military / defense sector.",
        "risk_appetite": "Moderate",
        "target_horizon": "6M"
    }

    jev_evaluated_trades = []

    for idx, trade in enumerate(trades):
        t_id = trade["id"]
        gt_constraint = verify_ground_truth_constraint(trade, investor_profile)

        evaluated_models = []
        for m_name, _, prov, par in models_meta:
            m_res = model_entries[m_name].get(t_id, {})
            audit = audit_model_output(trade, m_name, m_res, gt_constraint)
            audit["provider"] = prov
            audit["params"] = par
            audit["latency"] = m_res.get("inference", {}).get("elapsed_seconds")
            audit["tok_s"] = m_res.get("inference", {}).get("tokens_per_second")
            evaluated_models.append(audit)

        # Normalize weights for non-discounted models
        valid_models = [m for m in evaluated_models if m["status"] in ("SELECTED", "WEIGHTED")]
        sum_weights = sum(m["weight"] for m in valid_models)
        for m in evaluated_models:
            if m["status"] in ("SELECTED", "WEIGHTED") and sum_weights > 0:
                m["normalized_weight"] = round(m["weight"] / sum_weights, 3)
            else:
                m["normalized_weight"] = 0.0

        # Consensus & Dissent
        signals_seen = [m["signal"] for m in evaluated_models if m["signal"] not in ("ERROR", "UNKNOWN")]
        trusted_buys = sum(m["normalized_weight"] for m in valid_models if m["signal"] == "BUY")
        trusted_sells = sum(m["normalized_weight"] for m in valid_models if m["signal"] == "SELL")
        trusted_holds = sum(m["normalized_weight"] for m in valid_models if m["signal"] == "HOLD")

        # JEV Final Call Synthesis (Rule 1 First)
        if gt_constraint["passes"] is False:
            final_signal = "ABSTAIN"
            final_reason = "ETHICAL_DEFENSE_VETO"
            final_rationale = f"JEV Rule 1 Enforced: Issuer {trade['asset_name']} (${trade['ticker']}) operates in aerospace & defense. Ethical mandate strictly prohibits holding."
            confidence = 1.0
        elif trade["days_lag"] > 40:
            final_signal = "ABSTAIN"
            final_reason = "STALE_DISCLOSURE"
            final_rationale = f"JEV Rule 4 Enforced: Disclosure filing delay of {trade['days_lag']} days exceeds 40-day freshness horizon. Any informational edge is neutralized."
            confidence = 0.9
        elif trade["amount_max"] < 15000:
            final_signal = "ABSTAIN"
            final_reason = "LOW_CONVICTION_NOISE"
            final_rationale = f"JEV Rule 5 Enforced: Transaction amount bracket ({trade['amount']}) is under $15k threshold. Weak insider conviction filtered as noise."
            confidence = 0.85
        elif trusted_buys >= 0.5:
            final_signal = "BUY"
            final_reason = "HIGH_CONSENSUS_ENTRY"
            final_rationale = f"Trusted models agree ({round(trusted_buys*100)}% weighted conviction) that {trade['politician']}'s entry in {trade['asset_name']} represents actionable alpha."
            confidence = round(trusted_buys, 2)
        elif trusted_sells >= 0.5:
            final_signal = "SELL"
            final_reason = "DISPOSITION_CONSENSUS"
            final_rationale = f"Trusted models agree ({round(trusted_sells*100)}% weighted conviction) that {trade['politician']}'s sale signals risk distribution."
            confidence = round(trusted_sells, 2)
        elif trusted_holds >= 0.4:
            final_signal = "HOLD"
            final_reason = "NEUTRAL_CONVICTION"
            final_rationale = f"Constraint verified, but models advise neutral stance over 6-month horizon."
            confidence = round(trusted_holds, 2)
        else:
            final_signal = "ABSTAIN"
            final_reason = "MODEL_DIVERGENCE"
            final_rationale = "Signal dispersion among models exceeds consensus threshold. JEV enforces defensive abstention."
            confidence = 0.5

        selected_names = [m["model_name"] for m in evaluated_models if m["status"] == "SELECTED"]
        discounted_names = [m["model_name"] for m in evaluated_models if m["status"] == "DISCOUNTED"]

        jev_trade_record = {
            "trade_id": t_id,
            "trade_idx": idx + 1,
            "politician": trade["politician"],
            "party": trade["party"],
            "chamber": trade["chamber"],
            "district": trade["district"],
            "committees": trade["committees"],
            "ticker": trade["ticker"],
            "asset_name": trade["asset_name"],
            "asset_type": trade["asset_type"],
            "tx_type": trade["tx_type"],
            "amount": trade["amount"],
            "amount_min": trade["amount_min"],
            "amount_max": trade["amount_max"],
            "tx_date": trade["tx_date"],
            "filing_date": trade["filing_date"],
            "days_lag": trade["days_lag"],
            "ground_truth_constraint": gt_constraint,
            "models_evaluation": evaluated_models,
            "jev_decision": {
                "final_signal": final_signal,
                "reason_code": final_reason,
                "rationale": final_rationale,
                "confidence_score": confidence,
                "selected_models": selected_names,
                "discounted_models": discounted_names,
                "consensus_distribution": {
                    "BUY": round(trusted_buys, 2),
                    "SELL": round(trusted_sells, 2),
                    "HOLD": round(trusted_holds, 2),
                    "ABSTAIN": round(1.0 - (trusted_buys + trusted_sells + trusted_holds), 2)
                }
            }
        }
        jev_evaluated_trades.append(jev_trade_record)

    out_path = "benchmark_results_50/JEV_final_audit_50.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(jev_evaluated_trades, f, indent=2)

    print(f"JEV Arbiter Layer successfully evaluated all {len(jev_evaluated_trades)} trades!")
    print(f"Saved complete audit trail to {out_path}")

if __name__ == "__main__":
    run_full_jev_pipeline()
