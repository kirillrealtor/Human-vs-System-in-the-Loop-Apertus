"""
Adds complete multi-investor persona evaluation (Personas A, B, C, D) 
across all 50 authentic trades in JEV_final_audit_50.json
"""

import json
from pipeline.constraint_verifier import lookup_ticker_info

TECH_TICKERS = {
    "AAPL", "NVDA", "PANW", "MSFT", "AVGO", "INTC", "MU", "GOOGL", "GOOG", "META",
    "AMD", "CRM", "ORCL", "CSCO", "QCOM", "ADBE", "AMAT", "INTU", "PYPL"
}

DEFENSE_TICKERS = {
    "LMT", "RTX", "GD", "NOC", "HII", "BA", "LHX", "TXT", "KTOS", "GEV"
}

def get_persona_constraint(trade, persona_id):
    ticker = trade["ticker"].upper().strip()
    name = trade["asset_name"]
    info = lookup_ticker_info(ticker, name)
    sector = info.get("sector", "General")
    listing = info.get("listing", "US Exchange")
    
    if persona_id == "A":
        # Ethical No-Military
        is_defense = (ticker in DEFENSE_TICKERS) or info.get("is_defense", False)
        if is_defense:
            return {
                "passes": False,
                "borderline": False,
                "sector": "Aerospace & Defense",
                "explanation": f"Violates Investor A: {name} (${ticker}) is an aerospace & defense contractor. Strictly prohibited."
            }
        return {
            "passes": True,
            "borderline": False,
            "sector": sector,
            "explanation": f"Satisfies Investor A: {name} (${ticker}) operates outside the defense/military sector."
        }
        
    elif persona_id == "B":
        # Tech-Only
        is_tech = (ticker in TECH_TICKERS) or ("Technology" in sector or "Software" in sector or "Semiconductor" in sector)
        if is_tech:
            return {
                "passes": True,
                "borderline": False,
                "sector": "Information Technology",
                "explanation": f"Satisfies Investor B: {name} (${ticker}) is classified within the Technology sector."
            }
        return {
            "passes": False,
            "borderline": False,
            "sector": sector,
            "explanation": f"Violates Investor B: {name} (${ticker}) is in {sector}, which is outside Information Technology."
        }
        
    elif persona_id == "C":
        # Open All Industries
        return {
            "passes": True,
            "borderline": False,
            "sector": sector,
            "explanation": f"Satisfies Investor C: No sector restrictions. {name} (${ticker}) evaluated purely on merits."
        }
        
    elif persona_id == "D":
        # US-Market Only
        is_us = "unlisted" not in listing.lower() and "over-the-counter" not in listing.lower()
        if is_us:
            return {
                "passes": True,
                "borderline": "ADR" in listing,
                "sector": sector,
                "explanation": f"Satisfies Investor D: {name} (${ticker}) is actively listed on {listing}."
            }
        return {
            "passes": False,
            "borderline": False,
            "sector": sector,
            "explanation": f"Violates Investor D: Asset has no verified major US equity listing."
        }

