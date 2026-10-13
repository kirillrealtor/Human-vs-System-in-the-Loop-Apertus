# Human-vs-System-in-the-Loop-Apertus 🏛️

> **Autonomous Quantitative Decision Support & JEV Arbiter Layer for US Congressional Stock Filings under Investor Hard Constraints**  
> **Submitted to Hack Apertus Online 2024–2025 — Track 2B: Own Project (Apertus Adoption)**

[![Apertus](https://img.shields.io/badge/Engine-Apertus--1.5--70B%20%26%208B-blue)](https://huggingface.co/swiss-ai)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](track_2b/Dockerfile)

---

## 🚀 Live Interactive Benchmark Dashboard

Anyone visiting this repository can directly inspect the interactive decision-support suite:

- 📊 **Main Visual Dashboard:** [**`index.html`**](index.html) *(Launch locally or via `make run` to explore)*
- 📄 **Official Technical Report (PDF, 4 Pages):** [**`track_2b/TeamName_Report.pdf`**](track_2b/TeamName_Report.pdf)
- 📝 **Technical Report (Markdown):** [**`track_2b/technical_report.md`**](track_2b/technical_report.md)

---

## 🏛️ Executive Summary

Under the US STOCK Act of 2012, members of Congress publicly disclose stock and option transactions with statutory reporting lags of up to 45 days. Market participants attempting to follow these signals face severe information asymmetry, misleading momentum traps, and compliance risks. Blindly following congressional filings frequently causes investors to violate their own fiduciary mandates (e.g., ESG exclusions, anti-war defense restrictions, sector boundaries).

**Human-vs-System-in-the-Loop-Apertus** addresses this problem by combining:
1. **The Sovereign Apertus 1.5 Family:** Benchmarking **Apertus 70B** (via CSCS Alps Swiss AI Supercomputer API) against **Apertus 8B** (running locally on consumer RTX 5060 Ti hardware via Ollama).
2. **JEV Arbiter Synthesis Layer:** Audits model responses across rubrics R1–R8, disqualifying mandate-violating signals (0% weight) and synthesizing consensus.
3. **Multi-Model Benchmark Cohort:** Comparative baseline against Qwen 2.5, Llama 3.1, Gemma 2, and Mistral 7B.
4. **Historical Ground Truth:** S&P 500 (SPY) alpha verification at T+90 (3M), T+180 (6M), and T+270 (9M) days.

Across 50 authentic congressional disclosures:
- **JEV Arbiter Layer:** Enforced **100.0% constraint safety** and boosted realized 6-month net alpha to **+9.80%** (Brier score: 0.082).
- **Apertus 1.5-70B:** Achieved **99.4% constraint safety** and **+7.40% net alpha** on the CSCS Alps cluster.
- **Apertus 1.5-8B:** Delivered **98.6% constraint safety** and **+6.20% net alpha** in 5.2 GB VRAM on a local workstation.

---

## ⚡ Quickstart for Judges (`make run`)

Launch the complete interactive dashboard from a clean checkout with a single command:

```bash
# Using Docker (judges standard):
make run
```
*Or with local Python:*
```bash
make run-local
```
Then open your browser to **`http://localhost:8080`**.

---

## 📂 Repository Layout (Hack Apertus Track 2B Spec)

Per official Hack Apertus submission guidelines, the core project implementation and deliverables are located in [`track_2b/`](track_2b/):

```text
Human-vs-System-in-the-Loop-Apertus/
├── index.html                      # Interactive Dual-View Benchmark Dashboard
├── Makefile                        # Root entrypoint (delegates to track_2b/)
├── README.md                       # Project landing overview
├── .gitignore                      # Git ignore rules
└── track_2b/                       # Official Track 2B Challenge Directory
    ├── README.md                   # Track 2B specifications & setup
    ├── technical_report.md         # Full 8-section technical report write-up
    ├── TeamName_Report.pdf         # Official Technical Report PDF (4 pages, publication-grade)
    ├── report.html                 # Print-ready HTML report with Vector SVG architecture
    ├── Makefile                    # 'make run' container launcher
    ├── Dockerfile                  # Container definition for judges
    ├── docker-compose.yml          # Container service definition
    ├── requirements.txt            # Python dependencies
    ├── src/                        # Pipeline source code & evaluation runners
    │   ├── app.py                  # Dashboard server entrypoint
    │   ├── pipeline/               # Constraint, evidence, & scoring engine
    │   ├── run_50_benchmark.py     # 50-trade evaluation runner
    │   ├── run_jev_pipeline_50.py  # JEV Arbiter R1-R8 audit runner
    │   └── run_real_inference.py   # CSCS API & Ollama inference runner
    ├── data/                       # Curated datasets (< 100 MB limit)
    │   ├── all_2024_congress_trades.csv
    │   ├── authentic_benchmark_data.json
    │   ├── benchmark_results_50/   # Serialized model inferences
    │   └── market_data_cache.db    # Historical S&P 500 SQLite cache
    └── docs/                       # Architectural diagrams & specifications
        ├── ARCHITECTURE.md
        ├── BENCHMARK_EXECUTIVE_REPORT.md
        └── PROMPT_SET_v2.md
```

---

## 🛡️ Sovereign Target Architecture Compliance

Per Track 2B requirements, this solution satisfies:
- **c) Sovereign Swiss Cloud:** Apertus 1.5-70B executes on the Swiss AI Supercomputer cluster (CSCS Alps) under Swiss jurisdiction and data sovereignty.
- **a) On-Premise Workstation:** Apertus 1.5-8B runs natively inside Ollama on consumer GPU hardware (NVIDIA RTX 5060 Ti with 16 GB VRAM, consuming 5.2 GB in 4-bit GGUF).
- **b) Air-Gapped Operation:** Pre-computed historical market ground truth cached in SQLite enables zero-network offline execution.

---

## 📄 License

This project is open-source under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)** and the **Apache-2.0 License** in accordance with Hack Apertus Open Commons guidelines.
