"""
CLI tool for step-by-step model recording and JEV Arbiter evaluation.
Allows recording models one-by-one as you change models in Antigravity,
and generating the final stunning JEV report when ready.
"""

import sys
import argparse

# Force UTF-8 stdout for Windows consoles to support rich emojis and symbols
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pipeline.session_manager import (
    record_model_run,
    list_recorded_models,
    run_jev_on_session,
    generate_cool_markdown_report,
    load_trade_record,
)
from pipeline.dashboard_generator import generate_html_dashboard


def main():
    parser = argparse.ArgumentParser(description="Step-by-Step Model Recorder and JEV Arbiter")
    parser.add_argument("--trade", type=str, default="US-CONG-2024-00008", help="Trade ID to evaluate")
    parser.add_argument("--model", type=str, help="Record signal for this specific model (e.g. 'Gemini-3.8-Flash')")
    parser.add_argument("--version", type=str, default="1.0", help="Model version")
    parser.add_argument("--status", action="store_true", help="Show which models have recorded signals for this trade")
    parser.add_argument("--jev", action="store_true", help="Run JEV Arbiter on all recorded models and generate report")
    parser.add_argument("--output_md", type=str, help="Output markdown report path")
    args = parser.parse_args()

    trade_id = args.trade

    # Check status
    if args.status:
        recorded = list_recorded_models(trade_id)
        print(f"\n[Trade {trade_id}] Recorded Models Status:")
        if not recorded:
            print("  No models recorded yet.")
        else:
            for r in recorded:
                print(f"  • {r['model_name']} (Recorded at: {r['recorded_at']})")
        return

    # Record specific model
    if args.model:
        print(f"\nRecording signal for model: '{args.model}' on trade {trade_id}...")
        res = record_model_run(trade_id, args.model, args.version)
        print(f"✅ Successfully saved signals to: {res['saved_to']}")
        print(f"  Signals across investors: A={res['investor_signals']['A']['signal']}, "
              f"B={res['investor_signals']['B']['signal']}, C={res['investor_signals']['C']['signal']}, "
              f"D={res['investor_signals']['D']['signal']}")
        
        recorded = list_recorded_models(trade_id)
        print(f"\nTotal models recorded so far: {len(recorded)} ({[r['model_name'] for r in recorded]})")

    # Run JEV Arbiter
    if args.jev or not args.model:
        recorded = list_recorded_models(trade_id)
        if not recorded and args.model:
            # We just recorded one
            pass
        elif not recorded:
            print(f"No models recorded yet for {trade_id}. Auto-recording current model 'Gemini-3.8-Flash'...")
            record_model_run(trade_id, "Gemini-3.8-Flash", "1.0")

        print(f"\n⚖️ Running JEV Arbiter across recorded models for trade {trade_id}...")
        session_res = run_jev_on_session(trade_id)
        raw_rec = load_trade_record(trade_id)

        # Generate markdown report
        md_report = generate_cool_markdown_report(session_res, raw_rec)
        out_md = args.output_md or f"JEV_REPORT_{trade_id}.md"
        with open(out_md, "w", encoding="utf-8") as f:
            f.write(md_report)
        print(f"📄 Cool Markdown Report saved to: {out_md}")

        # Also update dashboard.html
        from pipeline.dashboard_generator import generate_html_dashboard
        trade_summary = {
            "trade_id": raw_rec.get("id"),
            "politician_name": raw_rec.get("politician_name"),
            "party": raw_rec.get("party"),
            "chamber": raw_rec.get("chamber"),
            "district": raw_rec.get("state_district"),
            "ticker": raw_rec.get("ticker"),
            "asset_name": raw_rec.get("asset_name"),
            "asset_type": raw_rec.get("asset_type"),
            "transaction_type": raw_rec.get("transaction_type"),
            "amount_range": raw_rec.get("amount_range"),
            "owner": raw_rec.get("owner"),
            "days_lag": raw_rec.get("days_to_disclosure"),
            "transaction_date": raw_rec.get("transaction_date"),
            "filing_date": raw_rec.get("filing_date"),
            "data_origin": raw_rec.get("source"),
            "flags": [],
        }
        
        formatted_investors = {}
        for inv_id in ["A", "B", "C", "D"]:
            from pipeline.investor_profiles import get_investor_profile
            prof = get_investor_profile(inv_id)
            formatted_investors[inv_id] = {
                "profile": prof.model_dump(),
                "jev_report": session_res["jev_reports"][inv_id],
                "model_outputs": [],
            }

        html = generate_html_dashboard(trade_summary, formatted_investors)
        with open("dashboard.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"🌐 Interactive HTML Dashboard updated: dashboard.html")


if __name__ == "__main__":
    main()