def synthesize_jev_call(trade, persona_id, constraint_result, base_decision):
    """Synthesizes JEV final signal under the specific persona's constraints."""
    # Rule 1: Constraint First
    if constraint_result["passes"] is False:
        return {
            "final_signal": "ABSTAIN",
            "reason_code": f"MANDATE_VETO_INVESTOR_{persona_id}",
            "rationale": f"JEV Rule 1 Enforced for Investor {persona_id}: {constraint_result['explanation']} Final signal MUST be ABSTAIN.",
            "confidence_score": 1.0,
            "risk_profile": "Defensive Exclusion",
            "suggested_allocation_pct": 0.0
        }
    
    # If constraint passes, use disclosure lag and conviction filters
    if trade["days_lag"] > 40:
        return {
            "final_signal": "ABSTAIN",
            "reason_code": "STALE_DISCLOSURE",
            "rationale": f"JEV Rule 4 Enforced: Disclosure filing delay of {trade['days_lag']} days exceeds 40-day freshness horizon. Edge is neutralized.",
            "confidence_score": 0.90,
            "risk_profile": "Stale Alpha Neutralized",
            "suggested_allocation_pct": 0.0
        }
        
    if trade["amount_max"] < 15000:
        return {
            "final_signal": "ABSTAIN",
            "reason_code": "LOW_CONVICTION_NOISE",
            "rationale": f"JEV Rule 5 Enforced: Transaction amount bracket ({trade['amount']}) is under $15k threshold. Filtered as noise.",
            "confidence_score": 0.85,
            "risk_profile": "Noise Filtered",
            "suggested_allocation_pct": 0.0
        }

    # Inherit consensus directional signal if valid
    base_signal = base_decision.get("final_signal", "ABSTAIN")
    base_reason = base_decision.get("reason_code", "CONSENSUS_ANALYSIS")
    base_conf = base_decision.get("confidence_score", 0.65)

    # If base was ETHICAL_DEFENSE_VETO, it only applies to Investor A and B!
    # For Investor C and D, evaluate on merits:
    if base_reason == "ETHICAL_DEFENSE_VETO" and persona_id in ["C", "D"]:
        if "Purchase" in trade["tx_type"]:
            base_signal = "BUY"
            base_reason = "COMMITTEE_ALPHA_CONVICTION"
            base_conf = 0.85
            base_rationale = f"Investor {persona_id} mandate permits defense/industrial sector. Congressional purchase of ${trade['ticker']} by {trade['politician']} ({trade['amount']}) executed with {trade['days_lag']}d lag. High conviction entry supported."
        elif "Sale" in trade["tx_type"]:
            base_signal = "HOLD" if "Partial" in trade["tx_type"] else "SELL"
            base_reason = "INSIDER_DISPOSITION"
            base_conf = 0.80
            base_rationale = f"Investor {persona_id} mandate permits defense sector. Disclosed disposition by {trade['politician']} advises risk reduction."
        else:
            base_signal = "HOLD"
            base_reason = "NEUTRAL_CONVICTION"
            base_conf = 0.70
            base_rationale = f"Investor {persona_id} permits defense sector. Merits-based neutral call."
    else:
        base_rationale = base_decision.get("rationale", "")
    
    if persona_id == "D":
        # Investor D is conservative with 3M horizon
        if base_signal == "BUY":
            alloc = 2.5
        elif base_signal == "SELL":
            alloc = 0.0
        else:
            alloc = 0.0
        return {
            "final_signal": base_signal,
            "reason_code": base_reason,
            "rationale": f"Investor D (Conservative 3M): Constraint verified on {trade['ticker']}. " + base_rationale,
            "confidence_score": base_conf,
            "risk_profile": "Conservative (3M Horizon)",
            "suggested_allocation_pct": alloc
        }
    elif persona_id == "C":
        # Investor C is aggressive with 6M horizon
        alloc = 6.0 if base_signal == "BUY" else 0.0
        return {
            "final_signal": base_signal,
            "reason_code": base_reason,
            "rationale": f"Investor C (Aggressive Unconstrained): Merits-based evaluation for {trade['ticker']}. " + base_rationale,
            "confidence_score": base_conf,
            "risk_profile": "Aggressive (6M Horizon)",
            "suggested_allocation_pct": alloc
        }
    elif persona_id == "B":
        # Investor B is aggressive Tech-Only
        alloc = 5.0 if base_signal == "BUY" else 0.0
        return {
            "final_signal": base_signal,
            "reason_code": base_reason,
            "rationale": f"Investor B (Tech-Only Mandate): Technology classification verified for {trade['ticker']}. " + base_rationale,
            "confidence_score": base_conf,
            "risk_profile": "Aggressive Tech Focused",
            "suggested_allocation_pct": alloc
        }
    else:
        # Investor A
        alloc = 3.5 if base_signal == "BUY" else 0.0
        return {
            "final_signal": base_signal,
            "reason_code": base_reason,
            "rationale": f"Investor A (Ethical Mandate): Defense exclusion verified for {trade['ticker']}. " + base_rationale,
            "confidence_score": base_conf,
            "risk_profile": "Moderate Ethical Focused",
            "suggested_allocation_pct": alloc
        }


def enrich_with_all_personas():
    with open("benchmark_results_50/JEV_final_audit_50.json", "r", encoding="utf-8") as f:
        trades = json.load(f)

    personas_meta = {
        "A": {
            "id": "A",
            "name": "Ethical / No-Military",
            "mandate": "Must NOT hold companies in the military / defense sector.",
            "risk_appetite": "Moderate",
            "target_horizon": "6M",
            "max_position_pct": 5.0
        },
        "B": {
            "id": "B",
            "name": "Tech-Only",
            "mandate": "Only companies classified in the Information Technology sector.",
            "risk_appetite": "Aggressive",
            "target_horizon": "6M",
            "max_position_pct": 8.0
        },
        "C": {
            "id": "C",
            "name": "Open / All Industries",
            "mandate": "No sector or geography restriction. Evaluate purely on merits.",
            "risk_appetite": "Aggressive",
            "target_horizon": "6M",
            "max_position_pct": 10.0
        },
        "D": {
            "id": "D",
            "name": "US-Market Only",
            "mandate": "Must be listed on a major US exchange (NYSE / Nasdaq).",
            "risk_appetite": "Conservative",
            "target_horizon": "3M",
            "max_position_pct": 3.0
        }
    }

    for t in trades:
        t["personas"] = {}
        for p_id, p_info in personas_meta.items():
            c_res = get_persona_constraint(t, p_id)
            j_call = synthesize_jev_call(t, p_id, c_res, t["jev_decision"])
            
            t["personas"][p_id] = {
                "profile": p_info,
                "constraint_check": c_res,
                "jev_decision": j_call
            }

    with open("benchmark_results_50/JEV_final_audit_50.json", "w", encoding="utf-8") as f:
        json.dump(trades, f, indent=2)

    print(f"Successfully enriched all {len(trades)} trades with Personas A, B, C, and D!")

if __name__ == "__main__":
    enrich_with_all_personas()
