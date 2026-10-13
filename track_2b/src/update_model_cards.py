# update_model_cards.py
import re

with open("build_hackathon_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
old_css_start = "        /* Model Weaknesses / Where They Lack Grid */"
old_css_end = """        .lacking-rescue strong {{
            color: #047857;
        }}"""

new_css = """        /* Model Weaknesses / Empirical Model Autopsy Grid */
        .lacking-section {{
            margin-top: 48px;
            margin-bottom: 48px;
        }}

        /* Quick Comparison Table */
        .summary-comparison-box {{
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 22px 24px;
            margin-top: 20px;
            margin-bottom: 28px;
            box-shadow: var(--shadow-sm);
        }}

        .summary-comparison-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .summary-comparison-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: #0F172A;
            margin: 0;
            letter-spacing: -0.01em;
        }}

        .summary-comparison-desc {{
            font-size: 0.875rem;
            color: #64748B;
            margin-top: 3px;
        }}

        .summary-comparison-tag {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #475569;
            background: #F1F5F9;
            border: 1px solid #CBD5E1;
            padding: 5px 12px;
            border-radius: 6px;
            white-space: nowrap;
        }}

        .summary-comp-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
            text-align: left;
        }}

        .summary-comp-table th {{
            background: #0F172A;
            color: #F8FAFC;
            padding: 11px 14px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            white-space: nowrap;
        }}

        .summary-comp-table td {{
            padding: 12px 14px;
            border-bottom: 1px solid #E2E8F0;
            color: #1E293B;
            vertical-align: middle;
        }}

        .summary-comp-table tr:nth-child(even) td {{
            background: #F8FAFC;
        }}

        .summary-comp-table tr:hover td {{
            background: #F1F5F9;
        }}

        /* 6 Model Grid & Cards */
        .model-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 24px;
            margin-top: 24px;
            margin-bottom: 44px;
        }}

        .model-card {{
            display: flex;
            flex-direction: column;
            padding: 28px;
            background: #ffffff;
            border: 1px solid #E2E8F0;
            border-top: 4px solid var(--model-color, #94A3B8);
            border-radius: 16px;
            box-shadow: var(--shadow-sm);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            position: relative;
        }}

        .model-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
        }}

        .model-card.card-70b {{ border-top-color: #1E3A8A; }}
        .model-card.card-8b {{ border-top-color: #2563EB; }}
        .model-card.card-qwen {{ border-top-color: #D97706; }}
        .model-card.card-sec {{ border-top-color: #DB2777; }}
        .model-card.card-neo {{ border-top-color: #7C3AED; }}
        .model-card.card-rabbit {{ border-top-color: #0D9488; }}

        .model-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 6px;
        }}

        .model-card h3 {{
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.3;
            margin: 0;
            color: #0F172A;
            letter-spacing: -0.01em;
        }}

        .model-card .tagline {{
            font-size: 0.875rem;
            color: #475569;
            margin: 4px 0 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .hw-chip {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 2px 8px;
            background: #F1F5F9;
            color: #475569;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            white-space: nowrap;
        }}

        .persona-tag {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: #334155;
        }}

        .verdict-line {{
            font-size: 0.9375rem;
            font-weight: 500;
            color: #1E293B;
            background: #F8FAFC;
            border-left: 3px solid #CBD5E1;
            padding: 9px 12px;
            border-radius: 4px;
            margin-bottom: 16px;
            line-height: 1.5;
        }}

        .stat-strip {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            padding: 14px 12px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            margin-bottom: 6px;
        }}

        .stat-strip-item {{
            display: flex;
            flex-direction: column;
        }}

        .stat-strip dt {{
            font-size: 0.75rem;
            letter-spacing: .05em;
            text-transform: uppercase;
            color: #64748B;
            white-space: nowrap;
            font-weight: 600;
            margin: 0;
        }}

        .stat-strip dd {{
            font-size: 1.125rem;
            font-weight: 700;
            font-variant-numeric: tabular-nums;
            font-family: 'JetBrains Mono', monospace;
            margin: 4px 0 0;
            line-height: 1.2;
        }}

        .compliance-progress-track {{
            width: 100%;
            height: 4px;
            background: #E2E8F0;
            border-radius: 2px;
            margin-top: 6px;
            overflow: hidden;
        }}

        .compliance-progress-fill {{
            height: 100%;
            border-radius: 2px;
        }}

        .more-stats {{
            font-size: 0.75rem;
            color: #64748B;
            font-family: 'JetBrains Mono', monospace;
            padding: 2px 4px;
            margin-bottom: 16px;
            line-height: 1.4;
        }}

        .model-strength {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
            background: #F0FDF4;
            border: 1px solid #BBF7D0;
            border-radius: 8px;
            padding: 9px 12px;
            font-size: 0.84375rem;
            color: #065F46;
            line-height: 1.45;
            margin-bottom: 16px;
        }}

        .strength-icon {{
            font-weight: 800;
            color: #047857;
            font-size: 0.9375rem;
            line-height: 1;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        .failure-heading {{
            font-size: 0.8125rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #475569;
            margin-bottom: 10px;
        }}

        .fail-list {{
            list-style: none;
            padding: 0;
            margin: 0 0 10px 0;
        }}

        .fail-list li {{
            position: relative;
            padding-left: 18px;
            margin-bottom: 10px;
            font-size: 0.9375rem;
            line-height: 1.55;
            color: #334155;
        }}

        .fail-list li::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0.6em;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #DC2626;
        }}

        .fail-list strong {{
            color: #0F172A;
        }}

        .more-failures {{
            margin-bottom: 18px;
        }}

        .more-failures summary {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: #2563EB;
            cursor: pointer;
            padding: 4px 0;
            outline: none;
            user-select: none;
        }}

        .more-failures summary:hover {{
            color: #1D4ED8;
            text-decoration: underline;
        }}

        .more-failures .fail-list {{
            margin-top: 10px;
            margin-bottom: 0;
        }}

        .jev-fix {{
            margin-top: auto;
            padding: 14px 16px;
            background: #ECFDF5;
            border-left: 3px solid #047857;
            border-radius: 8px;
            font-size: 0.875rem;
            line-height: 1.5;
            color: #065F46;
        }}

        .jev-fix-title {{
            font-weight: 700;
            color: #064E3B;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
            font-size: 0.875rem;
        }}

        .violation-badge {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }}

        .badge-amber {{
            background: #FFFBEB;
            color: #B45309;
            border: 1px solid #FDE68A;
        }}

        .badge-red {{
            background: #FEF2F2;
            color: #B91C1C;
            border: 1px solid #FECACA;
        }}"""

if old_css_start in content and old_css_end in content:
    idx1 = content.find(old_css_start)
    idx2 = content.find(old_css_end) + len(old_css_end)
    content = content[:idx1] + new_css + content[idx2:]
    print("CSS replaced successfully!")
else:
    print("ERROR: CSS markers not found!")

# 2. Update HTML
old_html_start = '            <!-- SECTION: MODEL-BY-MODEL WEAKNESSES & LACKING ANALYSIS -->'
old_html_end = '            </div>\n\n            <!-- Empirical Graphs Grid -->'

new_html = '''            <!-- SECTION: MODEL-BY-MODEL WEAKNESSES & EMPIRICAL AUTOPSY -->
            <h2>Empirical Model Autopsy: Where Each Individual Model Lacks</h2>
            <p>
                In quantitative finance and legislative insider trading, a single blindspot causes catastrophic capital loss or fiduciary non-compliance. Below is the standardized empirical autopsy of where each of the 6 evaluated models failed during the 300 benchmark runs across 50 authentic PolyTICK.us trades.
            </p>

            <!-- 6. Quick Comparison Table Above the Cards -->
            <div class="summary-comparison-box">
                <div class="summary-comparison-header">
                    <div>
                        <h3 class="summary-comparison-title">Quick Model Benchmark Summary</h3>
                        <div class="summary-comparison-desc">Scan key performance and safety metrics across all 6 evaluated models before inspecting individual failure mode cards below.</div>
                    </div>
                    <div class="summary-comparison-tag">
                        50 Trades &bull; 300 Benchmark Runs
                    </div>
                </div>
                <div class="table-wrap" style="margin-bottom: 0;">
                    <table class="summary-comp-table">
                        <thead>
                            <tr>
                                <th>Model Identifier</th>
                                <th>Role Tag</th>
                                <th>Deployment Hardware</th>
                                <th style="min-width: 140px;">Compliance</th>
                                <th>6M Net Alpha</th>
                                <th>Violations</th>
                                <th>Abstention</th>
                                <th>Primary Risk Factor</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong style="color: #1E3A8A;">Apertus 70B</strong></td>
                                <td><span class="persona-tag">&#9878; Flagship Jurist</span></td>
                                <td><span class="hw-chip">CSCS ALPS &bull; Cloud</span></td>
                                <td>
                                    <div style="font-weight: 700; color: #166534; font-family: 'JetBrains Mono', monospace;">86.0%</div>
                                    <div class="compliance-progress-track">
                                        <div class="compliance-progress-fill" style="width: 86.0%; background: #059669;"></div>
                                    </div>
                                </td>
                                <td><strong style="color: #166534; font-family: 'JetBrains Mono', monospace;">+4.89%</strong></td>
                                <td><span class="violation-badge badge-amber">11 Breaches</span></td>
                                <td style="font-family: 'JetBrains Mono', monospace;">18.0%</td>
                                <td style="color: #475569;">Dual-use defense conglomerate blindspots ($BA)</td>
                            </tr>
                            <tr>
                                <td><strong style="color: #2563EB;">Apertus 8B</strong></td>
                                <td><span class="persona-tag">&#128737; Over-Cautious</span></td>
                                <td><span class="hw-chip">CSCS ALPS / Local</span></td>
                                <td>
                                    <div style="font-weight: 700; color: #DC2626; font-family: 'JetBrains Mono', monospace;">26.0%</div>
                                    <div class="compliance-progress-track">
                                        <div class="compliance-progress-fill" style="width: 26.0%; background: #DC2626;"></div>
                                    </div>
                                </td>
                                <td><strong style="color: #475569; font-family: 'JetBrains Mono', monospace;">0.00%</strong></td>
                                <td><span class="violation-badge badge-amber">0 Breaches</span></td>
                                <td><strong style="color: #DC2626; font-family: 'JetBrains Mono', monospace;">94.0%</strong></td>
                                <td style="color: #475569;">Severe decision paralysis (freezes on 47/50 trades)</td>
                            </tr>
                            <tr>
                                <td><strong style="color: #B45309;">Qwen 14B</strong></td>
                                <td><span class="persona-tag">&#128187; Code Specialist</span></td>
                                <td><span class="hw-chip">RTX 5060 Ti &bull; Local</span></td>
                                <td>
                                    <div style="font-weight: 700; color: #B45309; font-family: 'JetBrains Mono', monospace;">80.0%</div>
                                    <div class="compliance-progress-track">
                                        <div class="compliance-progress-fill" style="width: 80.0%; background: #D97706;"></div>
                                    </div>
                                </td>
                                <td><strong style="color: #DC2626; font-family: 'JetBrains Mono', monospace;">-2.10%</strong></td>
                                <td><span class="violation-badge badge-red">22 Breaches</span></td>
                                <td style="font-family: 'JetBrains Mono', monospace;">18.0%</td>
                                <td style="color: #475569;">Misses corporate holding structures ($KMX auto finance)</td>
                            </tr>
                            <tr>
                                <td><strong style="color: #BE185D;">SecurityAI 14B</strong></td>
                                <td><span class="persona-tag">&#128680; Threat Overfitter</span></td>
                                <td><span class="hw-chip">RTX 5060 Ti &bull; Local</span></td>
                                <td>
                                    <div style="font-weight: 700; color: #B45309; font-family: 'JetBrains Mono', monospace;">79.5%</div>
                                    <div class="compliance-progress-track">
                                        <div class="compliance-progress-fill" style="width: 79.5%; background: #D97706;"></div>
                                    </div>
                                </td>
                                <td><strong style="color: #DC2626; font-family: 'JetBrains Mono', monospace;">-3.68%</strong></td>
                                <td><span class="violation-badge badge-red">23 Breaches</span></td>
                                <td style="font-family: 'JetBrains Mono', monospace;">16.0%</td>
                                <td style="color: #475569;">Overfits on regulatory noise; panic-sells tech winners</td>
                            </tr>
                            <tr>
                                <td><strong style="color: #6D28D9;">Neo 8B</strong></td>
                                <td><span class="persona-tag">&#9889; Reckless Trader</span></td>
                                <td><span class="hw-chip">RTX 5060 Ti &bull; Local</span></td>
                                <td>
                                    <div style="font-weight: 700; color: #DC2626; font-family: 'JetBrains Mono', monospace;">56.5%</div>
                                    <div class="compliance-progress-track">
                                        <div class="compliance-progress-fill" style="width: 56.5%; background: #DC2626;"></div>
                                    </div>
                                </td>
                                <td><strong style="color: #DC2626; font-family: 'JetBrains Mono', monospace;">-3.86%</strong></td>
                                <td><span class="violation-badge badge-red">28 Breaches</span></td>
                                <td style="font-family: 'JetBrains Mono', monospace;">22.0%</td>
                                <td style="color: #475569;">Completely ignores negative screens ($GD, $HII defense)</td>
                            </tr>
                            <tr>
                                <td><strong style="color: #0F766E;">WhiteRabbitNeo 8B</strong></td>
                                <td><span class="persona-tag">&#128007; Pen Tester</span></td>
                                <td><span class="hw-chip">RTX 5060 Ti &bull; Local</span></td>
                                <td>
                                    <div style="font-weight: 700; color: #DC2626; font-family: 'JetBrains Mono', monospace;">49.5%</div>
                                    <div class="compliance-progress-track">
                                        <div class="compliance-progress-fill" style="width: 49.5%; background: #DC2626;"></div>
                                    </div>
                                </td>
                                <td><strong style="color: #DC2626; font-family: 'JetBrains Mono', monospace;">-4.35%</strong></td>
                                <td><span class="violation-badge badge-red">31 Breaches</span></td>
                                <td style="font-family: 'JetBrains Mono', monospace;">24.0%</td>
                                <td style="color: #475569;">Schema crashes; extreme certainty on wrong predictions</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Standardized 6 Model Grid -->
            <div class="model-grid">
                <!-- 1. Apertus 70B -->
                <div class="model-card card-70b">
                    <div class="model-card-header">
                        <div>
                            <h3>Apertus 70B</h3>
                            <div class="tagline">
                                <span class="persona-tag">&#9878; The Flagship Jurist</span>
                                <span class="hw-chip">CSCS ALPS &bull; Cloud API</span>
                            </div>
                        </div>
                        <span class="violation-badge badge-amber">11 Violations</span>
                    </div>

                    <div class="verdict-line">
                        Smartest standalone model, but still broke client mandate 11 times.
                    </div>

                    <div class="stat-strip">
                        <div class="stat-strip-item">
                            <dt>Compliance</dt>
                            <dd style="color: #166534;">86.0%</dd>
                            <div class="compliance-progress-track">
                                <div class="compliance-progress-fill" style="width: 86.0%; background: #059669;"></div>
                            </div>
                        </div>
                        <div class="stat-strip-item">
                            <dt>6M Net Alpha</dt>
                            <dd style="color: #166534;">+4.89%</dd>
                        </div>
                        <div class="stat-strip-item">
                            <dt>Abstention</dt>
                            <dd style="color: #1E293B;">18.0%</dd>
                        </div>
                    </div>

                    <div class="more-stats">
                        Latency: 10.27s &bull; Win Rate: 58.8% &bull; Params: 70B (FP16)
                    </div>

                    <div class="model-strength">
                        <span class="strength-icon">&#10003;</span>
                        <span><strong>Key Strength:</strong> Deepest statutory comprehension of congressional conflicts and committee jurisdictions.</span>
                    </div>

                    <div class="failure-heading">Failure Modes</div>
                    <ul class="fail-list">
                        <li><strong>Supercomputer Resource Barrier:</strong> Requires ~140 GB VRAM in FP16; cannot run on edge or local workstation GPUs.</li>
                        <li><strong>Conglomerate Blindspots:</strong> Failed to catch defense exposure in complex multi-sector entities (permitted Boeing $BA dual-use entries).</li>
                    </ul>

                    <details class="more-failures">
                        <summary>Show all failure modes (2 more)</summary>
                        <ul class="fail-list">
                            <li><strong>API Latency Penalty (10.27s):</strong> Sluggish roundtrip API lag makes it unsuited for real-time disclosure feeds where execution speed dictates entry.</li>
                            <li><strong>Fiduciary Risk Without Audit:</strong> Even with 86% compliance, 11 violations prove that a 70B model cannot be deployed in financial fiduciary settings without an independent juried layer.</li>
                        </ul>
                    </details>

                    <div class="jev-fix">
                        <div class="jev-fix-title">&#128737; How JEV fixes it</div>
                        JEV isolates Apertus 70B's statutory depth while vetoing conglomerate breaches before orders execute.
                    </div>
                </div>

                <!-- 2. Apertus 8B -->
                <div class="model-card card-8b">
                    <div class="model-card-header">
                        <div>
                            <h3>Apertus 8B</h3>
                            <div class="tagline">
                                <span class="persona-tag">&#128737; The Over-Cautious One</span>
                                <span class="hw-chip">CSCS ALPS &bull; Workstation</span>
                            </div>
                        </div>
                        <span class="violation-badge badge-amber">0 Violations</span>
                    </div>

                    <div class="verdict-line">
                        Hypersensitive to constraint prompts, freezing on 94% of evaluated trades.
                    </div>

                    <div class="stat-strip">
                        <div class="stat-strip-item">
                            <dt>Compliance</dt>
                            <dd style="color: #DC2626;">26.0%</dd>
                            <div class="compliance-progress-track">
                                <div class="compliance-progress-fill" style="width: 26.0%; background: #DC2626;"></div>
                            </div>
                        </div>
                        <div class="stat-strip-item">
                            <dt>6M Net Alpha</dt>
                            <dd style="color: #475569;">0.00%</dd>
                        </div>
                        <div class="stat-strip-item">
                            <dt>Abstention</dt>
                            <dd style="color: #DC2626;">94.0%</dd>
                        </div>
                    </div>

                    <div class="more-stats">
                        Latency: 2.60s &bull; Speed: 134.6 tok/s &bull; Active Win Rate: 0.0%
                    </div>

                    <div class="model-strength">
                        <span class="strength-icon">&#10003;</span>
                        <span><strong>Key Strength:</strong> Ultra-fast generation (135 tok/s) and zero hallucinated mandate breaches.</span>
                    </div>

                    <div class="failure-heading">Failure Modes</div>
                    <ul class="fail-list">
                        <li><strong>Severe Decision Paralysis:</strong> Paralyzed by multi-layered investor constraints, defaulting to ABSTAIN on 47 out of 50 trades.</li>
                        <li><strong>Total Alpha Destruction:</strong> Misses all high-conviction insider market outperformance (e.g. Nancy Pelosi's $NVDA call option conversions).</li>
                    </ul>

                    <details class="more-failures">
                        <summary>Show all failure modes (1 more)</summary>
                        <ul class="fail-list">
                            <li><strong>Statutory Capacity Bottleneck:</strong> 8 billion parameters are insufficient to simultaneously juggle disclosure delays, committee jurisdictions, and position sizing without freezing.</li>
                        </ul>
                    </details>

                    <div class="jev-fix">
                        <div class="jev-fix-title">&#128737; How JEV fixes it</div>
                        JEV discounts Apertus 8B's active signal weight, utilizing it strictly as an ultra-fast negative exclusion filter.
                    </div>
                </div>

                <!-- 3. Qwen 14B -->
                <div class="model-card card-qwen">
                    <div class="model-card-header">
                        <div>
                            <h3>Qwen 14B</h3>
                            <div class="tagline">
                                <span class="persona-tag">&#128187; The Code Specialist</span>
                                <span class="hw-chip">RTX 5060 Ti &bull; Local</span>
                            </div>
                        </div>
                        <span class="violation-badge badge-red">22 Violations</span>
                    </div>

                    <div class="verdict-line">
                        Flawless JSON structure, but treats corporate finance like programming variables.
                    </div>

                    <div class="stat-strip">
                        <div class="stat-strip-item">
                            <dt>Compliance</dt>
                            <dd style="color: #B45309;">80.0%</dd>
                            <div class="compliance-progress-track">
                                <div class="compliance-progress-fill" style="width: 80.0%; background: #D97706;"></div>
                            </div>
                        </div>
                        <div class="stat-strip-item">
                            <dt>6M Net Alpha</dt>
                            <dd style="color: #DC2626;">-2.10%</dd>
                        </div>
                        <div class="stat-strip-item">
                            <dt>Abstention</dt>
                            <dd style="color: #1E293B;">18.0%</dd>
                        </div>
                    </div>

                    <div class="more-stats">
                        Latency: 13.31s &bull; Win Rate: 44.1% &bull; Schema Pass: 5/5
                    </div>

                    <div class="model-strength">
                        <span class="strength-icon">&#10003;</span>
                        <span><strong>Key Strength:</strong> Flawless syntactic JSON schema adherence (5/5) with zero formatting crashes across 300 evaluations.</span>
                    </div>

                    <div class="failure-heading">Failure Modes</div>
                    <ul class="fail-list">
                        <li><strong>Parent-Subsidiary Blindspot:</strong> Struggles with corporate holding structures (e.g. missed CarMax $KMX finance arms, causing 22 violations).</li>
                        <li><strong>Momentum Lag Drag:</strong> Chases past price action instead of legislative information edge, consistently buying at local cycle peaks.</li>
                    </ul>

                    <details class="more-failures">
                        <summary>Show all failure modes (2 more)</summary>
                        <ul class="fail-list">
                            <li><strong>Syntactic Coding Bias:</strong> Evaluates disclosure filings as logical software structures rather than dynamic macroeconomic events.</li>
                            <li><strong>Hardware Bottleneck:</strong> 13.31s latency on RTX 5060 Ti GPU, consuming maximum VRAM bandwidth for sub-market returns.</li>
                        </ul>
                    </details>

                    <div class="jev-fix">
                        <div class="jev-fix-title">&#128737; How JEV fixes it</div>
                        JEV audits Qwen against Rubrics R1 and R5, neutralizing its 22 violations to 0% signal weight.
                    </div>
                </div>

                <!-- 4. SecurityAI 14B -->
                <div class="model-card card-sec">
                    <div class="model-card-header">
                        <div>
                            <h3>SecurityAI 14B</h3>
                            <div class="tagline">
                                <span class="persona-tag">&#128680; The Threat Overfitter</span>
                                <span class="hw-chip">RTX 5060 Ti &bull; Local</span>
                            </div>
                        </div>
                        <span class="violation-badge badge-red">23 Violations</span>
                    </div>

                    <div class="verdict-line">
                        Overfits on regulatory threat keywords, panic-selling premier market winners.
                    </div>

                    <div class="stat-strip">
                        <div class="stat-strip-item">
                            <dt>Compliance</dt>
                            <dd style="color: #B45309;">79.5%</dd>
                            <div class="compliance-progress-track">
                                <div class="compliance-progress-fill" style="width: 79.5%; background: #D97706;"></div>
                            </div>
                        </div>
                        <div class="stat-strip-item">
                            <dt>6M Net Alpha</dt>
                            <dd style="color: #DC2626;">-3.68%</dd>
                        </div>
                        <div class="stat-strip-item">
                            <dt>Abstention</dt>
                            <dd style="color: #1E293B;">16.0%</dd>
                        </div>
                    </div>

                    <div class="more-stats">
                        Latency: 8.65s &bull; Win Rate: 45.2% &bull; Filing Decay: Unpenalized
                    </div>

                    <div class="model-strength">
                        <span class="strength-icon">&#10003;</span>
                        <span><strong>Key Strength:</strong> Exceptional threat detection on SEC inquiries and formal regulatory proceedings.</span>
                    </div>

                    <div class="failure-heading">Failure Modes</div>
                    <ul class="fail-list">
                        <li><strong>Domain Risk Overfitting:</strong> Over-indexes on security risk keywords, triggering false panic SELL signals on tech winners ($AAPL, $NVDA).</li>
                        <li><strong>Disclosure Decay Blindness:</strong> Fails to penalize stale filings (>40-day delay), entering trades after institutional alpha has decayed.</li>
                    </ul>

                    <details class="more-failures">
                        <summary>Show all failure modes (1 more)</summary>
                        <ul class="fail-list">
                            <li><strong>Mandate Boundary Confusion:</strong> In Investor B (Tech-only), accepted non-tech firms with vague "cyber exposure", generating 23 breaches.</li>
                        </ul>
                    </details>

                    <div class="jev-fix">
                        <div class="jev-fix-title">&#128737; How JEV fixes it</div>
                        JEV enforces strict 40-day disclosure decay rules (R3) and removes model weight when regulatory threats are hallucinated.
                    </div>
                </div>

                <!-- 5. Neo 8B -->
                <div class="model-card card-neo">
                    <div class="model-card-header">
                        <div>
                            <h3>Neo 8B</h3>
                            <div class="tagline">
                                <span class="persona-tag">&#9889; The Reckless Trader</span>
                                <span class="hw-chip">RTX 5060 Ti &bull; Local</span>
                            </div>
                        </div>
                        <span class="violation-badge badge-red">28 Violations</span>
                    </div>

                    <div class="verdict-line">
                        Overconfident buy signals that completely ignore client negative screens.
                    </div>

                    <div class="stat-strip">
                        <div class="stat-strip-item">
                            <dt>Compliance</dt>
                            <dd style="color: #DC2626;">56.5%</dd>
                            <div class="compliance-progress-track">
                                <div class="compliance-progress-fill" style="width: 56.5%; background: #DC2626;"></div>
                            </div>
                        </div>
                        <div class="stat-strip-item">
                            <dt>6M Net Alpha</dt>
                            <dd style="color: #DC2626;">-3.86%</dd>
                        </div>
                        <div class="stat-strip-item">
                            <dt>Abstention</dt>
                            <dd style="color: #1E293B;">22.0%</dd>
                        </div>
                    </div>

                    <div class="more-stats">
                        Latency: 34.20s &bull; Speed: 75.5 tok/s &bull; Win Rate: 38.6%
                    </div>

                    <div class="model-strength">
                        <span class="strength-icon">&#10003;</span>
                        <span><strong>Key Strength:</strong> Fast local token throughput (75.5 tok/s) and zero hesitation on market momentum.</span>
                    </div>

                    <div class="failure-heading">Failure Modes</div>
                    <ul class="fail-list">
                        <li><strong>Highest Raw Violations:</strong> Completely missed defense exclusions, routing illegal contractor trades ($GD, $HII) to Investor A.</li>
                        <li><strong>Reckless Hyper-Active Buying:</strong> Stripped of safety guardrails, it exhibits reckless overconfidence across high-risk disclosures.</li>
                    </ul>

                    <details class="more-failures">
                        <summary>Show all failure modes (1 more)</summary>
                        <ul class="fail-list">
                            <li><strong>Zero Timing Hygiene:</strong> Bought into 40+ day decayed insider filings, eroding investor capital by -3.86% vs the S&amp;P 500.</li>
                        </ul>
                    </details>

                    <div class="jev-fix">
                        <div class="jev-fix-title">&#128737; How JEV fixes it</div>
                        JEV slashes Neo's credibility weight to 0.0% on 28 trades due to hard negative screen violations.
                    </div>
                </div>

                <!-- 6. WhiteRabbitNeo 8B -->
                <div class="model-card card-rabbit">
                    <div class="model-card-header">
                        <div>
                            <h3>WhiteRabbitNeo 8B</h3>
                            <div class="tagline">
                                <span class="persona-tag">&#128007; The Penetration Tester</span>
                                <span class="hw-chip">RTX 5060 Ti &bull; Local</span>
                            </div>
                        </div>
                        <span class="violation-badge badge-red">31 Violations</span>
                    </div>

                    <div class="verdict-line">
                        Severe schema parse crashes and miscalibration; lowest score across all models.
                    </div>

                    <div class="stat-strip">
                        <div class="stat-strip-item">
                            <dt>Compliance</dt>
                            <dd style="color: #DC2626;">49.5%</dd>
                            <div class="compliance-progress-track">
                                <div class="compliance-progress-fill" style="width: 49.5%; background: #DC2626;"></div>
                            </div>
                        </div>
                        <div class="stat-strip-item">
                            <dt>6M Net Alpha</dt>
                            <dd style="color: #DC2626;">-4.35%</dd>
                        </div>
                        <div class="stat-strip-item">
                            <dt>Abstention</dt>
                            <dd style="color: #1E293B;">24.0%</dd>
                        </div>
                    </div>

                    <div class="more-stats">
                        Latency: 12.87s &bull; Brier Score: 0.2750 &bull; Speed: 75.3 tok/s
                    </div>

                    <div class="model-strength">
                        <span class="strength-icon">&#10003;</span>
                        <span><strong>Key Strength:</strong> Specialized domain insight into offensive cybersecurity and exploit vulnerability vectors.</span>
                    </div>

                    <div class="failure-heading">Failure Modes</div>
                    <ul class="fail-list">
                        <li><strong>JSON Schema Crashes:</strong> Frequently breaks output schema with conversational markdown, crashing automated trading APIs.</li>
                        <li><strong>Severe Miscalibration (0.275 Brier):</strong> Extreme certainty on wrong forecasts, yielding the worst 6-month alpha (-4.35% vs SPY).</li>
                    </ul>

                    <details class="more-failures">
                        <summary>Show all failure modes (1 more)</summary>
                        <ul class="fail-list">
                            <li><strong>Offensive Penetration Distortions:</strong> Inappropriately forces exploit and attack surface narratives onto routine financial filings.</li>
                        </ul>
                    </details>

                    <div class="jev-fix">
                        <div class="jev-fix-title">&#128737; How JEV fixes it</div>
                        JEV schema validation catches formatting failures instantly, discarding unparsable signals to 0% weight.
                    </div>
                </div>
            </div>'''

if old_html_start in content and old_html_end in content:
    idx1 = content.find(old_html_start)
    idx2 = content.find(old_html_end) + len(old_html_end)
    # Note: old_html_end includes "</div>\n\n            <!-- Empirical Graphs Grid -->"
    # We want to keep "<!-- Empirical Graphs Grid -->"
    content = content[:idx1] + new_html + "\n\n            <!-- Empirical Graphs Grid -->" + content[idx2:]
    print("HTML replaced successfully!")
else:
    print("ERROR: HTML markers not found!")

with open("build_hackathon_dashboard.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated build_hackathon_dashboard.py successfully.")
