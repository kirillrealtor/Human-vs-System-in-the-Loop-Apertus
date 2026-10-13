"""
Master Pipeline Runner for Congressional Trade Evaluation (v2).
Executes Part 0, Part 1, Part 2, and Part 3 across 2024 Congressional Trades.
"""

import os
import sys
import json
import argparse
import pandas as pd
from typing import List, Dict, Any

from pipeline.models import EvidencePacket, InvestorProfile, ModelOutput, JEVReport
from pipeline.investor_profiles import INVESTOR_PROFILES, get_investor_profile
from pipeline.evidence_packet import build_evidence_packet
from pipeline.evaluator_engine import generate_model_signal, run_jev_evaluation, MODELS_LIST
from pipeline.ground_truth import compute_ground_truth_returns
from pipeline.benchmark_scorer import ModelScorecard, JEVScorecard, format_leaderboard_table
from pipeline.dashboard_generator import generate_html_dashboard


def run_single_trade_evaluation(
    raw_record: Dict[str, Any],
    scorecards_by_model: Dict[str, Dict[str, ModelScorecard]],
    jev_scorecards: Dict[str, JEVScorecard],
    simulate_rogue_model: bool = False,
) -> Dict[str, Any]:
    """Evaluates a single trade disclosure record across all 4 investor profiles."""
    packet = build_evidence_packet(raw_record)
    print(f"\n================================================================================")
    print(f"TRADE: {packet.trade_id} | Politician: {packet.politician.name} ({packet.politician.party})")
    print(f"Asset: {packet.asset.ticker} ({packet.asset.asset_name}) | Type: {packet.asset.asset_type}")
    print(f"Transaction: {packet.trade.transaction_type} | Amount: {packet.trade.amount_range}")
    print(f"Date: {packet.timing.transaction_date} | Disclosure Lag: {packet.timing.days_to_disclosure} days")
    print(f"Flags: {packet.data_quality_flags}")
    print(f"================================================================================")

    # Ground truth returns
    gt_returns = compute_ground_truth_returns(packet.asset.ticker, packet.timing.transaction_date)
    if gt_returns.get("resolved"):
        print(f"[Ground Truth Market Returns]")
        for h in ["3M", "6M", "9M"]:
            ret_data = gt_returns.get(h, {})
            print(f"  {h}: Asset {ret_data.get('asset_return_pct')}% vs SPY {ret_data.get('spy_return_pct')}% "
                  f"(Alpha: {ret_data.get('alpha_pct'):+}% | Beat SPY: {ret_data.get('beat_spy')})")
    else:
        print("[Ground Truth Market Returns]: Unlisted / OTC / Data unavailable.")

    results_by_investor: Dict[str, Any] = {}

    for inv_id in ["A", "B", "C", "D"]:
        profile = get_investor_profile(inv_id)
        print(f"\n--- Investor {inv_id}: {profile.investor_name} ---")

        # Generate signals from all 6 models
        model_outputs: List[ModelOutput] = []
        for idx, m_info in enumerate(MODELS_LIST):
            # Optionally simulate one model making an aggressive constraint error on Investor A/B
            rogue = simulate_rogue_model and (idx == 2)  # GPT-4o simulates rogue on test
            mo = generate_model_signal(m_info, profile, packet, force_constraint_violation=rogue)
            model_outputs.append(mo)

        # Run JEV Arbiter
        jev_report = run_jev_evaluation(profile, packet, model_outputs)
        fc = jev_report.final_call
        print(f"  JEV Constraint Check: Passes={jev_report.jev_constraint_check.passes} "
              f"(Borderline={jev_report.jev_constraint_check.borderline})")
        print(f"  JEV Final Signal: [{fc.signal}] | Horizon: {fc.horizon or 'N/A'} | Abstain Reason: {fc.abstain_reason or 'None'}")
        print(f"  JEV Rationale: {fc.final_rationale}")
        print(f"  JEV Message to Investor: \"{jev_report.investor_message}\"")

        # Record model scorecards using ground truth constraint verification
        is_truth_pass = (jev_report.jev_constraint_check.passes is True)
        for m_info, mo in zip(MODELS_LIST, model_outputs):
            if inv_id in scorecards_by_model[m_info["name"]]:
                scorecards_by_model[m_info["name"]][inv_id].record_evaluation(
                    mo=mo,
                    constraint_truth=is_truth_pass,
                    gt_returns=gt_returns,
                    target_horizon=profile.target_horizon,
                )

        # Record JEV scorecard
        jev_scorecards[inv_id].record_report(
            report=jev_report,
            constraint_truth=is_truth_pass,
            gt_returns=gt_returns,
            target_horizon=profile.target_horizon,
        )

        results_by_investor[inv_id] = {
            "profile": profile.model_dump(),
            "jev_report": jev_report.model_dump(),
            "model_outputs": [mo.model_dump() for mo in model_outputs],
        }

    trade_summary = {
        "trade_id": packet.trade_id,
        "politician_name": packet.politician.name,
        "party": packet.politician.party,
        "chamber": packet.politician.chamber,
        "district": packet.politician.state_district,
        "ticker": packet.asset.ticker,
        "asset_name": packet.asset.asset_name,
        "asset_type": packet.asset.asset_type,
        "transaction_type": packet.trade.transaction_type,
        "amount_range": packet.trade.amount_range,
        "owner": packet.trade.owner,
        "days_lag": packet.timing.days_to_disclosure,
        "transaction_date": packet.timing.transaction_date,
        "filing_date": packet.timing.filing_date,
        "data_origin": packet.source.data_origin,
        "flags": packet.data_quality_flags,
    }

    return {
        "trade_summary": trade_summary,
        "investors": results_by_investor,
        "ground_truth": gt_returns,
    }


