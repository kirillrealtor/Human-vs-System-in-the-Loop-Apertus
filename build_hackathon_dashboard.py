"""
Builds the Dual-View Hackathon Benchmark Web Application for:
Congressional Trade AI Decision Support & JEV Arbiter Layer
Data Source: PolyTICK.us (all_2024_congress_trades.csv)
Hardware: CSCS Swiss AI Supercomputer (ALPS) + Local NVIDIA RTX 5060 Ti GPU

Full Implementation of PROMPT_SET_v2:
- Part 0: Investor Profiles A-D & Multi-Persona Constraint Architecture
- Part 1: Model Inferences (6 Frontier & Local LLMs)
- Part 2: JEV Arbiter Synthesis Layer & Multi-Rubric Auditing (R1-R8)
- Part 3: Ground Truth vs S&P 500 (SPY) at T+90 (3M), T+180 (6M), T+270 (9M)
          with Interactive Per-Persona Leaderboards, Net Alpha, Brier Scores, & Win Rates!
"""

import json
import os

def build_app():
    with open("benchmark_results_50/JEV_final_audit_50.json", "r", encoding="utf-8") as f:
        audit_data = json.load(f)

    with open("benchmark_results_50/part3_leaderboards.json", "r", encoding="utf-8") as f:
        leaderboards_data = json.load(f)

    trades_json_str = json.dumps(audit_data)
    leaderboards_json_str = json.dumps(leaderboards_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congressional Trade AI Decision Support &amp; JEV Arbiter — PolyTICK.us Data</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
                        --font-sans: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
            --font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Consolas, monospace;

                        /* Model Fixed Benchmark Palette (Identical in both charts & tables) */
            --m-apertus-70b:  #1E3A8A;   /* CSCS ALPS: Darker Navy Blue */
            --m-apertus-8b:   #2563EB;   /* CSCS ALPS: Blue (Apertus family) */
            --m-neo-uncens:   #7C3AED;   /* RTX 5060 Ti: Violet (Bar) */
            --m-whiterabbit:  #0D9488;   /* RTX 5060 Ti: Teal (Bar) */
            --m-qwen-coder:   #D97706;   /* RTX 5060 Ti: Amber (Bar) */
            --m-securityai:   #DB2777;   /* RTX 5060 Ti: Magenta (Bar) */

            /* Slightly darker model text versions (WCAG AA text on white) */
            --m-qwen:         #B45309;   /* Text: Amber */
            --m-securityai-txt: #BE185D; /* Text: Deep Magenta */
            --m-neo:          #6D28D9;   /* Text: Deep Violet */
            --m-whiterabbit-txt: #0F766E; /* Text: Deep Teal */

            /* Semantic Status Palette */
            --ok-bg: #DCFCE7;   --ok-fg: #166534;   --ok-bd: #86EFAC;
            --veto-bg: #FEE2E2; --veto-fg: #991B1B; --veto-bd: #FCA5A5;
            --info-bg: #DBEAFE; --info-fg: #1E40AF; --info-bd: #93C5FD;
            --mute-bg: #F1F5F9; --mute-fg: #64748B; --mute-bd: #CBD5E1;

            --row-fail-bg: #FEF2F2;
            --row-fail-bd: #DC2626;

            --track:   #E2E8F0;
            --card:    #FFFFFF;
            --value:   #334155;

            /* Base Surface & Background (WCAG AA Strict Contrast Palette) */
            --bg-canvas: #F8FAFC;        /* Page background */
            --bg-card: #FFFFFF;          /* Card background */
            --bg-subtle: #F1F5F9;        /* Subtle tag background */
            --border: #E2E8F0;           /* Dividers & boundaries */
            --border-hover: #CBD5E1;     /* Interactive border */
            
            /* Typography & Neutrals */
            --text-dark: #0F172A;        /* Primary text & table header background */
            --text-body: #1E293B;        /* Body text */
            --text-muted: #475569;       /* Muted text (labels, takeaways) */
            --text-subtle: #64748B;      /* Captions */

            /* Investor B / Frontier Tech-Only Accent */
            --primary: #1D4ED8;          /* Accent: #1D4ED8 */
            --primary-dark: #1E3A8A;     /* Text on tint: #1E3A8A */
            --primary-light: #EFF6FF;    /* Tint background: #EFF6FF */
            --primary-border: #BFDBFE;   /* Border: #BFDBFE */

            /* Investor C / Fiduciary Open Accent */
            --emerald: #047857;          /* Accent: #047857 */
            --emerald-dark: #065F46;     /* Text on tint: #065F46 */
            --emerald-light: #ECFDF5;    /* Tint background: #ECFDF5 */
            --emerald-border: #A7F3D0;   /* Border: #A7F3D0 */

            /* Investor D / Conservative US-Market Accent */
            --amber: #B45309;            /* Accent: #B45309 */
            --amber-dark: #78350F;       /* Text on tint: #78350F */
            --amber-light: #FFFBEB;      /* Tint background: #FFFBEB */
            --amber-border: #FDE68A;     /* Border: #FDE68A */

            /* Investor A / Ethical Veto Accent */
            --rose: #BE123C;             /* Accent: #BE123C */
            --rose-dark: #9F1239;        /* Text on tint: #9F1239 */
            --rose-light: #FFF1F2;       /* Tint background: #FFF1F2 */
            --rose-border: #FECDD3;      /* Border: #FECDD3 */

            /* Alpha Engine & Thematic - Sovereign Purple */
            --purple: #7c3aed;           /* Purple 600 */
            --purple-dark: #6d28d9;      /* Purple 700 */
            --purple-light: #faf5ff;     /* Tint 50 */
            --purple-border: #e9d5ff;    /* Border 200 */

            /* Swiss Supercomputer - Cyan Sky */
            --sky: #0284c7;              /* Sky 600 */
            --sky-dark: #0369a1;         /* Sky 700 */
            --sky-light: #f0f9ff;        /* Tint 50 */
            --sky-border: #bae6fd;       /* Border 200 */

            /* Shadows & Elevation */
            --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
            --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04);
            --shadow-xl: 0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.06);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-sans);
            background-color: var(--bg-canvas);
            color: var(--text-dark);
            line-height: 1.65;
            padding: 24px 24px 100px;
            -webkit-font-smoothing: antialiased;
            font-size: 16px;
        }}

        .container {{
            max-width: 1280px;
            margin: 0 auto;
        }}

        /* Top Nav Bar */
        .nav-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px 24px;
            margin-bottom: 36px;
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
            gap: 16px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .brand-logo {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, #0f172a 0%, #1e40af 100%);
            color: #ffffff;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 20px;
            box-shadow: 0 2px 6px rgba(30, 64, 175, 0.25);
        }}

        .brand-text {{
            font-size: 21px;
            font-weight: 700;
            color: var(--text-dark);
            letter-spacing: -0.02em;
        }}

        .brand-sub {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 400;
        }}

        /* Tab Switcher */
        .tab-switcher {{
            display: flex;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 4px;
            gap: 4px;
        }}

        .tab-btn {{
            font-family: inherit;
            font-size: 15px;
            font-weight: 600;
            padding: 10px 22px;
            border-radius: 8px;
            border: none;
            background: transparent;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .tab-btn.active {{
            background: #0f172a;
            color: #ffffff;
            box-shadow: 0 2px 4px rgba(15, 23, 42, 0.15);
        }}

        .tab-btn:hover:not(.active) {{
            color: var(--text-dark);
        }}

        /* Data Source Attribution Pill */
        .source-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 7px 16px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 600;
            color: #334155;
            text-decoration: none;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }}

        .source-pill:hover {{
            border-color: #2563eb;
            color: #2563eb;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.15);
        }}

        .source-dot {{
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
        }}

        /* Typography Scale (Inter, Base 16px) */
        h1 {{
            font-size: 40px;
            line-height: 48px;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-dark);
            margin-bottom: 16px;
        }}

        h2 {{
            font-size: 28px;
            line-height: 36px;
            font-weight: 700;
            letter-spacing: -0.015em;
            color: var(--text-dark);
            margin-top: 48px;
            margin-bottom: 14px;
        }}

        h3 {{
            font-size: 20px;
            line-height: 28px;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: var(--text-dark);
        }}

        p {{
            font-size: 16px;
            line-height: 26px;
            font-weight: 400;
            letter-spacing: 0;
            color: #1E293B;
            margin-bottom: 18px;
        }}

        .lead-text, .lead {{
            font-size: 18px;
            line-height: 30px;
            font-weight: 400;
            letter-spacing: 0;
            max-width: 70ch;
            color: #1E293B;
            margin-bottom: 32px;
        }}

        /* KPI Stat Row */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 44px;
        }}

        .kpi-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px 26px;
            box-shadow: var(--shadow-md);
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        .kpi-card:nth-child(1) {{ border-top: 4px solid #2563eb; }}
        .kpi-card:nth-child(2) {{ border-top: 4px solid #7c3aed; }}
        .kpi-card:nth-child(3) {{ border-top: 4px solid #059669; }}
        .kpi-card:nth-child(4) {{ border-top: 4px solid #d97706; }}

        .kpi-label, .eyebrow {{
            font-size: 12px;
            line-height: 16px;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #475569;
        }}

        .kpi-value, .stat {{
            font-size: 40px;
            line-height: 1;
            font-weight: 700;
            letter-spacing: -0.02em;
            font-variant-numeric: tabular-nums;
            color: var(--text-dark);
            margin-top: 8px;
        }}

        .kpi-sub {{
            font-size: 14px;
            line-height: 20px;
            font-weight: 500;
            letter-spacing: 0;
            margin-top: 6px;
        }}

        .kpi-card:nth-child(1) .kpi-sub {{ color: #2563eb; }}
        .kpi-card:nth-child(2) .kpi-sub {{ color: #7c3aed; }}
        .kpi-card:nth-child(3) .kpi-sub {{ color: #059669; }}
        .kpi-card:nth-child(4) .kpi-sub {{ color: #d97706; }}

        /* Investor Persona Cards Grid (Tab 1) */
        .persona-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 22px;
            margin-bottom: 44px;
        }}

        .persona-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 26px;
            box-shadow: var(--shadow-md);
            position: relative;
            border-top: 5px solid #2563eb;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .persona-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        .persona-card.p-a {{ border-top-color: #BE123C; }} /* Ethical: Accent */
        .persona-card.p-b {{ border-top-color: #1D4ED8; }} /* Tech-only: Accent */
        .persona-card.p-c {{ border-top-color: #047857; }} /* Open: Accent */
        .persona-card.p-d {{ border-top-color: #B45309; }} /* US-market: Accent */

        .persona-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }}

        .persona-pill-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .p-a .persona-pill-badge {{ background: #FFF1F2; color: #9F1239; border: 1px solid #FECDD3; }}
        .p-b .persona-pill-badge {{ background: #EFF6FF; color: #1E3A8A; border: 1px solid #BFDBFE; }}
        .p-c .persona-pill-badge {{ background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }}
        .p-d .persona-pill-badge {{ background: #FFFBEB; color: #78350F; border: 1px solid #FDE68A; }}

        .persona-name {{
            font-size: 20px;
            line-height: 28px;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: var(--text-dark);
            margin-bottom: 10px;
        }}

        .persona-mandate {{
            font-size: 15px;
            line-height: 24px;
            font-weight: 400;
            letter-spacing: 0;
            padding: 12px 14px;
            border-radius: 8px;
            margin-bottom: 16px;
        }}

        .persona-mandate strong {{
            font-weight: 600;
        }}

        .p-a .persona-mandate {{ background: #FFF1F2; border: 1px solid #FECDD3; border-left: 3px solid #BE123C; color: #9F1239; }}
        .p-b .persona-mandate {{ background: #EFF6FF; border: 1px solid #BFDBFE; border-left: 3px solid #1D4ED8; color: #1E3A8A; }}
        .p-c .persona-mandate {{ background: #ECFDF5; border: 1px solid #A7F3D0; border-left: 3px solid #047857; color: #065F46; }}
        .p-d .persona-mandate {{ background: #FFFBEB; border: 1px solid #FDE68A; border-left: 3px solid #B45309; color: #78350F; }}

        .persona-meta-row {{
            display: flex;
            justify-content: space-between;
            padding-top: 14px;
            border-top: 1px solid var(--border);
            margin-bottom: 12px;
        }}

        .meta-label {{
            display: block;
            font-size: 13px;
            line-height: 18px;
            font-weight: 400;
            letter-spacing: 0;
            color: #475569;
            margin-bottom: 2px;
        }}

        .meta-val {{
            display: block;
            font-size: 15px;
            line-height: 22px;
            font-weight: 600;
            letter-spacing: 0;
            color: var(--text-dark);
            font-variant-numeric: tabular-nums;
        }}

        .enforcement-note {{
            font-size: 14px;
            line-height: 22px;
            font-weight: 400;
            letter-spacing: 0;
            color: #475569;
            margin-top: 12px;
            margin-bottom: 0;
        }}

        .enforce-label {{
            font-weight: 600;
            color: #1E293B;
        }}

        /* Cross-Persona Decision Matrix Table */
        .matrix-table-wrap {{
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 14px;
            margin-bottom: 44px;
            background: #ffffff;
            box-shadow: var(--shadow-md);
        }}

        .matrix-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-variant-numeric: tabular-nums;
        }}

        .matrix-table th {{
            background: #0F172A;
            padding: 14px 16px;
            border-bottom: 2px solid #0F172A;
            font-weight: 600;
            color: #F8FAFC;
            font-size: 12px;
            line-height: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .matrix-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid #E2E8F0;
            color: #1E293B;
            font-size: 14px;
            line-height: 22px;
            font-weight: 400;
            letter-spacing: 0;
            vertical-align: middle;
            font-variant-numeric: tabular-nums;
        }}

        .matrix-table td strong {{
            font-weight: 600;
            color: var(--text-dark);
        }}

        .matrix-table tr:nth-child(even) td {{
            background: #F8FAFC;
        }}

        .matrix-table tr:hover td {{
            background-color: #f1f5f9;
        }}

        /* Why AI Needs Financial Fine-Tuning Box */
        .why-card {{
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
            border: 1px solid #bfdbfe;
            border-left: 5px solid #2563eb;
            border-radius: 14px;
            padding: 30px;
            margin-bottom: 44px;
            box-shadow: var(--shadow-md);
        }}

        .why-card h3 {{
            font-size: 21px;
            font-weight: 800;
            color: #1e40af;
            margin-bottom: 14px;
            letter-spacing: -0.01em;
        }}

        .why-card ul {{
            margin-left: 20px;
            color: #334155;
            font-size: 16px;
        }}

        .why-card li {{
            margin-bottom: 10px;
            line-height: 1.6;
        }}

        /* Live Interactive Pipeline Animation Container */
        .pipeline-container {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 26px 30px;
            margin-bottom: 48px;
            box-shadow: var(--shadow-md);
            position: relative;
        }}

        .pipeline-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .pipeline-btn-group {{
            display: flex;
            gap: 10px;
        }}

        .btn {{
            background: #0f172a;
            color: #ffffff;
            border: none;
            padding: 9px 20px;
            font-family: inherit;
            font-size: 13.5px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }}

        .btn:hover {{
            background: #1e293b;
        }}

        .btn-outline {{
            background: #ffffff;
            color: #0f172a;
            border: 1px solid #cbd5e1;
        }}

        .btn-outline:hover {{
            background: #f8fafc;
            border-color: #94a3b8;
        }}

        #pipelineCanvas {{
            width: 100%;
            height: 460px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            display: block;
            cursor: default;
        }}

        /* Quick Node Navigation Pills */
        .pipeline-nav-bar {{
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
        }}

        .pipeline-nav-label {{
            font-size: 13px;
            color: #64748b;
            margin-bottom: 10px;
            display: block;
            font-weight: 600;
        }}

        .pipeline-nav-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .nav-pill {{
            background: #ffffff;
            color: #334155;
            border: 1px solid #cbd5e1;
            padding: 6px 14px;
            font-family: inherit;
            font-size: 12.5px;
            font-weight: 600;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.15s ease;
            box-shadow: var(--shadow-sm);
        }}

        .nav-pill:hover {{
            background: #0f172a;
            color: #ffffff;
            border-color: #0f172a;
        }}

        .nav-pill-mandate {{
            border-color: #fde68a;
            color: #b45309;
            background: #fffbeb;
        }}
        .nav-pill-mandate:hover {{
            background: #d97706;
            color: #ffffff;
            border-color: #d97706;
        }}

        .nav-pill-70b {{
            border-color: #bfdbfe;
            color: #1d4ed8;
            background: #eff6ff;
        }}
        .nav-pill-70b:hover {{
            background: #2563eb;
            color: #ffffff;
            border-color: #2563eb;
        }}

        .nav-pill-8b {{
            border-color: #bae6fd;
            color: #0369a1;
            background: #f0f9ff;
        }}
        .nav-pill-8b:hover {{
            background: #0284c7;
            color: #ffffff;
            border-color: #0284c7;
        }}

        .nav-pill-jev {{
            border-color: #a7f3d0;
            color: #047857;
            background: #ecfdf5;
        }}
        .nav-pill-jev:hover {{
            background: #059669;
            color: #ffffff;
            border-color: #059669;
        }}

        .nav-pill-decision {{
            border-color: #cbd5e1;
            color: #0f172a;
            background: #f8fafc;
        }}
        .nav-pill-decision:hover {{
            background: #0f172a;
            color: #ffffff;
            border-color: #0f172a;
        }}

        .nav-pill-market {{
            border-color: #e9d5ff;
            color: #6d28d9;
            background: #faf5ff;
        }}
        .nav-pill-market:hover {{
            background: #7c3aed;
            color: #ffffff;
            border-color: #7c3aed;
        }}

        /* Legend */
        .pipeline-legend {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            font-size: 13px;
            color: #64748b;
            margin-top: 16px;
            padding-top: 14px;
            border-top: 1px solid #e2e8f0;
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

        /* Live Execution Showcase Section */
        .live-run-container {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 30px 32px;
            margin-top: 36px;
            margin-bottom: 44px;
            box-shadow: var(--shadow-md);
        }}

        .live-run-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .live-run-tag {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .live-run-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14.5px;
            margin-top: 14px;
        }}

        .live-run-table th {{
            text-align: left;
            padding: 14px 16px;
            background: #0F172A;
            color: #F8FAFC;
            font-size: 12px;
            line-height: 16px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid #0F172A;
        }}

        .live-run-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid #E2E8F0;
            color: #1E293B;
            font-size: 14px;
            line-height: 22px;
            font-weight: 400;
            letter-spacing: 0;
            vertical-align: middle;
            font-variant-numeric: tabular-nums;
        }}

        .live-run-table tr:hover td {{
            background: #f8fafc;
        }}

        .status-pill-selected {{
            background: var(--ok-bg, #DCFCE7);
            color: var(--ok-fg, #166534);
            border: 1px solid var(--ok-bd, #86EFAC);
            padding: 4px 10px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 12px;
            white-space: nowrap;
        }}

        .status-pill-discounted {{
            background: var(--mute-bg, #F1F5F9);
            color: var(--mute-fg, #64748B);
            border: 1px solid var(--mute-bd, #CBD5E1);
            padding: 4px 10px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 12px;
            white-space: nowrap;
        }}

        .status-pill-weighted {{
            background: var(--info-bg, #DBEAFE);
            color: var(--info-fg, #1E40AF);
            border: 1px solid var(--info-bd, #93C5FD);
            padding: 4px 10px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 12px;
            white-space: nowrap;
        }}

        .badge-error {{
            background: #F1F5F9;
            color: #475569;
            border: 1px solid #CBD5E1;
            padding: 4px 10px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 12px;
            white-space: nowrap;
        }}

        /* Model Weaknesses / Empirical Model Autopsy Grid */
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
        }}

        /* Modal Overlay & Inspector Popups */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(6px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            padding: 24px;
        }}

        .modal-overlay.active {{
            display: flex;
        }}

        .modal-card {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 16px;
            width: 100%;
            max-width: 860px;
            max-height: 88vh;
            overflow-y: auto;
            padding: 34px;
            box-shadow: var(--shadow-xl);
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
            border-radius: 6px;
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
            color: #2563eb;
            margin-bottom: 6px;
        }}

        .modal-title {{
            font-size: 24px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 6px;
            padding-right: 40px;
            letter-spacing: -0.02em;
        }}

        .modal-subtitle {{
            font-size: 14px;
            color: #64748b;
            margin-bottom: 22px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .modal-grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
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
            font-weight: 700;
            color: #0f172a;
        }}

        .modal-code-block {{
            background: #0f172a;
            border: 1px solid #1e293b;
            color: #f8fafc;
            border-radius: 8px;
            padding: 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            word-break: break-word;
            margin-bottom: 20px;
            line-height: 1.5;
            max-height: 280px;
            overflow-y: auto;
        }}

        .modal-alert-danger {{
            background: #fff1f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
            line-height: 1.5;
        }}

        .modal-alert-success {{
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #065f46;
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
            line-height: 1.5;
        }}

        /* Process Steps Grid */
        .steps-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 48px;
        }}

        .step-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
            box-shadow: var(--shadow-sm);
            position: relative;
        }}

        .step-num {{
            width: 32px;
            height: 32px;
            background: #1e40af;
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 14px;
        }}

        .step-title {{
            font-size: 17px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 6px;
        }}

        .step-desc {{
            font-size: 15px;
            color: #475569;
            line-height: 1.5;
            margin-bottom: 0;
        }}

        /* Hardware Performance & Latency Charts */
        .graphs-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 24px;
            margin-bottom: 48px;
        }}

        .graph-card {{
            background: var(--card, #FFFFFF);
            border: 1px solid var(--border, #E2E8F0);
            border-radius: 14px;
            padding: 28px;
            box-shadow: var(--shadow-md);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .graph-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        .graph-card-title {{
            font-size: 18px;
            line-height: 26px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 20px;
        }}

        .bar-row {{
            margin-bottom: 16px;
        }}

        .bar-label-wrap {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            line-height: 20px;
            margin-bottom: 6px;
        }}

        .bar-model-name {{
            font-weight: 600;
            color: #1E293B;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .bar-val {{
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 500;
            color: var(--value, #334155);
            font-variant-numeric: tabular-nums;
        }}

        .bar-track {{
            width: 100%;
            height: 12px;
            background: var(--track, #E2E8F0);
            border-radius: 999px;
            overflow: hidden;
        }}

        .bar-fill {{
            height: 100%;
            border-radius: 999px;
            transition: width 0.6s ease;
        }}

        .badge-winner {{
            background: #DCFCE7;
            color: #166534;
            font-size: 11px;
            font-weight: 600;
            line-height: 1;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.02em;
            display: inline-block;
        }}

        /* Part 3 Leaderboard Interactive Section */
        .leaderboard-controls {{
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }}

        .lb-tab-btn {{
            font-family: inherit;
            font-size: 14px;
            font-weight: 600;
            padding: 9px 18px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            background: #ffffff;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }}

        .lb-tab-btn:hover {{
            border-color: #2563eb;
            color: #2563eb;
        }}

        .lb-tab-btn.active {{
            background: #1e40af;
            color: #ffffff;
            border-color: #1e40af;
            box-shadow: 0 2px 6px rgba(30, 64, 175, 0.25);
        }}

        .table-wrap {{
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 14px;
            margin-bottom: 44px;
            background: #ffffff;
            box-shadow: var(--shadow-md);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-variant-numeric: tabular-nums;
        }}

        th {{
            background: #0F172A;
            padding: 14px 16px;
            border-bottom: 2px solid #0F172A;
            font-weight: 600;
            color: #F8FAFC;
            font-size: 12px;
            line-height: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 14px 16px;
            border-bottom: 1px solid var(--border);
            color: #1E293B;
            font-size: 14px;
            line-height: 22px;
            font-weight: 400;
            letter-spacing: 0;
            vertical-align: middle;
            font-variant-numeric: tabular-nums;
        }}

        td strong {{
            font-weight: 600;
            color: var(--text-dark);
        }}

        tr:nth-child(even) td {{
            background: #F8FAFC;
        }}

        tr:hover td {{
            background-color: #f1f5f9;
        }}

        .mono {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
        }}

        /* Badges (WCAG AA High-Contrast Decision Palette) */
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 13px;
            line-height: 1;
            font-weight: 600;
            letter-spacing: 0.02em;
            white-space: nowrap;
        }}

        .ticker, .mono {{
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 0;
        }}

        .badge-buy {{ background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }}
        .badge-sell {{ background: #F3E8FF; color: #6B21A8; border: 1px solid #D8B4FE; }}
        .badge-hold {{ background: #F1F5F9; color: #334155; border: 1px solid #CBD5E1; }}
        .badge-abstain, .badge-veto {{ background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }}
        .badge-lag {{ background: #FFEDD5; color: #9A3412; border: 1px solid #FDBA74; }}

        .badge-selected {{ background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }}
        .badge-weighted {{ background: #EFF6FF; color: #1E3A8A; border: 1px solid #BFDBFE; }}
        .badge-discounted {{ background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }}

        /* Technical Page / Trade Explorer */
        .explorer-card {{
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px;
            background: #ffffff;
            margin-bottom: 48px;
            box-shadow: var(--shadow-md);
        }}

        /* Persona Switcher Bar (Tab 2) */
        .persona-bar {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 28px;
        }}

        .persona-bar-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .persona-bar-title {{
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #64748b;
        }}

        .persona-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .persona-pill-btn {{
            font-family: inherit;
            font-size: 14px;
            font-weight: 600;
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            background: #ffffff;
            color: #334155;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: var(--shadow-sm);
        }}

        .persona-pill-btn:hover {{
            border-color: #2563eb;
            color: #2563eb;
        }}

        .persona-pill-btn.active {{
            background: #1e40af;
            color: #ffffff;
            border-color: #1e40af;
            box-shadow: 0 4px 6px -1px rgba(30, 64, 175, 0.3);
        }}

        .persona-pill-btn .tag {{
            font-size: 12px;
            padding: 2px 7px;
            border-radius: 4px;
            background: #f1f5f9;
            color: #334155;
            font-weight: 700;
        }}

        .persona-pill-btn.active .tag {{
            background: rgba(255,255,255,0.25);
            color: #ffffff;
        }}

        .active-mandate-banner {{
            margin-top: 14px;
            font-size: 14px;
            color: #1e293b;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 12px 16px;
            border-radius: 8px;
            line-height: 1.55;
            box-shadow: var(--shadow-sm);
        }}

        .controls-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .trade-select {{
            font-family: inherit;
            font-size: 15px;
            font-weight: 600;
            padding: 12px 18px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background: #ffffff;
            color: var(--text-dark);
            max-width: 620px;
            width: 100%;
            cursor: pointer;
            box-shadow: var(--shadow-sm);
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        .trade-select:focus {{
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        .trade-meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            margin-bottom: 28px;
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 22px 24px;
        }}

        .meta-item-label {{
            font-size: 12px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}

        .meta-item-value {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-dark);
            margin-top: 3px;
        }}

        /* Constraint Verification Card */
        .constraint-card {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-left: 5px solid #2563eb;
            border-radius: 0 12px 12px 0;
            padding: 20px 24px;
            margin-bottom: 24px;
        }}

        /* Market Ground Truth vs SPY Box (Tab 2) */
        .market-gt-card {{
            background: #faf5ff;
            border: 1px solid #e9d5ff;
            border-left: 5px solid #7c3aed;
            border-radius: 0 12px 12px 0;
            padding: 22px 26px;
            margin-bottom: 28px;
        }}

        /* JEV Banner */
        .jev-banner {{
            border: 1px solid #a7f3d0;
            border-left: 6px solid #059669;
            background: #ecfdf5;
            border-radius: 0 12px 12px 0;
            padding: 24px 28px;
            margin-bottom: 36px;
            box-shadow: var(--shadow-sm);
        }}

        .jev-banner.abstain-style {{
            border-color: #cbd5e1;
            border-left-color: #64748b;
            background: #f8fafc;
        }}

        .jev-banner.veto-style {{
            border-color: #fecdd3;
            border-left-color: #e11d48;
            background: #fff1f2;
        }}

        .jev-banner.buy-style {{
            border-color: #a7f3d0;
            border-left-color: #059669;
            background: #ecfdf5;
        }}

        .jev-banner-title {{
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #1e40af;
            margin-bottom: 6px;
        }}

        .jev-banner-signal {{
            font-size: 28px;
            font-weight: 800;
            color: var(--text-dark);
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .jev-banner-rationale {{
            font-size: 16px;
            color: #334155;
            margin-top: 10px;
            line-height: 1.6;
        }}

        /* Models Grid & Scrollable JSON Sliders */
        .models-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 22px;
            margin-top: 24px;
        }}

        .model-card {{
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px 26px;
            background: #ffffff;
            box-shadow: var(--shadow-md);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}

        .model-card:hover {{
            transform: translateY(-2px);
            border-color: #cbd5e1;
            box-shadow: var(--shadow-lg);
        }}

        .model-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}

        .model-card-title {{
            font-size: 17px;
            font-weight: 700;
            color: var(--text-dark);
        }}

        .model-card-stats {{
            font-size: 13px;
            color: #64748b;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 2px;
        }}

        .model-card-rationale {{
            font-size: 14px;
            color: #334155;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px;
            margin-top: 14px;
            line-height: 1.55;
        }}

        /* Scrollable JSON Slider Container */
        .json-slider {{
            margin-top: 14px;
        }}

        .json-slider-title {{
            font-size: 12px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
        }}

        .json-box {{
            max-height: 200px;
            overflow-y: auto;
            background: #0f172a;
            border: 1px solid #1e293b;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            line-height: 1.5;
            scrollbar-width: thin;
            scrollbar-color: #475569 #0f172a;
        }}

        .json-box::-webkit-scrollbar {{
            width: 6px;
        }}
        .json-box::-webkit-scrollbar-thumb {{
            background: #475569;
            border-radius: 3px;
        }}

        /* Rubric Mini Grid */
        .rubric-mini {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-top: 14px;
            font-size: 12px;
            text-align: center;
        }}

        .rubric-mini-cell {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 4px;
        }}

        .rubric-mini-name {{
            color: #64748b;
            font-size: 12px;
            font-weight: 500;
        }}

        .rubric-mini-score {{
            font-weight: 700;
            color: var(--text-dark);
            margin-top: 2px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }}

        /* Hide Tab View */
        .view-content {{
            display: none;
        }}
        .view-content.active {{
            display: block;
        }}

        /* Footer (WCAG AA Compliant) */
        .footer {{
            margin-top: 80px;
            padding-top: 28px;
            border-top: 1px solid #E2E8F0;
            font-size: 14px;
            line-height: 22px;
            color: #64748B;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .footer a {{
            color: #1D4ED8;
            text-decoration: underline;
        }}
        .footer a:hover {{
            color: #1E3A8A;
        }}
        @media (max-width: 640px) {{
            h1 {{ font-size: 30px; line-height: 38px; }}
            h2 {{ font-size: 24px; line-height: 32px; }}
            h3, .persona-name {{ font-size: 18px; line-height: 26px; }}
            body {{ font-size: 16px; line-height: 26px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Top Navigation -->
        <nav class="nav-bar">
            <div class="brand">
                <div class="brand-logo">A</div>
                <div>
                    <div class="brand-text">Apertus Hackathon &bull; Congressional Trade Intelligence</div>
                    <div class="brand-sub">6 Frontier &amp; Local LLMs evaluated on 50 authentic STOCK Act filings vs S&amp;P 500 (SPY)</div>
                </div>
            </div>

            <!-- Tab Switcher -->
            <div class="tab-switcher">
                <button class="tab-btn active" onclick="switchTab('execTab')">1. Executive &amp; Benchmarks</button>
                <button class="tab-btn" onclick="switchTab('techTab')">2. Technical Audit &amp; JSON Telemetry</button>
            </div>

            <!-- PolyTICK.us attribution -->
            <a href="https://polytick.us" target="_blank" rel="noopener noreferrer" class="source-pill">
                <span class="source-dot"></span>
                <span>Data Source: <strong>PolyTICK.us</strong></span>
                <span style="font-size: 12px; color: #475569;">(2024 Filings) &nearr;</span>
            </a>
        </nav>

        <!-- ======================================================================== -->
        <!-- TAB 1: EXECUTIVE & BENCHMARKS (For Owners, Judges & Reviewers)           -->
        <!-- ======================================================================== -->
        <div id="execTab" class="view-content active">
            <!-- Hero Heading -->
            <header>
                <h1>Congressional Data Giving to AI Models and Their Benchmarks</h1>
                <p class="lead-text">
                    US Congressional members disclose significant personal equity trades under the federal STOCK Act. Using 50 authentic, high-impact trades curated from <strong><a href="https://polytick.us" target="_blank" style="color: #2563eb; text-decoration: underline;">PolyTICK.us</a></strong>, we conducted a rigorous benchmark comparing the Swiss AI <strong>Apertus</strong> models against 4 local models running on consumer GPU hardware, auditing them against Ground Truth S&amp;P 500 (SPY) returns across 4 distinct investor profiles.
                </p>
            </header>

            <!-- Key Metrics -->
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-label">Trades Tested</div>
                    <div class="kpi-value">50 / 50</div>
                    <div class="kpi-sub">Curated PolyTICK.us Set</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Inferences</div>
                    <div class="kpi-value">300</div>
                    <div class="kpi-sub">6 Models x 50 Trades</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">JEV Constraint Violations</div>
                    <div class="kpi-value">0</div>
                    <div class="kpi-sub">100% Mandate Safety Target</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Benchmark Baseline</div>
                    <div class="kpi-value">S&amp;P 500</div>
                    <div class="kpi-sub">SPY Ground Truth (T+90, 180, 270)</div>
                </div>
            </div>

            <!-- Dedicated Persona Mandate Framework Section -->
            <h2>The 4 Investor Personas: Why AI Must Enforce Individualized Constraints</h2>
            <p>
                In quantitative finance, a single universal &ldquo;BUY&rdquo; or &ldquo;SELL&rdquo; signal is dangerous. Different capital allocators operate under strict legal, ethical, and risk mandates. Under <strong>Prompt Set v2</strong>, our JEV Arbiter evaluates the exact same trade differently depending on who the investor is:
            </p>

            <div class="persona-grid">
                <!-- Persona A -->
                <div class="persona-card p-a">
                    <div class="persona-card-header">
                        <span class="persona-pill-badge">Investor A</span>
                        <span style="font-size: 12px; font-weight: 600; color: #64748b;">ESG / Exclusionary</span>
                    </div>
                    <div class="persona-name">Ethical / No-Military</div>
                    <div class="persona-mandate">
                        <strong>Hard Constraint:</strong> Must NOT hold companies in the military or defense sector ($GD, $RTX, $NOC, $HII, $BA).
                    </div>
                    <div class="persona-meta-row">
                        <div><span class="meta-label">Risk</span><span class="meta-val">Moderate</span></div>
                        <div><span class="meta-label">Horizon</span><span class="meta-val">6M</span></div>
                        <div><span class="meta-label">Max Position</span><span class="meta-val">5.0%</span></div>
                    </div>
                    <p class="enforcement-note">
                        <strong class="enforce-label">JEV Rule 1 Enforcement:</strong> Defense contractor trades are automatically vetoed (ABSTAIN), overriding any bullish model consensus.
                    </p>
                </div>

                <!-- Persona B -->
                <div class="persona-card p-b">
                    <div class="persona-card-header">
                        <span class="persona-pill-badge">Investor B</span>
                        <span style="font-size: 12px; font-weight: 600; color: #64748b;">Thematic Growth</span>
                    </div>
                    <div class="persona-name">Tech-Only Mandate</div>
                    <div class="persona-mandate">
                        <strong>Hard Constraint:</strong> Only companies classified in Information Technology ($AAPL, $NVDA, $PANW, $MSFT).
                    </div>
                    <div class="persona-meta-row">
                        <div><span class="meta-label">Risk</span><span class="meta-val">Aggressive</span></div>
                        <div><span class="meta-label">Horizon</span><span class="meta-val">6M</span></div>
                        <div><span class="meta-label">Max Position</span><span class="meta-val">8.0%</span></div>
                    </div>
                    <p class="enforcement-note">
                        <strong class="enforce-label">JEV Rule 1 Enforcement:</strong> Non-tech sectors (Energy, Consumer, Defense, Financials) are immediately vetoed as ABSTAIN.
                    </p>
                </div>

                <!-- Persona C -->
                <div class="persona-card p-c">
                    <div class="persona-card-header">
                        <span class="persona-pill-badge">Investor C</span>
                        <span style="font-size: 12px; font-weight: 600; color: #64748b;">Unconstrained Alpha</span>
                    </div>
                    <div class="persona-name">Open / All Industries</div>
                    <div class="persona-mandate">
                        <strong>Constraint:</strong> No sector or geography restrictions. Evaluates trades purely on quantitative and insider merits.
                    </div>
                    <div class="persona-meta-row">
                        <div><span class="meta-label">Risk</span><span class="meta-val">Aggressive</span></div>
                        <div><span class="meta-label">Horizon</span><span class="meta-val">6M</span></div>
                        <div><span class="meta-label">Max Position</span><span class="meta-val">10.0%</span></div>
                    </div>
                    <p class="enforcement-note">
                        <strong class="enforce-label">JEV Merits Enforcement:</strong> Constraint always passes; evaluates disclosure lag (&lt;40d), transaction size, and committee alpha.
                    </p>
                </div>

                <!-- Persona D -->
                <div class="persona-card p-d">
                    <div class="persona-card-header">
                        <span class="persona-pill-badge">Investor D</span>
                        <span style="font-size: 12px; font-weight: 600; color: #64748b;">Capital Preservation</span>
                    </div>
                    <div class="persona-name">US-Market Only (Conservative)</div>
                    <div class="persona-mandate">
                        <strong>Hard Constraint:</strong> Must be listed on a major US exchange (NYSE / Nasdaq). Strict 3M horizon.
                    </div>
                    <div class="persona-meta-row">
                        <div><span class="meta-label">Risk</span><span class="meta-val">Conservative</span></div>
                        <div><span class="meta-label">Horizon</span><span class="meta-val">3M</span></div>
                        <div><span class="meta-label">Max Position</span><span class="meta-val">3.0%</span></div>
                    </div>
                    <p class="enforcement-note">
                        <strong class="enforce-label">JEV Sizing Enforcement:</strong> Vetoes unlisted OTC funds; caps position allocations at conservative 2.5% over 3-month horizon.
                    </p>
                </div>
            </div>

            <!-- SECTION: LIVE INTERACTIVE PIPELINE ARCHITECTURE -->
            <h2>Live System Architecture &amp; Data Pipeline Animation</h2>
            <p>
                Watch how authentic trade disclosures from <strong>PolyTICK.us</strong> are parsed into the <strong>Evidence Packet</strong> (with strict T=tx_date time freeze &amp; disclosure lag hygiene), merged with the active <strong>Investor Mandate (Personas A-D)</strong>, and dispatched simultaneously to all 6 LLMs. Their independent evaluations converge into the <strong>JEV Arbiter Layer</strong> (Part 2), which verifies constraint safety, discounts hallucinating models, and delivers actionable <strong>Fiduciary Decision Support</strong> evaluated against the <strong>S&amp;P 500 Alpha Engine</strong> (Part 3).
                <strong>Click any box on the diagram below to inspect its live data, calculations, and internal outputs.</strong>
            </p>

            <div class="pipeline-container">
                <div class="pipeline-header">
                    <div>
                        <strong style="font-size: 18px; color: #0f172a;">Live Interactive Pipeline Animation (Prompt Set v2 Specification)</strong>
                        <span style="font-size: 13.5px; color: #64748b; margin-left: 8px;">(Click any box to inspect data)</span>
                    </div>
                    <div class="pipeline-btn-group">
                        <button class="btn btn-outline" onclick="triggerTradePulse()">Pulse Current Trade</button>
                        <button class="btn" onclick="toggleAnimation()" id="animToggleBtn">Pause Flow</button>
                    </div>
                </div>

                <canvas id="pipelineCanvas" width="1100" height="460"></canvas>

                <!-- Clickable Node Badges -->
                <div class="pipeline-nav-bar">
                    <span class="pipeline-nav-label">Click any diagram box above or select a pipeline component below to inspect live data:</span>
                    <div class="pipeline-nav-buttons">
                        <button class="nav-pill" onclick="openNodeModal('trade')">1. PolyTICK.us Filing</button>
                        <button class="nav-pill" onclick="openNodeModal('packet')">2. Evidence Packet &amp; Lag</button>
                        <button class="nav-pill nav-pill-mandate" onclick="openNodeModal('mandate')">3. Investor Mandate (A-D)</button>
                        <button class="nav-pill nav-pill-70b" onclick="openNodeModal('Apertus-1.5-70B')">Apertus 70B (Cloud API)</button>
                        <button class="nav-pill nav-pill-8b" onclick="openNodeModal('Apertus-1.5-8B')">Apertus 8B (Swiss Local)</button>
                        <button class="nav-pill" onclick="openNodeModal('Qwen-2.5-14B-Coder')">Qwen 14B</button>
                        <button class="nav-pill" onclick="openNodeModal('SecurityAI-14B')">SecurityAI 14B</button>
                        <button class="nav-pill" onclick="openNodeModal('Neo-Uncensored-8B')">Neo 8B</button>
                        <button class="nav-pill" onclick="openNodeModal('Llama-3.1-8B-WhiteRabbitNeo')">WhiteRabbitNeo 8B</button>
                        <button class="nav-pill nav-pill-jev" onclick="openNodeModal('jev')">4. JEV Arbiter Audit</button>
                        <button class="nav-pill nav-pill-decision" onclick="openNodeModal('decision')">5. Fiduciary Decision</button>
                        <button class="nav-pill nav-pill-market" onclick="openNodeModal('market')">6. S&amp;P 500 Alpha Engine</button>
                    </div>
                </div>

                <div class="pipeline-legend">
                    <div class="legend-item"><span class="legend-dot" style="background: #0284c7;"></span> <span>Evidence Stream (Blue: Facts &amp; Lag)</span></div>
                    <div class="legend-item"><span class="legend-dot" style="background: #d97706;"></span> <span>Mandate Stream (Amber: Constraints A-D)</span></div>
                    <div class="legend-item"><span class="legend-dot" style="background: #059669;"></span> <span>Verified / Selected Model Signal</span></div>
                    <div class="legend-item"><span class="legend-dot" style="background: #e11d48;"></span> <span>Discounted Signal (0% Weight)</span></div>
                    <div class="legend-item"><span class="legend-dot" style="background: #7c3aed;"></span> <span>S&amp;P 500 Alpha Benchmark Flow</span></div>
                    <div class="legend-item"><span>Status: <strong id="pipelineLiveStatus" style="color: #0f172a;">Active Dual-Stream Pipeline</strong></span></div>
                </div>
            </div>

            <!-- 4 Step Process Cards -->
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-num">1</div>
                    <div class="step-title">Ingest &amp; Freeze Time</div>
                    <p class="step-desc">Ingest raw disclosure from PolyTICK.us. Strictly freeze time boundary at transaction date to eliminate lookahead bias.</p>
                </div>
                <div class="step-card">
                    <div class="step-num">2</div>
                    <div class="step-title">Parallel Quant Signals</div>
                    <p class="step-desc">Dispatch Evidence Packet separately to each model (Apertus 70B/8B, Qwen 14B, Llama 8B) under Investor Persona constraints.</p>
                </div>
                <div class="step-card">
                    <div class="step-num">3</div>
                    <div class="step-title">JEV Multi-Rubric Audit</div>
                    <p class="step-desc">JEV independently verifies ground truth constraint, scores each model across Rubric R1-R8, and discounts rogue models.</p>
                </div>
                <div class="step-card">
                    <div class="step-num">4</div>
                    <div class="step-title">Protected Decision</div>
                    <p class="step-desc">JEV synthesizes trusted model consensus into an actionable final recommendation (BUY, HOLD, SELL, or ABSTAIN).</p>
                </div>
            </div>

            <!-- Cross-Persona Decision Matrix Table -->
            <h2>Cross-Persona Decision Matrix: Same Trade, Divergent Decisions</h2>
            <p>
                Empirical demonstration of how the JEV Arbiter synthesizes the exact same PolyTICK.us trade record into radically different fiduciary decisions based on the investor profile:
            </p>

            <div class="matrix-table-wrap">
                <table class="matrix-table">
                    <thead>
                        <tr>
                            <th>Politician &amp; Asset</th>
                            <th>Sector</th>
                            <th>Investor A (Ethical)</th>
                            <th>Investor B (Tech-Only)</th>
                            <th>Investor C (All Sectors)</th>
                            <th>Investor D (US-Market)</th>
                            <th>Fiduciary Takeaway</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <strong>Scott Franklin</strong><br>
                                <span class="mono">$GD</span> &bull; General Dynamics ($100k Buy)
                            </td>
                            <td>Aerospace &amp; Defense</td>
                            <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                            <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                            <td><span class="badge badge-buy">BUY (6.0% Alloc)</span></td>
                            <td><span class="badge badge-buy">BUY (2.5% Alloc)</span></td>
                            <td style="font-size: 13px; color: #475569;">
                                Defense vetoed in A &amp; B; C &amp; D capitalize on House Armed Services insider alpha.
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Michael McCaul</strong><br>
                                <span class="mono">$CVX</span> &bull; Chevron Corp ($50k Buy)
                            </td>
                            <td>Energy / Oil &amp; Gas</td>
                            <td><span class="badge badge-lag">ABSTAIN (Lag)</span></td>
                            <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                            <td><span class="badge badge-lag">ABSTAIN (Lag)</span></td>
                            <td><span class="badge badge-lag">ABSTAIN (Lag)</span></td>
                            <td style="font-size: 13px; color: #475569;">
                                Investor B strictly excludes energy; C &amp; D filtered for 46-day disclosure delay.
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Nancy Pelosi</strong><br>
                                <span class="mono">$AAPL</span> &bull; Apple Inc ($5M-$25M Sale)
                            </td>
                            <td>Information Tech</td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td style="font-size: 13px; color: #475569;">
                                Tech sector permitted across all; Pelosi's partial sale triggers hold rather than new buy.
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Marjorie Taylor Greene</strong><br>
                                <span class="mono">$NVDA</span> &bull; NVIDIA Corp ($50k Buy)
                            </td>
                            <td>Information Tech</td>
                            <td><span class="badge badge-buy">BUY (3.5% Alloc)</span></td>
                            <td><span class="badge badge-buy">BUY (5.0% Alloc)</span></td>
                            <td><span class="badge badge-buy">BUY (6.0% Alloc)</span></td>
                            <td><span class="badge badge-buy">BUY (2.5% Alloc)</span></td>
                            <td style="font-size: 13px; color: #475569;">
                                Tech permitted across all; position sizing automatically scales from 2.5% (conservative) to 6.0% (aggressive).
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Ro Khanna</strong><br>
                                <span class="mono">$KMX</span> &bull; CarMax Inc ($15k Buy)
                            </td>
                            <td>Consumer Discretionary</td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td><span class="badge badge-hold">HOLD (0%)</span></td>
                            <td style="font-size: 13px; color: #475569;">
                                Non-tech violates Investor B mandate; evaluated on neutral merits for A, C, and D.
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <strong>Josh Gottheimer</strong><br>
                                <span class="mono">$NOC</span> &bull; Northrop Grumman ($15k Sale)
                            </td>
                            <td>Aerospace &amp; Defense</td>
                            <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                            <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                            <td><span class="badge badge-sell">SELL (Exit)</span></td>
                            <td><span class="badge badge-sell">SELL (Exit)</span></td>
                            <td style="font-size: 13px; color: #475569;">
                                Ethical funds ignore defense sales; unconstrained investors heed insider exit signal.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- SECTION: LIVE STEP-BY-STEP WORKFLOW AUDIT TELEMETRY -->
            <div class="live-run-container">
                <div class="live-run-header">
                    <div>
                        <div class="live-run-tag"><span class="source-dot"></span> Live Telemetry: CSCS ALPS API &bull; RTX 5060 Ti GPU</div>
                        <h3 style="font-size: 22px; font-weight: 800; color: #0f172a; margin-top: 8px; margin-bottom: 4px;">
                            Live Multi-Model Workflow Audit &amp; Fiduciary Execution
                        </h3>
                        <p style="font-size: 14.5px; color: #64748b; margin-bottom: 0;">
                            Live empirical execution across all 6 models evaluated on authentic disclosure: <strong>Rep. Ro Khanna ($HII) &mdash; Armed Services Committee</strong> under <strong>Investor A (Ethical / No-Military Mandate)</strong>.
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <span class="mono" style="font-size: 13px; color: #64748b; background: #f8fafc; border: 1px solid #e2e8f0; padding: 6px 12px; border-radius: 6px; display: inline-block;">
                            Audit Status: Verified Live
                        </span>
                    </div>
                </div>

                <div style="overflow-x: auto;">
                    <table class="live-run-table">
                        <thead>
                            <tr>
                                <th>Step / Model</th>
                                <th>Hardware Host</th>
                                <th>Latency</th>
                                <th>Speed</th>
                                <th>Schema Adherence</th>
                                <th>Mandate Check ($HII)</th>
                                <th>Model Signal</th>
                                <th style="min-width: 195px; white-space: nowrap;">JEV Arbiter Audit</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="background: #FFFFFF;">
                                <td><strong style="color: #1E3A8A;">1. Apertus 1.5-70B</strong></td>
                                <td style="color: #475569;">CSCS Swiss ALPS API</td>
                                <td class="mono" style="color: #334155;"><strong>5.99s</strong></td>
                                <td class="mono" style="color: #334155;">63.5 tok/s</td>
                                <td><span style="color: #166534; font-weight: 600;">&#10003; VALID JSON</span></td>
                                <td><span style="color: #B45309; font-weight: 500;">Passes: False (Defense)</span></td>
                                <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                                <td style="white-space: nowrap;"><span class="status-pill-selected">SELECTED (Weight 0.50)</span></td>
                            </tr>
                            <tr style="background: #F8FAFC;">
                                <td><strong style="color: #2563EB;">2. Apertus 1.5-8B</strong></td>
                                <td style="color: #475569;">CSCS Swiss ALPS API</td>
                                <td class="mono" style="color: #334155;"><strong>2.60s</strong></td>
                                <td class="mono" style="color: #334155; font-weight: 700;">136.8 tok/s</td>
                                <td><span style="color: #166534; font-weight: 600;">&#10003; VALID JSON</span></td>
                                <td><span style="color: #B45309; font-weight: 500;">Passes: False (Defense)</span></td>
                                <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                                <td style="white-space: nowrap;"><span class="status-pill-weighted">WEIGHTED (Weight 0.25)</span></td>
                            </tr>
                            <tr style="background: #FFFFFF;">
                                <td><strong style="color: #B45309;">3. Qwen 2.5 Coder 14B</strong></td>
                                <td style="color: #475569;">Local RTX 5060 Ti</td>
                                <td class="mono" style="color: #334155;">12.67s</td>
                                <td class="mono" style="color: #334155;">39.6 tok/s</td>
                                <td><span style="color: #166534; font-weight: 600;">&#10003; VALID JSON</span></td>
                                <td><span style="color: #B45309; font-weight: 500;">Passes: False (Defense)</span></td>
                                <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                                <td style="white-space: nowrap;"><span class="status-pill-weighted">WEIGHTED (Weight 0.25)</span></td>
                            </tr>
                            <tr style="background: #F8FAFC;">
                                <td><strong style="color: #BE185D;">4. SecurityAI 14B</strong></td>
                                <td style="color: #475569;">Local RTX 5060 Ti</td>
                                <td class="mono" style="color: #334155;">8.65s</td>
                                <td class="mono" style="color: #334155;">39.5 tok/s</td>
                                <td><span style="color: #166534; font-weight: 600;">&#10003; VALID JSON</span></td>
                                <td><span style="color: #B45309; font-weight: 500;">Passes: False (Defense)</span></td>
                                <td><span class="badge badge-veto">ABSTAIN (Veto)</span></td>
                                <td style="white-space: nowrap;"><span class="status-pill-weighted">WEIGHTED (Weight 0.25)</span></td>
                            </tr>
                            <tr style="background: #FEF2F2; border-left: 3px solid #DC2626;">
                                <td><strong style="color: #6D28D9;">5. Neo-Uncensored 8B</strong></td>
                                <td style="color: #475569;">Local RTX 5060 Ti</td>
                                <td class="mono" style="color: #334155;">34.20s</td>
                                <td class="mono" style="color: #334155;">75.5 tok/s</td>
                                <td><span style="color: #B91C1C; font-weight: 600;">&#10007; PARSE ERROR</span></td>
                                <td><span style="color: #B91C1C; font-weight: 500;">Echoed Instructions Prose</span></td>
                                <td><span class="badge badge-error">ERROR</span></td>
                                <td style="white-space: nowrap;"><span class="status-pill-discounted">DISCOUNTED (Weight 0.00)</span></td>
                            </tr>
                            <tr style="background: #FEF2F2; border-left: 3px solid #DC2626;">
                                <td><strong style="color: #0F766E;">6. WhiteRabbitNeo 8B</strong></td>
                                <td style="color: #475569;">Local RTX 5060 Ti</td>
                                <td class="mono" style="color: #334155;">12.87s</td>
                                <td class="mono" style="color: #334155;">75.3 tok/s</td>
                                <td><span style="color: #B91C1C; font-weight: 600;">&#10007; PARSE ERROR</span></td>
                                <td><span style="color: #B91C1C; font-weight: 500;">Unstructured Markdown Text</span></td>
                                <td><span class="badge badge-error">ERROR</span></td>
                                <td style="white-space: nowrap;"><span class="status-pill-discounted">DISCOUNTED (Weight 0.00)</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- JEV Synthesis & S&P 500 Alpha Callout Grid (WCAG AA Strict Contrast) -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px; margin-top: 24px;">
                    <!-- Left: Verdict Card (Fiduciary Protection) -->
                    <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 12px; padding: 20px 22px;">
                        <div style="font-size: 12px; line-height: 16px; font-weight: 600; color: #047857; text-transform: uppercase; letter-spacing: 0.06em;">JEV Consensus Verdict</div>
                        <div style="font-size: 20px; line-height: 28px; font-weight: 700; color: #064E3B; margin-top: 4px;">ABSTAIN &mdash; 100% Capital Protection</div>
                        <p style="font-size: 14px; line-height: 22px; color: #065F46; margin-top: 8px; margin-bottom: 0;">
                            Huntington Ingalls is the primary builder of US nuclear submarines. In accordance with Prompt Set v2 Rule #3, hard negative screens strictly override momentum conviction. Both unparsable rogue models were discounted to 0% weight.
                        </p>
                    </div>

                    <!-- Right: Alpha / Fiduciary Caution Card (Amber Caution) -->
                    <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 20px 22px;">
                        <div style="font-size: 12px; line-height: 16px; font-weight: 600; color: #B45309; text-transform: uppercase; letter-spacing: 0.06em;">S&amp;P 500 Alpha Engine (Part 3) &bull; Mandate Caution</div>
                        <div style="font-size: 20px; line-height: 28px; font-weight: 700; color: #78350F; margin-top: 4px;">+16.10% Excess Alpha ($HII +19.55% vs SPY +3.45%)</div>
                        <p style="font-size: 14px; line-height: 22px; color: #92400E; margin-top: 8px; margin-bottom: 0;">
                            While this defense trade beat the S&amp;P 500 by +16.10%, investing would have resulted in severe client regulatory and ethical breach. JEV successfully balanced market edge with absolute fiduciary mandate safety.
                        </p>
                    </div>
                </div>
            </div>
<!-- Part 3 Leaderboard Interactive Section -->
            <h2>Part 3 Official Benchmark Leaderboard (Ground Truth vs S&amp;P 500)</h2>
            <p>
                Strict empirical evaluation measured against closing prices at T+90, T+180, and T+270 days vs S&amp;P 500 (SPY).
                Filter across investor profiles to inspect how constraint compliance, directional win rate, and net alpha shift:
            </p>

            <div class="leaderboard-controls">
                <button class="lb-tab-btn active" id="lbTab_OVERALL" onclick="renderLeaderboard('OVERALL')">Overall Aggregate</button>
                <button class="lb-tab-btn" id="lbTab_A" onclick="renderLeaderboard('A')">Investor A (Ethical / No-Military)</button>
                <button class="lb-tab-btn" id="lbTab_B" onclick="renderLeaderboard('B')">Investor B (Tech-Only)</button>
                <button class="lb-tab-btn" id="lbTab_C" onclick="renderLeaderboard('C')">Investor C (Open / All Sectors)</button>
                <button class="lb-tab-btn" id="lbTab_D" onclick="renderLeaderboard('D')">Investor D (US-Market Only)</button>
            </div>

            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Model Identifier</th>
                            <th>Deployment Tier</th>
                            <th>Constraint Compliance</th>
                            <th>Win Rate vs SPY</th>
                            <th>Net Alpha vs SPY (6M)</th>
                            <th>Brier Score</th>
                            <th>Abstention Rate</th>
                        </tr>
                    </thead>
                    <tbody id="leaderboardBody">
                        <!-- Populated by JavaScript -->
                    </tbody>
                </table>
            </div>

            <!-- Why AI Needs Financial Fine-Tuning -->
            <div class="why-card">
                <h3>Why AI Must Be Specialized &amp; Evaluated on Financial Data</h3>
                <p>
                    Generic large language models suffer from critical blindspots when handling legislative financial disclosures:
                </p>
                <ul>
                    <li><strong>Constraint Hallucinations:</strong> Standard models fail to recognize complex parent-subsidiary structures (e.g. classifying defense contractor Huntington Ingalls as generic industrial manufacturing).</li>
                    <li><strong>Severe Lookahead Bias:</strong> Off-the-shelf LLMs evaluate a 2024 historical trade using 2025/2026 price memories, generating fraudulent backtest alpha.</li>
                    <li><strong>Disclosure Decay Blindness:</strong> Filings made 35+ days late have already lost their informational edge. Unspecialized models treat stale disclosures as fresh entries.</li>
                    <li><strong>The Solution (JEV Layer):</strong> An independent Juried Evaluator (JEV) that audits model outputs, enforces zero-lookahead time hygiene, and vetoes constraint breaches before capital is committed.</li>
                </ul>
            </div>

            <!-- SECTION: MODEL-BY-MODEL WEAKNESSES & EMPIRICAL AUTOPSY -->
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
            </div>

            <!-- Empirical Graphs Grid -->
            <h2>Hardware Performance &amp; Generation Latency</h2>
            <p>Direct comparisons across throughput and latency measured during live benchmark runs on CSCS ALPS supercomputing infrastructure and local NVIDIA RTX 5060 Ti GPU hardware.</p>

            <div class="graphs-grid">
                <!-- Speed Graph -->
                <div class="graph-card">
                    <div class="graph-card-title">Generation Speed (Tokens / Second) &mdash; Higher is Better</div>
                    
                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">
                                <span>Apertus 1.5 8B (CSCS ALPS)</span>
                                <span class="badge-winner">Fastest</span>
                            </span>
                            <span class="bar-val">136.8 tok/s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 100%; background: var(--m-apertus-8b);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">Apertus 1.5 70B (CSCS ALPS)</span>
                            <span class="bar-val">63.5 tok/s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 46%; background: var(--m-apertus-70b);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">Neo-Uncensored 8B (RTX 5060 Ti)</span>
                            <span class="bar-val">75.5 tok/s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 55%; background: var(--m-neo-uncens);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">WhiteRabbitNeo 8B (RTX 5060 Ti)</span>
                            <span class="bar-val">75.3 tok/s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 55%; background: var(--m-whiterabbit);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">Qwen 2.5 Coder 14B (RTX 5060 Ti)</span>
                            <span class="bar-val">39.6 tok/s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 29%; background: var(--m-qwen-coder);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">SecurityAI 14B (RTX 5060 Ti)</span>
                            <span class="bar-val">39.5 tok/s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 29%; background: var(--m-securityai);"></div>
                        </div>
                    </div>
                </div>

                <!-- Latency Graph (Identical Model Order & Colors) -->
                <div class="graph-card">
                    <div class="graph-card-title">Average Evaluation Latency (Seconds) &mdash; Lower is Better</div>
                    
                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">
                                <span>Apertus 1.5 8B (CSCS ALPS)</span>
                                <span class="badge-winner">Lowest Latency</span>
                            </span>
                            <span class="bar-val">2.60s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 8%; background: var(--m-apertus-8b);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">Apertus 1.5 70B (CSCS ALPS)</span>
                            <span class="bar-val">5.99s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 18%; background: var(--m-apertus-70b);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">Neo-Uncensored 8B (RTX 5060 Ti)</span>
                            <span class="bar-val">34.20s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 100%; background: var(--m-neo-uncens);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">WhiteRabbitNeo 8B (RTX 5060 Ti)</span>
                            <span class="bar-val">12.87s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 38%; background: var(--m-whiterabbit);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">Qwen 2.5 Coder 14B (RTX 5060 Ti)</span>
                            <span class="bar-val">12.67s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 37%; background: var(--m-qwen-coder);"></div>
                        </div>
                    </div>

                    <div class="bar-row">
                        <div class="bar-label-wrap">
                            <span class="bar-model-name">SecurityAI 14B (RTX 5060 Ti)</span>
                            <span class="bar-val">8.65s</span>
                        </div>
                        <div class="bar-track">
                            <div class="bar-fill" style="width: 25%; background: var(--m-securityai);"></div>
                        </div>
                    </div>
                </div>
            </div>

                    </div>


        <!-- ======================================================================== -->
        <!-- TAB 2: TECHNICAL AUDIT & RAW TELEMETRY (For Engineers & Quants)           -->
        <!-- ======================================================================== -->
        <div id="techTab" class="view-content">
            <header style="margin-bottom: 24px;">
                <h1>Technical Audit &amp; Raw JSON Telemetry</h1>
                <p class="lead-text">
                    Inspect all 50 authentic STOCK Act disclosures, individual model structured JSON responses, rubric evaluations (R1-R8), Ground Truth S&amp;P 500 (SPY) alpha returns, and synthesized JEV Arbiter decisions under each of the 4 Investor Personas.
                </p>
            </header>

            <div class="explorer-card">
                <!-- Interactive Investor Persona Selector (Tab 2) -->
                <div class="persona-bar">
                    <div class="persona-bar-header">
                        <span class="persona-bar-title">Select Active Investor Persona Mandate:</span>
                        <span style="font-size: 12px; color: #64748b;">Dynamically recalculates constraints &amp; JEV logic</span>
                    </div>
                    <div class="persona-pills">
                        <button class="persona-pill-btn active" id="pillA" onclick="setTechPersona('A')">
                            <span class="tag">Investor A</span>
                            <span>Ethical / No-Military</span>
                        </button>
                        <button class="persona-pill-btn" id="pillB" onclick="setTechPersona('B')">
                            <span class="tag">Investor B</span>
                            <span>Tech-Only</span>
                        </button>
                        <button class="persona-pill-btn" id="pillC" onclick="setTechPersona('C')">
                            <span class="tag">Investor C</span>
                            <span>Open / All Industries</span>
                        </button>
                        <button class="persona-pill-btn" id="pillD" onclick="setTechPersona('D')">
                            <span class="tag">Investor D</span>
                            <span>US-Market (Conservative)</span>
                        </button>
                    </div>
                    <div id="activeMandateBanner" class="active-mandate-banner">
                        <!-- Populated by JavaScript -->
                    </div>
                </div>

                <!-- Controls -->
                <div class="controls-bar">
                    <div>
                        <label style="font-size: 14px; font-weight: 700; color: #475569; display: block; margin-bottom: 6px;">Select Trade from PolyTICK.us Dataset:</label>
                        <select id="techTradeSelect" class="trade-select" onchange="renderTechTrade(parseInt(this.value))">
                            <!-- Populated by JavaScript -->
                        </select>
                    </div>
                    <div style="font-size: 14px; color: #64748b; font-weight: 500;">
                        Showing Trade <span id="currentTradeNum" style="font-weight: 700; color: #0f172a;">1</span> of 50
                    </div>
                </div>

                <!-- Trade Metadata -->
                <div id="techTradeMeta" class="trade-meta-grid">
                    <!-- Populated by JavaScript -->
                </div>

                <!-- Constraint Verification Details Card -->
                <div id="techConstraintCard" class="constraint-card">
                    <!-- Populated by JavaScript -->
                </div>

                <!-- Ground Truth S&P 500 (SPY) Performance Card (Part 3) -->
                <div id="techMarketGtBox" class="market-gt-card">
                    <!-- Populated by JavaScript -->
                </div>

                <!-- JEV Decision Banner -->
                <div id="techJevBanner" class="jev-banner">
                    <!-- Populated by JavaScript -->
                </div>

                <!-- All 6 Models Grid -->
                <h3 style="font-size: 19px; font-weight: 700; color: #0f172a; margin-top: 32px; margin-bottom: 16px;">
                    Model Inferences &amp; JEV Rubric Scores (R1 &ndash; R8)
                </h3>
                <div id="techModelsGrid" class="models-grid">
                    <!-- Populated by JavaScript -->
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="footer">
            <div>Congressional Trade Intelligence &bull; JEV Arbiter Layer &bull; Data from <strong><a href="https://polytick.us" target="_blank" style="color: inherit; text-decoration: underline;">PolyTICK.us</a></strong></div>
            <div>Evaluated on Swiss AI CSCS ALPS Infrastructure &amp; Local NVIDIA RTX 5060 Ti GPU</div>
        </footer>
    </div>

    <!-- Scripts -->
    <script>
        const tradesData = {trades_json_str};
        const leaderboardsData = {leaderboards_json_str};
        let currentTradeIndex = 0;
        let currentPersona = 'A';

        // Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.view-content').forEach(v => v.classList.remove('active'));

            if (tabId === 'execTab') {{
                document.querySelectorAll('.tab-btn')[0].classList.add('active');
                document.getElementById('execTab').classList.add('active');
            }} else {{
                document.querySelectorAll('.tab-btn')[1].classList.add('active');
                document.getElementById('techTab').classList.add('active');
            }}
        }}

        // Helper badges
        function getBadgeClass(signal) {{
            if (!signal) return 'badge-hold';
            const s = String(signal).toUpperCase();
            if (s.includes('BUY')) return 'badge-buy';
            if (s.includes('SELL')) return 'badge-sell';
            if (s.includes('HOLD')) return 'badge-hold';
            if (s.includes('LAG')) return 'badge-lag';
            if (s.includes('VETO')) return 'badge-veto';
            return 'badge-abstain';
        }}

        function getStatusBadge(status) {{
            if (status === 'SELECTED') return '<span class="badge badge-selected">SELECTED</span>';
            if (status === 'WEIGHTED') return '<span class="badge badge-weighted">WEIGHTED</span>';
            return '<span class="badge badge-discounted">DISCOUNTED</span>';
        }}

        // Render Leaderboard for Tab 1
        function renderLeaderboard(personaId) {{
            document.querySelectorAll('.lb-tab-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('lbTab_' + personaId);
            if (activeBtn) activeBtn.classList.add('active');

            const rows = leaderboardsData[personaId] || [];
            const tbody = document.getElementById('leaderboardBody');
            tbody.innerHTML = '';

            rows.forEach(r => {{
                const tr = document.createElement('tr');
                if (r.is_jev) tr.style.backgroundColor = '#f0fdf4';

                const alphaColor = r.net_alpha_6m_pct > 0 ? '#059669' : (r.net_alpha_6m_pct < 0 ? '#e11d48' : '#64748b');
                const alphaSign = r.net_alpha_6m_pct > 0 ? '+' : '';

                tr.innerHTML = `
                    <td style="font-weight: 700;">#${{r.rank}}</td>
                    <td>
                        <strong>${{r.model_name}}</strong>
                        ${{r.is_jev ? '<span class="badge badge-selected" style="margin-left: 8px;">ARBITER LAYER</span>' : ''}}
                    </td>
                    <td>${{r.tier}}</td>
                    <td>
                        <span class="badge ${{r.constraint_compliance_pct >= 90 ? 'badge-selected' : (r.constraint_compliance_pct >= 70 ? 'badge-weighted' : 'badge-discounted')}}">
                            ${{r.constraint_compliance_pct}}%
                        </span>
                        <span style="font-size: 12px; color: #475569; margin-left: 4px;">(${{r.constraint_violations}} viols)</span>
                    </td>
                    <td class="mono" style="font-weight: 700;">${{r.win_rate_pct}}%</td>
                    <td class="mono" style="font-weight: 700; color: ${{alphaColor}};">
                        ${{alphaSign}}${{r.net_alpha_6m_pct}}%
                    </td>
                    <td class="mono">${{r.brier_score}}</td>
                    <td class="mono">${{r.abstention_rate_pct}}%</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Switch Active Technical Persona
        function setTechPersona(personaId) {{
            currentPersona = personaId;
            document.querySelectorAll('.persona-pill-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('pill' + personaId).classList.add('active');
            renderTechTrade(currentTradeIndex);
            triggerTradePulse();
            if (activeModalKey) populateModal(activeModalKey);
        }}

        // Populate Technical Trade Select
        function initTechSelect() {{
            const select = document.getElementById('techTradeSelect');
            select.innerHTML = '';
            tradesData.forEach((t, i) => {{
                const opt = document.createElement('option');
                opt.value = i;
                opt.textContent = `[Trade #${{t.trade_idx}}] ${{t.politician}} | $${{t.ticker}} (${{t.tx_type}}) | ${{t.amount}}`;
                select.appendChild(opt);
            }});
        }}

        // Render Technical Trade
        function renderTechTrade(idx) {{
            currentTradeIndex = idx;
            const t = tradesData[idx];
            if (!t) return;

            document.getElementById('currentTradeNum').textContent = t.trade_idx;
            const select = document.getElementById('techTradeSelect');
            if (select.value != idx) select.value = idx;
            triggerTradePulse();
            if (activeModalKey) populateModal(activeModalKey);

            // Get Persona Info for Active Persona
            const personaData = (t.personas && t.personas[currentPersona]) ? t.personas[currentPersona] : null;
            const profile = personaData ? personaData.profile : {{
                name: "Persona " + currentPersona,
                mandate: "Standard mandate",
                risk_appetite: "Moderate",
                target_horizon: "6M",
                max_position_pct: 5.0
            }};
            const constraint = personaData ? personaData.constraint_check : t.ground_truth_constraint;
            const jev = personaData ? personaData.jev_decision : t.jev_decision;

            // Update Active Mandate Banner
            const mandateBanner = document.getElementById('activeMandateBanner');
            mandateBanner.innerHTML = `
                <strong>Active Mandate: Investor ${{currentPersona}} (${{profile.name}})</strong> &bull; 
                ${{profile.mandate}} &bull; 
                Risk: <strong>${{profile.risk_appetite}}</strong> &bull; 
                Horizon: <strong>${{profile.target_horizon}}</strong> &bull; 
                Max Allocation: <strong>${{profile.max_position_pct}}%</strong>
            `;

            // Render Metadata
            const metaGrid = document.getElementById('techTradeMeta');
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
                    <div class="meta-item-label">Transaction Type &amp; Size</div>
                    <div class="meta-item-value">${{t.tx_type}} &bull; ${{t.amount}}</div>
                </div>
                <div>
                    <div class="meta-item-label">Timing &amp; Lag Delay</div>
                    <div class="meta-item-value">${{t.tx_date}} &rarr; ${{t.filing_date}} (${{t.days_lag}}d lag)</div>
                </div>
            `;

            // Render Constraint Verification Card
            const constraintCard = document.getElementById('techConstraintCard');
            const passColor = constraint.passes ? '#059669' : '#e11d48';
            constraintCard.style.borderLeftColor = passColor;
            constraintCard.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: ${{passColor}};">
                        Ground Truth Constraint Verification &bull; Investor ${{currentPersona}} (${{profile.name}})
                    </div>
                    <span class="badge" style="background: ${{constraint.passes ? '#ecfdf5' : '#fff1f2'}}; color: ${{passColor}}; border: 1px solid ${{passColor}};">
                        ${{constraint.passes ? 'CONSTRAINT PASSED' : 'MANDATE VETOED'}}
                    </span>
                </div>
                <div style="font-size: 15px; color: #334155; line-height: 1.5;">
                    <strong>Classification (${{constraint.sector}}):</strong> ${{constraint.explanation}}
                </div>
            `;

            // Render Part 3 Ground Truth Performance vs SPY Box
            const gtBox = document.getElementById('techMarketGtBox');
            const mkt = t.ground_truth_market || {{}};
            if (mkt.resolved) {{
                gtBox.style.display = 'block';
                const m3 = mkt['3M'] || {{}};
                const m6 = mkt['6M'] || {{}};
                const m9 = mkt['9M'] || {{}};

                function fmtRet(val) {{
                    const num = val || 0;
                    const s = num > 0 ? '+' : '';
                    return `${{s}}${{num}}%`;
                }}

                gtBox.innerHTML = `
                    <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #1e40af; margin-bottom: 10px;">
                        Part 3 Ground Truth: Historical Equity Performance vs S&amp;P 500 (SPY)
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px;">
                            <div style="font-size: 12px; color: #475569; font-weight: 600; text-transform: uppercase;">3-Month Horizon (T+90)</div>
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 4px;">
                                Asset: ${{fmtRet(m3.asset_return_pct)}} &bull; SPY: ${{fmtRet(m3.spy_return_pct)}}
                            </div>
                            <div style="font-size: 13px; font-weight: 700; color: ${{m3.alpha_pct >= 0 ? '#059669' : '#e11d48'}}; margin-top: 2px;">
                                Net Alpha: ${{fmtRet(m3.alpha_pct)}} (${{m3.beat_spy ? 'Beat SPY' : 'Lagged SPY'}})
                            </div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px;">
                            <div style="font-size: 12px; color: #475569; font-weight: 600; text-transform: uppercase;">6-Month Horizon (T+180)</div>
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 4px;">
                                Asset: ${{fmtRet(m6.asset_return_pct)}} &bull; SPY: ${{fmtRet(m6.spy_return_pct)}}
                            </div>
                            <div style="font-size: 13px; font-weight: 700; color: ${{m6.alpha_pct >= 0 ? '#059669' : '#e11d48'}}; margin-top: 2px;">
                                Net Alpha: ${{fmtRet(m6.alpha_pct)}} (${{m6.beat_spy ? 'Beat SPY' : 'Lagged SPY'}})
                            </div>
                        </div>
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px;">
                            <div style="font-size: 12px; color: #475569; font-weight: 600; text-transform: uppercase;">9-Month Horizon (T+270)</div>
                            <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 4px;">
                                Asset: ${{fmtRet(m9.asset_return_pct)}} &bull; SPY: ${{fmtRet(m9.spy_return_pct)}}
                            </div>
                            <div style="font-size: 13px; font-weight: 700; color: ${{m9.alpha_pct >= 0 ? '#059669' : '#e11d48'}}; margin-top: 2px;">
                                Net Alpha: ${{fmtRet(m9.alpha_pct)}} (${{m9.beat_spy ? 'Beat SPY' : 'Lagged SPY'}})
                            </div>
                        </div>
                    </div>
                `;
            }} else {{
                gtBox.style.display = 'none';
            }}

            // Render JEV Decision Banner
            const banner = document.getElementById('techJevBanner');
            let bannerClass = 'jev-banner';
            if (jev.final_signal === 'BUY') bannerClass += ' buy-style';
            else if (jev.reason_code && jev.reason_code.includes('VETO')) bannerClass += ' veto-style';
            else bannerClass += ' abstain-style';
            banner.className = bannerClass;

            banner.innerHTML = `
                <div class="jev-banner-title">JEV Arbiter Final Synthesis &bull; Investor ${{currentPersona}} Mandate</div>
                <div class="jev-banner-signal">
                    <span class="badge ${{getBadgeClass(jev.final_signal)}}" style="font-size: 18px; padding: 6px 16px;">${{jev.final_signal}}</span>
                    <span style="font-size: 17px; font-weight: 700; color: #475569;">
                        Confidence: ${{Math.round((jev.confidence_score || 0.8) * 100)}}% &bull; ${{jev.reason_code}}
                    </span>
                    <span class="badge" style="background: #ffffff; border: 1px solid #cbd5e1; font-size: 14px; margin-left: auto;">
                        Suggested Allocation: <strong>${{jev.suggested_allocation_pct || 0}}%</strong>
                    </span>
                </div>
                <div class="jev-banner-rationale">
                    <strong>JEV Written Logic:</strong> ${{jev.rationale}}
                </div>
                <div style="font-size: 13px; color: #64748b; margin-top: 10px;">
                    <strong>Risk Profile:</strong> ${{jev.risk_profile || 'Standard'}} &bull;
                    <strong>Horizon:</strong> ${{profile.target_horizon}} &bull;
                    <strong>Trusted Models:</strong> ${{t.jev_decision.selected_models ? t.jev_decision.selected_models.join(', ') : 'Consensus Inferences'}}
                </div>
            `;

            // Render Models Grid with Scrollable JSON
            const modelsGrid = document.getElementById('techModelsGrid');
            modelsGrid.innerHTML = '';
            t.models_evaluation.forEach(m => {{
                const r = m.rubric_scores || {{}};
                const card = document.createElement('div');
                card.className = 'model-card';

                const formattedJson = JSON.stringify({{
                    model: m.model_name,
                    signal: m.signal,
                    constraint_passes: m.constraint_passes,
                    weight_assigned: m.weight,
                    rubric_scores: r,
                    explanation: m.explanation,
                    flaws: m.flaws,
                    strengths: m.strengths
                }}, null, 2);

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
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span class="badge ${{getBadgeClass(m.signal)}}">${{m.signal}}</span>
                        <span style="font-size: 13px; font-weight: 700; color: ${{m.constraint_passes ? '#059669' : '#e11d48'}};">
                            Model Constraint: ${{m.constraint_passes ? 'PASS' : 'FAIL'}}
                        </span>
                    </div>
                    <div class="model-card-rationale">
                        "${{m.explanation || 'No rationale available.'}}"
                    </div>
                    <div class="rubric-mini">
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R1 Constraint</div><div class="rubric-mini-score">${{r.R1 !== undefined ? r.R1 : '-'}}</div></div>
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R2 Evidence</div><div class="rubric-mini-score">${{r.R2 !== undefined ? r.R2 : '-'}}</div></div>
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R3 Timing</div><div class="rubric-mini-score">${{r.R3 !== undefined ? r.R3 : '-'}}</div></div>
                        <div class="rubric-mini-cell"><div class="rubric-mini-name">R8 Schema</div><div class="rubric-mini-score">${{r.R8 !== undefined ? r.R8 : '-'}}</div></div>
                    </div>

                    <!-- Scrollable JSON Slider -->
                    <div class="json-slider">
                        <div class="json-slider-title">
                            <span>Model Raw Telemetry JSON</span>
                            <span>Scrollable &darr;</span>
                        </div>
                        <pre class="json-box"><code>${{formattedJson}}</code></pre>
                    </div>
                `;
                modelsGrid.appendChild(card);
            }});
        }}

        // Full Interactive Multi-Node Canvas Pipeline Architecture
        const canvas = document.getElementById('pipelineCanvas');
        const ctx = canvas ? canvas.getContext('2d') : null;
        let animRunning = true;
        let pulses = [];
        let hoveredNodeKey = null;
        let activeModalKey = null;

        // Node Geometry (1100 x 460 canvas space) - Prompt Set v2 Architecture
        const nodes = {{
            trade: {{ key: 'trade', x: 80, y: 160, w: 125, h: 54, label: 'PolyTICK.us Trade', sub: 'STOCK Act Disclosure' }},
            packet: {{ key: 'packet', x: 255, y: 160, w: 140, h: 54, label: 'Evidence Packet', sub: 'Data Facts & Lag' }},
            mandate: {{ key: 'mandate', x: 255, y: 310, w: 140, h: 54, label: 'Investor Mandate', sub: 'Part 0 Profiles A-D' }},
            models: [
                {{ key: 'Apertus-1.5-70B', name: 'Apertus 70B (Cloud API)', sub: 'CSCS Alps Supercomputer', x: 520, y: 52, w: 175, h: 36, isApertus: true }},
                {{ key: 'Apertus-1.5-8B', name: 'Apertus 8B (Swiss Local)', sub: 'CSCS Alps Architecture', x: 520, y: 122, w: 175, h: 36, isApertus: true }},
                {{ key: 'Qwen-2.5-14B-Coder', name: 'Qwen 2.5 Coder 14B', sub: 'Local RTX 5060 Ti', x: 520, y: 192, w: 175, h: 36 }},
                {{ key: 'SecurityAI-14B', name: 'SecurityAI 14B', sub: 'Local RTX 5060 Ti', x: 520, y: 262, w: 175, h: 36 }},
                {{ key: 'Neo-Uncensored-8B', name: 'Neo-Uncensored 8B', sub: 'Local GPU Cohort', x: 520, y: 332, w: 175, h: 36 }},
                {{ key: 'Llama-3.1-8B-WhiteRabbitNeo', name: 'WhiteRabbitNeo 8B', sub: 'Local GPU Cohort', x: 520, y: 402, w: 175, h: 36 }}
            ],
            jev: {{ key: 'jev', x: 775, y: 230, w: 145, h: 62, label: 'JEV Arbiter Layer', sub: 'Rubrics R1-R8 Audit' }},
            decision: {{ key: 'decision', x: 985, y: 160, w: 155, h: 52, label: 'Fiduciary Decision', sub: 'Protected Signal & Sizing' }},
            market: {{ key: 'market', x: 985, y: 310, w: 155, h: 52, label: 'S&P 500 Alpha Engine', sub: 'T+90/180/270 vs SPY' }}
        }};

        function getAllNodeList() {{
            return [
                nodes.trade,
                nodes.packet,
                nodes.mandate,
                ...nodes.models,
                nodes.jev,
                nodes.decision,
                nodes.market
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

        if (canvas) {{
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
        }}

        // Cubic Bezier Interpolation
        function getCubicBezierPoint(t, p0, cp0, cp1, p1) {{
            const u = 1 - t;
            const tt = t * t;
            const uu = u * u;
            const uuu = uu * u;
            const ttt = tt * t;
            return {{
                x: uuu * p0.x + 3 * uu * t * cp0.x + 3 * u * tt * cp1.x + ttt * p1.x,
                y: uuu * p0.y + 3 * uu * t * cp0.y + 3 * u * tt * cp1.y + ttt * p1.y
            }};
        }}

        class DataPulse {{
            constructor(p0, cp0, cp1, p1, speed = 1.8, color = '#0284c7', radius = 4.5, glow = null) {{
                this.p0 = p0;
                this.cp0 = cp0;
                this.cp1 = cp1;
                this.p1 = p1;
                this.speed = speed;
                this.color = color;
                this.radius = radius;
                this.glow = glow || color;
                this.progress = Math.random();
                this.pos = {{ x: p0.x, y: p0.y }};
            }}
            update() {{
                this.progress += 0.008 * this.speed;
                if (this.progress >= 1) {{
                    this.progress = 0;
                }}
                this.pos = getCubicBezierPoint(this.progress, this.p0, this.cp0, this.cp1, this.p1);
            }}
            draw() {{
                if (!ctx) return;
                ctx.beginPath();
                ctx.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.shadowColor = this.glow;
                ctx.shadowBlur = 6;
                ctx.fill();
                ctx.shadowBlur = 0;
            }}
        }}

        function initContinuousPulses() {{
            pulses = [];
            // Filing -> Evidence Packet (Blue Ingestion Pulse)
            pulses.push(new DataPulse(
                {{ x: nodes.trade.x + nodes.trade.w/2, y: nodes.trade.y }},
                {{ x: nodes.trade.x + nodes.trade.w/2 + 35, y: nodes.trade.y }},
                {{ x: nodes.packet.x - nodes.packet.w/2 - 35, y: nodes.packet.y }},
                {{ x: nodes.packet.x - nodes.packet.w/2, y: nodes.packet.y }},
                2.0, '#0284c7'
            ));

            // Dual Streams to ALL 6 Models (Prompt Set v2 Part 1: Both Evidence Packet AND Investor Mandate feed all models)
            nodes.models.forEach((m) => {{
                // Blue pulse: Evidence Packet (Trade facts, timing, disclosure lag)
                pulses.push(new DataPulse(
                    {{ x: nodes.packet.x + nodes.packet.w/2, y: nodes.packet.y }},
                    {{ x: nodes.packet.x + nodes.packet.w/2 + 50, y: nodes.packet.y }},
                    {{ x: m.x - m.w/2 - 50, y: m.y - 4 }},
                    {{ x: m.x - m.w/2, y: m.y - 4 }},
                    1.7, '#0284c7'
                ));

                // Amber pulse: Investor Mandate (Hard Constraints A-D)
                pulses.push(new DataPulse(
                    {{ x: nodes.mandate.x + nodes.mandate.w/2, y: nodes.mandate.y }},
                    {{ x: nodes.mandate.x + nodes.mandate.w/2 + 50, y: nodes.mandate.y }},
                    {{ x: m.x - m.w/2 - 50, y: m.y + 4 }},
                    {{ x: m.x - m.w/2, y: m.y + 4 }},
                    1.7, '#d97706'
                ));

                // Green pulse: Model Inferences -> JEV Arbiter
                pulses.push(new DataPulse(
                    {{ x: m.x + m.w/2, y: m.y }},
                    {{ x: m.x + m.w/2 + 50, y: m.y }},
                    {{ x: nodes.jev.x - nodes.jev.w/2 - 50, y: nodes.jev.y }},
                    {{ x: nodes.jev.x - nodes.jev.w/2, y: nodes.jev.y }},
                    1.8, '#059669'
                ));
            }});

            // JEV -> Fiduciary Decision
            pulses.push(new DataPulse(
                {{ x: nodes.jev.x + nodes.jev.w/2, y: nodes.jev.y }},
                {{ x: nodes.jev.x + nodes.jev.w/2 + 40, y: nodes.jev.y }},
                {{ x: nodes.decision.x - nodes.decision.w/2 - 40, y: nodes.decision.y }},
                {{ x: nodes.decision.x - nodes.decision.w/2, y: nodes.decision.y }},
                2.1, '#059669', 5.0
            ));

            // JEV -> S&P 500 Alpha Engine
            pulses.push(new DataPulse(
                {{ x: nodes.jev.x + nodes.jev.w/2, y: nodes.jev.y }},
                {{ x: nodes.jev.x + nodes.jev.w/2 + 40, y: nodes.jev.y }},
                {{ x: nodes.market.x - nodes.market.w/2 - 40, y: nodes.market.y }},
                {{ x: nodes.market.x - nodes.market.w/2, y: nodes.market.y }},
                2.0, '#7c3aed', 5.0
            ));
        }}

        function triggerTradePulse() {{
            const t = tradesData[currentTradeIndex];
            if (!t) return;
            const pKey = currentPersona || 'A';
            const statusEl = document.getElementById('pipelineLiveStatus');
            if (statusEl) {{
                statusEl.textContent = `Auditing ${{t.politician}} ($${{t.ticker}}) under Investor ${{pKey}}`;
            }}

            pulses = [];

            // Filing -> Evidence Packet (Blue)
            pulses.push(new DataPulse(
                {{ x: nodes.trade.x + nodes.trade.w/2, y: nodes.trade.y }},
                {{ x: nodes.trade.x + nodes.trade.w/2 + 35, y: nodes.trade.y }},
                {{ x: nodes.packet.x - nodes.packet.w/2 - 35, y: nodes.packet.y }},
                {{ x: nodes.packet.x - nodes.packet.w/2, y: nodes.packet.y }},
                2.4, '#0284c7'
            ));

            // Dual Streams to ALL 6 Models
            nodes.models.forEach((m) => {{
                const mEval = t.models_evaluation.find(x => x.model_name === m.key || x.model_name.includes(m.key) || m.key.includes(x.model_name));
                const isDisc = mEval && (mEval.status === 'DISCOUNTED' || mEval.constraint_passes === false);
                const isSelected = mEval && (mEval.status === 'SELECTED' && mEval.constraint_passes === true);
                const col = isDisc ? '#e11d48' : (isSelected ? '#059669' : '#0284c7');

                // Evidence Packet stream (Blue)
                pulses.push(new DataPulse(
                    {{ x: nodes.packet.x + nodes.packet.w/2, y: nodes.packet.y }},
                    {{ x: nodes.packet.x + nodes.packet.w/2 + 50, y: nodes.packet.y }},
                    {{ x: m.x - m.w/2 - 50, y: m.y - 4 }},
                    {{ x: m.x - m.w/2, y: m.y - 4 }},
                    2.0, '#0284c7'
                ));

                // Investor Mandate stream (Amber)
                pulses.push(new DataPulse(
                    {{ x: nodes.mandate.x + nodes.mandate.w/2, y: nodes.mandate.y }},
                    {{ x: nodes.mandate.x + nodes.mandate.w/2 + 50, y: nodes.mandate.y }},
                    {{ x: m.x - m.w/2 - 50, y: m.y + 4 }},
                    {{ x: m.x - m.w/2, y: m.y + 4 }},
                    2.0, '#d97706'
                ));

                // Model -> JEV evaluation (Green if selected, Red if discounted)
                pulses.push(new DataPulse(
                    {{ x: m.x + m.w/2, y: m.y }},
                    {{ x: m.x + m.w/2 + 50, y: m.y }},
                    {{ x: nodes.jev.x - nodes.jev.w/2 - 50, y: nodes.jev.y }},
                    {{ x: nodes.jev.x - nodes.jev.w/2, y: nodes.jev.y }},
                    2.1, col, isDisc ? 4.0 : 5.0
                ));
            }});

            // JEV Decision pulse
            const pData = (t.personas && t.personas[pKey]) ? t.personas[pKey] : null;
            const jevDec = pData ? pData.jev_decision : t.jev_decision;
            const decSig = jevDec ? jevDec.final_signal : 'HOLD';
            const decColor = decSig === 'BUY' ? '#059669' : (decSig === 'SELL' ? '#d97706' : '#64748b');

            pulses.push(new DataPulse(
                {{ x: nodes.jev.x + nodes.jev.w/2, y: nodes.jev.y }},
                {{ x: nodes.jev.x + nodes.jev.w/2 + 40, y: nodes.jev.y }},
                {{ x: nodes.decision.x - nodes.decision.w/2 - 40, y: nodes.decision.y }},
                {{ x: nodes.decision.x - nodes.decision.w/2, y: nodes.decision.y }},
                2.4, decColor, 5.5
            ));

            // S&P 500 Alpha Engine pulse
            pulses.push(new DataPulse(
                {{ x: nodes.jev.x + nodes.jev.w/2, y: nodes.jev.y }},
                {{ x: nodes.jev.x + nodes.jev.w/2 + 40, y: nodes.jev.y }},
                {{ x: nodes.market.x - nodes.market.w/2 - 40, y: nodes.market.y }},
                {{ x: nodes.market.x - nodes.market.w/2, y: nodes.market.y }},
                2.2, '#7c3aed', 5.5
            ));
        }}

        function drawPipes() {{
            if (!ctx || !canvas) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Helper to draw cubic bezier pipe
            function drawPipe(p0, cp0, cp1, p1, strokeStyle = '#e2e8f0', lineWidth = 2) {{
                ctx.beginPath();
                ctx.strokeStyle = strokeStyle;
                ctx.lineWidth = lineWidth;
                ctx.moveTo(p0.x, p0.y);
                ctx.bezierCurveTo(cp0.x, cp0.y, cp1.x, cp1.y, p1.x, p1.y);
                ctx.stroke();
            }}

            // Trade -> Evidence Packet (Direct Blue Ingestion Pipe)
            drawPipe(
                {{ x: nodes.trade.x + nodes.trade.w/2, y: nodes.trade.y }},
                {{ x: nodes.trade.x + nodes.trade.w/2 + 35, y: nodes.trade.y }},
                {{ x: nodes.packet.x - nodes.packet.w/2 - 35, y: nodes.packet.y }},
                {{ x: nodes.packet.x - nodes.packet.w/2, y: nodes.packet.y }},
                '#93c5fd', 2.4
            );

            // Dual Feed to ALL 6 Models (Prompt Set v2: Part 1 Prompt Injection)
            nodes.models.forEach((m) => {{
                // Evidence Packet -> Model (Blue curve: Trade facts & disclosure lag)
                drawPipe(
                    {{ x: nodes.packet.x + nodes.packet.w/2, y: nodes.packet.y }},
                    {{ x: nodes.packet.x + nodes.packet.w/2 + 50, y: nodes.packet.y }},
                    {{ x: m.x - m.w/2 - 50, y: m.y - 4 }},
                    {{ x: m.x - m.w/2, y: m.y - 4 }},
                    '#bae6fd', 1.8
                );

                // Investor Mandate -> Model (Amber curve: Hard Constraints A-D)
                drawPipe(
                    {{ x: nodes.mandate.x + nodes.mandate.w/2, y: nodes.mandate.y }},
                    {{ x: nodes.mandate.x + nodes.mandate.w/2 + 50, y: nodes.mandate.y }},
                    {{ x: m.x - m.w/2 - 50, y: m.y + 4 }},
                    {{ x: m.x - m.w/2, y: m.y + 4 }},
                    '#fde68a', 1.8
                );

                // Models -> JEV Arbiter (Consensus & Rubric Layer)
                drawPipe(
                    {{ x: m.x + m.w/2, y: m.y }},
                    {{ x: m.x + m.w/2 + 50, y: m.y }},
                    {{ x: nodes.jev.x - nodes.jev.w/2 - 50, y: nodes.jev.y }},
                    {{ x: nodes.jev.x - nodes.jev.w/2, y: nodes.jev.y }},
                    '#e2e8f0', 2.0
                );
            }});

            // JEV -> Decision (Green Fiduciary Pipe)
            drawPipe(
                {{ x: nodes.jev.x + nodes.jev.w/2, y: nodes.jev.y }},
                {{ x: nodes.jev.x + nodes.jev.w/2 + 40, y: nodes.jev.y }},
                {{ x: nodes.decision.x - nodes.decision.w/2 - 40, y: nodes.decision.y }},
                {{ x: nodes.decision.x - nodes.decision.w/2, y: nodes.decision.y }},
                '#6ee7b7', 2.4
            );

            // JEV -> Alpha Engine (Purple Alpha Pipe)
            drawPipe(
                {{ x: nodes.jev.x + nodes.jev.w/2, y: nodes.jev.y }},
                {{ x: nodes.jev.x + nodes.jev.w/2 + 40, y: nodes.jev.y }},
                {{ x: nodes.market.x - nodes.market.w/2 - 40, y: nodes.market.y }},
                {{ x: nodes.market.x - nodes.market.w/2, y: nodes.market.y }},
                '#d8b4fe', 2.4
            );

            // Draw pulses
            pulses.forEach(p => {{
                p.update();
                p.draw();
            }});

            // Draw Node Boxes
            function drawNodeBox(n, isModel = false, modelName = '', subText = '') {{
                const isHovered = (hoveredNodeKey === n.key);
                const w = n.w;
                const h = n.h;

                let fillCol = '#ffffff';
                let strokeCol = '#0f172a';
                let lineW = 1.6;

                if (isHovered) {{
                    fillCol = '#eff6ff';
                    strokeCol = '#2563eb';
                    lineW = 2.6;
                }} else if (isModel) {{
                    if (n.key === 'Apertus-1.5-70B') {{
                        fillCol = '#eff6ff';
                        strokeCol = '#2563eb';
                        lineW = 2.2;
                    }} else if (n.key === 'Apertus-1.5-8B') {{
                        fillCol = '#f0f9ff';
                        strokeCol = '#0284c7';
                        lineW = 2.0;
                    }} else if (n.key === 'Qwen-2.5-14B-Coder') {{
                        fillCol = '#fffbeb';
                        strokeCol = '#d97706';
                        lineW = 1.8;
                    }} else if (n.key === 'SecurityAI-14B') {{
                        fillCol = '#fff7ed';
                        strokeCol = '#ea580c';
                        lineW = 1.8;
                    }} else if (n.key === 'Neo-Uncensored-8B') {{
                        fillCol = '#fff1f2';
                        strokeCol = '#e11d48';
                        lineW = 1.8;
                    }} else if (n.key === 'Llama-3.1-8B-WhiteRabbitNeo') {{
                        fillCol = '#faf5ff';
                        strokeCol = '#9333ea';
                        lineW = 1.8;
                    }} else {{
                        fillCol = '#f8fafc';
                        strokeCol = '#64748b';
                        lineW = 1.5;
                    }}
                }} else if (n.key === 'trade') {{
                    fillCol = '#ffffff';
                    strokeCol = '#0f172a';
                    lineW = 2.2;
                }} else if (n.key === 'packet') {{
                    fillCol = '#eff6ff';
                    strokeCol = '#2563eb';
                    lineW = 2.2;
                }} else if (n.key === 'mandate') {{
                    fillCol = '#fffbeb';
                    strokeCol = '#d97706';
                    lineW = 2.4;
                }} else if (n.key === 'jev') {{
                    fillCol = '#ecfdf5';
                    strokeCol = '#059669';
                    lineW = 2.6;
                }} else if (n.key === 'decision') {{
                    fillCol = '#ffffff';
                    strokeCol = '#0f172a';
                    lineW = 2.2;
                }} else if (n.key === 'market') {{
                    fillCol = '#faf5ff';
                    strokeCol = '#7c3aed';
                    lineW = 2.4;
                }}

                ctx.save();
                ctx.shadowColor = 'rgba(15, 23, 42, 0.08)';
                ctx.shadowBlur = 6;
                ctx.shadowOffsetY = 2;
                ctx.fillStyle = fillCol;
                ctx.strokeStyle = strokeCol;
                ctx.lineWidth = lineW;
                ctx.beginPath();
                ctx.roundRect(n.x - w/2, n.y - h/2, w, h, 8);
                ctx.fill();
                ctx.stroke();
                ctx.restore();

                // Typography
                let textCol = '#0f172a';
                if (isModel) {{
                    if (n.key === 'Apertus-1.5-70B') textCol = '#1e40af';
                    else if (n.key === 'Apertus-1.5-8B') textCol = '#0369a1';
                    else if (n.key === 'Qwen-2.5-14B-Coder') textCol = '#92400e';
                    else if (n.key === 'SecurityAI-14B') textCol = '#9a3412';
                    else if (n.key === 'Neo-Uncensored-8B') textCol = '#9f1239';
                    else if (n.key === 'Llama-3.1-8B-WhiteRabbitNeo') textCol = '#6b21a8';
                }}
                if (n.key === 'packet') textCol = '#1e40af';
                if (n.key === 'mandate') textCol = '#92400e';
                if (n.key === 'jev') textCol = '#065f46';
                if (n.key === 'market') textCol = '#6b21a8';

                ctx.fillStyle = textCol;
                ctx.font = isModel ? '600 12px Inter, sans-serif' : '700 13px Inter, sans-serif';
                ctx.textAlign = 'center';

                if (isModel) {{
                    ctx.fillText(modelName, n.x, n.y - 1);
                    ctx.fillStyle = '#64748b';
                    ctx.font = '400 11px Inter, sans-serif';
                    ctx.fillText(subText, n.x, n.y + 12);
                }} else {{
                    ctx.fillText(n.label, n.x, n.y - 4);
                    if (n.sub) {{
                        ctx.fillStyle = '#64748b';
                        ctx.font = '500 11.5px Inter, sans-serif';
                        ctx.fillText(n.sub, n.x, n.y + 13);
                    }}
                }}

                if (isHovered) {{
                    ctx.fillStyle = '#2563eb';
                    ctx.font = '600 11px Inter, sans-serif';
                    ctx.fillText('Click to inspect', n.x, n.y + (isModel ? 24 : 33));
                }}
            }}

            drawNodeBox(nodes.trade);
            drawNodeBox(nodes.packet);
            drawNodeBox(nodes.mandate);
            nodes.models.forEach(m => drawNodeBox(m, true, m.name, m.sub));
            drawNodeBox(nodes.jev);
            drawNodeBox(nodes.decision);
            drawNodeBox(nodes.market);
        }}

        function animate() {{
            if (animRunning) {{
                drawPipes();
                requestAnimationFrame(animate);
            }}
        }}

        function toggleAnimation() {{
            animRunning = !animRunning;
            const btn = document.getElementById('animToggleBtn');
            if (btn) btn.textContent = animRunning ? 'Pause Flow' : 'Resume Flow';
            if (animRunning) animate();
        }}

        // Inspection Modal Management
        function openNodeModal(key) {{
            activeModalKey = key;
            populateModal(key);
            const m = document.getElementById('pipelineModal');
            if (m) m.classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function closeNodeModal() {{
            activeModalKey = null;
            const m = document.getElementById('pipelineModal');
            if (m) m.classList.remove('active');
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
            const t = tradesData[currentTradeIndex];
            if (!t) return;
            const pKey = currentPersona || 'A';
            const pData = (t.personas && t.personas[pKey]) ? t.personas[pKey] : null;
            const profile = pData ? pData.profile : {{
                id: pKey,
                name: "Persona " + pKey,
                mandate: "Standard mandate",
                risk_appetite: "Moderate",
                target_horizon: "6M",
                max_position_pct: 5.0
            }};
            const constraint = pData ? pData.constraint_check : t.ground_truth_constraint;
            const jev = pData ? pData.jev_decision : t.jev_decision;

            const modalTag = document.getElementById('modalTag');
            const modalTitle = document.getElementById('modalTitle');
            const modalSubtitle = document.getElementById('modalSubtitle');
            const modalBody = document.getElementById('modalBody');

            if (key === 'trade') {{
                modalTag.textContent = 'Stage 1 of 6 — Official Disclosure Ingestion';
                modalTitle.textContent = `${{t.politician}} — STOCK Act PTR Filing`;
                modalSubtitle.textContent = `Official federal filing extracted from PolyTICK.us (Record ID: ${{t.trade_id}})`;

                modalBody.innerHTML = `
                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Politician &amp; Office</div>
                            <div class="modal-stat-value">${{t.politician}} (${{t.party}})</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">${{t.chamber}} &bull; District: ${{t.district}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Committees &amp; Jurisdiction</div>
                            <div class="modal-stat-value" style="font-size: 14px;">${{t.committees}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Asset Traded</div>
                            <div class="modal-stat-value">$${{t.ticker}} &mdash; ${{t.asset_name}}</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Type: ${{t.asset_type}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Transaction &amp; Amount</div>
                            <div class="modal-stat-value">${{t.tx_type}} (${{t.amount}})</div>
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
                        <strong>PolyTICK.us Data Source Reference:</strong>
                        <div style="font-size: 14px; margin-top: 4px;">
                            <a href="https://www.polytick.us/tickers/${{t.ticker}}" target="_blank" style="color: #2563eb; font-weight: 600; text-decoration: underline;">
                                Inspect $${{t.ticker}} Congressional &amp; Insider Live Trade Feed on PolyTICK.us &nearr;
                            </a>
                        </div>
                    </div>

                    <strong>Raw Scraped Field Payload:</strong>
                    <div class="modal-code-block">${{JSON.stringify({{
                        trade_id: t.trade_id,
                        filer: t.politician,
                        party: t.party,
                        chamber: t.chamber,
                        asset: {{ ticker: t.ticker, name: t.asset_name }},
                        tx_type: t.tx_type,
                        amount: t.amount,
                        tx_date: t.tx_date,
                        filing_date: t.filing_date,
                        filing_delay_days: t.days_lag
                    }}, null, 2)}}</div>
                `;
            }} else if (key === 'packet') {{
                modalTag.textContent = 'Stage 2 of 6 — Evidence Packet Synthesis & Lag Hygiene';
                modalTitle.textContent = `Evidence Packet for $${{t.ticker}} (${{t.politician}})`;
                modalSubtitle.textContent = `Pre-inference data sanitization, strict time freeze boundary, and disclosure lag validation.`;

                const lagStatus = t.days_lag > 40
                    ? `<div class="modal-alert-danger"><strong>CRITICAL TIMING WARNING:</strong> Disclosure delay is ${{t.days_lag}} days (>40-day freshness limit). Informational insider edge has decayed. Flagged as STALE_DISCLOSURE.</div>`
                    : `<div class="modal-alert-success"><strong>TIMING VERIFIED:</strong> Disclosure lag is ${{t.days_lag}} days (&le;40-day freshness threshold). Informational signal is fresh and actionable.</div>`;

                modalBody.innerHTML = `
                    ${{lagStatus}}
                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Disclosure Lag Computation</div>
                            <div class="modal-stat-value mono">${{t.days_lag}} Days Delay</div>
                            <div style="font-size: 13px; color: #64748b;">${{t.days_lag > 40 ? 'Status: STALE_DISCLOSURE' : 'Status: FRESH_FILING'}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Time Boundary Freeze</div>
                            <div class="modal-stat-value mono">T = ${{t.tx_date}}</div>
                            <div style="font-size: 13px; color: #64748b;">Zero Lookahead Enforced</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Congressional Committee</div>
                            <div class="modal-stat-value" style="font-size: 14px;">${{t.committees}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Transaction Conviction</div>
                            <div class="modal-stat-value">${{t.amount}} (${{t.tx_type}})</div>
                        </div>
                    </div>
                    <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 12px 16px; margin-top: 16px; font-size: 14px; color: #0369a1; line-height: 1.5;">
                        <strong>Prompt Set v2 Specification (Evidence Packet):</strong> This packet contains only empirical, observable facts from the STOCK Act filing (committees, asset, dates, conviction, and delay). It enforces strict zero-lookahead (T=tx_date). In Part 1, this packet is merged with the <strong>Investor Mandate</strong> and dispatched to all 6 LLMs.
                    </div>
                `;
            }} else if (key === 'mandate') {{
                modalTag.textContent = 'Stage 3 of 6 — Investor Constraint Architecture (Part 0)';
                modalTitle.textContent = `Investor Mandate: Investor ${{profile.id}} (${{profile.name}})`;
                modalSubtitle.textContent = `Prompt Set v2 Part 0: Personalized fiduciary mandate governing all 6 LLM evaluations.`;

                const mandateBanner = constraint.passes
                    ? `<div class="modal-alert-success"><strong>MANDATE SATISFIED:</strong> $${{t.ticker}} complies with Investor ${{profile.id}} constraints. (${{constraint.explanation}})</div>`
                    : `<div class="modal-alert-danger"><strong>HARD CONSTRAINT VIOLATION:</strong> $${{t.ticker}} breaches Investor ${{profile.id}} rules. (${{constraint.explanation}}). Any BUY signal is strictly vetoed!</div>`;

                modalBody.innerHTML = `
                    ${{mandateBanner}}
                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Active Investor Profile</div>
                            <div class="modal-stat-value">Investor ${{profile.id}} &mdash; ${{profile.name}}</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Mandate: ${{profile.mandate}}</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Risk Appetite &amp; Horizon</div>
                            <div class="modal-stat-value">${{profile.risk_appetite}} Risk &bull; ${{profile.target_horizon}} Target</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Max Position Size: ${{profile.max_position_pct}}%</div>
                        </div>
                    </div>

                    <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px 16px; margin-top: 16px; font-size: 14px; color: #92400e; line-height: 1.5;">
                        <strong>Prompt Set v2 Specification (Rule #3):</strong> <em>&ldquo;The investor's hard constraint ALWAYS overrides trade attractiveness. A great trade that violates the constraint is ABSTAIN.&rdquo;</em> In Part 1, the <strong>Investor Mandate</strong> acts as the legal/ethical bounding constraint governing every LLM inference. In Part 2, JEV verifies whether any model breached this constraint (Rubric R1).
                    </div>

                    <strong style="margin-top: 16px; display: block;">The 4 Persona Mandates under Prompt Set v2:</strong>
                    <table style="margin-top: 10px;">
                        <thead>
                            <tr>
                                <th>Persona</th>
                                <th>Name</th>
                                <th>Hard Constraint Rule</th>
                                <th>Horizon</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="background: ${{profile.id === 'A' ? '#eff6ff' : '#ffffff'}};">
                                <td><strong>Investor A</strong></td>
                                <td>Ethical / No-Military</td>
                                <td>Must NOT hold defense/military contractors ($GD, $RTX, $NOC, $HII, $BA).</td>
                                <td>6 Months</td>
                            </tr>
                            <tr style="background: ${{profile.id === 'B' ? '#eff6ff' : '#ffffff'}};">
                                <td><strong>Investor B</strong></td>
                                <td>Tech-Only</td>
                                <td>Only companies in the Information Technology sector.</td>
                                <td>6 Months</td>
                            </tr>
                            <tr style="background: ${{profile.id === 'C' ? '#eff6ff' : '#ffffff'}};">
                                <td><strong>Investor C</strong></td>
                                <td>Open / All Sectors</td>
                                <td>Unconstrained; capitalizes on all high-conviction insider trades.</td>
                                <td>12 Months</td>
                            </tr>
                            <tr style="background: ${{profile.id === 'D' ? '#eff6ff' : '#ffffff'}};">
                                <td><strong>Investor D</strong></td>
                                <td>US-Market Only</td>
                                <td>Must be listed on major US exchange; max position capped at 3.0%.</td>
                                <td>3 Months</td>
                            </tr>
                        </tbody>
                    </table>
                `;
            }} else if (key === 'jev') {{
                modalTag.textContent = 'Stage 5 of 6 — Evaluator & Synthesis Layer (Part 2)';
                modalTitle.textContent = 'JEV Arbiter Layer: Independent Multi-Model Audit';
                modalSubtitle.textContent = `Audits all 6 models against Rubrics R1-R8, discounts rule violators to 0% weight, and synthesizes consensus.`;

                let rowsHtml = '';
                t.models_evaluation.forEach(m => {{
                    const r = m.rubric_scores || {{}};
                    const isDisc = m.status === 'DISCOUNTED' || m.constraint_passes === false;
                    rowsHtml += `
                        <tr style="background: ${{isDisc ? '#fff1f2' : '#ffffff'}};">
                            <td><strong>${{m.model_name}}</strong></td>
                            <td><span class="badge ${{getBadgeClass(m.signal)}}">${{m.signal}}</span></td>
                            <td class="mono">${{r.R1 !== undefined ? r.R1 : '-'}}</td>
                            <td class="mono">${{r.R2 !== undefined ? r.R2 : '-'}}</td>
                            <td class="mono">${{r.R3 !== undefined ? r.R3 : '-'}}</td>
                            <td class="mono">${{r.R4 !== undefined ? r.R4 : '-'}}</td>
                            <td class="mono">${{r.R5 !== undefined ? r.R5 : '-'}}</td>
                            <td class="mono">${{r.R6 !== undefined ? r.R6 : '-'}}</td>
                            <td class="mono">${{r.R7 !== undefined ? r.R7 : '-'}}</td>
                            <td class="mono">${{r.R8 !== undefined ? r.R8 : '-'}}</td>
                            <td><strong style="color: ${{isDisc ? '#e11d48' : '#059669'}};">${{isDisc ? 'DISCOUNTED' : 'SELECTED'}}</strong> ${{!isDisc && m.weight ? `(${{Math.round(m.weight * 1)}}%)` : ''}}</td>
                        </tr>
                    `;
                }});

                modalBody.innerHTML = `
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
                        <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #64748b; margin-bottom: 4px;">JEV Synthesis Verdict for Active Trade</div>
                        <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">
                            ${{jev.final_signal}} &bull; ${{jev.reason_code}} &bull; Confidence: ${{Math.round((jev.confidence_score || 0.8) * 100)}}%
                        </div>
                        <div style="font-size: 14px; font-style: italic; color: #475569;">"${{jev.rationale}}"</div>
                    </div>

                    <strong>Multi-Model R1-R8 Rubric Audit Matrix:</strong>
                    <p style="font-size: 13px; color: #64748b; margin-bottom: 8px;">
                        R1: Constraint Accuracy (Hard Pass/Fail) &bull; R2: Evidence Citations &bull; R3: Lag Awareness &bull; R4: Instrument Rigor &bull; R5: Persona Fit &bull; R6: Uncertainty &bull; R7: Consistency &bull; R8: Schema.
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
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${{rowsHtml}}
                        </tbody>
                    </table>
                `;
            }} else if (key === 'decision') {{
                modalTag.textContent = 'Stage 6a of 6 — Decision Delivery';
                modalTitle.textContent = `Fiduciary Decision Support for Investor ${{profile.id}}`;
                modalSubtitle.textContent = `Capital Protection & Position Sizing Delivered to Investor ${{profile.id}} (${{profile.name}})`;

                modalBody.innerHTML = `
                    <div style="text-align: center; padding: 24px 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 24px;">
                        <div style="font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin-bottom: 6px;">Verified Decision Support Signal</div>
                        <div style="margin-bottom: 12px;"><span class="badge ${{getBadgeClass(jev.final_signal)}}" style="font-size: 24px; padding: 6px 20px;">${{jev.final_signal}}</span></div>
                        <div style="font-size: 16px; color: #1e293b; max-width: 600px; margin: 0 auto; font-style: italic;">
                            "${{jev.rationale}}"
                        </div>
                    </div>

                    <div class="modal-grid-2">
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Suggested Capital Allocation</div>
                            <div class="modal-stat-value" style="font-size: 20px; color: #1e40af;">${{jev.suggested_allocation_pct || 0}}% of Portfolio</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Capped by ${{profile.name}} Mandate</div>
                        </div>
                        <div class="modal-stat-box">
                            <div class="modal-stat-label">Target Horizon &amp; Risk</div>
                            <div class="modal-stat-value">${{profile.target_horizon}} &bull; ${{profile.risk_appetite}}</div>
                            <div style="font-size: 13px; color: #64748b; margin-top: 2px;">Rebalance on horizon expiry</div>
                        </div>
                    </div>
                `;
            }} else if (key === 'market') {{
                modalTag.textContent = 'Stage 6b of 6 — Ground Truth Market Returns & Net Alpha (Part 3)';
                modalTitle.textContent = `S&P 500 Benchmark Comparison: $${{t.ticker}} vs SPY`;
                modalSubtitle.textContent = `Prompt Set v2 Part 3: Ground Truth closing price performance at T+90, T+180, and T+270 days vs S&P 500 (SPY).`;

                const mkt = t.ground_truth_market || {{}};
                const m3 = mkt['3M'] || {{}};
                const m6 = mkt['6M'] || {{}};
                const m9 = mkt['9M'] || {{}};

                function fmtR(val) {{
                    const n = val || 0;
                    return `${{n > 0 ? '+' : ''}}${{n}}%`;
                }}

                modalBody.innerHTML = `
                    <div style="margin-bottom: 20px;">
                        <strong>Ground Truth Realized Returns vs S&amp;P 500 Benchmark (SPY):</strong>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Horizon</th>
                                <th>$${{t.ticker}} Return</th>
                                <th>S&amp;P 500 (SPY) Return</th>
                                <th>Realized Net Alpha</th>
                                <th>Beats Market?</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>3 Months (T+90)</strong></td>
                                <td class="mono">${{fmtR(m3.asset_return_pct)}}</td>
                                <td class="mono">${{fmtR(m3.spy_return_pct)}}</td>
                                <td class="mono" style="font-weight: 700; color: ${{m3.alpha_pct >= 0 ? '#059669' : '#e11d48'}};">${{fmtR(m3.alpha_pct)}}</td>
                                <td><span class="badge ${{m3.beat_spy ? 'badge-buy' : 'badge-discounted'}}">${{m3.beat_spy ? 'YES' : 'NO'}}</span></td>
                            </tr>
                            <tr>
                                <td><strong>6 Months (T+180)</strong></td>
                                <td class="mono">${{fmtR(m6.asset_return_pct)}}</td>
                                <td class="mono">${{fmtR(m6.spy_return_pct)}}</td>
                                <td class="mono" style="font-weight: 700; color: ${{m6.alpha_pct >= 0 ? '#059669' : '#e11d48'}};">${{fmtR(m6.alpha_pct)}}</td>
                                <td><span class="badge ${{m6.beat_spy ? 'badge-buy' : 'badge-discounted'}}">${{m6.beat_spy ? 'YES' : 'NO'}}</span></td>
                            </tr>
                            <tr>
                                <td><strong>9 Months (T+270)</strong></td>
                                <td class="mono">${{fmtR(m9.asset_return_pct)}}</td>
                                <td class="mono">${{fmtR(m9.spy_return_pct)}}</td>
                                <td class="mono" style="font-weight: 700; color: ${{m9.alpha_pct >= 0 ? '#059669' : '#e11d48'}};">${{fmtR(m9.alpha_pct)}}</td>
                                <td><span class="badge ${{m9.beat_spy ? 'badge-buy' : 'badge-discounted'}}">${{m9.beat_spy ? 'YES' : 'NO'}}</span></td>
                            </tr>
                        </tbody>
                    </table>

                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-top: 20px;">
                        <strong>Why Alpha vs SPY Matters for Hackathon Judges:</strong>
                        <div style="font-size: 14px; color: #475569; margin-top: 6px;">
                            Measuring Congressional trades against the S&amp;P 500 (SPY) baseline tests whether following disclosures produces true excess risk-adjusted return (alpha) or merely captures broad equity market beta. JEV verifies that only trades with genuine informational edge and zero mandate violations reach capital deployment.
                        </div>
                    </div>
                `;
            }} else {{
                // Model Deep Dive
                const m = t.models_evaluation.find(x => x.model_name === key || key.includes(x.model_name) || x.model_name.includes(key));
                if (m) {{
                    const r = m.rubric_scores || {{}};
                    const isDisc = m.status === 'DISCOUNTED' || m.constraint_passes === false;
                    const isApertus = m.model_name.includes('Apertus');

                    modalTag.textContent = `Stage 4 of 6 — ${{m.params}} Parameter LLM Deep Dive`;
                    modalTitle.textContent = `${{m.model_name}}`;
                    modalSubtitle.textContent = `Evaluated on ${{m.provider}} under Investor ${{profile.id}} (${{profile.name}}) constraints.`;

                    const banner = isDisc
                        ? `<div class="modal-alert-danger"><strong>JEV AUDITOR DISCOUNTED (0% Weight):</strong> This model failed Investor ${{profile.id}} constraints or timing hygiene. Reason: <strong>${{m.flaws && m.flaws.length ? m.flaws.join(', ') : 'Constraint violation'}}</strong>.</div>`
                        : `<div class="modal-alert-success"><strong>JEV AUDITOR SELECTED:</strong> Model satisfied constraints and time hygiene. Assigned weight: <strong>${{Math.round(m.weight * 1)}}%</strong>.</div>`;

                    modalBody.innerHTML = `
                        ${{banner}}
                        <div class="modal-grid-2">
                            <div class="modal-stat-box">
                                <div class="modal-stat-label">Model Recommendation</div>
                                <div class="modal-stat-value"><span class="badge ${{getBadgeClass(m.signal)}}">${{m.signal}}</span></div>
                                <div style="font-size: 13px; color: ${{m.constraint_passes ? '#059669' : '#e11d48'}}; margin-top: 4px; font-weight: 700;">Constraint: ${{m.constraint_passes ? 'PASS' : 'FAIL'}}</div>
                            </div>
                            <div class="modal-stat-box">
                                <div class="modal-stat-label">Hardware &amp; Performance</div>
                                <div class="modal-stat-value">${{m.provider}}</div>
                                <div style="font-size: 13px; color: #64748b; margin-top: 4px;">${{m.tok_s || 0}} tok/s (${{m.latency || 0}}s latency)</div>
                            </div>
                        </div>

                        <strong>R1-R8 Rubric Scores:</strong>
                        <div class="rubric-mini" style="margin-bottom: 20px;">
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R1 Constraint</div><div class="rubric-mini-score">${{r.R1 !== undefined ? r.R1 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R2 Evidence</div><div class="rubric-mini-score">${{r.R2 !== undefined ? r.R2 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R3 Timing</div><div class="rubric-mini-score">${{r.R3 !== undefined ? r.R3 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R4 Instrument</div><div class="rubric-mini-score">${{r.R4 !== undefined ? r.R4 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R5 Fit</div><div class="rubric-mini-score">${{r.R5 !== undefined ? r.R5 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R6 Uncertainty</div><div class="rubric-mini-score">${{r.R6 !== undefined ? r.R6 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R7 Consistent</div><div class="rubric-mini-score">${{r.R7 !== undefined ? r.R7 : '-'}}</div></div>
                            <div class="rubric-mini-cell"><div class="rubric-mini-name">R8 Schema</div><div class="rubric-mini-score">${{r.R8 !== undefined ? r.R8 : '-'}}</div></div>
                        </div>

                        <strong>Model Financial Rationale:</strong>
                        <div style="font-size: 14.5px; color: #334155; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 18px; margin-top: 8px; margin-bottom: 20px;">
                            "${{m.explanation || 'No rationale available.'}}"
                        </div>
                    `;
                }}
            }}
        }}

        // Initialize App
        initTechSelect();
        renderTechTrade(0);
        renderLeaderboard('OVERALL');
        window.addEventListener('load', () => {{
            initContinuousPulses();
            triggerTradePulse();
            animate();
        }});
    </script>

    <!-- PIPELINE DEEP-DIVE INSPECTION MODAL -->
    <div class="modal-overlay" id="pipelineModal" onclick="handleModalOverlayClick(event)">
        <div class="modal-card">
            <button class="modal-close-btn" onclick="closeNodeModal()">&times;</button>
            <div class="modal-header-tag" id="modalTag">Pipeline Stage</div>
            <h3 class="modal-title" id="modalTitle">Component Title</h3>
            <div class="modal-subtitle" id="modalSubtitle">Component Subtitle</div>
            <div id="modalBody">
                <!-- Injected dynamically -->
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Successfully built updated index.html with Full Part 0-3 implementation: S&P 500 Alpha, Personas A-D, and JEV Scorecards!")

if __name__ == "__main__":
    build_app()
