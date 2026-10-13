"""
Real Local LLM Inference Engine using Ollama.
Sends real Evidence Packets and Part 1 Prompts to locally running models on your RTX 5060 Ti GPU,
captures genuine model responses, and stores them in evaluation_sessions/.
"""

import sys
import json
import requests
import argparse

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pipeline.models import EvidencePacket
from pipeline.evidence_packet import build_evidence_packet
from pipeline.investor_profiles import INVESTOR_PROFILES, get_investor_profile
from pipeline.prompts import build_model_prompt
from pipeline.session_manager import load_trade_record, ensure_sessions_dir


OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"


def run_real_model_inference(
    trade_id: str,
    ollama_model: str,
    investor_id: str,
    temperature: float = 0.1,
) -> dict:
    """
    Sends the exact prompt to the local Ollama instance on GPU,
    captures real LLM output, and parses the JSON response.
    """
    raw_record = load_trade_record(trade_id)
    packet = build_evidence_packet(raw_record)
    profile = get_investor_profile(investor_id)

    # Build the exact prompt from Part 1 specification
    prompt = build_model_prompt(
        profile=profile,
        packet=packet,
        model_identifier=ollama_model,
        model_version="local-ollama",
    )

    print(f"\n[1/3] Feeding trade {trade_id} to local model: {ollama_model} on GPU...")
    print(f"      Investor Mandate: Investor {investor_id} ({profile.investor_name})")

    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024,
        }
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        if response.status_code != 200:
            print(f"Ollama error: HTTP {response.status_code} - {response.text}")
            return {}
        
        res_json = response.json()
        raw_text = res_json.get("response", "").strip()
        print(f"\n[2/3] Raw Model Output Received ({res_json.get('eval_count', 0)} tokens generated):")
        print("-" * 60)
        print(raw_text[:400] + ("..." if len(raw_text) > 400 else ""))
        print("-" * 60)

        # Parse JSON from model output
        parsed_output = None
        # Try direct parse
        try:
            parsed_output = json.loads(raw_text)
        except Exception:
            # Extract JSON block if wrapped in markdown ```json ... ```
            if "```" in raw_text:
                parts = raw_text.split("```")
                for p in parts:
                    clean_p = p.replace("json", "").strip()
                    try:
                        parsed_output = json.loads(clean_p)
                        break
                    except Exception:
                        continue

        if not parsed_output:
            print("⚠️ Warning: Model did not return strict JSON. Raw text captured.")
            parsed_output = {
                "raw_response": raw_text,
                "model_name": ollama_model,
                "trade_id": trade_id,
                "investor_id": investor_id,
            }

        # Save to session directory
        s_dir = ensure_sessions_dir(trade_id)
        clean_name = ollama_model.replace(":", "_").replace("/", "_").replace(".", "_")
        out_file = f"{s_dir}/real_{clean_name}_inv_{investor_id}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(parsed_output, f, indent=2)

        print(f"\n[3/3] ✅ Authentic model output saved to disk: {out_file}")
        return parsed_output

    except Exception as e:
        print(f"Inference connection error: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(description="Real Local LLM Inference for Congressional Trades")
    parser.add_argument("--trade", type=str, default="US-CONG-2024-00390", help="Trade ID to evaluate")
    parser.add_argument("--model", type=str, default="WhiteRabbitNeo/Llama-3.1-WhiteRabbitNeo-2-8B:latest", help="Ollama model name")
    parser.add_argument("--investor", type=str, default="A", help="Investor ID (A, B, C, or D)")
    args = parser.parse_args()

    run_real_model_inference(
        trade_id=args.trade,
        ollama_model=args.model,
        investor_id=args.investor,
    )


if __name__ == "__main__":
    main()
