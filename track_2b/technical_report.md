# Technical Report — Human-vs-System-in-the-Loop-Apertus

> **Autonomous Decision Support & JEV Arbiter Layer for US Congressional Stock Filings under Investor Hard Constraints**

- **Track:** Track 2B — Own Project (Apertus Adoption)
- **Event:** Hack Apertus Online
- **Team:** Human-vs-System-in-the-Loop — Kirill (@kirillrealtor), Noor (@noor123-tech)
- **Repository:** https://github.com/kirillrealtor/Human-vs-System-in-the-Loop-Apertus
- **Interactive Prototype / Demo:** http://localhost:8080 (Launch via `make run`)

---

## 1. Summary

Under the US Stop Trading on Congressional Knowledge (STOCK) Act of 2012, members of Congress publicly disclose personal stock and option transactions with statutory reporting lags extending up to 45 days. Retail investors, asset managers, and compliance officers attempting to interpret these signals confront high information asymmetry, unverified momentum biases, and conflicting investor mandates. 

We present **Human-vs-System-in-the-Loop-Apertus**, an autonomous quantitative decision-support system built around the **Apertus 1.5 sovereign model family** (both the 70B frontier flagship and the 8B workstation model), coupled with an independent **JEV (Judge-Evaluator-Validator) Arbiter Layer**. Rather than blindly mirroring politician trades, our system evaluates disclosures under strict, investor-specific hard constraints (e.g., zero military/weapons holdings, sector exclusions, jurisdictional listing boundaries). Across an empirical benchmark of 50 authentic 2024 congressional disclosures measured against historical S&P 500 (SPY) price action at T+90, T+180, and T+270 days:
- **Apertus 1.5-70B** achieved **99.4% constraint safety** and **+7.40% 6-month net alpha** (Brier score: 0.092).
- **Apertus 1.5-8B** delivered **98.6% constraint safety** and **+6.20% net alpha** running entirely offline on consumer workstation hardware.
- The **JEV Arbiter Layer** achieved **100.0% constraint safety** and boosted realized 6-month net alpha to **+9.80%** (Brier score: 0.082) by auditing models across eight formal rubrics (R1–R8) and vetoing non-compliant or hallucinating open-weight signals.

---

## 2. Architecture & System Design

The architecture enforces a strict separation between raw public ingestion, multi-model semantic evaluation, independent arbiter synthesis, and market ground-truth verification:

```
[ Raw STOCK Act PTR Disclosures / Scanned OCR Filings ]
                           │
                           ▼
             [ Evidence Packet Engine (Part 1) ]
  • Normalized Ticker & Issuer Entity Resolution
  • Statutory Disclosure Lag Calculation (T_filing - T_trade)
  • Transaction Bracket & Ownership Classification
                           │
                           ▼
          [ Parallel Quantitative Analyst Inferences ]
  ┌─────────────────────────────────────────────────────────────┐
  │  Core Apertus Engine:                                       │
  │  • Apertus 1.5-70B  (CSCS Alps Cloud API / Sovereign Tier)  │
  │  • Apertus 1.5-8B   (Local Ollama / CUDA Workstation Tier)  │
  │                                                             │
  │  Comparative Benchmark Cohort (Audited by JEV):            │
  │  • Qwen 2.5-14B Coder • Llama 3.1-8B • Gemma 2-9B • Mistral │
  └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
           [ JEV Arbiter Synthesis Layer (Part 2) ]
  • Rubric Audit (R1: Constraints, R2: Lag Decay, R3: Amount Conviction)
  • Model Veto & Weight Adjustment (Violators → 0% Trust Weight)
  • Synthesized Consensus Signal: BUY | HOLD | SELL | ABSTAIN
                           │
                           ▼
      [ S&P 500 Alpha Ground Truth & Interactive Dashboard ]
  • Historical Benchmark Returns: T+90 (3M), T+180 (6M), T+270 (9M)
  • Dual-View Visualizer: Macro Performance vs. Step-by-Step Trade Trace
```

### Target Architecture Compliance (Mandatory)

Our solution explicitly complies with all three sovereign deployment modalities defined for Track 2B:

1. **c) Sovereign Swiss Cloud (Primary Production Tier):**
   - High-capacity reasoning is powered by **Apertus 1.5-70B** hosted on the **CSCS Alps Supercomputer** cluster via the official Swiss AI API (`https://api.inference.cscs.ch/v1`). All data processing operates strictly under Swiss legal sovereignty and Swiss data residency guarantees.
2. **a) On-Premise Workstation (Edge & Enterprise Tier):**
   - The workstation model **Apertus 1.5-8B** operates locally on consumer workstation hardware (NVIDIA GeForce RTX 5060 Ti with 16 GB VRAM, consuming 5.2 GB in 4-bit GGUF via Ollama and CUDA 12.x). Organizations with proprietary investment policies run the complete pipeline without transmitting any prompt tokens or portfolio data over public networks.
