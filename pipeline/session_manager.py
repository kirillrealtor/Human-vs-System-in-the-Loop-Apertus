"""
Session Manager for Step-by-Step Multi-Model Congressional Trade Evaluation.
Allows recording outputs from one model at a time (e.g. as the user switches models in Antigravity),
accumulating signals across models, and executing the JEV Arbiter evaluation to generate visual reports.
"""

import os
import json
import datetime
from typing import Dict, Any, List, Optional
import pandas as pd

from .models import EvidencePacket, InvestorProfile, ModelOutput, JEVReport
from .investor_profiles import INVESTOR_PROFILES, get_investor_profile
from .evidence_packet import build_evidence_packet
from .constraint_verifier import verify_constraint
from .evaluator_engine import generate_model_signal, run_jev_evaluation
from .ground_truth import compute_ground_truth_returns

SESSIONS_DIR = "evaluation_sessions"


def ensure_sessions_dir(trade_id: str) -> str:
    path = os.path.join(SESSIONS_DIR, trade_id.replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    return path


def load_trade_record(trade_id: str, csv_path: str = "all_2024_congress_trades.csv") -> Dict[str, Any]:
    df = pd.read_csv(csv_path)
    match = df[df["id"] == trade_id]
    if match.empty:
        raise ValueError(f"Trade ID {trade_id} not found in {csv_path}")
    return match.iloc[0].to_dict()


def record_model_run(
    trade_id: str,
    model_name: str,
    model_version: str = "1.0",
    csv_path: str = "all_2024_congress_trades.csv",
    custom_signals: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Evaluates or records signals for ONE model across all 4 investors (A, B, C, D)
    and saves them to the persistent session directory.
    """
    s_dir = ensure_sessions_dir(trade_id)
    raw_record = load_trade_record(trade_id, csv_path)
    packet = build_evidence_packet(raw_record)

    model_results: Dict[str, Any] = {}
    model_info = {"name": model_name, "version": model_version}

    for inv_id in ["A", "B", "C", "D"]:
        profile = get_investor_profile(inv_id)
        if custom_signals and inv_id in custom_signals:
            # User or LLM supplied custom output
            mo_dict = custom_signals[inv_id]
            model_results[inv_id] = mo_dict
        else:
            # Generate quantitative analyst signal for this model
            mo = generate_model_signal(model_info, profile, packet)
            model_results[inv_id] = mo.model_dump()

    # Save to model file
    safe_name = model_name.lower().replace(" ", "_").replace(".", "_").replace("-", "_")
    model_file = os.path.join(s_dir, f"{safe_name}.json")
    with open(model_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "model_name": model_name,
                "model_version": model_version,
                "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "investor_signals": model_results,
            },
            f,
            indent=2,
        )

    return {
        "trade_id": trade_id,
        "model_name": model_name,
        "saved_to": model_file,
        "investor_signals": model_results,
    }


def list_recorded_models(trade_id: str) -> List[Dict[str, Any]]:
    """Returns a list of all models that have submitted signals for this trade so far."""
    s_dir = os.path.join(SESSIONS_DIR, trade_id.replace(" ", "_"))
    if not os.path.exists(s_dir):
        return []

    models = []
    for fname in os.listdir(s_dir):
        if fname.endswith(".json") and not fname.startswith("jev_"):
            fpath = os.path.join(s_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    models.append({
                        "model_name": data.get("model_name"),
                        "recorded_at": data.get("recorded_at"),
                        "file": fname,
                    })
            except Exception:
                pass
    return models


def run_jev_on_session(trade_id: str, csv_path: str = "all_2024_congress_trades.csv") -> Dict[str, Any]:
    """
    Executes JEV Arbiter across ALL models recorded in the session for this trade.
    Produces the final decision support per investor profile.
    """
    s_dir = ensure_sessions_dir(trade_id)
    raw_record = load_trade_record(trade_id, csv_path)
    packet = build_evidence_packet(raw_record)
    gt_returns = compute_ground_truth_returns(packet.asset.ticker, packet.timing.transaction_date)

    # Gather all recorded model files
    recorded = list_recorded_models(trade_id)
    if not recorded:
        raise ValueError(f"No models have recorded signals for trade {trade_id} yet.")

    model_outputs_by_investor: Dict[str, List[ModelOutput]] = {"A": [], "B": [], "C": [], "D": []}

    for rec in recorded:
        fpath = os.path.join(s_dir, rec["file"])
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            signals = data.get("investor_signals", {})
            for inv_id in ["A", "B", "C", "D"]:
                if inv_id in signals:
                    mo = ModelOutput.model_validate(signals[inv_id])
                    model_outputs_by_investor[inv_id].append(mo)

    # Run JEV for each investor
    jev_reports: Dict[str, Any] = {}
    for inv_id in ["A", "B", "C", "D"]:
        profile = get_investor_profile(inv_id)
        m_list = model_outputs_by_investor[inv_id]
        report = run_jev_evaluation(profile, packet, m_list)
        jev_reports[inv_id] = report.model_dump()

    # Save JEV session report
    jev_file = os.path.join(s_dir, "jev_evaluation_report.json")
    session_result = {
        "trade_id": trade_id,
        "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "models_audited": [r["model_name"] for r in recorded],
        "ground_truth": gt_returns,
        "jev_reports": jev_reports,
    }
    with open(jev_file, "w", encoding="utf-8") as f:
        json.dump(session_result, f, indent=2)

    return session_result


def generate_cool_markdown_report(session_result: Dict[str, Any], raw_record: Dict[str, Any]) -> str:
    """
    Generates a stunning, visual markdown report with formatted badges, cards,
    tables, and analysis.
    """
    trade_id = session_result["trade_id"]
    packet = build_evidence_packet(raw_record)
    gt = session_result.get("ground_truth", {})
    models_audited = session_result.get("models_audited", [])
    jev_reports = session_result.get("jev_reports", {})

    lines = [
        f"# 🏛️ Congressional Trade Decision Support: JEV Arbiter Report",
        f"",
        f"> **Trade Identifier:** `{packet.trade_id}` | **Audited Models:** `{', '.join(models_audited)}` | **Evaluation Date:** `{datetime.date.today()}`",
        f"",
        f"---",
        f"",
        f"## 📋 1. Evidence Packet Overview",
        f"",
        f"| Dimension | Disclosure Data | Verification Status |",
        f"| :--- | :--- | :---: |",
        f"| **Politician** | **{packet.politician.name}** ({packet.politician.party or 'N/A'}, {packet.politician.chamber or 'Congress'}) | Verified Public Record |",
        f"| **Committees** | `{', '.join(packet.politician.committees) if packet.politician.committees else 'General / None Reported'}` | STOCK Act Filing |",
        f"| **Asset / Ticker** | **${packet.asset.ticker or 'N/A'}** ({packet.asset.asset_name}) | Security Type: `{packet.asset.asset_type}` |",
        f"| **Transaction** | **{packet.trade.transaction_type}** ({packet.trade.amount_range}) | Owner: `{packet.trade.owner}` |",
        f"| **Timing & Freshness** | Executed: `{packet.timing.transaction_date}` \| Disclosed: `{packet.timing.filing_date}` | **{packet.timing.days_to_disclosure} Days Lag** |",
        f"| **Data Quality Flags** | `{', '.join(packet.data_quality_flags) if packet.data_quality_flags else 'None (Clean Filing)'}` | Automated Integrity Scan |",
        f"",
    ]

    if gt.get("resolved"):
        lines.extend([
            f"### 📈 Ground Truth Market Performance vs SPY (Benchmark)",
            f"",
            f"| Horizon | Asset Return | S&P 500 (SPY) Return | Net Alpha vs SPY | Beat Market? |",
            f"| :---: | :---: | :---: | :---: | :---: |",
            f"| **3M (T+90d)** | `{gt['3M']['asset_return_pct']}%` | `{gt['3M']['spy_return_pct']}%` | **{gt['3M']['alpha_pct']:+}%** | {'✅ YES' if gt['3M']['beat_spy'] else '❌ NO'} |",
            f"| **6M (T+180d)** | `{gt['6M']['asset_return_pct']}%` | `{gt['6M']['spy_return_pct']}%` | **{gt['6M']['alpha_pct']:+}%** | {'✅ YES' if gt['6M']['beat_spy'] else '❌ NO'} |",
            f"| **9M (T+270d)** | `{gt['9M']['asset_return_pct']}%` | `{gt['9M']['spy_return_pct']}%` | **{gt['9M']['alpha_pct']:+}%** | {'✅ YES' if gt['9M']['beat_spy'] else '❌ NO'} |",
            f"",
        ])

    lines.extend([
        f"---",
        f"",
        f"## 🛡️ 2. Investor-Specific Decisions & JEV Audit",
        f"",
    ])

    for inv_id in ["A", "B", "C", "D"]:
        rep = jev_reports.get(inv_id)
        if not rep:
            continue
        prof = get_investor_profile(inv_id)
        fc = rep["final_call"]
        c_check = rep["jev_constraint_check"]
        sig = fc["signal"]

        sig_icon = "🟢" if sig == "BUY" else ("🔴" if sig == "SELL" else "⚪")
        pass_badge = "✅ PASSED" if c_check["passes"] is True else ("❌ FAILED" if c_check["passes"] is False else "⚠️ UNVERIFIED")

        lines.extend([
            f"### Investor {inv_id}: {prof.investor_name}",
            f"",
            f"> **Mandate:** *{prof.hard_constraint}*",
            f"> ",
            f"> **Constraint Verification:** {pass_badge} — {c_check['explanation']}",
            f"",
            f"#### {sig_icon} JEV Verdict: `{sig}`",
            f"- **Target Horizon:** `{fc['horizon'] or 'N/A'}`",
            f"- **Abstention Reason:** `{fc['abstain_reason'] or 'None'}`",
            f"- **Final Rationale:** {fc['final_rationale']}",
            f"- **Investor Message:** *\"{rep['investor_message']}\"*",
            f"",
            f"**Model Audit & Rubric (R1–R8) Matrix:**",
            f"",
            f"| Model | Model Signal | JEV Status | Weight | Rubric Score | Key Audit Findings |",
            f"| :--- | :---: | :---: | :---: | :---: | :--- |",
        ])

        for me in rep["model_evaluations"]:
            st = me["status"]
            st_icon = "⭐" if st == "SELECTED" else ("🔹" if st == "WEIGHTED" else "⛔")
            total_r = sum(me["rubric_scores"].values())
            flaws_str = f"Flaws: {', '.join(me['flaws'])}" if me["flaws"] else "Clean analysis"
            lines.append(
                f"| **{me['model_id']}** | `{me['model_signal']}` | {st_icon} `{st}` | "
                f"**{(me['weight_assigned'] * 100):.1f}%** | `{total_r}/40` | {flaws_str} |"
            )

        lines.extend([
            f"",
            f"*Selection Analytics:* {rep['model_selection_analytics']['selection_rationale']}",
            f"",
            f"---",
            f"",
        ])

    lines.extend([
        f"## ⚖️ 3. Regulatory & Research Guardrails",
        f"- **No Automated Execution:** All signals are research decision support. The investor decides whether to paper-trade or follow.",
        f"- **Zero Lookahead Bias:** All model evaluations strictly enforce knowledge available on or before `{packet.timing.transaction_date}`.",
        f"- **Disclosure Lag:** Disclosures over 40 days are treated as stale with informational advantage priced out.",
        f"",
    ])

    return "\n".join(lines)
