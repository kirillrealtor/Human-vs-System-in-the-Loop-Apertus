"""
Benchmark Cohort Selection and Full Dataset Evaluation Engine.
Curates a stratified, representative sample of congressional trades across:
- Defense contractors (Investor A audit)
- Technology leaders (Investor B audit)
- Broad multi-sector equities (Investor C audit)
- Unlisted / OTC assets (Investor D audit)
- Options and derivatives (Instrument rigor R4)
- Stale disclosure filings > 40 days (Timing lag R3)
- Top congressional traders (Pelosi, Khanna, McCaul, Tuberville, etc.)

Executes all 5 Peer Models + JEV Arbiter across Investors A, B, C, D,
and evaluates against real market ground-truth vs S&P 500 (SPY).
"""

import os
import json
import datetime
import pandas as pd
from typing import List, Dict, Any

from .models import EvidencePacket, InvestorProfile, ModelOutput, JEVReport
from .investor_profiles import INVESTOR_PROFILES, get_investor_profile
from .evidence_packet import build_evidence_packet
from .evaluator_engine import generate_model_signal, run_jev_evaluation, MODELS_LIST
from .ground_truth import compute_ground_truth_returns
from .benchmark_scorer import ModelScorecard, JEVScorecard, format_leaderboard_table


def select_stratified_cohort(csv_path: str = "all_2024_congress_trades.csv", sample_size: int = 50) -> pd.DataFrame:
    """
    Selects a stratified, balanced cohort of trades that thoroughly stresses every rule
    and investor constraint in the v2 specification.
    """
    df = pd.read_csv(csv_path)

    defense_tickers = ['LMT', 'RTX', 'NOC', 'GD', 'BA', 'HII', 'LHX', 'KTOS', 'TXT', 'PLTR']
    tech_tickers = ['NVDA', 'MSFT', 'AAPL', 'AMD', 'INTC', 'PANW', 'CRM', 'ADBE', 'ORCL', 'AVGO', 'CSCO', 'QCOM']
    non_tech_tickers = ['JNJ', 'PFE', 'UNH', 'JPM', 'BAC', 'GS', 'XOM', 'CVX', 'SBUX', 'CAT', 'DIS']

    # 1. Defense trades (Crucial for Investor A)
    defense_df = df[df['ticker'].isin(defense_tickers)].head(10)

    # 2. Tech purchases & sales (Crucial for Investor B)
    tech_df = df[df['ticker'].isin(tech_tickers)].head(12)

    # 3. Non-tech diversified blue chips (Crucial for Investor C & B negative testing)
    non_tech_df = df[df['ticker'].isin(non_tech_tickers)].head(10)

    # 4. Derivative options (Testing R4 instrument rigor)
    options_df = df[df['is_option'] == True].head(6)

    # 5. Stale disclosures > 40 days (Testing R3 timing awareness)
    stale_df = df[df['days_to_disclosure'] > 40].head(6)

    # 6. Unlisted / municipal / OTC assets (Testing Investor D & unresolvable edge cases)
    unlisted_df = df[df['ticker'].isna()].head(6)

    cohort = pd.concat([defense_df, tech_df, non_tech_df, options_df, stale_df, unlisted_df]).drop_duplicates(subset=['id'])

    # If below sample_size, fill with high-conviction trades
    if len(cohort) < sample_size:
        remaining_needed = sample_size - len(cohort)
        high_conv = df[~df['id'].isin(cohort['id']) & (df['amount_max_usd'] >= 250000)].head(remaining_needed)
        cohort = pd.concat([cohort, high_conv]).drop_duplicates(subset=['id'])

    return cohort.head(sample_size)


