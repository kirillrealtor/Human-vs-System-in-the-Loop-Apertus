"""
Master Benchmark Execution Script for 2024 Congressional Trades Dataset.
Runs full evaluation across 5 Peer Models and JEV Arbiter for Investors A-D,
computes ground-truth vs S&P 500, and generates publication-grade reports and dashboards.
"""

import sys
import argparse

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pipeline.benchmark_cohort import run_full_cohort_evaluation
from pipeline.report_generator import generate_executive_markdown, generate_interactive_html


def main():
    parser = argparse.ArgumentParser(description="Congressional Trades Comprehensive Peer Benchmark")
    parser.add_argument("--size", type=int, default=50, help="Number of stratified trades to evaluate (default: 50)")
    parser.add_argument("--output_json", type=str, default="benchmark_results_full.json", help="Output JSON path")
    parser.add_argument("--output_report", type=str, default="BENCHMARK_EXECUTIVE_REPORT.md", help="Output Markdown report path")
    parser.add_argument("--output_html", type=str, default="dashboard.html", help="Output HTML dashboard path")
    args = parser.parse_args()

    print("=" * 80)
    print("CONGRESSIONAL TRADE EVALUATION: COMPREHENSIVE PEER BENCHMARK (v2)")
    print("=" * 80)
    print(f"Target Cohort Size: {args.size} stratified trades across 2024 STOCK Act dataset.")

    # Execute full cohort evaluation
    benchmark_data = run_full_cohort_evaluation(sample_size=args.size, output_json=args.output_json)

    # Generate Executive Markdown Report
    print(f"\n📝 Generating Executive Research Report...")
    report_md = generate_executive_markdown(benchmark_data)
    with open(args.output_report, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"📄 Publication-grade report saved to: {args.output_report}")

    # Generate Interactive HTML Dashboard
    print(f"\n🌐 Generating Multi-Tab Interactive Dashboard...")
    dashboard_html = generate_interactive_html(benchmark_data)
    with open(args.output_html, "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    print(f"✨ Interactive Dashboard saved to: {args.output_html}")

    print("\n" + "=" * 80)
    print("✅ BENCHMARK EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