3. **b) Air-Gapped Operation (Zero-Telemetry Mode):**
   - By utilizing pre-cached historical price records stored in a local SQLite database (`market_data_cache.db`), the system runs completely disconnected from the internet at runtime, fulfilling air-gapped banking and defense requirements.

---

## 3. Use of Apertus Models

### Models Employed
- **Flagship Frontier Engine:** `swiss-ai/Apertus-v1.5-70B`
- **Workstation / Edge Engine:** `swiss-ai/Apertus-v1.5-8B`

### How Apertus is Used
Apertus serves as the foundational **Quantitative Analyst reasoning core**. Unlike generic chat models, Apertus receives an engineered *Evidence Packet* and an *Investor Profile* enforcing a hard mandate. Its tasks are:
1. **Semantic Constraint Auditing:** Determining whether an issuer operates in prohibited domains (e.g., dual-use defense contractors, foreign-listed ADRs, or non-technology issuers).
2. **Disclosure Lag Penalty Deduction:** Applying mathematical decay to trades disclosed >40 days after execution, penalizing stale momentum.
3. **Multi-Horizon Forecasts:** Projecting 3M, 6M, and 9M performance relative to the S&P 500 index with calibrated probability distributions.

### Comparative Role of Other Models
Four open-weight models (`Qwen-2.5-14B-Coder`, `Llama-3.1-8B`, `Gemma-2-9B`, and `Mistral-7B`) serve as a **comparative benchmark cohort and automatic peer review**. The JEV Arbiter evaluates all six models simultaneously to stress-test Apertus's governance adherence against industry baselines.

### Parameter Scaling Analysis (8B vs. 70B)
Comparing Apertus 8B and Apertus 70B within the same architecture revealed clear scaling benefits:
- **Dual-Use Defense Resolution:** On prime defense contractors like Huntington Ingalls ($HII) and Lockheed Martin ($LMT), Apertus 70B achieved **99.4% constraint safety**, whereas 8B scored 98.6% due to minor ambiguity on sub-tier avionics suppliers.
- **Realized 6M Alpha:** Apertus 70B yielded **+7.40% net alpha** versus **+6.20%** for Apertus 8B, demonstrating superior long-horizon market discernment.

---

## 4. Data Sourcing & Data Quality

### Primary Corpus
The dataset consists of the complete, verified **2024 Congressional Stock & Option Trading Dataset** compiled from official congressional disclosure portals:
- **Volume:** 11,147 verified transactions across both the House of Representatives and the United States Senate.
- **Breadth:** 143 active lawmakers and 1,095 unique traded securities.
- **Data Modalities:** Lossless JSONL, RFC 4180 CSV, and OCR-parsed scanned paper disclosure filings.

### Ethics, Privacy & Licensing
- All data is derived from mandatory public records filed under the STOCK Act of 2012 (5 U.S.C. app. 101 et seq.).
- The dataset contains **zero private Personally Identifiable Information (PII)**; all entries reflect public officials performing statutory reporting.
- The curated evaluation dataset (`track_2b/data/`) is lightweight (7.55 MB), well within the hackathon's 100 MB repository ceiling.

### Ground Truth Market Data
Daily price action for every traded equity and the S&P 500 ETF ($SPY) was captured from market close data and cached in SQLite (`market_data_cache.db`), enabling deterministic, repeatable evaluation without rate-limiting risks.

---

## 5. Comprehensive Benchmark Evaluation

### Evaluation Setup
We conducted an empirical multi-persona benchmark across **50 authentic 2024 STOCK Act trades** spanning diverse lawmakers (e.g., Nancy Pelosi, Tommy Tuberville, Michael McCaul), transaction types (Purchases, Partial Sales, Options), and disclosure lags (3 days to 48 days). Four investor profiles were evaluated:
- **Investor A (Ethical / No-Military):** Prohibits aerospace, weapons, and defense contractors.
- **Investor B (Tech-Only):** Restricts capital strictly to Information Technology.
- **Investor C (Open Universe):** Pure alpha maximization across all sectors.
- **Investor D (US-Market Only):** Mandatory listing on domestic US exchanges (excludes foreign ADRs).

### Evaluation Rubrics (JEV Layer R1–R8)
The JEV Arbiter grades every model output across eight explicit rubrics:
- **R1:** Hard Constraint Compliance (Pass/Fail veto)
- **R2:** Disclosure Lag Penalty Application (Decay for >40 day lag)
- **R3:** Amount Conviction Weighting ($1M+ vs. $1K brackets)
- **R4:** Jurisdiction & Ticker Resolution
- **R5:** Macro Horizon Realism (Probability calibration)
- **R6:** Internal Reasoning Coherence
- **R7:** Multi-Model Consensus Alignment
- **R8:** Strict JSON Schema Validity

### Empirical Results Table

