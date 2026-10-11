"""
Interactive HTML Dashboard Generator for Congressional Trade Evaluation (v2).
Produces a modern, responsive HTML view of Trade Evidence, Investor Constraints, Model Signals, and JEV Decisions.
"""

from typing import List, Dict, Any
import json


def generate_html_dashboard(
    trade_summary: Dict[str, Any],
    results_per_investor: Dict[str, Dict[str, Any]],
    leaderboard_html: str = "",
) -> str:
    """Generate a self-contained, high-aesthetic HTML dashboard."""
    
    # Pre-render investor cards
    investor_cards = ""
    for inv_id in ["A", "B", "C", "D"]:
        data = results_per_investor.get(inv_id, {})
        if not data:
            continue
        profile = data["profile"]
        report = data["jev_report"]
        models = data["model_outputs"]

        # Signal color styling
        sig = report["final_call"]["signal"]
        sig_class = "sig-buy" if sig == "BUY" else ("sig-sell" if sig == "SELL" else "sig-abstain")
        constraint_passed = report["jev_constraint_check"]["passes"]
        c_status_class = "badge-pass" if constraint_passed is True else ("badge-fail" if constraint_passed is False else "badge-warn")
        c_status_text = "PASSED" if constraint_passed is True else ("FAILED" if constraint_passed is False else "UNVERIFIED")

        # Models table rows
        model_rows = ""
        for me in report["model_evaluations"]:
            st = me["status"]
            st_class = "badge-selected" if st == "SELECTED" else ("badge-weighted" if st == "WEIGHTED" else "badge-discounted")
            flaws_str = ", ".join(me["flaws"]) if me["flaws"] else "None"
            r_scores = me["rubric_scores"]
            total_r = sum(r_scores.values())

            model_rows += f"""
            <tr>
                <td><strong>{me['model_id']}</strong></td>
                <td><span class="signal-tag {me['model_signal'].lower()}">{me['model_signal']}</span></td>
                <td><span class="{st_class}">{st}</span></td>
                <td>{(me['weight_assigned'] * 100):.1f}%</td>
                <td><strong>{total_r}/40</strong> <small class="text-muted">(R1:{r_scores['R1_constraint_accuracy']}, R3:{r_scores['R3_timing_awareness']}, R8:{r_scores['R8_time_boundary_hygiene']})</small></td>
                <td><small class="flaws-text">{flaws_str}</small></td>
            </tr>
            """

        investor_cards += f"""
        <div class="investor-panel card" id="inv-panel-{inv_id}">
            <div class="card-header d-flex justify-between align-center">
                <div>
                    <span class="inv-id-badge">Investor {inv_id}</span>
                    <h3 class="panel-title">{profile['investor_name']}</h3>
                </div>
                <div class="d-flex align-center gap-10">
                    <span class="badge {c_status_class}">Constraint {c_status_text}</span>
                    <span class="final-signal-badge {sig_class}">{sig}</span>
                </div>
            </div>
            
            <div class="card-body">
                <div class="constraint-box">
                    <strong>Mandate & Constraint:</strong> {profile['hard_constraint']}
                    <div class="mt-5 text-secondary"><strong>JEV Audit:</strong> {report['jev_constraint_check']['explanation']}</div>
                </div>

                <div class="jev-call-box mt-15">
                    <div class="d-flex justify-between align-center">
                        <h4 class="jev-heading">JEV Arbiter Decision Support</h4>
                        <span class="text-muted">Target Horizon: <strong>{report['final_call']['horizon'] or 'N/A'}</strong> | Abstain Reason: <strong>{report['final_call']['abstain_reason'] or 'N/A'}</strong></span>
                    </div>
                    <p class="final-rationale mt-5">{report['final_call']['final_rationale']}</p>
                    <div class="investor-msg-box mt-10">
                        <span class="msg-icon">&#128172;</span> <em>"{report['investor_message']}"</em>
                    </div>
                </div>

                <div class="models-section mt-20">
                    <h4 class="sub-heading">Multi-Model Audit & Scoring Matrix (Rubric R1-R8)</h4>
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Model</th>
                                    <th>Model Signal</th>
                                    <th>JEV Status</th>
                                    <th>Assigned Weight</th>
                                    <th>Rubric Score</th>
                                    <th>Detected Flaws</th>
                                </tr>
                            </thead>
                            <tbody>
                                {model_rows}
                            </tbody>
                        </table>
                    </div>
                    <div class="selection-rationale mt-10">
                        <strong>Model Selection Analytics:</strong> {report['model_selection_analytics']['selection_rationale']}
                    </div>
                </div>
            </div>
        </div>
        """

    # Data quality flags tags
    flags_html = "".join([f'<span class="flag-tag">{f}</span>' for f in trade_summary.get("flags", [])]) or "<span class='text-muted'>None</span>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congressional Trade Evaluation v2 - JEV Arbiter</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #0b0f17;
            --bg-surface: #141b26;
            --bg-elevated: #1d2737;
            --text-primary: #f0f4f8;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border-color: #243144;
            --accent-blue: #38bdf8;
            --accent-indigo: #6366f1;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-amber: #f59e0b;
            --accent-purple: #a855f7;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg-base);
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, sans-serif;
            line-height: 1.5;
            padding: 24px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 28px 36px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .header-title {{
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header-sub {{ color: var(--text-secondary); font-size: 14px; margin-top: 6px; }}
        .card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            margin-bottom: 20px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card-header {{
            background: var(--bg-elevated);
            padding: 16px 24px;
            border-bottom: 1px solid var(--border-color);
        }}
        .card-body {{ padding: 22px 24px; }}
        .d-flex {{ display: flex; }}
        .justify-between {{ justify-content: space-between; }}
        .align-center {{ align-items: center; }}
        .gap-10 {{ gap: 10px; }}
        .gap-15 {{ gap: 15px; }}
        .mt-5 {{ margin-top: 5px; }}
        .mt-10 {{ margin-top: 10px; }}
        .mt-15 {{ margin-top: 15px; }}
        .mt-20 {{ margin-top: 20px; }}
        .text-muted {{ color: var(--text-muted); }}
        .text-secondary {{ color: var(--text-secondary); }}
        
        /* Trade Summary Grid */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }}
        .metric-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px 18px;
        }}
        .metric-label {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; }}
        .metric-val {{ font-size: 18px; font-weight: 700; color: var(--text-primary); margin-top: 4px; font-family: 'JetBrains Mono', monospace; }}
        
        /* Badges & Signals */
        .badge {{
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge-pass {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }}
        .badge-fail {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626; }}
        .badge-warn {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #d97706; }}
        .badge-selected {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #0284c7; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}
        .badge-weighted {{ background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid #7e22ce; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}
        .badge-discounted {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #b91c1c; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}

        .final-signal-badge {{
            padding: 6px 18px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 800;
            letter-spacing: 0.05em;
        }}
        .sig-buy {{ background: #059669; color: #fff; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }}
        .sig-sell {{ background: #dc2626; color: #fff; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }}
        .sig-abstain {{ background: #475569; color: #f1f5f9; }}
        .signal-tag {{ padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }}
        .signal-tag.buy {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
        .signal-tag.sell {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
        .signal-tag.abstain {{ background: rgba(100, 116, 139, 0.2); color: #94a3b8; }}

        .inv-id-badge {{
            background: var(--accent-indigo);
            color: #fff;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .panel-title {{ font-size: 18px; font-weight: 700; margin-top: 4px; }}
        .constraint-box {{
            background: rgba(15, 23, 42, 0.5);
            border-left: 4px solid var(--accent-blue);
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            font-size: 13px;
        }}
        .jev-call-box {{
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 16px;
        }}
        .jev-heading {{ font-size: 14px; font-weight: 700; color: var(--accent-blue); }}
        .final-rationale {{ font-size: 14px; color: var(--text-primary); }}
        .investor-msg-box {{
            background: rgba(15, 23, 42, 0.8);
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            color: #cbd5e1;
        }}
        
        /* Table Styles */
        .table-responsive {{ overflow-x: auto; margin-top: 10px; }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}
        .data-table th {{
            background: var(--bg-elevated);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 10px 14px;
            border-bottom: 1px solid var(--border-color);
        }}
        .data-table td {{
            padding: 10px 14px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
        }}
        .data-table tr:hover td {{ background: rgba(255, 255, 255, 0.02); }}
        .flaws-text {{ color: #f87171; font-family: 'JetBrains Mono', monospace; font-size: 11px; }}
        .selection-rationale {{ font-size: 12px; color: var(--text-secondary); }}
        .flag-tag {{
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 11px;
            margin-right: 6px;
            display: inline-block;
            margin-top: 4px;
        }}
        .leaderboard-container {{ margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="header-title">Congressional Trade Evaluation Pipeline (v2)</h1>
            <p class="header-sub">Multi-Model Decision Support & JEV Arbiter System with Hard Investor Constraints</p>
        </header>

        <!-- Trade Evidence Card -->
        <div class="card">
            <div class="card-header d-flex justify-between align-center">
                <h3 style="font-size: 17px; font-weight: 700;">Trade Evidence Packet: {trade_summary.get('trade_id')}</h3>
                <span class="text-muted">Origin: <strong>{trade_summary.get('data_origin')}</strong></span>
            </div>
            <div class="card-body">
                <div class="summary-grid">
                    <div class="metric-box">
                        <div class="metric-label">Politician</div>
                        <div class="metric-val">{trade_summary.get('politician_name')}</div>
                        <small class="text-muted">{trade_summary.get('party')} | {trade_summary.get('chamber')} ({trade_summary.get('district') or 'At-Large'})</small>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Security & Issuer</div>
                        <div class="metric-val">{trade_summary.get('ticker') or 'N/A'}</div>
                        <small class="text-muted">{trade_summary.get('asset_name')} ({trade_summary.get('asset_type')})</small>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Transaction Type & Size</div>
                        <div class="metric-val">{trade_summary.get('transaction_type')}</div>
                        <small class="text-muted">{trade_summary.get('amount_range')} (Owner: {trade_summary.get('owner')})</small>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Timing & Disclosure Lag</div>
                        <div class="metric-val">{trade_summary.get('days_lag')} Days Lag</div>
                        <small class="text-muted">Traded: {trade_summary.get('transaction_date')} | Filed: {trade_summary.get('filing_date')}</small>
                    </div>
                </div>

                <div class="mt-15">
                    <strong style="font-size: 12px; text-transform: uppercase; color: var(--text-muted);">Data Quality Flags:</strong>
                    <div class="mt-5">{flags_html}</div>
                </div>
            </div>
        </div>

        <!-- 4 Investor Profiles Cards -->
        <h2 style="font-size: 20px; font-weight: 800; margin: 26px 0 16px 4px; color: #e2e8f0;">
            Investor-Specific Evaluations (Zero Cross-Talk Architecture)
        </h2>
        {investor_cards}

        <!-- Leaderboard section -->
        <div class="leaderboard-container card">
            <div class="card-header">
                <h3 style="font-size: 17px; font-weight: 700;">Track 1 & Track 2 Benchmark Leaderboard</h3>
            </div>
            <div class="card-body">
                {leaderboard_html}
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html
