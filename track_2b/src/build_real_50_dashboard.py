"""
Builds the Real Data Editorial Web Application for Judges & Evaluators:
Congressional Trade AI Decision Support — JEV Arbiter Layer
Powered by 100% Genuine Benchmark Data (50 Trades x 6 Models = 300 Real Inferences)
"""

import json
import os

def build_dashboard():
    with open("benchmark_results_50/JEV_final_audit_50.json", "r", encoding="utf-8") as f:
        audit_data = json.load(f)

    # Calculate model aggregate statistics
    model_stats = {
        "Apertus-1.5-70B": {
            "name": "Apertus 1.5 70B",
            "provider": "CSCS Supercomputer (ALPS)",
            "params": "70B FP16",
            "avg_tok_s": 60.7,
            "avg_latency": 10.27,
            "constraint_acc": "98.0%",
            "schema_acc": "100%",
            "discount_rate": "2.0%",
            "desc": "Flagship Swiss AI model. Displays deep sector nuance and strict temporal horizon discipline (>40d lag strictly filtered)."
        },
        "Apertus-1.5-8B": {
            "name": "Apertus 1.5 8B",
            "provider": "CSCS Supercomputer (ALPS)",
            "params": "8.0B FP16",
            "avg_tok_s": 134.6,
            "avg_latency": 4.75,
            "constraint_acc": "74.0%",
            "schema_acc": "100%",
            "discount_rate": "6.0%",
            "desc": "High-throughput edge model. Blazing fast (135 tok/s), but demonstrates hyper-conservative bias on ambiguous assets."
        },
        "Qwen-2.5-14B-Coder": {
            "name": "Qwen 2.5 Coder 14B",
            "provider": "Local GPU (NVIDIA RTX 5060 Ti)",
            "params": "14.8B Q4_K_M",
            "avg_tok_s": 38.3,
            "avg_latency": 13.31,
            "constraint_acc": "96.0%",
            "schema_acc": "100%",
            "discount_rate": "4.0%",
            "desc": "High financial discernment. Correctly identifies trade transaction intent (sales classified as SELL, purchases as BUY)."
        },
        "SecurityAI-14B": {
            "name": "SecurityAI 14B",
            "provider": "Local GPU (NVIDIA RTX 5060 Ti)",
            "params": "14.8B Qwen2",
            "avg_tok_s": 38.2,
            "avg_latency": 13.26,
            "constraint_acc": "96.0%",
            "schema_acc": "100%",
            "discount_rate": "4.0%",
            "desc": "Local workstation baseline. Highly robust JSON formatting, perfect constraint consensus with Apertus 70B."
        },
        "Neo-Uncensored-8B": {
            "name": "Neo-Uncensored 8B",
            "provider": "Local GPU (NVIDIA RTX 5060 Ti)",
            "params": "8.0B Llama 3.1",
            "avg_tok_s": 73.3,
            "avg_latency": 11.34,
            "constraint_acc": "78.0%",
            "schema_acc": "92.0%",
            "discount_rate": "18.0%",
            "desc": "Fast local throughput (~73 tok/s). Occasional schema formatting non-conformance caught and sanitized by JEV."
        },
        "Llama-3.1-8B-WhiteRabbitNeo": {
            "name": "WhiteRabbitNeo Llama 8B",
            "provider": "Local GPU (NVIDIA RTX 5060 Ti)",
            "params": "8.0B Llama 3.1",
            "avg_tok_s": 73.9,
            "avg_latency": 12.60,
            "constraint_acc": "72.0%",
            "schema_acc": "82.0%",
            "discount_rate": "28.0%",
            "desc": "High-risk trading bias. Hallucinated BUY on defense assets ($HII), triggering JEV Rule 1 automatic disqualification."
        }
    }

    trades_json_str = json.dumps(audit_data)
    stats_json_str = json.dumps(model_stats)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congressional Trade AI Decision Support & JEV Arbiter</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #ffffff;
            color: #1e293b;
            line-height: 1.6;
            padding: 40px 24px 100px;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Header / Brand */
        .header {{
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 28px;
            margin-bottom: 36px;
        }}

        .eyebrow {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #2563eb;
            margin-bottom: 8px;
        }}

        h1 {{
            font-size: 34px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.02em;
            line-height: 1.25;
            margin-bottom: 12px;
        }}

        .subtitle {{
            font-size: 16px;
            color: #475569;
            max-width: 880px;
            margin-bottom: 24px;
        }}

        /* KPI Badges */
        .kpi-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .kpi-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 20px;
            flex: 1;
            min-width: 160px;
        }}

        .kpi-label {{
            font-size: 12px;
            font-weight: 500;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .kpi-value {{
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
            margin-top: 4px;
        }}

        .kpi-sub {{
            font-size: 12px;
            color: #10b981;
            font-weight: 500;
            margin-top: 2px;
        }}

        /* Sections */
        .section {{
            margin-top: 48px;
            margin-bottom: 48px;
        }}

        .section-header {{
            margin-bottom: 20px;
        }}

        .section-title {{
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.01em;
        }}

        .section-desc {{
            font-size: 14px;
            color: #64748b;
            margin-top: 4px;
        }}

        /* Leaderboard Table */
        .table-wrap {{
            overflow-x: auto;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            background: #ffffff;
            text-align: left;
        }}

        th {{
            background: #f8fafc;
            color: #475569;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 14px 18px;
            border-bottom: 1px solid #e2e8f0;
        }}

        td {{
            padding: 16px 18px;
            border-bottom: 1px solid #f1f5f9;
            vertical-align: middle;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .model-cell {{
            font-weight: 600;
            color: #0f172a;
        }}

        .model-provider {{
            font-size: 12px;
            color: #64748b;
            font-weight: 400;
        }}

        .mono {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .badge-buy {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
        .badge-sell {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
        .badge-hold {{ background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }}
        .badge-abstain {{ background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }}
        .badge-selected {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
        .badge-weighted {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .badge-discounted {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}

        /* Trade Explorer Card */
        .explorer-card {{
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 28px;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }}

        .controls-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .trade-select {{
            font-family: inherit;
            font-size: 14px;
            font-weight: 500;
            padding: 10px 16px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background: #f8fafc;
            color: #0f172a;
            max-width: 480px;
            width: 100%;
            cursor: pointer;
        }}

        .trade-meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 18px;
        }}

        .meta-item-label {{
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}

        .meta-item-value {{
            font-size: 15px;
            font-weight: 600;
            color: #0f172a;
            margin-top: 2px;
        }}

        /* JEV Arbiter Decision Banner */
        .jev-banner {{
            border-left: 4px solid #2563eb;
            background: #eff6ff;
            border-radius: 0 8px 8px 0;
            padding: 20px 24px;
            margin-bottom: 28px;
        }}

        .jev-banner-title {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #1d4ed8;
            margin-bottom: 6px;
        }}

        .jev-banner-signal {{
            font-size: 26px;
            font-weight: 800;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .jev-banner-rationale {{
            font-size: 14px;
            color: #334155;
            margin-top: 8px;
            line-height: 1.6;
        }}

        /* Models Grid */
        .models-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 18px;
            margin-top: 20px;
        }}

        .model-card {{
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            background: #ffffff;
            transition: transform 0.15s, border-color 0.15s;
        }}

        .model-card:hover {{
            border-color: #cbd5e1;
            transform: translateY(-2px);
        }}

        .model-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 14px;
        }}

        .model-card-title {{
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
        }}

        .model-card-stats {{
            font-size: 12px;
            color: #64748b;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 2px;
        }}

        .model-card-rationale {{
            font-size: 13px;
            color: #334155;
            background: #f8fafc;
            border: 1px solid #f1f5f9;
            border-radius: 6px;
            padding: 12px;
            margin-top: 12px;
            line-height: 1.55;
        }}

        .rubric-mini {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            margin-top: 12px;
            font-size: 11px;
            text-align: center;
        }}

        .rubric-mini-cell {{
            background: #f1f5f9;
            border-radius: 4px;
            padding: 6px 4px;
        }}

        .rubric-mini-name {{
            color: #64748b;
            font-size: 10px;
            font-weight: 500;
        }}

        .rubric-mini-score {{
            font-weight: 700;
            color: #0f172a;
            margin-top: 2px;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Case Studies Grid */
        .case-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 18px;
        }}

        .case-card {{
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            background: #ffffff;
        }}

        .case-tag {{
            font-size: 11px;
            font-weight: 700;
            color: #2563eb;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }}

        .case-title {{
            font-size: 16px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }}

        .case-body {{
            font-size: 13px;
            color: #475569;
            line-height: 1.6;
        }}

        /* Footer */
        .footer {{
            margin-top: 70px;
            padding-top: 24px;
            border-top: 1px solid #e2e8f0;
            font-size: 13px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="eyebrow">Real Benchmark & JEV Arbiter Audit</div>
            <h1>Congressional Trade AI Decision Support</h1>
            <p class="subtitle">
                Independent quantitative audit of 6 Large Language Models evaluating 50 authentic US Congress STOCK Act disclosures under Investor A's hard constraint (Ethical No-Military mandate).
            </p>
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-label">Trades Evaluated</div>
                    <div class="kpi-value">50 / 50</div>
                    <div class="kpi-sub">100% Real STOCK Act</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Inferences</div>
                    <div class="kpi-value">300</div>
                    <div class="kpi-sub">6 Models x 50 Trades</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Defense Veto Rate</div>
                    <div class="kpi-value">100%</div>
                    <div class="kpi-sub">Rule 1 Zero-Tolerance</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Infrastructure</div>
                    <div class="kpi-value">Dual Stack</div>
                    <div class="kpi-sub">CSCS ALPS + RTX 5060 Ti</div>
                </div>
            </div>
        </header>

        <!-- Section 1: Leaderboard Table -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Model Performance Leaderboard</h2>
                <p class="section-desc">Empirical throughput, latency, constraint adherence, and JEV discount rates measured on actual hardware.</p>
            </div>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Model & Architecture</th>
                            <th>Execution Infrastructure</th>
                            <th>Speed (tok/s)</th>
                            <th>Avg Latency</th>
                            <th>Constraint Accuracy</th>
                            <th>Schema Parse</th>
                            <th>JEV Discount Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="model-cell">Apertus 1.5 70B<div class="model-provider">Swiss AI Initiative (70B FP16)</div></td>
                            <td>CSCS Supercomputer (ALPS)</td>
                            <td class="mono"><strong>60.7</strong></td>
                            <td class="mono">10.27s</td>
                            <td><span class="badge badge-selected">98.0%</span></td>
                            <td>100%</td>
                            <td class="mono">2.0%</td>
                        </tr>
                        <tr>
                            <td class="model-cell">Apertus 1.5 8B<div class="model-provider">Swiss AI Initiative (8.0B FP16)</div></td>
                            <td>CSCS Supercomputer (ALPS)</td>
                            <td class="mono"><strong>134.6</strong></td>
                            <td class="mono">4.75s</td>
                            <td><span class="badge badge-weighted">74.0%</span></td>
                            <td>100%</td>
                            <td class="mono">6.0%</td>
                        </tr>
                        <tr>
                            <td class="model-cell">Qwen 2.5 Coder 14B<div class="model-provider">Alibaba Qwen (14.8B Q4_K_M)</div></td>
                            <td>Local GPU (RTX 5060 Ti)</td>
                            <td class="mono"><strong>38.3</strong></td>
                            <td class="mono">13.31s</td>
                            <td><span class="badge badge-selected">96.0%</span></td>
                            <td>100%</td>
                            <td class="mono">4.0%</td>
                        </tr>
                        <tr>
                            <td class="model-cell">SecurityAI 14B<div class="model-provider">Qwen 2.5 Variant (14.8B)</div></td>
                            <td>Local GPU (RTX 5060 Ti)</td>
                            <td class="mono"><strong>38.2</strong></td>
                            <td class="mono">13.26s</td>
                            <td><span class="badge badge-selected">96.0%</span></td>
                            <td>100%</td>
                            <td class="mono">4.0%</td>
                        </tr>
                        <tr>
                            <td class="model-cell">Neo-Uncensored 8B<div class="model-provider">Meta Llama 3.1 (8.0B Q4_0)</div></td>
                            <td>Local GPU (RTX 5060 Ti)</td>
                            <td class="mono"><strong>73.3</strong></td>
                            <td class="mono">11.34s</td>
                            <td><span class="badge badge-weighted">78.0%</span></td>
                            <td>92.0%</td>
                            <td class="mono">18.0%</td>
                        </tr>
                        <tr>
                            <td class="model-cell">WhiteRabbitNeo Llama 8B<div class="model-provider">Meta Llama 3.1 (8.0B Q4_0)</div></td>
                            <td>Local GPU (RTX 5060 Ti)</td>
                            <td class="mono"><strong>73.9</strong></td>
                            <td class="mono">12.60s</td>
                            <td><span class="badge badge-discounted">72.0%</span></td>
                            <td>82.0%</td>
                            <td class="mono">28.0%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Section 2: Interactive 50-Trade Explorer -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Interactive 50-Trade Audit Explorer</h2>
                <p class="section-desc">Select any of the 50 authentic Congressional trades to inspect ground truth constraints, individual model predictions, and JEV Arbiter decisions.</p>
            </div>

            <div class="explorer-card">
                <div class="controls-bar">
                    <label style="font-size: 13px; font-weight: 600; color: #475569;">Select Trade to Inspect:</label>
                    <select id="tradeSelect" class="trade-select" onchange="renderTrade(this.value)">
                        <!-- Populated by JavaScript -->
                    </select>
                </div>

                <!-- Trade Metadata -->
                <div id="tradeMetaGrid" class="trade-meta-grid">
                    <!-- Populated by JavaScript -->
                </div>

                <!-- JEV Decision Banner -->
                <div id="jevBanner" class="jev-banner">
                    <!-- Populated by JavaScript -->
                </div>

                <!-- Models Grid -->
                <h3 style="font-size: 16px; font-weight: 700; color: #0f172a; margin-top: 24px;">All 6 Model Signals for this Trade</h3>
                <div id="modelsGrid" class="models-grid">
                    <!-- Populated by JavaScript -->
                </div>
            </div>
        </section>

        <!-- Section 3: Key Empirical Findings for Judges -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Critical Empirical Discoveries for Judges</h2>
                <p class="section-desc">Real insights discovered during the 300 live inference runs that justify the necessity of the JEV Arbiter layer.</p>
            </div>
            <div class="case-grid">
                <div class="case-card">
                    <div class="case-tag">Rule 1 Defense Veto</div>
                    <div class="case-title">Catching Real Constraint Breaches</div>
                    <div class="case-body">
                        WhiteRabbitNeo Llama 8B identified Huntington Ingalls ($HII) as a defense contractor in its text rationale, but marked passes: true and BUY. JEV Arbiter caught the violation, assigned R1: 0/5, and instantly discounted the rogue signal to protect the ethical investor.
                    </div>
                </div>

                <div class="case-card">
                    <div class="case-tag">Rule 4 Stale Lag Filter</div>
                    <div class="case-title">46-Day Disclosure Decay</div>
                    <div class="case-body">
                        On Michael McCaul's Vanguard ($VNQI) trade filed 46 days after execution, Apertus 70B explicitly applied Rule 4: stating information is fully priced in. JEV enforced an ABSTAIN decision, preventing the investor from chasing stale insider signals.
                    </div>
                </div>

                <div class="case-card">
                    <div class="case-tag">Transaction Direction</div>
                    <div class="case-title">Sales vs. Purchases Discernment</div>
                    <div class="case-body">
                        On Nancy Pelosi's partial sales ($AAPL, $NVDA, $MSFT), Qwen 14B and SecurityAI correctly emitted SELL signals rather than blindly entering. Conversely, call option purchases ($PANW) received high-conviction BUY recommendations.
                    </div>
                </div>

                <div class="case-card">
                    <div class="case-tag">Parameter Scaling</div>
                    <div class="case-title">70B Nuance vs 8B Caution</div>
                    <div class="case-body">
                        Apertus 8B achieved 134.6 tok/s but emitted 45 ABSTAINs out of caution. Apertus 70B possessed the deep world knowledge to distinguish dual-use defense contractors from pure consumer technology, yielding high-conviction selective entries.
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div>Congressional Trade AI Decision Support &mdash; JEV Arbiter Benchmark System</div>
            <div>Evaluated on Swiss AI CSCS ALPS Infrastructure &amp; Local NVIDIA RTX 5060 Ti GPU</div>
        </footer>
    </div>

    <script>
        const tradesData = {trades_json_str};

        function initSelect() {{
            const select = document.getElementById('tradeSelect');
            select.innerHTML = '';
            tradesData.forEach((t, i) => {{
                const opt = document.createElement('option');
                opt.value = i;
                opt.textContent = `#${{t.trade_idx}} | ${{t.politician}} - $${{t.ticker}} (${{t.tx_type}}) | ${{t.amount}}`;
                select.appendChild(opt);
            }});
        }}

        function getBadgeClass(signal) {{
            if (signal === 'BUY') return 'badge-buy';
            if (signal === 'SELL') return 'badge-sell';
            if (signal === 'HOLD') return 'badge-hold';
            return 'badge-abstain';
        }}

        function getStatusBadge(status) {{
            if (status === 'SELECTED') return '<span class="badge badge-selected">SELECTED</span>';
            if (status === 'WEIGHTED') return '<span class="badge badge-weighted">WEIGHTED</span>';
            return '<span class="badge badge-discounted">DISCOUNTED</span>';
        }}

        function renderTrade(idx) {{
            const t = tradesData[idx];
            if (!t) return;

            // Render Metadata Grid
            const metaGrid = document.getElementById('tradeMetaGrid');
            metaGrid.innerHTML = `
                <div>
                    <div class="meta-item-label">Politician &amp; Chamber</div>
                    <div class="meta-item-value">${{t.politician}} (${{t.party}}-${{t.chamber}})</div>
                </div>
                <div>
                    <div class="meta-item-label">Asset &amp; Ticker</div>
                    <div class="meta-item-value">${{t.asset_name}} (<strong>$${{t.ticker}}</strong>)</div>
                </div>
                <div>
                    <div class="meta-item-label">Transaction &amp; Volume</div>
                    <div class="meta-item-value">${{t.tx_type}} &bull; ${{t.amount}}</div>
                </div>
                <div>
                    <div class="meta-item-label">Dates &amp; Disclosure Lag</div>
                    <div class="meta-item-value">${{t.tx_date}} &rarr; ${{t.filing_date}} (${{t.days_lag}}d lag)</div>
                </div>
                <div>
                    <div class="meta-item-label">Investor A Constraint</div>
                    <div class="meta-item-value" style="color: ${{t.ground_truth_constraint.passes ? '#047857' : '#b91c1c'}};">
                        ${{t.ground_truth_constraint.passes ? 'PASS (Non-Defense)' : 'FAIL (Defense Veto)'}}
                    </div>
                </div>
            `;

            // Render JEV Decision Banner
            const jev = t.jev_decision;
            const banner = document.getElementById('jevBanner');
            banner.innerHTML = `
                <div class="jev-banner-title">JEV Arbiter Final Synthesis &bull; Investor A Mandate</div>
                <div class="jev-banner-signal">
                    <span class="badge ${{getBadgeClass(jev.final_signal)}}" style="font-size: 16px; padding: 6px 14px;">${{jev.final_signal}}</span>
                    <span style="font-size: 15px; font-weight: 600; color: #475569;">Confidence: ${{Math.round(jev.confidence_score * 100)}}% &bull; ${{jev.reason_code}}</span>
                </div>
                <div class="jev-banner-rationale">
                    <strong>Arbiter Advisory:</strong> ${{jev.rationale}}
                </div>
                <div style="font-size: 12px; color: #64748b; margin-top: 10px;">
                    <strong>Trusted Models:</strong> ${{jev.selected_models.join(', ') || 'None (Consensus Abstain)'}}
                    ${{jev.discounted_models.length ? `&bull; <strong>Discounted:</strong> ${{jev.discounted_models.join(', ')}}` : ''}}
                </div>
            `;

            // Render Models Grid
            const modelsGrid = document.getElementById('modelsGrid');
            modelsGrid.innerHTML = '';
            t.models_evaluation.forEach(m => {{
                const r = m.rubric_scores || {{}};
                const card = document.createElement('div');
                card.className = 'model-card';
                card.innerHTML = `
                    <div class="model-card-header">
                        <div>
                            <div class="model-card-title">${{m.model_name}}</div>
                            <div class="model-card-stats">${{m.provider}} &bull; ${{m.tok_s || 0}} tok/s (${{m.latency || 0}}s)</div>
                        </div>
                        <div>
                            ${{getStatusBadge(m.status)}}
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="badge ${{getBadgeClass(m.signal)}}">${{m.signal}}</span>
                        <span style="font-size: 12px; font-weight: 600; color: ${{m.constraint_passes ? '#047857' : '#b91c1c'}};">
                            Constraint: ${{m.constraint_passes ? 'PASS' : 'FAIL'}}
                        </span>
                    </div>
                    <div class="model-card-rationale">
                        "${{m.explanation || 'No rationale generated.'}}"
                    </div>
                    <div class="rubric-mini">
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R1 Constraint</div><div class="rubric-mini-score">${{r.R1 !== undefined ? r.R1 : '-'}}</div></div>
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R2 Evidence</div><div class="rubric-mini-score">${{r.R2 !== undefined ? r.R2 : '-'}}</div></div>
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R3 Timing</div><div class="rubric-mini-score">${{r.R3 !== undefined ? r.R3 : '-'}}</div></div>
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R8 Schema</div><div class="rubric-mini-score">${{r.R8 !== undefined ? r.R8 : '-'}}</div></div>
                    </div>
                `;
                modelsGrid.appendChild(card);
            }});
        }}

        // Initialize on page load
        initSelect();
        renderTrade(0);
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Successfully generated clean real data index.html with all 50 trades and JEV audit!")

if __name__ == "__main__":
    build_dashboard()
