# Track 2B: Own Project — Human-vs-System-in-the-Loop-Apertus

> **Autonomous Decision Support & JEV Arbiter Layer for US Congressional Stock Filings under Investor Hard Constraints**

Built for the **Hack Apertus Online Hackathon** (Track 2B: Own Project).

[![Apertus](https://img.shields.io/badge/Model-Apertus--1.5--70B%20%26%208B-blue)](https://huggingface.co/swiss-ai)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](Dockerfile)

---

## 🏛️ Executive Overview

Following disclosures under the US STOCK Act of 2012, politicians report stock and option trades with up to 45-day reporting lags. Retail and institutional investors following these signals often violate their own ethical or risk mandates. 

**Human-vs-System-in-the-Loop-Apertus** addresses this problem by combining:
1. **The Apertus 1.5 Family:** Benchmarking **Apertus 70B** (via CSCS Alps Swiss AI Supercomputer API) against **Apertus 8B** (running locally on consumer RTX 5060 Ti hardware).
2. **JEV Arbiter Synthesis Layer:** Audits model responses across rubrics R1–R8, disqualifying mandate-violating signals (0% weight) and synthesizing consensus.
3. **Multi-Model Benchmark Cohort:** Comparative baseline against Qwen 2.5, Llama 3.1, Gemma 2, and Mistral 7B.
4. **Historical Ground Truth:** S&P 500 (SPY) alpha verification at T+90 (3M), T+180 (6M), and T+270 (9M) days.

---

## 🚀 Quickstart & Reproduction

Judges can launch the complete interactive benchmark dashboard with a single command:

### Option 1: Docker (Standard Hackathon Requirement)
```bash
# From the track_2b directory:
make run
```
*Or directly via Docker Compose:*
```bash
docker compose up --build
```
Open your browser to: **`http://localhost:8080`**

### Option 2: Local Python Execution
```bash
cd track_2b
pip install -r requirements.txt
python src/app.py
```
Open your browser to: **`http://localhost:8080`**

---

## 📂 Repository Structure

```
track_2b/
├── Dockerfile              # Container definition for reproducible evaluation
├── Makefile                # 'make run' entrypoint for judges
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Minimal Python dependencies
├── README.md               # Challenge & project overview
├── technical_report.md     # In-depth architectural write-up, benchmarks & analysis
├── index.html              # Interactive Dual-View Hackathon Benchmark Dashboard
├── data/                   # Curated benchmark datasets (< 100 MB total)
│   ├── all_2024_congress_trades.csv     # 11,147 2024 STOCK Act transactions
│   ├── authentic_benchmark_data.json    # 50 iconic audited trades
│   ├── benchmark_results_50/            # Model outputs and JEV final audit JSONs
│   └── market_data_cache.db             # Offline historical S&P 500 price cache
├── docs/                   # Supporting specifications & executive reports
│   ├── ARCHITECTURE.md
│   ├── BENCHMARK_EXECUTIVE_REPORT.md
│   └── PROMPT_SET_v2.md
└── src/                    # Implementation & evaluation scripts
    ├── app.py                           # Dashboard server entrypoint
    ├── pipeline/                        # Modular evaluation & constraint engine
    ├── run_50_benchmark.py              # 50-trade evaluation runner
    ├── run_jev_pipeline_50.py           # JEV Arbiter R1-R8 audit runner
    └── run_real_inference.py            # Local Ollama & CSCS API inference runner
```

---

## 🛡️ Target Architecture (Mandatory Compliance)

Per Track 2B requirements, this solution satisfies:

- **a) On-Premise:** Apertus 1.5-8B runs natively inside Ollama on a consumer workstation (NVIDIA RTX 5060 Ti 16GB VRAM, consuming 5.2 GB in 4-bit GGUF) with zero cloud dependencies.
- **b) Air-Gapped:** Pre-computed historical ground truth and local SQLite caching enable fully offline execution.
- **c) Sovereign Swiss Cloud:** Flagship Apertus 1.5-70B executes on the Swiss AI Supercomputer cluster (CSCS Alps) under Swiss jurisdiction and data sovereignty.

---

## 📊 Key Benchmark Results

Across 50 authentic congressional disclosures:
- **Apertus 1.5-70B:** Achieved **99.4% constraint compliance**, **+7.40% 6-month net alpha**, and a **0.092 Brier score**.
- **Apertus 1.5-8B:** Delivered **98.6% constraint compliance** and **+6.20% net alpha** on local consumer GPU hardware.
- **JEV Arbiter Layer:** Enforced **100.0% constraint safety** and boosted net alpha to **+9.80%** by filtering out hallucinatory and non-compliant open-weight models.

For complete statistical tables and per-persona leaderboards, consult [technical_report.md](technical_report.md) or explore the interactive dashboard.

---

## 📄 License

This project is licensed under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)** in accordance with Hack Apertus Open Commons guidelines.
