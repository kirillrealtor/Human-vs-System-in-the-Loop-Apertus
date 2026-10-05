# 2024 US Congress & Senate Trading Dataset

This directory contains the **complete, verified 2024 Congressional Stock & Option Trading Dataset**, compiling all disclosures filed under the STOCK Act of 2012 across both the **House of Representatives** and the **United States Senate**.

## Summary Overview
- **Total Transactions:** 11,147
- **House PTR Electronic Disclosures:** 3,189 trades
- **Senate PTR Disclosures:** 1,234 trades
- **House Scanned Document (OCR Parsed):** 6,724 trades
- **Unique Politicians Active in 2024:** 143
- **Unique Securities Traded:** 1095
- **Master Files:** Lossless JSONL, RFC CSV, and JSON

---

## Directory Structure

```
Aspertus/
├── all_2024_congress_trades_layman.txt  # [EASIEST FOR AI & HUMANS] Plain English sentences (1 trade per line)
├── all_2024_congress_trades.jsonl       # Master JSON Lines (1 JSON object per line)
├── all_2024_congress_trades.csv         # Master RFC 4180 CSV (for Code Interpreter / Pandas)
├── all_2024_congress_trades.json        # Master JSON Array
├── dataset_manifest.json                # Metadata & record counts
├── politicians_summary_2024.json        # Aggregated politician stats (trades, volume, tickers)
├── politicians_summary_2024.md          # Human/LLM-readable politician ranking table
├── tickers_summary_2024.json            # Aggregated ticker stats (most traded stocks by Congress)
├── tickers_summary_2024.md              # Human/LLM-readable most traded securities table
├── layman_text/                         # Plain English quarterly & profile text files
│   ├── congress_trades_2024_Q1_layman.txt
│   ├── congress_trades_2024_Q2_layman.txt
│   ├── congress_trades_2024_Q3_layman.txt
│   ├── congress_trades_2024_Q4_layman.txt
│   └── politicians_2024_layman_stories.txt
├── by_chamber/                          # Filtered by legislative body
│   ├── house_trades_2024.jsonl / .csv   # House electronic PTR filings
│   ├── senate_trades_2024.jsonl / .csv  # Senate PTR filings
│   └── scanned_house_trades_2024.jsonl  # Scanned paper disclosures parsed by OCR
└── by_quarter/                          # Markdown chunks for LLM Context Window
    ├── congress_trades_2024_Q1.md       # Q1 2024 (Jan - Mar)
    ├── congress_trades_2024_Q2.md       # Q2 2024 (Apr - Jun)
    ├── congress_trades_2024_Q3.md       # Q3 2024 (Jul - Sep)
    └── congress_trades_2024_Q4.md       # Q4 2024 (Oct - Dec)
```

---

## How to Feed This Data to AI Models (Zero Line Missed)

### 1. Vector Search / Embeddings / RAG
Use `all_2024_congress_trades.jsonl`. Iterate line by line. Embed each line directly or embed with metadata:
```python
import json

with open("Aspertus/all_2024_congress_trades.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        trade = json.loads(line)
        # Feed to vector database / embedding model
```

### 2. LLM Context Ingestion (Prompting)
Use the files in `by_quarter/` (e.g. `congress_trades_2024_Q1.md`). They are wrapped in `<congressional_trades>` tags and formatted with clean Markdown tables to prevent token hallucination and anchor the model's attention.

### 3. Quantitative / Python Code Interpreter
Feed `all_2024_congress_trades.csv` directly to the AI model or analysis environment:
```python
import pandas as pd
df = pd.read_csv("Aspertus/all_2024_congress_trades.csv")
# Calculate win rates, volume by party, top buying politicians, etc.
```

---

## Schema Definitions (Sanitized Public Dataset)

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Standardized sequential trade ID (`US-CONG-2024-00001` to `US-CONG-2024-11147`) |
| `chamber` | string | `House` or `Senate` |
| `source` | string | Filing source (`House PTR Electronic`, `Senate PTR Electronic`, `House Scanned Document OCR`) |
| `politician_name` | string | Authoritative canonical member name (e.g. `Nancy Pelosi`, `Tommy Tuberville`) |
| `party` | string | Political party affiliation (`Democrat`, `Republican`, `Independent`) |
| `state_district` | string | State / District representation (e.g. `CA-11`, `TX-2`, `AL`) |
| `committee` | string | Congressional committee assignment (if available) |
| `subcommittee` | string | Subcommittee assignment (if available) |
| `ticker` | string | Traded stock ticker symbol (e.g. `NVDA`, `AAPL`) |
| `asset_name` | string | Full name of corporate issuer or asset |
| `asset_type` | string | Security type (`Stock`, `Option`, `Corporate Bond`, etc.) |
| `transaction_type` | string | `Purchase`, `Sale (Full)`, `Sale (Partial)`, `Exchange` |
| `transaction_date` | string | Trade execution date (`YYYY-MM-DD`, normalized to 2024) |
| `filing_date` | string | Official public STOCK Act filing date (`YYYY-MM-DD`) |
| `days_to_disclosure` | integer | Number of days between trade and public filing |
| `amount_range` | string | Official STOCK Act bracket (e.g. `$1,001 - $15,000`, `$50,001 - $100,000`) |
| `amount_min_usd` | integer | Lower boundary of transaction value in USD |
| `amount_max_usd` | integer | Upper boundary of transaction value in USD |
| `price_per_share` | float | Execution share price (if reported on filing) |
| `is_option` | boolean | `true` if derivative contract (call/put), `false` otherwise |
| `option_type` | string | `Call` or `Put` (if option) |
| `option_strike` | string | Strike price (if option) |
| `option_expiry` | string | Expiration date (if option) |
| `owner` | string | Account ownership (`Self`, `Spouse`, `Child`, `Joint`) |
| `pdf_url` | string | Official clerk PDF download URL |

