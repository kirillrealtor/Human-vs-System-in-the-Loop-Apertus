# System Architecture — Human-vs-System-in-the-Loop-Apertus

```mermaid
flowchart TD
    subgraph Data Layer
        A[STOCK Act PTR Disclosures] --> B[PolyTICK.us Master Dataset]
        B --> C[Evidence Packet Engine]
    end

    subgraph Inference Layer
        C --> D1[Apertus 1.5-70B\nCSCS Alps Swiss Cloud API]
        C --> D2[Apertus 1.5-8B\nLocal Workstation RTX 5060 Ti]
        C --> D3[Benchmark Cohort\nQwen 2.5 / Llama 3.1 / Gemma 2 / Mistral]
    end

    subgraph Evaluation & Arbiter Layer
        D1 --> E[JEV Arbiter Layer]
        D2 --> E
        D3 --> E
        E --> F1[Hard Constraint Check R1]
        E --> F2[Disclosure Lag Audit R2]
        E --> F3[Amount Conviction R3]
        E --> F4[Schema Compliance R8]
    end

    subgraph Output & Verification
        F1 --> G[Consensus Decision Support]
        F2 --> G
        F3 --> G
        F4 --> G
        G --> H[S&P 500 Alpha Ground Truth\n3M / 6M / 9M]
        H --> I[Interactive Dual-View Dashboard\nhttp://localhost:8080]
    end
```

## Deployment Specifications

1. **CSCS Alps Supercomputer (Sovereign Swiss Cloud):**
   - Model: Apertus 1.5-70B (70 Billion Parameters)
   - Endpoint: `https://api.inference.cscs.ch/v1`
   - Data Sovereignty: Strictly governed under Swiss data residency laws.

2. **Local Edge / Workstation (On-Premise):**
   - Model: Apertus 1.5-8B (8 Billion Parameters)
   - Runtime: Ollama with CUDA 12.x on NVIDIA RTX 5060 Ti (16 GB VRAM)
   - Footprint: 5.2 GB in 4-bit GGUF quantization.

3. **Air-Gapped Offline Mode:**
   - Pre-cached historical ground-truth data in SQLite (`market_data_cache.db`).
   - Zero outbound HTTP network calls during evaluation runs.
