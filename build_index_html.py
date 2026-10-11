"""
Clean White-Background Editorial HTML Builder for Congressional Trade Decision Support.
Design requirements:
- White background (#ffffff)
- Font: Poppins
- Large, beautiful, readable text with clear hierarchy
- NO boxes, NO icons, NO rainbow colors
- Layman terms step-by-step explanation
- Complete workflow: One-by-one model feeding -> Storing outputs -> JEV Arbiter layer -> Final verdict
"""

import json

def build():
    with open("sample_trades_detailed.json", "r", encoding="utf-8") as f:
        sample_trades = json.load(f)

    sample_trades_json_str = json.dumps(sample_trades)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congressional Trade AI Evaluation — Research Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
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
            font-size: 17px;
            line-height: 1.8;
            padding: 60px 24px 120px;
            -webkit-font-smoothing: antialiased;
        }}

        .article-container {{
            max-width: 860px;
            margin: 0 auto;
        }}

        /* Typography Hierarchy */
        h1 {{
            font-size: 40px;
            font-weight: 700;
            line-height: 1.25;
            color: #0f172a;
            letter-spacing: -0.03em;
            margin-bottom: 16px;
        }}

        .subtitle {{
            font-size: 20px;
            font-weight: 400;
            color: #64748b;
            line-height: 1.5;
            margin-bottom: 32px;
        }}

        h2 {{
            font-size: 26px;
            font-weight: 600;
            line-height: 1.35;
            color: #0f172a;
            letter-spacing: -0.02em;
            margin-top: 56px;
            margin-bottom: 16px;
        }}

        h3 {{
            font-size: 20px;
            font-weight: 600;
            line-height: 1.4;
            color: #1e293b;
            margin-top: 32px;
            margin-bottom: 12px;
        }}

        p {{
            margin-bottom: 22px;
            color: #334155;
            font-weight: 400;
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

        /* Editorial Highlight / Lead Paragraph */
        .lead {{
            font-size: 19px;
            color: #1e293b;
            font-weight: 400;
            line-height: 1.75;
            margin-bottom: 32px;
        }}

        .quote-block {{
            border-left: 3px solid #cbd5e1;
            padding-left: 20px;
            margin: 28px 0;
            color: #475569;
            font-style: italic;
        }}

        /* Clean Minimal Table (No Rainbow, No Boxes) */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 28px 0;
            font-size: 15px;
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
            vertical-align: top;
        }}

        tr:last-child td {{
            border-bottom: 1px solid #cbd5e1;
        }}

        /* Interactive Select (Clean, Minimal) */
        .interactive-section {{
            margin-top: 48px;
            padding-top: 32px;
            border-top: 2px solid #0f172a;
        }}

        .selector-label {{
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            margin-bottom: 10px;
            display: block;
        }}

        select {{
            width: 100%;
            padding: 14px 16px;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            background: #ffffff;
            color: #0f172a;
            margin-bottom: 28px;
            outline: none;
        }}

        select:focus {{
            border-color: #0f172a;
        }}

        .tab-nav {{
            display: flex;
            gap: 20px;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 24px;
        }}

        .tab-link {{
            background: none;
            border: none;
            padding: 10px 0;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            font-weight: 500;
            color: #64748b;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -1px;
        }}

        .tab-link.active {{
            color: #0f172a;
            font-weight: 600;
            border-bottom: 2px solid #0f172a;
        }}

        .signal-pill {{
            font-weight: 700;
            display: inline-block;
            margin-right: 8px;
        }}

        .signal-pill.buy {{ color: #047857; }}
        .signal-pill.sell {{ color: #b91c1c; }}
        .signal-pill.abstain {{ color: #475569; }}
    </style>
</head>
<body>
    <div class="article-container">
        <!-- Header -->
        <header>
            <div style="font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin-bottom: 12px;">
                Quantitative Research & Empirical Auditing
            </div>
            <h1>Congressional Trade AI Evaluation: The Complete Workflow</h1>
            <div class="subtitle">
                How we evaluate STOCK Act disclosures across peer AI models, store individual outputs, and apply the JEV Arbiter layer.
            </div>
        </header>

        <p class="lead">
            Every year, members of the United States Congress buy and sell millions of dollars worth of stock. 
            Because politicians sit on influential committees and oversee national policy, their trades are heavily scrutinized. 
            However, blind copy-trading does not work because different investors have different rules, and AI models frequently hallucinate or recommend trades that were disclosed weeks too late.
        </p>

        <hr>

        <!-- Step 1: The Dataset -->
        <section>
            <h2>1. The Raw Dataset: What Data Are We Using?</h2>
            <p>
                Under the <strong>STOCK Act of 2012</strong>, all US Representatives and Senators are legally required to file public Periodic Transaction Reports (PTRs) within 45 days of making a trade.
            </p>
            <p>
                In our workspace, we are using the complete verified <strong>2024 Congressional Trading Dataset</strong>:
            </p>
            <ul>
                <li><strong>11,147 Total Transactions:</strong> Every single trade disclosed during the 2024 calendar year.</li>
                <li><strong>143 Active Politicians:</strong> Including prominent figures like Nancy Pelosi, Ro Khanna, Michael McCaul, and Tommy Tuberville.</li>
                <li><strong>1,095 Unique Securities:</strong> Covering technology stocks, prime defense contractors, pharmaceuticals, banking, and unlisted municipal bonds.</li>
                <li><strong>Filing Formats:</strong> Both official electronic PTR filings (clean data) and scanned handwritten disclosures parsed through OCR (which can contain optical scanning noise).</li>
            </ul>
        </section>

        <!-- Step 2: The 4 Investor Profiles -->
        <section>
            <h2>2. The 4 Investor Mandates: Why One Signal Does Not Fit All</h2>
            <p>
                An AI cannot simply say "buy this" to every person. A trade that is profitable might be completely illegal or unethical for a specific fund to hold. 
                We evaluate every trade for <strong>four distinct investor profiles</strong>:
            </p>
            <ul>
                <li><strong>Investor A (Ethical / No-Military):</strong> Has a strict mandate to never hold defense or weapons manufacturers (such as Lockheed Martin, General Dynamics, or Raytheon). If a politician buys a defense stock, the signal <strong>must be ABSTAIN</strong>.</li>
                <li><strong>Investor B (Tech-Only):</strong> A dedicated technology fund. Can only hold Information Technology companies (software, chips, hardware). Any non-tech stock (like healthcare or banks) <strong>must be ABSTAIN</strong>.</li>
                <li><strong>Investor C (Open / All Industries):</strong> An unrestricted investor who can buy any sector. Serves as our benchmark for pure trade attractiveness.</li>
                <li><strong>Investor D (US-Market Only):</strong> Mandated to hold only stocks listed on major US national exchanges (NYSE and Nasdaq). Foreign-only listings, private companies, or unlisted municipal bonds fail this constraint.</li>
            </ul>
        </section>

        <!-- Step 3: The Baari-Baari Workflow -->
        <section>
            <h2>3. The Exact Step-by-Step AI Execution Process</h2>
            <p>
                To ensure a scientifically fair evaluation, we test <strong>five peer models of the same parameter scale (~7B to 9B parameters)</strong>:
                Apertus 1.5 (8B), Qwen 2.5 (7B), Llama 3.1 (8B), Gemma 2 (9B), and Mistral (7B).
            </p>
            <p>
                Here is the exact step-by-step process of how the pipeline runs:
            </p>

            <h3>Step 1: Build the Evidence Packet</h3>
            <p>
                Each raw filing is converted into a standardized Evidence Packet containing the politician's name, chamber, committee assignments, asset ticker, transaction type (Purchase vs. Sale), dollar amount bracket, transaction date, filing date, and disclosure lag.
            </p>

            <h3>Step 2: Feed the Evidence Packet to Model 1 (Baari-Baari)</h3>
            <p>
                Model 1 (for example, Apertus 8B) receives the trade packet along with the investor profile. 
                Under strict rules, the model is forbidden from looking at any news or stock price moves that happened <em>after</em> the transaction date (zero lookahead). 
                The model checks the hard constraint. If the trade passes, it evaluates the trade's conviction and timing.
            </p>

            <h3>Step 3: Save Model 1's Output to Disk</h3>
            <p>
                The model generates a structured JSON output (Signal: BUY, HOLD, SELL, or ABSTAIN, along with its reasoning and probability). 
                This output is immediately saved into a permanent file on disk (<code>evaluation_sessions/[trade_id]/model1.json</code>).
            </p>

            <h3>Step 4: Repeat for Model 2, Model 3, Model 4, and Model 5</h3>
            <p>
                The exact same Evidence Packet is fed one by one to Qwen, Llama, Gemma, and Mistral. 
                Each model's response is independently captured and saved. There is zero cross-talk between models.
            </p>

            <h3>Step 5: Apply the JEV Arbiter Layer</h3>
            <p>
                Once all five models have recorded their signals, the <strong>JEV Arbiter Layer</strong> executes. 
                JEV does not rely on simple majority vote. Instead, JEV audits each model against an 8-point rubric:
            </p>
            <ul>
                <li><strong>Constraint Accuracy (R1):</strong> Did the model correctly respect the investor's restriction? If a model recommended buying a defense stock for Investor A, JEV discounts that model and sets its weight to zero.</li>
                <li><strong>Timing Awareness (R3):</strong> Was the disclosure filed more than 40 days late? If so, JEV enforces ABSTAIN because the informational advantage has already evaporated.</li>
                <li><strong>Time-Boundary Hygiene (R8):</strong> Did the model cheat by mentioning future earnings or events that had not yet occurred on the trade date?</li>
            </ul>
            <p>
                JEV weights the credible, disciplined models, discounts rule-breakers, and delivers the final verdict and a plain-language summary message for the investor.
            </p>
        </section>

        <hr>

        <!-- Step 4: Interactive Live Trade Inspection -->
        <section class="interactive-section">
            <h2>4. Inspect Real Congressional Trades</h2>
            <p>
                Use the selector below to view how real 2024 congressional trades are evaluated across the 5 peer models and how JEV makes the final call for each investor mandate.
            </p>

            <span class="selector-label">Select a Real Congressional Trade:</span>
            <select id="tradeSelect" onchange="renderTrade(this.value)">
                <!-- Populated via JavaScript -->
            </select>

            <!-- Trade Overview -->
            <div style="margin-bottom: 24px;">
                <h3 id="viewPolitician" style="font-size: 24px; color: #0f172a; margin-bottom: 4px;">Nancy Pelosi</h3>
                <p id="viewSub" style="color: #64748b; font-size: 15px; margin-bottom: 12px;">Democrat, House (Speaker Emerita)</p>
                <p id="viewDetails" style="font-size: 16px; margin-bottom: 8px;">
                    <strong>Security:</strong> $NVDA (NVIDIA Corporation) | <strong>Transaction:</strong> Sale (Partial), $1M - $5M | <strong>Filing Lag:</strong> 17 Days
                </p>
                <p id="viewMarket" style="font-size: 15px; color: #475569;">
                    <strong>Ground Truth Performance vs. S&P 500 (SPY):</strong> Asset +17.67% vs. SPY +6.05% at 6 months (+11.62% Alpha).
                </p>
            </div>

            <!-- Investor Profile Selector -->
            <div class="tab-nav">
                <button class="tab-link active" onclick="setInvestor('A')">Investor A: No-Military</button>
                <button class="tab-link" onclick="setInvestor('B')">Investor B: Tech-Only</button>
                <button class="tab-link" onclick="setInvestor('C')">Investor C: Open All</button>
                <button class="tab-link" onclick="setInvestor('D')">Investor D: US-Market</button>
            </div>

            <!-- JEV Verdict Block -->
            <div style="margin-bottom: 32px;">
                <div style="font-size: 13px; font-weight: 600; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">
                    JEV Final Call for <span id="viewInvName">Ethical No-Military</span>:
                </div>
                <div style="font-size: 22px; font-weight: 700; margin: 8px 0;" id="viewSignalBlock">
                    <span class="signal-pill sell">SELL</span>
                </div>
                <p id="viewRationale" style="font-size: 16px; color: #1e293b;">
                    Constraint verified. Trusted models signal asset distribution.
                </p>
                <div class="quote-block" id="viewMessage">
                    "JEV Recommendation for Ethical No-Military: SELL. Disclosures can be delayed or incomplete, losses are possible, this is not financial advice."
                </div>
            </div>

            <!-- Peer Models Table -->
            <h3>Peer Models Audit Table</h3>
            <p style="font-size: 14px; color: #64748b; margin-bottom: 12px;">
                Shows how each individual peer model evaluated the trade and whether JEV selected or discounted them:
            </p>
            <table>
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Model Signal</th>
                        <th>Constraint Check</th>
                        <th>JEV Status</th>
                        <th>Assigned Weight</th>
                        <th>Rubric Score</th>
                    </tr>
                </thead>
                <tbody id="modelsTableBody">
                    <!-- Populated via JavaScript -->
                </tbody>
            </table>
        </section>

        <hr>

        <!-- Hardware & Local Execution -->
        <section>
            <h2>5. Hardware and Local Execution: What Can Your Computer Run?</h2>
            <p>
                A very common question is whether you can run all these models on your personal machine:
            </p>
            <ul>
                <li><strong>Your System Specs:</strong> NVIDIA GeForce RTX 5060 Ti with <strong>16 GB of VRAM</strong> and <strong>32 GB of System RAM</strong>.</li>
                <li><strong>Can it run 7B to 9B models? YES!</strong> A 7B or 8B model takes roughly 5.5 GB to 6.5 GB of VRAM. It fits completely inside your 16 GB GPU with room to spare, running at ~90 tokens per second.</li>
                <li><strong>Can it run all models simultaneously at the exact same second? No.</strong> If you tried to load five 8B models into memory at the exact same moment, they would require over 30 GB of VRAM.</li>
                <li><strong>The Solution: The Sequential Runner.</strong> Our pipeline loads Model 1, evaluates the trade, saves the JSON to disk, unloads Model 1 from VRAM, and then loads Model 2. This runs completely comfortably on your RTX 5060 Ti without running out of memory!</li>
            </ul>
        </section>

        <footer style="margin-top: 64px; padding-top: 24px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #94a3b8;">
            Congressional Trade Evaluation (v2) — Pure Research Decision Support. Disclosures are public record under the STOCK Act of 2012. Not personalized financial advice.
        </footer>
    </div>

    <!-- JavaScript for Live Interactive Switching -->
    <script>
        const trades = {sample_trades_json_str};
        let activeTradeIdx = 0;
        let activeInvestorId = 'A';

        const tradeSelect = document.getElementById('tradeSelect');
        trades.forEach((item, idx) => {{
            const p = item.packet;
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = `${{p.trade_id}} — ${{p.politician.name}} (${{p.trade.transaction_type}} ${{p.asset.ticker || 'Unlisted'}}, ${{p.trade.amount_range}})`;
            tradeSelect.appendChild(opt);
        }});

        function renderTrade(idx) {{
            activeTradeIdx = idx;
            const item = trades[activeTradeIdx];
            const p = item.packet;
            const gt = item.ground_truth;

            document.getElementById('viewPolitician').textContent = p.politician.name;
            document.getElementById('viewSub').textContent = `${{p.politician.party || 'Independent'}}, ${{p.politician.chamber || 'Congress'}} (${{p.politician.committees.join(', ') || 'General Committee'}});`;
            
            const tickerStr = p.asset.ticker ? `$${{p.asset.ticker}} (${{p.asset.asset_name}})` : (p.asset.asset_name || 'Unlisted Asset');
            document.getElementById('viewDetails').innerHTML = `<strong>Security:</strong> ${{tickerStr}} | <strong>Transaction:</strong> ${{p.trade.transaction_type}} (${{p.trade.amount_range}}) | <strong>Filing Lag:</strong> ${{p.timing.days_to_disclosure}} Days`;

            if (gt && gt.resolved) {{
                const a6 = gt['6M'].alpha_pct;
                const beatStr = gt['6M'].beat_spy ? 'Outperformed S&P 500' : 'Underperformed S&P 500';
                document.getElementById('viewMarket').innerHTML = `<strong>Ground Truth Market Performance:</strong> Asset returned ${{gt['6M'].asset_return_pct}}% vs. SPY ${{gt['6M'].spy_return_pct}}% at 6 months (${{a6 > 0 ? '+' : ''}}${{a6}}% Net Alpha — ${{beatStr}}).`;
            }} else {{
                document.getElementById('viewMarket').innerHTML = `<strong>Ground Truth Market Performance:</strong> Unlisted asset or fixed income (over-the-counter).`;
            }}

            renderInvestor();
        }}

        function setInvestor(invId) {{
            activeInvestorId = invId;
            document.querySelectorAll('.tab-link').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            renderInvestor();
        }}

        function renderInvestor() {{
            const item = trades[activeTradeIdx];
            const invData = item.investors[activeInvestorId];
            if (!invData) return;

            const rep = invData.jev_report;
            const prof = invData.profile;
            const fc = rep.final_call;

            document.getElementById('viewInvName').textContent = `${{prof.investor_name}} (Investor ${{activeInvestorId}})`;

            const pillClass = fc.signal === 'BUY' ? 'buy' : (fc.signal === 'SELL' ? 'sell' : 'abstain');
            document.getElementById('viewSignalBlock').innerHTML = `<span class="signal-pill ${{pillClass}}">${{fc.signal}}</span>`;
            document.getElementById('viewRationale').textContent = fc.final_rationale;
            document.getElementById('viewMessage').textContent = `"${{rep.investor_message}}"`;

            // Models Table
            const tbody = document.getElementById('modelsTableBody');
            tbody.innerHTML = '';
            rep.model_evaluations.forEach(me => {{
                const tr = document.createElement('tr');
                const sigClass = me.model_signal === 'BUY' ? 'buy' : (me.model_signal === 'SELL' ? 'sell' : 'abstain');
                const totalR = Object.values(me.rubric_scores).reduce((a, b) => a + b, 0);
                const cPassStr = rep.jev_constraint_check.passes === true ? 'Passes' : (rep.jev_constraint_check.passes === false ? 'Fails Constraint' : 'Unknown');

                tr.innerHTML = `
                    <td><strong>${{me.model_id}}</strong></td>
                    <td><span class="signal-pill ${{sigClass}}">${{me.model_signal}}</span></td>
                    <td>${{cPassStr}}</td>
                    <td><strong>${{me.status}}</strong></td>
                    <td>${{(me.weight_assigned * 100).toFixed(1)}}%</td>
                    <td>${{totalR}} / 40</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Initial render
        renderTrade(0);
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Successfully built clean white-background index.html with Poppins typography!")

if __name__ == "__main__":
    build()
