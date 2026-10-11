"""
Master Sequential Runner to bring all local PC models to 50 Trades
Runs:
1. qwen2.5-coder (from 10 to 50)
2. whiterabbitneo (from 10 to 50)
3. neo-uncensored (from 5 to 50)
4. my-security-ai (from 5 to 50)
"""

import sys
import time
from run_50_benchmark import run_benchmark

MODELS_TO_COMPLETE = [
    "qwen2.5-coder",
    "whiterabbitneo",
    "neo-uncensored",
    "my-security-ai"
]

def main():
    print("=" * 80)
    print("  STARTING FULL 50-TRADE RUN FOR ALL LOCAL GPU MODELS")
    print("=" * 80)
    
    for m in MODELS_TO_COMPLETE:
        print(f"\n>>> Running Model to 50 Trades: {m}")
        start_time = time.time()
        try:
            run_benchmark(m, investor_id="A", limit=50)
            elapsed = time.time() - start_time
            print(f">>> Finished {m} in {round(elapsed, 1)} seconds!")
        except Exception as e:
            print(f">>> Error running {m}: {e}")

    print("\n" + "=" * 80)
    print("  ALL REMAINING LOCAL MODELS HAVE COMPLETED 50 TRADES!")
    print("=" * 80)

if __name__ == "__main__":
    main()
