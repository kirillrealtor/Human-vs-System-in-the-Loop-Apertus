"""
Evidence Packet Builder for Congressional Trade Evaluation (v2).
Transforms raw dataset records (from all_2024_congress_trades) into standardized EvidencePacket instances.
"""

from typing import Dict, Any, List
import math
from .models import (
    EvidencePacket,
    PoliticianInfo,
    AssetInfo,
    TradeInfo,
    TimingInfo,
    SourceInfo,
)


def _clean_str(val: Any) -> str:
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return ""
    return str(val).strip()


def _clean_float(val: Any) -> float | None:
    if val is None:
        return None
    try:
        f = float(val)
        return None if math.isnan(f) else f
    except (ValueError, TypeError):
        return None


def _clean_int(val: Any, default: int = 0) -> int:
    if val is None:
        return default
    try:
        f = float(val)
        return default if math.isnan(f) else int(f)
    except (ValueError, TypeError):
        return default


def _map_data_origin(source: str) -> str:
    s = source.lower()
    if "ocr" in s or "scanned" in s:
        return "scanned_ocr"
    elif "senate" in s:
        return "senate"
    else:
        return "house_electronic"


def _normalize_asset_type(record: Dict[str, Any]) -> str:
    is_option = record.get("is_option")
    if is_option is True or str(is_option).lower() == "true":
        opt_type = _clean_str(record.get("option_type")).lower()
        if "call" in opt_type:
            return "Call Option"
        elif "put" in opt_type:
            return "Put Option"
        return "Option"
    
    raw_type = _clean_str(record.get("asset_type"))
    if "stock" in raw_type.lower():
        return "Common Stock"
    elif "bond" in raw_type.lower():
        return "Bond"
    elif "fund" in raw_type.lower() or "etf" in raw_type.lower():
        return "Fund / ETF"
    return raw_type or "Common Stock"


def _normalize_owner(owner: str) -> str:
    o = owner.strip().upper()
    if o in ("SELF", ""):
        return "Self"
    elif o in ("SP", "SPOUSE"):
        return "Spouse"
    elif o in ("DC", "CHILD"):
        return "Child"
    elif o in ("JT", "JOINT"):
        return "Joint"
    return owner.capitalize()


def build_evidence_packet(record: Dict[str, Any]) -> EvidencePacket:
    """Build a validated EvidencePacket from a raw trade record dictionary."""
    trade_id = _clean_str(record.get("id")) or "US-CONG-2024-UNKNOWN"
    
    # Politician committees
    committees: List[str] = []
    comm = _clean_str(record.get("committee"))
    subcomm = _clean_str(record.get("subcommittee"))
    if comm and comm.upper() not in ("N/A", "NONE"):
        for c in comm.split(";"):
            c_str = c.strip()
            if c_str:
                committees.append(c_str)
    if subcomm and subcomm.upper() not in ("N/A", "NONE"):
        committees.append(f"Subcommittee: {subcomm}")

    politician = PoliticianInfo(
        name=_clean_str(record.get("politician_name")),
        party=_clean_str(record.get("party")) or None,
        chamber=_clean_str(record.get("chamber")) or None,
        state_district=_clean_str(record.get("state_district")) or None,
        committees=committees,
    )

    asset = AssetInfo(
        ticker=_clean_str(record.get("ticker")) or None,
        asset_name=_clean_str(record.get("asset_name")) or None,
        asset_type=_normalize_asset_type(record),
    )

    trade = TradeInfo(
        transaction_type=_clean_str(record.get("transaction_type")) or "Purchase",
        owner=_normalize_owner(_clean_str(record.get("owner"))),
        amount_range=_clean_str(record.get("amount_range")) or None,
        amount_min_usd=_clean_float(record.get("amount_min_usd")),
        amount_max_usd=_clean_float(record.get("amount_max_usd")),
        price_per_share=_clean_float(record.get("price_per_share")),
    )

    days_lag = _clean_int(record.get("days_to_disclosure"), default=0)
    timing = TimingInfo(
        transaction_date=_clean_str(record.get("transaction_date")),
        filing_date=_clean_str(record.get("filing_date")),
        days_to_disclosure=days_lag,
    )

    source = SourceInfo(
        source_url=_clean_str(record.get("pdf_url")) or None,
        data_origin=_map_data_origin(_clean_str(record.get("source"))),
    )

    # Compute data quality flags
    flags: List[str] = []
    if days_lag > 40:
        flags.append(f"STALE_DISCLOSURE_CRITICAL ({days_lag} days lag > 40d)")
    elif days_lag > 30:
        flags.append(f"STALE_DISCLOSURE_WARNING ({days_lag} days lag > 30d)")

    amount_max = trade.amount_max_usd or 0
    if amount_max > 0 and amount_max < 15000:
        flags.append("LOW_CONVICTION_AMOUNT (< $15,000)")
    elif amount_max >= 500000:
        flags.append("HIGH_CONVICTION_AMOUNT (>= $500,000)")

    if source.data_origin == "scanned_ocr":
        flags.append("SCANNED_OCR_DOCUMENT (potential optical recognition noise)")

    if not trade.price_per_share:
        flags.append("PRICE_PER_SHARE_UNAVAILABLE (assume close on transaction date)")

    if not politician.committees or any("RETIRED" in c.upper() for c in politician.committees):
        flags.append("COMMITTEE_DATA_SPARSE_OR_RETIRED")

    if not asset.ticker:
        flags.append("TICKER_MISSING_FROM_FILING")

    if record.get("is_option") is True or str(record.get("is_option")).lower() == "true":
        flags.append(f"DERIVATIVE_OPTION ({record.get('option_type', 'Option')})")

    return EvidencePacket(
        trade_id=trade_id,
        politician=politician,
        asset=asset,
        trade=trade,
        timing=timing,
        source=source,
        data_quality_flags=flags,
    )