def run_full_cohort_evaluation(sample_size: int = 50, output_json: str = "benchmark_results_full.json") -> Dict[str, Any]:
    """
    Executes the entire v2 evaluation pipeline on the stratified cohort:
    - 5 Peer Models (Apertus 1.5-8B, Qwen 2.5-7B, Llama 3.1-8B, Gemma 2-9B, Mistral 7B)
    - 4 Investor Profiles (A, B, C, D)
    - JEV Arbiter Layer
    - Ground Truth market returns at 3M, 6M, 9M vs SPY
    """
    print(f"\n🚀 Selecting Stratified Benchmark Cohort ({sample_size} trades)...")
    cohort_df = select_stratified_cohort(sample_size=sample_size)
    print(f"✅ Selected {len(cohort_df)} unique trades covering Defense, Tech, Healthcare, Options, and Stale Filings.")

    # Initialize scorecards for all 5 peer models + JEV
    scorecards_by_model: Dict[str, Dict[str, ModelScorecard]] = {}
    for m in MODELS_LIST:
        scorecards_by_model[m["name"]] = {inv: ModelScorecard(m["name"], inv) for inv in ["A", "B", "C", "D"]}

    jev_scorecards = {inv: JEVScorecard(inv) for inv in ["A", "B", "C", "D"]}

    all_trade_records = []
    total_trades = len(cohort_df)

    print(f"⚡ Starting multi-model evaluation across {total_trades} trades (5 peer models x 4 investors = {total_trades * 20} model signals)...")

    for idx, (_, row) in enumerate(cohort_df.iterrows(), 1):
        raw_rec = row.to_dict()
        packet = build_evidence_packet(raw_rec)

        # Ground truth returns
        gt_returns = compute_ground_truth_returns(packet.asset.ticker, packet.timing.transaction_date)

        results_by_investor: Dict[str, Any] = {}

        for inv_id in ["A", "B", "C", "D"]:
            profile = get_investor_profile(inv_id)

            # Generate signals from all 5 peer models
            model_outputs: List[ModelOutput] = []
            for m_info in MODELS_LIST:
                mo = generate_model_signal(m_info, profile, packet)
                model_outputs.append(mo)

            # Run JEV Arbiter
            jev_report = run_jev_evaluation(profile, packet, model_outputs)

            # Record model scorecards using verified constraint status
            is_truth_pass = (jev_report.jev_constraint_check.passes is True)
            for m_info, mo in zip(MODELS_LIST, model_outputs):
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
            "ticker": packet.asset.ticker,
            "asset_name": packet.asset.asset_name,
            "asset_type": packet.asset.asset_type,
            "transaction_type": packet.trade.transaction_type,
            "amount_range": packet.trade.amount_range,
            "days_lag": packet.timing.days_to_disclosure,
            "transaction_date": packet.timing.transaction_date,
            "filing_date": packet.timing.filing_date,
            "flags": packet.data_quality_flags,
            "ground_truth": gt_returns,
            "investor_evaluations": results_by_investor,
        }
        all_trade_records.append(trade_summary)

        if idx % 10 == 0 or idx == total_trades:
            print(f"  [{idx}/{total_trades}] Trades evaluated with market benchmark.")

    # Compile Leaderboard Metrics
    leaderboard_data = {}
    for inv_id in ["A", "B", "C", "D"]:
        metrics_list = []
        for m in MODELS_LIST:
            metrics_list.append(scorecards_by_model[m["name"]][inv_id].to_metrics())
        metrics_list.append(jev_scorecards[inv_id].to_metrics())
        leaderboard_data[inv_id] = metrics_list

    final_results = {
        "benchmark_metadata": {
            "total_trades_evaluated": total_trades,
            "evaluation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "peer_models": [m["name"] for m in MODELS_LIST],
            "investor_profiles": ["A", "B", "C", "D"],
            "ground_truth_benchmark": "S&P 500 (SPY)",
        },
        "leaderboards": leaderboard_data,
        "trades": all_trade_records,
    }

    # Save to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2)
    print(f"\n💾 Full Benchmark Dataset saved to: {output_json}")

    return final_results
