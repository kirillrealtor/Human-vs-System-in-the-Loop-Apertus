"""
Ground Truth Engine for Congressional Trade Evaluation (v2).
Fetches historical stock prices and SPY benchmark prices to compute returns at T+90, T+180, and T+270 days.
Includes persistent SQLite disk caching to prevent redundant network calls and rate limits.
"""

import os
import sqlite3
import datetime
from typing import Dict, Any, Optional
import pandas as pd
import yfinance as yf

DB_PATH = "market_data_cache.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_prices (
            ticker TEXT,
            trade_date TEXT,
            close_price REAL,
            PRIMARY KEY (ticker, trade_date)
        )
    """)
    conn.commit()
    conn.close()


_init_db()


def get_cached_price(ticker: str, target_date: datetime.date) -> Optional[float]:
    """Retrieve the close price on or the closest next trading day within 7 days from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    target_str = target_date.isoformat()
    limit_str = (target_date + datetime.timedelta(days=7)).isoformat()
    cursor.execute("""
        SELECT close_price FROM daily_prices 
        WHERE ticker = ? AND trade_date >= ? AND trade_date <= ?
        ORDER BY trade_date ASC LIMIT 1
    """, (ticker.upper(), target_str, limit_str))
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else None


def save_prices_to_cache(ticker: str, df: pd.DataFrame):
    """Save downloaded prices into SQLite."""
    if df is None or df.empty:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    clean_t = ticker.upper()

    for idx, row in df.iterrows():
        try:
            d_str = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
            close_val = float(row["Close"])
            cursor.execute("""
                INSERT OR REPLACE INTO daily_prices (ticker, trade_date, close_price)
                VALUES (?, ?, ?)
            """, (clean_t, d_str, close_val))
        except Exception:
            continue

    conn.commit()
    conn.close()


def ensure_ticker_cached(ticker: str, start_date: str = "2023-11-01", end_date: str = "2026-03-31"):
    """Check if ticker is in DB; if not or incomplete, download from yfinance and cache."""
    clean_t = ticker.strip().upper()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM daily_prices WHERE ticker = ?", (clean_t,))
    count = cursor.fetchone()[0]
    conn.close()

    if count < 50:  # Need adequate price history
        try:
            df = yf.download(clean_t, start=start_date, end=end_date, progress=False)
            if df is not None and not df.empty:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                save_prices_to_cache(clean_t, df)
        except Exception:
            pass


def compute_ground_truth_returns(ticker: Optional[str], transaction_date_str: str) -> Dict[str, Any]:
    """
    Computes asset return and SPY benchmark return at:
    - 3M (T+90 days)
    - 6M (T+180 days)
    - 9M (T+270 days)
    """
    default_res = {
        "resolved": False,
        "entry_date": transaction_date_str,
        "3M": {"asset_return_pct": 0.0, "spy_return_pct": 0.0, "alpha_pct": 0.0, "beat_spy": False},
        "6M": {"asset_return_pct": 0.0, "spy_return_pct": 0.0, "alpha_pct": 0.0, "beat_spy": False},
        "9M": {"asset_return_pct": 0.0, "spy_return_pct": 0.0, "alpha_pct": 0.0, "beat_spy": False},
    }

    if not ticker or ticker.upper() in ("N/A", "NONE", ""):
        return default_res

    clean_t = ticker.strip().upper()

    try:
        t_date = datetime.date.fromisoformat(transaction_date_str)
    except Exception:
        return default_res

    # Ensure ticker and SPY are in database
    ensure_ticker_cached(clean_t)
    ensure_ticker_cached("SPY")

    p0_asset = get_cached_price(clean_t, t_date)
    p0_spy = get_cached_price("SPY", t_date)

    if not p0_asset or not p0_spy or p0_asset <= 0 or p0_spy <= 0:
        return default_res

    res: Dict[str, Any] = {"resolved": True, "entry_date": transaction_date_str}

    horizons = {"3M": 90, "6M": 180, "9M": 270}
    for h_label, days_offset in horizons.items():
        target_d = t_date + datetime.timedelta(days=days_offset)
        p_asset = get_cached_price(clean_t, target_d)
        p_spy = get_cached_price("SPY", target_d)

        if p_asset and p_spy:
            r_asset = ((p_asset - p0_asset) / p0_asset) * 100.0
            r_spy = ((p_spy - p0_spy) / p0_spy) * 100.0
            alpha = r_asset - r_spy
            res[h_label] = {
                "asset_return_pct": round(r_asset, 2),
                "spy_return_pct": round(r_spy, 2),
                "alpha_pct": round(alpha, 2),
                "beat_spy": alpha > 0,
            }
        else:
            res[h_label] = default_res[h_label]

    return res