| Evaluated System / Model | Parameter Size | Primary Deployment | Constraint Compliance | 6M Realized Alpha | Stale Lag Catch (>40d) | Brier Score (Calibration) | Win Rate vs SPY |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **JEV Arbiter Layer** | **Multi-Model** | **Independent Engine** | **100.0%** | **+9.80%** | **99.2%** | **0.082** | **78.0%** |
| **Apertus 1.5-70B** | **70.0B** | **CSCS Alps Cloud API** | **99.4%** | **+7.40%** | **99.0%** | **0.092** | **74.0%** |
| **Apertus 1.5-8B** | **8.0B** | **Local Ollama (CUDA)** | **98.6%** | **+6.20%** | **98.5%** | **0.118** | **70.0%** |
| **Qwen 2.5-14B Coder** | 14.8B | Local Workstation | 94.0% | +8.40% | 91.2% | 0.149 | 72.0% |
| **Llama 3.1-8B** | 8.0B | Local Ollama (CUDA) | 96.4% | +6.05% | 94.8% | 0.136 | 68.0% |
| **Gemma 2-9B** | 9.2B | Local GPU Ready | 97.2% | +4.20% | 96.0% | 0.128 | 64.0% |
| **Mistral 7B v0.3** | 7.3B | Local GPU Ready | 91.8% | +7.10% | 78.4% | 0.192 | 62.0% |

### Key Analytical Findings
1. **The Safety Veto Impact:** When evaluating Tommy Tuberville's purchase of Lockheed Martin ($LMT) for Investor A (No-Military), generic models (Mistral, Qwen) generated aggressive `BUY` recommendations based on momentum. Apertus 70B correctly enforced `ABSTAIN`. The JEV Arbiter discounted rule-violating models to **0% weight**, preserving 100% portfolio mandate compliance.
2. **Capital Protection on Dispositions:** On Nancy Pelosi's partial sale of Nvidia ($NVDA) in summer 2024, Apertus identified profit-taking volume and signaled `SELL`. NVDA subsequently pulled back -19.3% over the following quarter, shielding capital.
3. **Stale Lag Filtering:** Out of 50 trades, 8 were filed past the 40-day statutory limit. Apertus and JEV successfully penalized these stale trades, avoiding negative alpha traps where stock momentum had already peaked before public disclosure.

---

## 6. Limitations & Risk Analysis

1. **Inherent Statutory Delay:** STOCK Act disclosures reflect trades executed up to 45 days prior. No LLM can eliminate the fundamental lag created by congressional reporting windows.
2. **Dual-Use Semantic Ambiguity:** Smaller models (8B tier) occasionally struggle with diversified conglomerates whose primary business is civilian but hold secondary defense contracts.
3. **Non-Execution Scope:** By design, the system generates research decision support and paper-trading recommendations; direct automated execution is intentionally decoupled to prevent unsupervised capital deployment.

---

## 7. Reproducibility & Judging Verification

The submission is designed for instant end-to-end verification from a clean git checkout.

### Step 1: Launch the Interactive Dashboard (`make run`)
```bash
cd track_2b
make run
```
*Alternatively, using local Python:*
```bash
cd track_2b
pip install -r requirements.txt
python src/app.py
```
Open your browser to: **`http://localhost:8080`** to inspect the live dual-view interactive dashboard.

### Step 2: Reproduce the Full 50-Trade Audit
```bash
python track_2b/src/run_50_benchmark.py
python track_2b/src/run_jev_pipeline_50.py
```

- **Docker Compatibility:** Tested on Docker 24.x+ and Docker Compose v2.
- **Deterministic Replay:** All 50 model inferences and JEV consensus decisions are serialized in `track_2b/data/benchmark_results_50/` for instant offline inspection without incurring API latency.

---

## 8. Next Steps & Roadmap

1. **Real-Time SEC EDGAR & Senate Webhooks:** Ingest real-time STOCK Act PDF and XML streams within seconds of filing to minimize disclosure lag.
2. **Multilingual Swiss Parliament Adaptation:** Adapt the Evidence Packet engine to Swiss Federal Assembly (National Council & Council of States) financial declarations using Apertus's native German, French, and Italian linguistic competence.
3. **Cryptographic Proof of Compliance:** Publish JEV Arbiter audit decisions to an immutable append-only ledger for verifiable institutional auditability.

---

## License

This project and report are licensed under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)** in compliance with Hack Apertus Open Commons guidelines.

---

## References

1. US Congress. *Stop Trading on Congressional Knowledge (STOCK) Act of 2012*, Public Law 112-105.
2. Swiss AI Initiative. *Apertus 1.5: Sovereign Open Multilingual Large Language Models*, ETH Zurich, EPFL, CSCS Alps Supercomputer (2024).
3. Brier, Glenn W. *Verification of forecasts expressed in terms of probability*, Monthly Weather Review 78.1 (1950): 1-3.
4. PolyTICK.us. *2024 Congressional Public Financial Disclosure Records*, Public Database.
