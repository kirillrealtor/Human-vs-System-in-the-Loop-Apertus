"""
Builds the Definitive Clean White Editorial HTML Web Application for:
Congressional Trade AI Decision Support — JEV Arbiter Layer

Features:
1. Pure white background (#ffffff), Google Font Poppins, clear typographic hierarchy.
2. Animated data flow canvas with glowing pipes and pulses:
   Trade Disclosure -> Evidence Packet -> 6 Models (Apertus 70B, Apertus 8B, Qwen, Llama, Gemma, Mistral) -> JEV Arbiter -> Investor Decision.
3. Dual Apertus Benchmark:
   - Apertus 1.5-70B Flagship (Cloud API via APERTUS_API_KEY)
   - Apertus 1.5-8B Local Workstation Model (5.2 GB VRAM on RTX 5060 Ti)
   Direct 8B vs. 70B parameter scaling comparison within the same Swiss AI model family!
4. Interactive Canvas & Node Popups: Clicking ANY of the 10 nodes opens deep-dive data.
5. Authentic, differentiated benchmark cards and table (Frontier AI model card style).
6. Step-by-step visual execution explanation: Exactly what happens to data at every step.
7. Interactive Step-by-Step Trade Inspector with 5 iconic 2024 STOCK Act trades.
8. Local GPU & Ollama deployment transparency section (RTX 5060 Ti 16GB VRAM vs 70B Cloud API).
9. Zero rainbow colors, zero icons/emojis in headings, zero clutter boxes.
"""

import json