def main():
    parser = argparse.ArgumentParser(description="Congressional Trade Evaluation Pipeline (v2)")
    parser.add_argument("--trade", type=str, help="Specific trade ID to evaluate (e.g. US-CONG-2024-00008)")
    parser.add_argument("--politician", type=str, help="Filter by politician name (e.g. Pelosi)")
    parser.add_argument("--limit", type=int, default=3, help="Number of trades to evaluate")
    parser.add_argument("--output_html", type=str, default="dashboard.html", help="HTML dashboard output file")
    parser.add_argument("--output_json", type=str, default="evaluation_results.json", help="JSON output file")
    parser.add_argument("--simulate_dissent", action="store_true", help="Simulate a rogue model to test JEV audit filters")
    args = parser.parse_args()

    csv_path = "all_2024_congress_trades.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found in current directory.")
        sys.exit(1)

    print("Loading 2024 Congressional Trades Dataset...")
    df = pd.read_csv(csv_path)

    # Filter trades
    if args.trade:
        selected_df = df[df["id"] == args.trade]
        if selected_df.empty:
            print(f"No trade found with ID: {args.trade}")
            sys.exit(1)
    elif args.politician:
        selected_df = df[df["politician_name"].str.contains(args.politician, case=False, na=False)].head(args.limit)
    else:
        # Pick 3 diverse representative trades:
        # 1. Tech purchase: Nancy Pelosi NVDA (US-CONG-2024-00008)
        # 2. Defense trade: Ro Khanna HII (US-CONG-2024-00390)
        # 3. Non-Tech / Health purchase: Ann Wagner JNJ (US-CONG-2024-00001)
        target_ids = ["US-CONG-2024-00008", "US-CONG-2024-00390", "US-CONG-2024-00001"]
        selected_df = df[df["id"].isin(target_ids)]
        if selected_df.empty or len(selected_df) < len(target_ids):
            selected_df = df.head(args.limit)

    # Initialize scorecards
    scorecards_by_model: Dict[str, Dict[str, ModelScorecard]] = {}
    for m in MODELS_LIST:
        scorecards_by_model[m["name"]] = {inv: ModelScorecard(m["name"], inv) for inv in ["A", "B", "C", "D"]}

    jev_scorecards = {inv: JEVScorecard(inv) for inv in ["A", "B", "C", "D"]}

    all_trade_results = []
    for _, row in selected_df.iterrows():
        res = run_single_trade_evaluation(
            raw_record=row.to_dict(),
            scorecards_by_model=scorecards_by_model,
            jev_scorecards=jev_scorecards,
            simulate_rogue_model=args.simulate_dissent,
        )
        all_trade_results.append(res)

    # Generate benchmark leaderboards
    print("\n" + "=" * 80)
    print("PART 3: BENCHMARK SCORECARDS & LEADERBOARDS")
    print("=" * 80)

    leaderboard_html_parts = []
    for inv_id in ["A", "B", "C", "D"]:
        prof = get_investor_profile(inv_id)
        metrics_list = []
        # Add models
        for m in MODELS_LIST:
            metrics_list.append(scorecards_by_model[m["name"]][inv_id].to_metrics())
        # Add JEV
        metrics_list.append(jev_scorecards[inv_id].to_metrics())

        md_table = format_leaderboard_table(metrics_list, f"Investor {inv_id}: {prof.investor_name}")
        print(md_table)

        # Convert to HTML snippet
        table_html = f"<h4>Investor {inv_id}: {prof.investor_name}</h4><table class='data-table'><thead><tr>"
        table_html += "<th>Rank</th><th>Model</th><th>Constraint Compliance</th><th>Win Rate</th><th>Net Alpha (6M)</th><th>Abstention Rate</th></tr></thead><tbody>"
        for idx, met in enumerate(sorted(metrics_list, key=lambda x: x["constraint_compliance_pct"], reverse=True), 1):
            is_jev = "JEV" in met["model_name"]
            row_style = "style='background: rgba(56, 189, 248, 0.08); font-weight: bold;'" if is_jev else ""
            table_html += f"<tr {row_style}><td>{idx}</td><td>{met['model_name']}</td><td>{met['constraint_compliance_pct']}%</td><td>{met['win_rate_pct']}%</td><td>+{met['net_alpha_6m_pct']}%</td><td>{met['abstention_rate_pct']}%</td></tr>"
        table_html += "</tbody></table><br/>"
        leaderboard_html_parts.append(table_html)

    # Save JSON results
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(all_trade_results, f, indent=2)
    print(f"\n[Artifact Saved] JSON Results: {args.output_json}")

    # Generate HTML Dashboard for the primary evaluated trade
    if all_trade_results:
        primary_res = all_trade_results[0]
        html_content = generate_html_dashboard(
            trade_summary=primary_res["trade_summary"],
            results_per_investor=primary_res["investors"],
            leaderboard_html="".join(leaderboard_html_parts),
        )
        with open(args.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[Artifact Saved] Interactive HTML Dashboard: {args.output_html}")


if __name__ == "__main__":
    main()