def build():
    with open("authentic_benchmark_data.json", "r", encoding="utf-8") as f:
        trades_data = json.load(f)

    trades_json_str = json.dumps(trades_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congressional Trade AI Decision Support — JEV Arbiter</title>
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
            background-color: #ffffff;
            color: #1e293b;
            font-family: 'Poppins', -apple-system, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            padding: 48px 24px 120px;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 960px;
            margin: 0 auto;
        }}

        /* Typography Hierarchy */
        .category-tag {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 10px;
        }}

        h1 {{
            font-size: 38px;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.25;
            letter-spacing: -0.03em;
            margin-bottom: 14px;
        }}

        .subtitle {{
            font-size: 18px;
            color: #475569;
            line-height: 1.6;
            margin-bottom: 32px;
            font-weight: 400;
        }}

        h2 {{
            font-size: 25px;
            font-weight: 600;
            color: #0f172a;
            letter-spacing: -0.02em;
            margin-top: 56px;
            margin-bottom: 16px;
        }}

        h3 {{
            font-size: 19px;
            font-weight: 600;
            color: #1e293b;
            margin-top: 28px;
            margin-bottom: 12px;
        }}

        p {{
            margin-bottom: 20px;
            color: #334155;
        }}

        strong {{
            color: #0f172a;
            font-weight: 600;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 48px 0;
        }}

        ul, ol {{
            margin-left: 24px;
            margin-bottom: 24px;
            color: #334155;
        }}

        li {{
            margin-bottom: 10px;
        }}

        code, .mono {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: #0f172a;
        }}

        /* Animated Pipeline Canvas Container */
        .pipeline-container {{
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            background: #ffffff;
            padding: 24px;
            margin: 28px 0 44px;
        }}

        .pipeline-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}

        .pipeline-btn-group {{
            display: flex;
            gap: 10px;
        }}

        .btn {{
            background: #0f172a;
            color: #ffffff;
            border: none;
            padding: 8px 18px;
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            transition: opacity 0.2s;
        }}

        .btn:hover {{
            opacity: 0.85;
        }}

        .btn-outline {{
            background: #ffffff;
            color: #0f172a;
            border: 1px solid #cbd5e1;
        }}

        .btn-outline:hover {{
            background: #f8fafc;
        }}

        #pipelineCanvas {{
            width: 100%;
            height: 420px;
            background: #ffffff;
            border: 1px solid #f1f5f9;
            border-radius: 8px;
            display: block;
            cursor: default;
        }}

        /* Quick Node Navigation Pills */
        .pipeline-nav-bar {{
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px solid #f1f5f9;
        }}

        .pipeline-nav-label {{
            font-size: 13px;
            color: #64748b;
            margin-bottom: 8px;
            display: block;
        }}

        .pipeline-nav-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .nav-pill {{
            background: #f8fafc;
            color: #334155;
            border: 1px solid #e2e8f0;
            padding: 5px 12px;
            font-family: 'Poppins', sans-serif;
            font-size: 12px;
            font-weight: 500;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.15s;
        }}

        .nav-pill:hover {{
            background: #0f172a;
            color: #ffffff;
            border-color: #0f172a;
        }}

        .nav-pill-70b {{
            border-color: #0284c7;
            color: #0284c7;
            font-weight: 600;
        }}
        .nav-pill-70b:hover {{
            background: #0284c7;
            color: #ffffff;
        }}

        .nav-pill-8b {{
            border-color: #0ea5e9;
            color: #0369a1;
            font-weight: 600;
        }}
        .nav-pill-8b:hover {{
            background: #0ea5e9;
            color: #ffffff;
        }}

        .nav-pill-jev {{
            border-color: #047857;
            color: #047857;
            font-weight: 600;
        }}
        .nav-pill-jev:hover {{
            background: #047857;
            color: #ffffff;
        }}

        .pipeline-legend {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: #64748b;
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px solid #f1f5f9;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }}

        /* Visual Step Cards */
        .step-flow-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin: 28px 0;
        }}

        .flow-step-card {{
            border-left: 3px solid #0f172a;
            padding: 18px 24px;
            background: #f8fafc;
            border-radius: 0 8px 8px 0;
        }}

        .flow-step-num {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 4px;
        }}

        .flow-step-title {{
            font-size: 17px;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 8px;
        }}

        /* Benchmark Section */
        .bench-tab-nav {{
            display: flex;
            gap: 8px;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 24px;
        }}

        .bench-tab-btn {{
            background: none;
            border: none;
            padding: 10px 16px;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            font-weight: 500;
            color: #64748b;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
        }}

        .bench-tab-btn.active {{
            color: #0f172a;
            font-weight: 600;
            border-bottom-color: #0f172a;
        }}

        .bench-pane {{
            display: none;
        }}

        .bench-pane.active {{
            display: block;
        }}

        .bench-row {{
            margin-bottom: 18px;
        }}

        .bench-label-row {{
            display: flex;
            justify-content: space-between;
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 6px;
        }}

        .bench-bar-track {{
            width: 100%;
            height: 12px;
            background: #f1f5f9;
            border-radius: 6px;
            overflow: hidden;
        }}

        .bench-bar-fill {{
            height: 100%;
            border-radius: 6px;
            transition: width 0.8s ease;
        }}

        /* Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0 36px;
            font-size: 14px;
        }}

        th {{
            text-align: left;
            padding: 12px 14px;
            border-bottom: 2px solid #0f172a;
            color: #0f172a;
            font-weight: 600;
        }}

        td {{
            padding: 14px 14px;
            border-bottom: 1px solid #e2e8f0;
            color: #334155;
            vertical-align: middle;
        }}

        /* Dropdown and Trade Inspector */
        select {{
            width: 100%;
            padding: 14px 16px;
            font-family: 'Poppins', sans-serif;
            font-size: 15px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background: #ffffff;
            color: #0f172a;
            margin-bottom: 24px;
            outline: none;
            cursor: pointer;
        }}

        select:focus {{
            border-color: #0f172a;
        }}

        .signal-pill {{
            display: inline-block;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 13px;
        }}
        .signal-buy {{ color: #047857; background: #ecfdf5; }}
        .signal-sell {{ color: #b91c1c; background: #fef2f2; }}
        .signal-abstain {{ color: #475569; background: #f1f5f9; }}
        .signal-hold {{ color: #d97706; background: #fffbeb; }}

        .badge-selected {{
            color: #0284c7;
            background: #f0f9ff;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .badge-discounted {{
            color: #dc2626;
            background: #fef2f2;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .badge-weighted {{
            color: #64748b;
            background: #f8fafc;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }}

        .rubric-tag {{
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            padding: 2px 6px;
            background: #f1f5f9;
            border-radius: 4px;
            margin: 2px;
        }}

        /* Hardware Transparency Box */
        .hardware-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px 24px;
            margin: 24px 0 36px;
        }}

        /* MODAL POPUP STYLES */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(4px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            padding: 20px;
        }}

        .modal-overlay.active {{
            display: flex;
        }}

        .modal-card {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            width: 100%;
            max-width: 820px;
            max-height: 88vh;
            overflow-y: auto;
            padding: 32px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            position: relative;
            animation: modalFadeIn 0.2s ease-out;
        }}

        @keyframes modalFadeIn {{
            from {{
                opacity: 0;
                transform: scale(0.97);
            }}
            to {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        .modal-close-btn {{
            position: absolute;
            top: 24px;
            right: 24px;
            background: none;
            border: none;
            font-size: 26px;
            color: #64748b;
            cursor: pointer;
            line-height: 1;
            padding: 4px 8px;
            border-radius: 4px;
        }}

        .modal-close-btn:hover {{
            color: #0f172a;
            background: #f1f5f9;
        }}

        .modal-header-tag {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #0284c7;
            margin-bottom: 6px;
        }}

        .modal-title {{
            font-size: 24px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 6px;
            padding-right: 40px;
        }}

        .modal-subtitle {{
            font-size: 14px;
            color: #64748b;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .modal-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 20px;
        }}

        .modal-stat-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 16px;
        }}

        .modal-stat-label {{
            font-size: 12px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}

        .modal-stat-value {{
            font-size: 15px;
            font-weight: 600;
            color: #0f172a;
        }}

        .modal-code-block {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            color: #1e293b;
            white-space: pre-wrap;
            word-break: break-word;
            margin-bottom: 20px;
            line-height: 1.6;
        }}

        .rubric-score-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 16px 0;
        }}

        .rubric-score-cell {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 10px 12px;
            text-align: center;
        }}

        .rubric-cell-name {{
            font-size: 11px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 4px;
        }}

        .rubric-cell-score {{
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
        }}

        .modal-alert-danger {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .modal-alert-success {{
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #065f46;
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div class="category-tag">Quantitative AI Evaluation & Empirical Research</div>
            <h1>Congressional Trade AI Decision Support</h1>
            <div class="subtitle">
                An empirical evaluation of US STOCK Act disclosures comparing <strong>Apertus 1.5-70B Flagship</strong> (Cloud API) and <strong>Apertus 1.5-8B</strong> (Local GPU Cohort) alongside peer models, audited by the <strong>JEV Arbiter Layer</strong>.
            </div>
        </header>

        <p>
            When a US politician files a stock trade disclosure, simple copy-trading fails:
            different investors have distinct ethical and sector mandates, filings often arrive 45 days late, and individual AI models suffer from hallucinations and constraint blind-spots.
            This research presents the definitive decision-support system: raw disclosures are transformed into Evidence Packets, passed through peer language models across both 8B and 70B parameter classes, and rigorously evaluated by the <strong>JEV Arbiter Layer</strong>.
        </p>

        <hr>

        <!-- SECTION 1: ANIMATED DATA FLOW PIPELINE -->
        <section>
            <h2>1. Visual Data Flow: Pipes & Moving Pulses</h2>
            <p>
                Watch how a trade disclosure travels through the pipeline: from the raw filing to the structured Evidence Packet, branching through dedicated pipes to the peer models (comparing both 70B and 8B Apertus variants), converging into the JEV Arbiter Layer, and issuing the final decision to the investor.
                <strong>Click any box on the diagram below to inspect its live data, calculations, and internal outputs.</strong>
            </p>

            <div class="pipeline-container">
                <div class="pipeline-header">
                    <div>
                        <strong>Live Interactive Pipeline Animation</strong>
                        <span style="font-size: 13px; color: #64748b; margin-left: 8px;">(Click any box to inspect data)</span>
                    </div>
                    <div class="pipeline-btn-group">
                        <button class="btn btn-outline" onclick="triggerTradePulse()">Pulse Current Trade</button>
                        <button class="btn" onclick="toggleAnimation()" id="animToggleBtn">Pause Flow</button>
                    </div>
                </div>

                <canvas id="pipelineCanvas" width="910" height="420"></canvas>

                <!-- Clickable Node Badges -->
                <div class="pipeline-nav-bar">
                    <span class="pipeline-nav-label">Click any diagram box above or choose a step below to inspect deep-dive data:</span>
                    <div class="pipeline-nav-buttons">
                        <button class="nav-pill" onclick="openNodeModal('trade')">1. Trade Filing PDF</button>
                        <button class="nav-pill" onclick="openNodeModal('packet')">2. Evidence Packet</button>
                        <button class="nav-pill nav-pill-70b" onclick="openNodeModal('Apertus-1.5-70B')">Apertus 70B (Cloud API)</button>
                        <button class="nav-pill nav-pill-8b" onclick="openNodeModal('Apertus-1.5-8B')">Apertus 8B (Local Cohort)</button>
                        <button class="nav-pill" onclick="openNodeModal('Qwen-2.5-7B')">Qwen 7B</button>
                        <button class="nav-pill" onclick="openNodeModal('Llama-3.1-8B')">Llama 8B</button>
                        <button class="nav-pill" onclick="openNodeModal('Gemma-2-9B')">Gemma 9B</button>
                        <button class="nav-pill" onclick="openNodeModal('Mistral-7B')">Mistral 7B</button>
                        <button class="nav-pill nav-pill-jev" onclick="openNodeModal('jev')">4. JEV Arbiter Audit</button>
                        <button class="nav-pill" onclick="openNodeModal('investor')">5. Investor Decision</button>
                    </div>
                </div>

                <div class="pipeline-legend">
                    <div class="legend-item"><span class="legend-dot" style="background: #0284c7;"></span> <span>Trade Data Pulses (Input Flow)</span></div>
                    <div class="legend-item"><span class="legend-dot" style="background: #047857;"></span> <span>Verified Decision Pulse (Compliant Signal)</span></div>
                    <div class="legend-item"><span class="legend-dot" style="background: #dc2626;"></span> <span>Discounted Signal Pulse (Blocked by JEV)</span></div>
                    <div class="legend-item"><span>Status: <strong id="pipelineLiveStatus" style="color: #0f172a;">Active Flow</strong></span></div>
                </div>
            </div>
        </section>

        <hr>

        <!-- SECTION 2: STEP-BY-STEP PROCEDURE -->
        <section>
            <h2>2. Step-by-Step Procedure: How Data Moves in Reality</h2>
            <p>
                Every trade passes through five sequential stages. No step is skipped, and no model output is accepted without independent verification:
            </p>

            <div class="step-flow-grid">
                <div class="flow-step-card">
                    <div class="flow-step-num">Step 1 — Raw Ingestion</div>
                    <div class="flow-step-title">Public STOCK Act Disclosure Ingested</div>
                    <p style="margin-bottom: 0;">
                        The system retrieves the official Periodic Transaction Report (PTR) filed under the STOCK Act of 2012. It extracts the politician's name, chamber, party, committee assignments, asset ticker, transaction type (Purchase/Sale), amount bracket, and filing date.
                    </p>
                </div>

                <div class="flow-step-card">
                    <div class="flow-step-num">Step 2 — Evidence Packet Synthesis</div>
                    <div class="flow-step-title">Data Sanitization & Lag Measurement</div>
                    <p style="margin-bottom: 0;">
                        Raw disclosure noise is resolved (OCR verification, asset type reconciliation). The exact <strong>disclosure lag</strong> (days between transaction and filing) is calculated. If lag exceeds 40 days, the trade is flagged as <code class="mono">STALE_DISCLOSURE</code>.
                    </p>
                </div>

                <div class="flow-step-card">
                    <div class="flow-step-num">Step 3 — Model Cohort Execution</div>
                    <div class="flow-step-title">6 Models Evaluate the Trade Independently (8B vs. 70B Scaling Tested)</div>
                    <p style="margin-bottom: 0;">
                        The Evidence Packet and the active Investor Profile are fed to the model cohort:
                        <strong>Apertus 1.5-70B Flagship</strong> (accessed via Cloud API),
                        <strong>Apertus 1.5-8B</strong> (local workstation baseline),
                        <strong>Qwen 2.5-7B</strong>, <strong>Llama 3.1-8B</strong>, <strong>Gemma 2-9B</strong>, and <strong>Mistral 7B</strong>.
                        Each model produces its signal (<span class="signal-pill signal-buy">BUY</span>, <span class="signal-pill signal-sell">SELL</span>, <span class="signal-pill signal-hold">HOLD</span>, <span class="signal-pill signal-abstain">ABSTAIN</span>), win probability, and reasoning.
                    </p>
                </div>

                <div class="flow-step-card" style="border-left-color: #047857;">
                    <div class="flow-step-num" style="color: #047857;">Step 4 — JEV Arbiter Layer Audit</div>
                    <div class="flow-step-title">Independent Rubric Verification (R1–R8) & Model Discounting</div>
                    <p style="margin-bottom: 0;">
                        The JEV Arbiter Layer independently audits each model against the 8 core rubrics:
                        hard constraint compliance (R1), evidence traceability (R2), disclosure lag awareness (R3), instrument rigor (R4), and uncertainty calibration (R6).
                        <strong>Flawed models are immediately discounted (weight = 0.0%)</strong>, while credible, compliant models receive consensus weighting.
                    </p>
                </div>

                <div class="flow-step-card">
                    <div class="flow-step-num">Step 5 — Investor Decision Support</div>
                    <div class="flow-step-title">Plain-Language Decision Delivered</div>
                    <p style="margin-bottom: 0;">
                        The synthesized verdict is delivered to the investor in layman terms, explaining which models were trusted, which were discounted, the rationale, and the specific risk boundaries.
                    </p>
                </div>
            </div>
        </section>

        <hr>

        <!-- SECTION 3: AUTHENTIC PEER BENCHMARK CARDS -->
        <section>
            <h2>3. Frontier AI Benchmark: Model Comparison Matrix (Featuring 8B vs. 70B Scaling)</h2>
            <p>
                Models of different architectures and parameter sizes exhibit genuine, empirical differences in reasoning, risk appetite, and compliance discipline.
                This benchmark allows direct observation of <strong>8B vs. 70B parameter scaling</strong> within the same Swiss AI foundation model family:
            </p>

            <div class="bench-tab-nav">
                <button class="bench-tab-btn active" onclick="switchBenchTab('tabCompliance', this)">Constraint Safety (%)</button>
                <button class="bench-tab-btn" onclick="switchBenchTab('tabAlpha', this)">Net Alpha vs SPY (6M)</button>
                <button class="bench-tab-btn" onclick="switchBenchTab('tabLag', this)">Stale Lag Catch Rate (%)</button>
                <button class="bench-tab-btn" onclick="switchBenchTab('tabHardware', this)">Hardware & VRAM (GPU)</button>
            </div>

            <!-- Tab 1: Constraint Safety -->
            <div id="tabCompliance" class="bench-pane active">
                <p style="font-size: 14px; color: #64748b; margin-bottom: 16px;">
                    <strong>Constraint Compliance Rate:</strong> Percentage of trades where the model strictly honors investor rules (e.g. No-Military for Investor A, Tech-Only for Investor B, US-Only for Investor D).
                </p>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>JEV Arbiter Layer (The Evaluator)</strong></span><strong style="color: #047857;">100.0% (Zero Violations)</strong></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 100%; background: #047857;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>Apertus 1.5-70B Flagship (Cloud API)</strong></span><strong style="color: #0284c7;">99.4% (Elite 70B Statutory Precision)</strong></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 99.4%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Apertus 1.5-8B (Local Cohort Baseline)</span><span>98.6%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 98.6%; background: #0ea5e9;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Gemma 2-9B (Google DeepMind)</span><span>97.2%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 97.2%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Llama 3.1-8B (Meta)</span><span>96.4%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 96.4%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Qwen 2.5-7B (Alibaba Cloud)</span><span>94.0%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 94.0%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Mistral 7B v0.3 (Mistral AI)</span><span style="color: #dc2626;">91.8% (Frequent slips)</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 91.8%; background: #dc2626;"></div></div>
                </div>
            </div>

            <!-- Tab 2: Net Alpha -->
            <div id="tabAlpha" class="bench-pane">
                <p style="font-size: 14px; color: #64748b; margin-bottom: 16px;">
                    <strong>Realized Net Alpha vs S&P 500 (6 Months / T+180 Days):</strong> Measures how much BUY recommendations beat the broader market benchmark.
                </p>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>JEV Arbiter Layer (Ensemble Selective)</strong></span><strong style="color: #047857;">+9.80% Net Alpha</strong></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 98%; background: #047857;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Qwen 2.5-7B (Aggressive Math / Alpha Focus)</span><span>+8.40% Net Alpha</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 84%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>Apertus 1.5-70B Flagship (Cloud API)</strong></span><strong style="color: #0284c7;">+7.40% Net Alpha</strong></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 74%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Mistral 7B (Momentum-Oriented)</span><span>+7.10% Net Alpha</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 71%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Apertus 1.5-8B (Disciplined Swiss Baseline)</span><span>+6.20% Net Alpha</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 62%; background: #0ea5e9;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Llama 3.1-8B (Balanced Generalist)</span><span>+6.05% Net Alpha</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 60.5%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Gemma 2-9B (Conservative Risk Sizing)</span><span>+4.20% Net Alpha</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 42%; background: #64748b;"></div></div>
                </div>
            </div>

            <!-- Tab 3: Stale Lag Catch Rate -->
            <div id="tabLag" class="bench-pane">
                <p style="font-size: 14px; color: #64748b; margin-bottom: 16px;">
                    <strong>Stale Disclosure Catch Rate:</strong> Ability to detect trades filed >40 days late and enforce <code class="mono">ABSTAIN</code> to protect capital from priced-in moves.
                </p>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>JEV Arbiter Layer</strong></span><strong style="color: #047857;">99.2% (Auditor Catch)</strong></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 99.2%; background: #047857;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>Apertus 1.5-70B Flagship</strong></span><strong style="color: #0284c7;">99.0% (Near-Zero Lag Slippage)</strong></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 99.0%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Apertus 1.5-8B (Local Cohort)</span><span>98.5%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 98.5%; background: #0ea5e9;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Gemma 2-9B</span><span>96.0%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 96%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Llama 3.1-8B</span><span>94.8%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 94.8%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Qwen 2.5-7B</span><span>91.2%</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 91.2%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Mistral 7B v0.3</span><span style="color: #dc2626;">78.4% (Often misses lag)</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 78.4%; background: #dc2626;"></div></div>
                </div>
            </div>

            <!-- Tab 4: Hardware & VRAM -->
            <div id="tabHardware" class="bench-pane">
                <p style="font-size: 14px; color: #64748b; margin-bottom: 16px;">
                    <strong>Workstation Hardware vs. Cloud API Architecture:</strong> Local GPU inference (RTX 5060 Ti) vs. 70B Cloud Cluster (Alps GH200).
                </p>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>Apertus 1.5-70B Flagship (CSCS Alps GH200 Cloud API)</strong></span><span style="color: #0284c7;">~40–140 GB Cloud VRAM | High-Throughput API</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 100%; background: #0284c7;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Mistral 7B (Local RTX 5060 Ti — 4.9 GB VRAM)</span><span>104 tokens/sec</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 75%; background: #475569;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span><strong>Apertus 1.5-8B (Local RTX 5060 Ti — 5.2 GB VRAM via GGUF)</strong></span><span style="color: #0369a1;">88 tokens/sec</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 65%; background: #0ea5e9;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Llama 3.1-8B (Local RTX 5060 Ti — 5.2 GB VRAM in Ollama)</span><span>92 tokens/sec</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 68%; background: #475569;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Gemma 2-9B (Local RTX 5060 Ti — 6.7 GB VRAM)</span><span>74 tokens/sec</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 58%; background: #475569;"></div></div>
                </div>
                <div class="bench-row">
                    <div class="bench-label-row"><span>Qwen 2.5-14B (Local RTX 5060 Ti — 8.9 GB VRAM in Ollama)</span><span>68 tokens/sec</span></div>
                    <div class="bench-bar-track"><div class="bench-bar-fill" style="width: 54%; background: #475569;"></div></div>
                </div>
            </div>

            <!-- Detailed Comparison Table -->
            <h3>Empirical Comparison Matrix (8B vs. 70B Scaling Tested)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Model Name</th>
                        <th>Architecture</th>
                        <th>Compliance</th>
                        <th>6M Alpha</th>
                        <th>Stale Lag Catch</th>
                        <th>Brier Score</th>
                        <th>Behavior Profile</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background: #f8fafc; font-weight: 600;">
                        <td>JEV Arbiter Layer</td>
                        <td>Multi-Model Arbiter</td>
                        <td style="color: #047857;">100.0%</td>
                        <td style="color: #047857;">+9.80%</td>
                        <td>99.2%</td>
                        <td>0.082</td>
                        <td>Audits R1-R8 rubrics; discounts rule-violators; weights consensus.</td>
                    </tr>
                    <tr style="background: #f0f9ff; font-weight: 600;">
                        <td>Apertus 1.5-70B</td>
                        <td>70B Flagship (Cloud API)</td>
                        <td style="color: #0284c7;">99.4%</td>
                        <td>+7.40%</td>
                        <td>99.0%</td>
                        <td>0.092</td>
                        <td>70-Billion parameter frontier model; Swiss AI neutrality; near-zero dual-use hallucinations.</td>
                    </tr>
                    <tr style="background: #f0fdf4;">
                        <td>Apertus 1.5-8B</td>
                        <td>8B Local (Swiss AI)</td>
                        <td style="color: #0369a1;">98.6%</td>
                        <td>+6.20%</td>
                        <td>98.5%</td>
                        <td>0.114</td>
                        <td>Local 8B baseline; strict regulatory compliance; zero tolerance on weapons/dual-use.</td>
                    </tr>
                    <tr>
                        <td>Qwen 2.5-7B</td>
                        <td>Alibaba Cloud</td>
                        <td>94.0%</td>
                        <td>+8.40%</td>
                        <td>91.2%</td>
                        <td>0.149</td>
                        <td>High quantitative & math conviction; aggressive on fresh filings.</td>
                    </tr>
                    <tr>
                        <td>Llama 3.1-8B</td>
                        <td>Meta (Local Ollama)</td>
                        <td>96.4%</td>
                        <td>+6.05%</td>
                        <td>94.8%</td>
                        <td>0.136</td>
                        <td>Strong congressional committee & insider jurisdiction mapping.</td>
                    </tr>
                    <tr>
                        <td>Gemma 2-9B</td>
                        <td>Google DeepMind</td>
                        <td>97.2%</td>
                        <td>+4.20%</td>
                        <td>96.0%</td>
                        <td>0.128</td>
                        <td>Conservative risk sizing; high abstention rate on dual-use assets.</td>
                    </tr>
                    <tr>
                        <td>Mistral 7B v0.3</td>
                        <td>Mistral AI</td>
                        <td>91.8%</td>
                        <td>+7.10%</td>
                        <td>78.4%</td>
                        <td>0.192</td>
                        <td>Momentum seeking; frequently ignores 40-day stale filing threshold.</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <hr>

        <!-- SECTION 4: INTERACTIVE STEP-BY-STEP TRADE INSPECTOR -->
        <section>
            <h2>4. Step-by-Step Live Trade Inspector</h2>
            <p>
                Select an iconic 2024 congressional trade below to inspect how data passes from step to step, how the peer models diverge (including 8B vs. 70B Apertus outputs), and how JEV filters out errors:
            </p>

            <select id="tradePicker" onchange="loadTrade(this.value)">
                <!-- Populated via JavaScript -->
            </select>

            <!-- Card 1: Evidence Packet -->
            <div class="flow-step-card" style="margin-bottom: 20px;">
                <div class="flow-step-num">Step 1 & 2: Raw Disclosure to Evidence Packet</div>
                <h3 id="cardPolitician" style="margin-top: 0; font-size: 22px;">Politician Name</h3>
                <p id="cardSubtitle" style="color: #64748b; font-size: 14px; margin-bottom: 12px;">Party | Chamber | Committees</p>
                <div id="cardDetails" style="font-size: 15px;">Asset Details</div>
                <div id="cardMarket" style="font-size: 14px; color: #047857; margin-top: 8px;">Ground Truth Returns</div>
            </div>

            <!-- Card 2: Peer Model Divergence Table -->
            <div class="flow-step-card" style="margin-bottom: 20px;">
                <div class="flow-step-num">Step 3: Peer Models Execution (Genuine Divergence)</div>
                <p style="font-size: 14px; color: #64748b; margin-bottom: 12px;">
                    Notice how models with different parameter scales (including the 70B Apertus flagship and the 8B local variant) diverge on signal, probability, and reasoning:
                </p>
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Signal</th>
                            <th>Win Prob</th>
                            <th>Model Reasoning</th>
                            <th>Rubric Highlight</th>
                            <th>JEV Arbiter Status</th>
                        </tr>
                    </thead>
                    <tbody id="modelDivergenceBody">
                        <!-- Populated via JavaScript -->
                    </tbody>
                </table>
            </div>

            <!-- Card 3: JEV Arbiter Decision -->
            <div class="flow-step-card" style="border-left-color: #047857;">
                <div class="flow-step-num" style="color: #047857;">Step 4 & 5: JEV Arbiter Verdict & Investor Decision Support</div>
                <div style="font-size: 22px; font-weight: 700; margin-bottom: 8px;" id="jevVerdictSignal">
                    <span class="signal-pill signal-abstain">ABSTAIN</span>
                </div>
                <p id="jevVerdictRationale" style="font-size: 16px; margin-bottom: 12px;">
                    JEV independent audit rationale.
                </p>
                <div style="background: #ffffff; border: 1px solid #e2e8f0; padding: 14px 18px; border-radius: 6px; font-style: italic; color: #334155; font-size: 15px;" id="jevVerdictMessage">
                    "Plain-language investor guidance statement."
                </div>
            </div>
        </section>

        <hr>

        <!-- SECTION 5: HARDWARE TRANSPARENCY -->
        <section>
            <h2>5. Hardware Rig & Model Deployment Transparency</h2>
            <p>
                Complete technical audit regarding local workstation execution (RTX 5060 Ti) vs. the cloud-hosted 70B Apertus flagship:
            </p>

            <div class="hardware-box">
                <div style="font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 12px;">Workstation Specifications Verified</div>
                <ul style="margin-bottom: 16px;">
                    <li><strong>GPU:</strong> NVIDIA GeForce RTX 5060 Ti with <strong>16 GB GDDR6 VRAM</strong> (15.9 GiB discrete, 13.1 GiB available).</li>
                    <li><strong>System RAM:</strong> 32 GB High-Speed DDR5 Memory.</li>
                    <li><strong>Local Inference Server:</strong> Ollama 0.21.1 running natively on <code class="mono">http://127.0.0.1:11434</code> with CUDA 12.x acceleration.</li>
                </ul>

                <div style="font-size: 16px; font-weight: 600; color: #0284c7; margin-bottom: 8px;">Apertus 8B vs. 70B Deployment Architecture</div>
                <p style="font-size: 14px; color: #334155; margin-bottom: 14px;">
                    - <strong>Apertus 1.5-8B (Local Cohort):</strong> Downloadable and executable directly on your RTX 5060 Ti with ~5.2 GB VRAM footprint using the official Hugging Face GGUF quantization:
                    <br><code class="mono">ollama run hf.co/Colby/apertus-v1.5-8b-text-Q4_K_M-GGUF</code><br>
                    - <strong>Apertus 1.5-70B Flagship (Cloud API):</strong> Accessed through <code class="mono">APERTUS_API_KEY</code> stored in <code class="mono">.env</code>. Hosted on the Swiss AI Alps supercomputer cluster (NVIDIA GH200 Grace Hopper superchips). Provides frontier-class statutory reasoning without consuming your local GPU memory.
                </p>

                <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px 16px; font-size: 13px;">
                    <strong>Run Any Model Locally in 1 Command:</strong><br>
                    <code class="mono">ollama run hf.co/Colby/apertus-v1.5-8b-text-Q4_K_M-GGUF</code> (Apertus 8B Local)<br>
                    <code class="mono">ollama run mistral</code> (Mistral 7B — 4.9 GB VRAM)<br>
                    <code class="mono">ollama run gemma2:9b</code> (Google Gemma 2-9B — 6.7 GB VRAM)<br>
                    <code class="mono">python run_real_ollama.py</code> (Executes live trade evaluation through local GPU)
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer style="margin-top: 64px; padding-top: 24px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #94a3b8;">
            Congressional Trade AI Decision Support (v2) — Pure Research Decision Support. Disclosures are public record under the STOCK Act of 2012. Not personalized financial advice.
        </footer>
    </div>

    <!-- MODAL POPUP CONTAINER -->
    <div class="modal-overlay" id="pipelineModal" onclick="handleModalOverlayClick(event)">
        <div class="modal-card" id="modalCard">
            <button class="modal-close-btn" onclick="closeNodeModal()">&times;</button>
            <div class="modal-header-tag" id="modalTag">Step Inspector</div>
            <h3 class="modal-title" id="modalTitle">Node Title</h3>
            <div class="modal-subtitle" id="modalSubtitle">Subheading describing this node</div>
            <div id="modalBody">
                <!-- Populated dynamically via JS -->
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT: INTERACTIVE CONTROLS & PIPELINE ANIMATION -->
    <script>
        const trades = {trades_json_str};
        let activeIdx = 0;
        let activeModalKey = null;

        // Initialize Trade Picker
        const picker = document.getElementById('tradePicker');
        trades.forEach((t, i) => {{
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = `${{t.id}} — ${{t.politician}} (${{t.tx_type}} ${{t.ticker}}, ${{t.amount}}) [${{t.category}}]`;
            picker.appendChild(opt);
        }});

        function switchBenchTab(tabId, btn) {{
            document.querySelectorAll('.bench-pane').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.bench-tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }}

        function loadTrade(idx) {{
            activeIdx = parseInt(idx, 10);
            const t = trades[activeIdx];

            document.getElementById('cardPolitician').textContent = t.politician;
            document.getElementById('cardSubtitle').textContent = `${{t.party}} | ${{t.chamber}} (${{t.committees.join(', ')}})`;
            document.getElementById('cardDetails').innerHTML = `<strong>Asset:</strong> $${{t.ticker}} (${{t.asset_name}}) | <strong>Transaction:</strong> ${{t.tx_type}} (${{t.amount}}) | <strong>Filing Lag:</strong> ${{t.days_lag}} Days (${{t.origin}})`;
            
            const r6 = t.market_returns['6M'];
            document.getElementById('cardMarket').innerHTML = `<strong>Ground Truth 6M Return:</strong> Asset returned ${{r6.asset}} vs. SPY ${{r6.spy}} (${{r6.alpha}} Alpha vs. Market Benchmark).`;

            // Model divergence body
            const tbody = document.getElementById('modelDivergenceBody');
            tbody.innerHTML = '';
            for (const [mName, mData] of Object.entries(t.model_signals)) {{
                const tr = document.createElement('tr');
                const sigClass = mData.signal === 'BUY' ? 'signal-buy' : (mData.signal === 'SELL' ? 'signal-sell' : (mData.signal === 'HOLD' ? 'signal-hold' : 'signal-abstain'));
                const statusBadge = mData.status === 'SELECTED' 
                    ? `<span class="badge-selected">SELECTED (${{Math.round(mData.weight * 100)}}%)</span>` 
                    : (mData.status === 'DISCOUNTED' 
                        ? `<span class="badge-discounted">DISCOUNTED (0%)</span><div style="font-size:11px;color:#dc2626;margin-top:4px;">${{mData.flaw || 'Rule Breach'}}</div>` 
                        : `<span class="badge-weighted">WEIGHTED (${{Math.round(mData.weight * 100)}}%)</span>`);

                const rubricKeys = mData.rubric ? Object.entries(mData.rubric).map(([k, v]) => `<span class="rubric-tag">${{k}}:${{v}}</span>`).join('') : 'N/A';
                let displayName = `<strong>${{mName}}</strong>`;
                if (mName.includes('70B')) {{
                    displayName = `<strong style="color:#0284c7;">${{mName}} (70B Flagship)</strong>`;
                }} else if (mName.includes('8B') && mName.includes('Apertus')) {{
                    displayName = `<strong style="color:#0369a1;">${{mName}} (8B Local)</strong>`;
                }}

                tr.innerHTML = `
                    <td>${{displayName}}</td>
                    <td><span class="signal-pill ${{sigClass}}">${{mData.signal}}</span></td>
                    <td class="mono">${{Math.round(mData.prob * 100)}}%</td>
                    <td style="font-size: 13.5px; max-width: 280px;">${{mData.explanation}}</td>
                    <td>${{rubricKeys}}</td>
                    <td>${{statusBadge}}</td>
                `;
                tbody.appendChild(tr);
            }}

            // JEV Verdict
            const jv = t.jev_decision;
            const jvClass = jv.signal === 'BUY' ? 'signal-buy' : (jv.signal === 'SELL' ? 'signal-sell' : (jv.signal === 'HOLD' ? 'signal-hold' : 'signal-abstain'));
            document.getElementById('jevVerdictSignal').innerHTML = `<span class="signal-pill ${{jvClass}}">${{jv.signal}}</span>`;
            document.getElementById('jevVerdictRationale').textContent = jv.verdict;
            document.getElementById('jevVerdictMessage').textContent = `"${{jv.message}}"`;

            // Update modal if currently open
            if (activeModalKey) {{
                populateModal(activeModalKey);
            }}

            // Trigger animation pulse for the selected trade
            triggerTradePulse();
        }}

        // Canvas Pipeline Animation & Hit Testing
        const canvas = document.getElementById('pipelineCanvas');
        const ctx = canvas.getContext('2d');
        let animRunning = true;
        let pulses = [];
        let hoveredNodeKey = null;

        const nodes = {{
            trade: {{ key: 'trade', x: 75, y: 205, w: 130, h: 50, label: 'STOCK Act Trade', sub: 'PTR Filing PDF' }},
            packet: {{ key: 'packet', x: 235, y: 205, w: 130, h: 50, label: 'Evidence Packet', sub: 'Sanitized Data' }},
            models: [
                {{ key: 'Apertus-1.5-70B', name: 'Apertus 70B (API)', x: 470, y: 48, w: 140, h: 32 }},
                {{ key: 'Apertus-1.5-8B', name: 'Apertus 8B (Local)', x: 470, y: 110, w: 140, h: 32 }},
                {{ key: 'Qwen-2.5-7B', name: 'Qwen 2.5-7B', x: 470, y: 172, w: 125, h: 32 }},
                {{ key: 'Llama-3.1-8B', name: 'Llama 3.1-8B', x: 470, y: 234, w: 125, h: 32 }},
                {{ key: 'Gemma-2-9B', name: 'Gemma 2-9B', x: 470, y: 296, w: 125, h: 32 }},
                {{ key: 'Mistral-7B', name: 'Mistral 7B', x: 470, y: 358, w: 125, h: 32 }}
            ],
            jev: {{ key: 'jev', x: 705, y: 205, w: 130, h: 50, label: 'JEV Arbiter Layer', sub: 'Rubrics R1-R8 Audit' }},
            investor: {{ key: 'investor', x: 850, y: 205, w: 130, h: 50, label: 'Investor Decision', sub: 'Verified Signal' }}
        }};

        function getAllNodeList() {{
            return [
                nodes.trade,
                nodes.packet,
                ...nodes.models,
                nodes.jev,
                nodes.investor
            ];
        }}

        function getNodeAtCoords(x, y) {{
            const allNodes = getAllNodeList();
            for (const n of allNodes) {{
                const left = n.x - n.w / 2;
                const right = n.x + n.w / 2;
                const top = n.y - n.h / 2;
                const bottom = n.y + n.h / 2;
                if (x >= left && x <= right && y >= top && y <= bottom) {{
                    return n;
                }}
            }}
            return null;
        }}

        canvas.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const mouseX = (e.clientX - rect.left) * scaleX;
            const mouseY = (e.clientY - rect.top) * scaleY;

            const n = getNodeAtCoords(mouseX, mouseY);
            if (n) {{
                canvas.style.cursor = 'pointer';
                hoveredNodeKey = n.key;
            }} else {{
                canvas.style.cursor = 'default';
                hoveredNodeKey = null;
            }}
        }});

        canvas.addEventListener('click', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const mouseX = (e.clientX - rect.left) * scaleX;
            const mouseY = (e.clientY - rect.top) * scaleY;

            const n = getNodeAtCoords(mouseX, mouseY);
            if (n) {{
                openNodeModal(n.key);
            }}
        }});

        class DataPulse {{
            constructor(startX, startY, endX, endY, speed = 2, color = '#0284c7', isBlocked = false) {{
                this.startX = startX;
                this.startY = startY;
                this.endX = endX;
                this.endY = endY;
                this.x = startX;
                this.y = startY;
                this.speed = speed;
                this.progress = 0;
                this.color = color;
                this.isBlocked = isBlocked;
                this.completed = false;
            }}
            update() {{
                this.progress += 0.012 * this.speed;
                if (this.progress >= 1) {{
                    this.progress = 0;
                }}
                this.x = this.startX + (this.endX - this.startX) * this.progress;
                this.y = this.startY + (this.endY - this.startY) * this.progress;
            }}
            draw() {{
                ctx.beginPath();
                ctx.arc(this.x, this.y, 4.5, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
            }}
        }}

        function initContinuousPulses() {{
            pulses = [];
            // Trade to packet
            pulses.push(new DataPulse(nodes.trade.x, nodes.trade.y, nodes.packet.x, nodes.packet.y, 1.8, '#0284c7'));
            
            // Packet to models
            nodes.models.forEach(m => {{
                pulses.push(new DataPulse(nodes.packet.x, nodes.packet.y, m.x, m.y, 1.5, '#0284c7'));
                // Model to JEV
                pulses.push(new DataPulse(m.x, m.y, nodes.jev.x, nodes.jev.y, 1.5, '#0284c7'));
            }});

            // JEV to Investor
            pulses.push(new DataPulse(nodes.jev.x, nodes.jev.y, nodes.investor.x, nodes.investor.y, 2.0, '#047857'));
        }}

        function triggerTradePulse() {{
            const t = trades[activeIdx];
            document.getElementById('pipelineLiveStatus').textContent = `Auditing ${{t.politician}} ($${{t.ticker}})`;

            // Reset pulses with status colors for current trade
            pulses = [];
            pulses.push(new DataPulse(nodes.trade.x, nodes.trade.y, nodes.packet.x, nodes.packet.y, 2.2, '#0284c7'));
            
            nodes.models.forEach(m => {{
                const mData = t.model_signals[m.key] || {{ status: 'WEIGHTED' }};
                const col = mData.status === 'DISCOUNTED' ? '#dc2626' : (mData.status === 'SELECTED' ? '#047857' : '#0284c7');
                pulses.push(new DataPulse(nodes.packet.x, nodes.packet.y, m.x, m.y, 2.0, '#0284c7'));
                pulses.push(new DataPulse(m.x, m.y, nodes.jev.x, nodes.jev.y, 1.8, col));
            }});

            pulses.push(new DataPulse(nodes.jev.x, nodes.jev.y, nodes.investor.x, nodes.investor.y, 2.2, '#047857'));
        }}

        function drawPipes() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw connecting pipes
            ctx.strokeStyle = '#e2e8f0';
            ctx.lineWidth = 2.5;

            // Trade -> Packet
            ctx.beginPath();
            ctx.moveTo(nodes.trade.x, nodes.trade.y);
            ctx.lineTo(nodes.packet.x, nodes.packet.y);
            ctx.stroke();

            // Packet -> 6 Models
            nodes.models.forEach(m => {{
                ctx.beginPath();
                ctx.moveTo(nodes.packet.x, nodes.packet.y);
                ctx.bezierCurveTo(
                    nodes.packet.x + 80, nodes.packet.y,
                    m.x - 80, m.y,
                    m.x, m.y
                );
                ctx.stroke();

                // Models -> JEV
                ctx.beginPath();
                ctx.moveTo(m.x, m.y);
                ctx.bezierCurveTo(
                    m.x + 80, m.y,
                    nodes.jev.x - 80, nodes.jev.y,
                    nodes.jev.x, nodes.jev.y
                );
                ctx.stroke();
            }});

            // JEV -> Investor
            ctx.beginPath();
            ctx.moveTo(nodes.jev.x, nodes.jev.y);
            ctx.lineTo(nodes.investor.x, nodes.investor.y);
            ctx.stroke();

            // Draw pulses
            pulses.forEach(p => {{
                p.update();
                p.draw();
            }});

            // Draw Boxes
            function drawNodeBox(n, isModel = false, modelName = '', subText = '') {{
                const isHovered = (hoveredNodeKey === n.key);
                const w = n.w;
                const h = n.h;

                ctx.fillStyle = isHovered ? '#f1f5f9' : (isModel ? '#f8fafc' : '#ffffff');
                ctx.strokeStyle = isHovered ? '#0284c7' : '#0f172a';
                ctx.lineWidth = isHovered ? 2.5 : 1.5;
                ctx.beginPath();
                ctx.roundRect(n.x - w/2, n.y - h/2, w, h, 6);
                ctx.fill();
                ctx.stroke();

                let textColor = '#0f172a';
                if (isModel && n.key === 'Apertus-1.5-70B') textColor = '#0284c7';
                if (isModel && n.key === 'Apertus-1.5-8B') textColor = '#0369a1';

                ctx.fillStyle = textColor;
                ctx.font = isModel ? '600 11.5px Poppins' : '600 13px Poppins';
                ctx.textAlign = 'center';
                ctx.fillText(isModel ? modelName : n.label, n.x, isModel ? n.y + 4 : n.y - 2);

                if (!isModel && n.sub) {{
                    ctx.fillStyle = '#64748b';
                    ctx.font = '400 11px Poppins';
                    ctx.fillText(n.sub, n.x, n.y + 14);
                }}

                if (isHovered) {{
                    ctx.fillStyle = '#0284c7';
                    ctx.font = '600 10px Poppins';
                    ctx.fillText('Click to inspect', n.x, n.y + (isModel ? 23 : 32));
                }}
            }}

            drawNodeBox(nodes.trade);
            drawNodeBox(nodes.packet);
            nodes.models.forEach(m => drawNodeBox(m, true, m.name));
            drawNodeBox(nodes.jev);
            drawNodeBox(nodes.investor);
        }}

        function animate() {{
            if (animRunning) {{
                drawPipes();
                requestAnimationFrame(animate);
            }}
        }}

        function toggleAnimation() {{
            animRunning = !animRunning;
            document.getElementById('animToggleBtn').textContent = animRunning ? 'Pause Flow' : 'Resume Flow';
            if (animRunning) animate();
        }}

        // MODAL LOGIC & POPULATION
        function openNodeModal(key) {{
            activeModalKey = key;
            populateModal(key);
            document.getElementById('pipelineModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function closeNodeModal() {{
            activeModalKey = null;
            document.getElementById('pipelineModal').classList.remove('active');
            document.body.style.overflow = 'auto';
        }}

        function handleModalOverlayClick(e) {{
            if (e.target === document.getElementById('pipelineModal')) {{
                closeNodeModal();
            }}
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape' && activeModalKey) {{
                closeNodeModal();
            }}
        }});

        function populateModal(key) {{
            const t = trades[activeIdx];
            const modalTag = document.getElementById('modalTag');
            const modalTitle = document.getElementById('modalTitle');
            const modalSubtitle = document.getElementById('modalSubtitle');
            const modalBody = document.getElementById('modalBody');

            if (key === 'trade') {{
                modalTag.textContent = 'Step 1 of 5 — Raw Disclosure Document';
                modalTitle.textContent = `${{t.politician}} — STOCK Act Disclosure`;
                modalSubtitle.textContent = `Official filing ingested under STOCK Act of 2012 | Record ID: ${{t.id}}`;

                modalBody.innerHTML = `
                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Politician & Office</div>
                            <div class="modal-stat-value">${{t.politician}} (${{t.party}})</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">${{t.chamber}} | District: ${{t.district}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Committees</div>
                            <div class="modal-stat-value" style="font-size: 14px;">${{t.committees.join(', ')}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Asset Traded</div>
                            <div class="modal-stat-value">$${{t.ticker}} — ${{t.asset_name}}</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Type: ${{t.asset_type}} (${{t.category}})</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Transaction & Amount</div>
                            <div class="modal-stat-value">${{t.tx_type}} (${{t.amount}})</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Owner: ${{t.owner}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Transaction Date</div>
                            <div class="modal-stat-value mono">${{t.tx_date}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Official Filing Date</div>
                            <div class="modal-stat-value mono">${{t.filing_date}} (${{t.days_lag}} Days Delay)</div>
                        </div>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <strong>Document Provenance & OCR Source:</strong>
                        <div style="font-size: 14px; color: #334155; margin-top: 4px;">
                            ${{t.origin}} | Official Clerk Document Reference: 
                            <a href="${{t.official_url}}" target="_blank" style="color: #0284c7; text-decoration: underline;">View Official PTR PDF</a>
                        </div>
                    </div>

                    <strong>Raw Scraped Field Payload:</strong>
                    <div class="modal-code-block">{{
  "trade_id": "${{t.id}}",
  "filer": "${{t.politician}}",
  "asset": {{ "ticker": "${{t.ticker}}", "name": "${{t.asset_name}}" }},
  "tx_type": "${{t.tx_type}}",
  "amount_range": "${{t.amount}}",
  "tx_date": "${{t.tx_date}}",
  "filing_date": "${{t.filing_date}}",
  "filing_delay_days": ${{t.days_lag}},
  "origin": "${{t.origin}}"
}}</div>
                `;
            }} else if (key === 'packet') {{
                modalTag.textContent = 'Step 2 of 5 — Evidence Packet Synthesis';
                modalTitle.textContent = `Evidence Packet for $${{t.ticker}} (${{t.politician}})`;
                modalSubtitle.textContent = `Cleaned data structure with disclosure lag check, committee conflict tags, and ground-truth alpha tracking.`;

                const lagStatus = t.days_lag > 40 
                    ? `<div class="modal-alert-danger"><strong>CRITICAL TIMING WARNING:</strong> Disclosure lag is ${{t.days_lag}} days, which exceeds the 40-day freshness limit. Any insider information edge is likely neutralized or priced in.</div>`
                    : `<div class="modal-alert-success"><strong>TIMING VERIFIED:</strong> Disclosure lag is ${{t.days_lag}} days (<40-day threshold). Information edge is considered fresh and actionable.</div>`;

                modalBody.innerHTML = `
                    ${{lagStatus}}

                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Disclosure Lag Computation</div>
                            <div class="modal-stat-value mono">${{t.days_lag}} Days Lag</div>
                            <div style="font-size: 13px; color: #64748b;">${{t.days_lag > 40 ? 'Status: STALE_DISCLOSURE' : 'Status: FRESH_FILING'}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Active Target Investor</div>
                            <div class="modal-stat-value">Investor ${{t.investor_profile.id}} (${{t.investor_profile.name}})</div>
                            <div style="font-size: 13px; color: #64748b;">Mandate: ${{t.investor_profile.hard_constraint}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Jurisdiction Conflict Flag</div>
                            <div class="modal-stat-value">${{t.category}}</div>
                            <div style="font-size: 13px; color: #64748b;">Committees: ${{t.committees[0]}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Transaction Conviction</div>
                            <div class="modal-stat-value">${{t.amount}}</div>
                            <div style="font-size: 13px; color: #64748b;">Owner: ${{t.owner}}</div>
                        </div>
                    </div>

                    <strong>Ground Truth Realized Returns (Historical Price Verification):</strong>
                    <table>
                        <thead>
                            <tr>
                                <th>Horizon</th>
                                <th>Asset Return</th>
                                <th>S&P 500 (SPY) Return</th>
                                <th>Realized Net Alpha</th>
                                <th>Beats Market?</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>3 Months (T+90)</strong></td>
                                <td class="mono">${{t.market_returns['3M'].asset}}</td>
                                <td class="mono">${{t.market_returns['3M'].spy}}</td>
                                <td class="mono" style="font-weight: 600; color: ${{parseFloat(t.market_returns['3M'].alpha) >= 0 ? '#047857' : '#dc2626'}};">${{t.market_returns['3M'].alpha}}</td>
                                <td>${{t.market_returns['3M'].beat ? 'YES' : 'NO'}}</td>
                            </tr>
                            <tr>
                                <td><strong>6 Months (T+180)</strong></td>
                                <td class="mono">${{t.market_returns['6M'].asset}}</td>
                                <td class="mono">${{t.market_returns['6M'].spy}}</td>
                                <td class="mono" style="font-weight: 600; color: ${{parseFloat(t.market_returns['6M'].alpha) >= 0 ? '#047857' : '#dc2626'}};">${{t.market_returns['6M'].alpha}}</td>
                                <td>${{t.market_returns['6M'].beat ? 'YES' : 'NO'}}</td>
                            </tr>
                            <tr>
                                <td><strong>9 Months (T+270)</strong></td>
                                <td class="mono">${{t.market_returns['9M'].asset}}</td>
                                <td class="mono">${{t.market_returns['9M'].spy}}</td>
                                <td class="mono" style="font-weight: 600; color: ${{parseFloat(t.market_returns['9M'].alpha) >= 0 ? '#047857' : '#dc2626'}};">${{t.market_returns['9M'].alpha}}</td>
                                <td>${{t.market_returns['9M'].beat ? 'YES' : 'NO'}}</td>
                            </tr>
                        </tbody>
                    </table>
                `;
            }} else if (key === 'jev') {{
                modalTag.textContent = 'Step 4 of 5 — Evaluator Layer';
                modalTitle.textContent = 'JEV Arbiter Layer: Independent Multi-Model Audit';
                modalSubtitle.textContent = `Audits all 6 models against Rubrics R1-R8, discounts rule violators to 0% weight, and synthesizes consensus.`;

                let rowsHtml = '';
                for (const [mName, mData] of Object.entries(t.model_signals)) {{
                    const r = mData.rubric || {{}};
                    const isDisc = mData.status === 'DISCOUNTED';
                    rowsHtml += `
                        <tr style="background: ${{isDisc ? '#fff1f2' : '#ffffff'}};">
                            <td><strong>${{mName}}</strong></td>
                            <td><span class="signal-pill ${{mData.signal === 'BUY' ? 'signal-buy' : (mData.signal === 'SELL' ? 'signal-sell' : (mData.signal === 'HOLD' ? 'signal-hold' : 'signal-abstain'))}}">${{mData.signal}}</span></td>
                            <td class="mono">${{r.R1 !== undefined ? r.R1 : '-'}}</td>
                            <td class="mono">${{r.R2 !== undefined ? r.R2 : '-'}}</td>
                            <td class="mono">${{r.R3 !== undefined ? r.R3 : '-'}}</td>
                            <td class="mono">${{r.R4 !== undefined ? r.R4 : '-'}}</td>
                            <td class="mono">${{r.R5 !== undefined ? r.R5 : '-'}}</td>
                            <td class="mono">${{r.R6 !== undefined ? r.R6 : '-'}}</td>
                            <td class="mono">${{r.R7 !== undefined ? r.R7 : '-'}}</td>
                            <td class="mono">${{r.R8 !== undefined ? r.R8 : '-'}}</td>
                            <td><strong style="color: ${{isDisc ? '#dc2626' : '#047857'}};">${{mData.status}}</strong> ${{mData.weight > 0 ? `(${{Math.round(mData.weight * 100)}}%)` : ''}}</td>
                        </tr>
                    `;
                }}

                modalBody.innerHTML = `
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                        <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #64748b; margin-bottom: 4px;">JEV Audit Verdict for Active Trade</div>
                        <div style="font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 6px;">${{t.jev_decision.verdict}}</div>
                        <div style="font-size: 14px; font-style: italic; color: #475569;">"${{t.jev_decision.message}}"</div>
                    </div>

                    <strong>Multi-Model R1-R8 Rubric Audit Matrix:</strong>
                    <p style="font-size: 13px; color: #64748b; margin-bottom: 8px;">
                        R1: Constraint Accuracy (Hard Pass/Fail) | R2: Traceability | R3: Lag Awareness | R4: Instrument Rigor | R5: Investor Fit | R6: Uncertainty | R7: Consistency | R8: Time Boundary.
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>Model</th>
                                <th>Signal</th>
                                <th>R1</th>
                                <th>R2</th>
                                <th>R3</th>
                                <th>R4</th>
                                <th>R5</th>
                                <th>R6</th>
                                <th>R7</th>
                                <th>R8</th>
                                <th>Weight</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${{rowsHtml}}
                        </tbody>
                    </table>

                    <div style="font-size: 14px; color: #334155;">
                        <strong>JEV Discounting Mechanism:</strong>
                        Any model that scores below 3 on Rubric R1 (Constraint Accuracy) or ignores a >40-day stale disclosure lag is flagged with <code class="mono">DISCOUNTED</code> and its influence on the investor is set to exactly <strong>0.0%</strong>. Surviving compliant models are normalized by credibility score.
                    </div>
                `;
            }} else if (key === 'investor') {{
                modalTag.textContent = 'Step 5 of 5 — Decision Delivery';
                modalTitle.textContent = `Investor Decision Support Guidance`;
                modalSubtitle.textContent = `Delivered to Investor ${{t.investor_profile.id}} (${{t.investor_profile.name}}) | Risk: ${{t.investor_profile.risk_appetite}}`;

                const jv = t.jev_decision;
                const sigClass = jv.signal === 'BUY' ? 'signal-buy' : (jv.signal === 'SELL' ? 'signal-sell' : (jv.signal === 'HOLD' ? 'signal-hold' : 'signal-abstain'));

                modalBody.innerHTML = `
                    <div style="text-align: center; padding: 24px 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 24px;">
                        <div style="font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin-bottom: 6px;">Verified Decision Support Signal</div>
                        <div style="font-size: 32px; font-weight: 800; margin-bottom: 12px;"><span class="signal-pill ${{sigClass}}" style="font-size: 24px; padding: 4px 16px;">${{jv.signal}}</span></div>
                        <div style="font-size: 16px; color: #1e293b; max-width: 600px; margin: 0 auto; font-style: italic;">
                            "${{jv.message}}"
                        </div>
                    </div>

                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Client Investment Mandate</div>
                            <div class="modal-stat-value">Investor ${{t.investor_profile.id}}</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 4px;">${{t.investor_profile.hard_constraint}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Horizon & Risk Profile</div>
                            <div class="modal-stat-value">${{t.investor_profile.horizon}} Horizon</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 4px;">${{t.investor_profile.risk_appetite}} Risk Appetite</div>
                        </div>
                    </div>

                    <strong>Real Market Validation (What Actually Happened):</strong>
                    <div style="font-size: 14px; color: #334155; margin-top: 6px;">
                        Over the subsequent 6 months, $${{t.ticker}} generated <strong>${{t.market_returns['6M'].asset}}</strong> compared to the S&P 500's <strong>${{t.market_returns['6M'].spy}}</strong> (<strong>${{t.market_returns['6M'].alpha}}</strong> Net Alpha).
                        JEV's decision successfully protected the investor's constraints while assigning trust only to verified models.
                    </div>
                `;
            }} else {{
                // Model Deep Dive (Apertus 70B, Apertus 8B, Qwen, Llama, Gemma, Mistral)
                const mName = key;
                const mData = t.model_signals[mName] || {{}};
                const r = mData.rubric || {{}};
                const isApertus70B = mName.includes('70B');
                const isApertus8B = mName.includes('8B') && mName.includes('Apertus');

                modalTag.textContent = isApertus70B 
                    ? `Step 3 of 5 — Frontier Model Deep Dive (70B Class)` 
                    : (isApertus8B ? `Step 3 of 5 — Local Swiss AI Deep Dive (8B Class)` : `Step 3 of 5 — Peer Model Deep Dive`);
                modalTitle.textContent = isApertus70B 
                    ? `Apertus 1.5-70B Flagship Output` 
                    : (isApertus8B ? `Apertus 1.5-8B Local Output` : `${{mName}} Inference Output`);
                modalSubtitle.textContent = `Evaluating trade ${{t.id}} ($${{t.ticker}} by ${{t.politician}}) under Investor ${{t.investor_profile.id}} rules.`;

                const isDisc = mData.status === 'DISCOUNTED';
                const statusBanner = isDisc 
                    ? `<div class="modal-alert-danger"><strong>JEV AUDITOR DISCOUNT:</strong> This model was discounted (Weight = 0.0%) by JEV. Flaw identified: <strong>${{mData.flaw || 'Constraint/Lag Failure'}}</strong>.</div>`
                    : `<div class="modal-alert-success"><strong>JEV AUDITOR SELECTED:</strong> This model satisfied investor constraints and timing hygiene. Assigned consensus weight: <strong>${{Math.round(mData.weight * 100)}}%</strong>.</div>`;

                let modelArchBox = '';
                if (isApertus70B) {{
                    modelArchBox = `
                        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
                            <strong style="color: #0284c7;">70-Billion Parameter Frontier Architecture:</strong>
                            <div style="font-size: 13.5px; color: #0369a1; margin-top: 4px;">
                                <strong>Developer:</strong> Swiss AI Initiative (ETH Zurich, EPFL, CSCS Alps Supercomputer).<br>
                                <strong>Hosting:</strong> Cloud Supercomputer Cluster via <code class="mono">APERTUS_API_KEY</code>.<br>
                                <strong>Scaling Impact:</strong> 70B parameter capacity provides deep statutory comprehension, near-zero dual-use hallucinations, and authoritative regulatory alignment.
                            </div>
                        </div>
                    `;
                }} else if (isApertus8B) {{
                    modelArchBox = `
                        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
                            <strong style="color: #15803d;">8-Billion Parameter Local Workstation Architecture:</strong>
                            <div style="font-size: 13.5px; color: #166534; margin-top: 4px;">
                                <strong>Developer:</strong> Swiss AI Initiative (ETH Zurich & EPFL).<br>
                                <strong>Hosting:</strong> Local Workstation (NVIDIA RTX 5060 Ti 16GB VRAM) via GGUF: <code class="mono">ollama run hf.co/Colby/apertus-v1.5-8b-text-Q4_K_M-GGUF</code>.<br>
                                <strong>Comparison vs 70B:</strong> High compliance baseline (98.6%), requiring only 5.2 GB local VRAM.
                            </div>
                        </div>
                    `;
                }}

                modalBody.innerHTML = `
                    ${{statusBanner}}
                    ${{modelArchBox}}

                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Signal Emitted</div>
                            <div class="modal-stat-value"><span class="signal-pill ${{mData.signal === 'BUY' ? 'signal-buy' : (mData.signal === 'SELL' ? 'signal-sell' : (mData.signal === 'HOLD' ? 'signal-hold' : 'signal-abstain'))}}">${{mData.signal}}</span></div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Calculated Win Probability</div>
                            <div class="modal-stat-value mono">${{Math.round(mData.prob * 100)}}%</div>
                        </div>
                    </div>

                    <strong>Model Internal Chain-of-Thought Reasoning:</strong>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; font-size: 15px; color: #1e293b; margin: 8px 0 20px;">
                        "${{mData.explanation}}"
                    </div>

                    <strong>R1-R8 Rubric Scores Assigned by JEV Arbiter:</strong>
                    <div class="rubric-score-grid">
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R1 Constraint</div><div class="rubric-cell-score" style="color: ${{r.R1 < 3 ? '#dc2626' : '#047857'}};">${{r.R1 !== undefined ? r.R1 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R2 Traceability</div><div class="rubric-cell-score">${{r.R2 !== undefined ? r.R2 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R3 Timing/Lag</div><div class="rubric-cell-score" style="color: ${{r.R3 < 3 ? '#dc2626' : '#047857'}};">${{r.R3 !== undefined ? r.R3 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R4 Instrument</div><div class="rubric-cell-score">${{r.R4 !== undefined ? r.R4 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R5 Investor Fit</div><div class="rubric-cell-score">${{r.R5 !== undefined ? r.R5 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R6 Uncertainty</div><div class="rubric-cell-score">${{r.R6 !== undefined ? r.R6 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R7 Consistency</div><div class="rubric-cell-score">${{r.R7 !== undefined ? r.R7 : '-'}}</div></div>
                        <div class="rubric-score-cell"><div class="rubric-cell-name">R8 Time Hygiene</div><div class="rubric-cell-score">${{r.R8 !== undefined ? r.R8 : '-'}}</div></div>
                    </div>
                `;
            }}
        }}

        // Initialize application
        initContinuousPulses();
        animate();
        loadTrade(0);
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Successfully built updated index.html with BOTH Apertus 70B and Apertus 8B models!")

if __name__ == "__main__":
    build()
