"""
Constraint Verification Engine for Congressional Trade Evaluation (v2).
Implements the rules from Part 0 for Investors A, B, C, and D.
"""

from typing import Dict, Any, Tuple, Optional
from .models import ConstraintCheck, EvidencePacket, InvestorProfile

# Reference Sector and Defense knowledge dictionary for common tickers
TICKER_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    # Defense prime & major contractors
    "LMT": {"name": "Lockheed Martin", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "NYSE"},
    "RTX": {"name": "RTX Corporation", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "NYSE"},
    "NOC": {"name": "Northrop Grumman", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "NYSE"},
    "GD": {"name": "General Dynamics", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "NYSE"},
    "BA": {"name": "Boeing Co", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": True, "listing": "NYSE"},
    "HII": {"name": "Huntington Ingalls Industries", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "NYSE"},
    "LHX": {"name": "L3Harris Technologies", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "NYSE"},
    "BAH": {"name": "Booz Allen Hamilton", "sector": "Defense IT Services", "is_defense": True, "dual_use": True, "listing": "NYSE"},
    "LDOS": {"name": "Leidos Holdings", "sector": "Defense & Intelligence IT", "is_defense": True, "dual_use": True, "listing": "NYSE"},
    "TXT": {"name": "Textron", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": True, "listing": "NYSE"},
    "KTOS": {"name": "Kratos Defense & Security", "sector": "Aerospace & Defense", "is_defense": True, "dual_use": False, "listing": "Nasdaq"},
    "PLTR": {"name": "Palantir Technologies", "sector": "Information Technology / Defense Software", "is_defense": True, "dual_use": True, "listing": "NYSE"},

    # Information Technology
    "NVDA": {"name": "NVIDIA Corporation", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "AAPL": {"name": "Apple Inc.", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "AMD": {"name": "Advanced Micro Devices", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "INTC": {"name": "Intel Corporation", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "PANW": {"name": "Palo Alto Networks", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "CRM": {"name": "Salesforce Inc.", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "ADBE": {"name": "Adobe Inc.", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "ORCL": {"name": "Oracle Corporation", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "AVGO": {"name": "Broadcom Inc.", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "CSCO": {"name": "Cisco Systems", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "QCOM": {"name": "Qualcomm Inc.", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},

    # Non-Tech Sectors (Communication, Consumer, Healthcare, Financial, Energy)
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Communication Services", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "GOOG": {"name": "Alphabet Inc.", "sector": "Communication Services", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "META": {"name": "Meta Platforms Inc.", "sector": "Communication Services", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Discretionary", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Consumer Discretionary", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "PFE": {"name": "Pfizer Inc.", "sector": "Healthcare", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "UNH": {"name": "UnitedHealth Group", "sector": "Healthcare", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financials", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "BAC": {"name": "Bank of America", "sector": "Financials", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "GS": {"name": "Goldman Sachs", "sector": "Financials", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "BRK.B": {"name": "Berkshire Hathaway", "sector": "Financials", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "XOM": {"name": "Exxon Mobil", "sector": "Energy", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "CVX": {"name": "Chevron Corp", "sector": "Energy", "is_defense": False, "dual_use": False, "listing": "NYSE"},
    "SBUX": {"name": "Starbucks Corp", "sector": "Consumer Discretionary", "is_defense": False, "dual_use": False, "listing": "Nasdaq"},

    # Foreign / ADR Examples
    "BABA": {"name": "Alibaba Group", "sector": "Consumer Discretionary", "is_defense": False, "dual_use": False, "listing": "NYSE (ADR)"},
    "TSM": {"name": "Taiwan Semiconductor", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "NYSE (ADR)"},
    "ASML": {"name": "ASML Holding", "sector": "Information Technology", "is_defense": False, "dual_use": False, "listing": "Nasdaq (ADR)"},
}


def lookup_ticker_info(ticker: Optional[str], asset_name: Optional[str]) -> Dict[str, Any]:
    """Resolve asset metadata, sector, defense exposure, and exchange listing."""
    if not ticker or ticker.upper() in ("N/A", "NONE", "UNKNOWN", ""):
        # Check if asset name indicates bond, municipal, or fund
        name = (asset_name or "").lower()
        if "due" in name or "bond" in name or "muni" in name or "tn 5%" in name:
            return {
                "name": asset_name,
                "sector": "Fixed Income / Municipal Bond",
                "is_defense": False,
                "dual_use": False,
                "listing": "Over-The-Counter (Unlisted)",
            }
        return {
            "name": asset_name or "Unknown Asset",
            "sector": "Unresolvable",
            "is_defense": False,
            "dual_use": False,
            "listing": "Unlisted / Unknown",
        }

    clean_t = ticker.strip().upper()
    if clean_t in TICKER_KNOWLEDGE:
        return TICKER_KNOWLEDGE[clean_t]

    # Heuristic fallback for other tickers
    name_str = (asset_name or "").lower()
    is_defense = any(term in name_str for term in ["defense", "aerospace", "weapon", "munitions", "missile"])
    is_tech = any(term in name_str for term in ["technolog", "software", "semiconductor", "micro", "systems", "cyber"])

    return {
        "name": asset_name or clean_t,
        "sector": "Information Technology" if is_tech else ("Aerospace & Defense" if is_defense else "General Equities"),
        "is_defense": is_defense,
        "dual_use": False,
        "listing": "US Exchange (NYSE/Nasdaq assumed for standard tickers)",
    }


def verify_constraint(packet: EvidencePacket, profile: InvestorProfile) -> ConstraintCheck:
    """
    Evaluates whether the asset satisfies the hard constraint of the specified investor.
    Returns a validated ConstraintCheck model.
    """
    ticker = packet.asset.ticker
    asset_name = packet.asset.asset_name
    info = lookup_ticker_info(ticker, asset_name)
    resolved_ticker = ticker if ticker else None
    sector = info.get("sector")
    listing = info.get("listing")
    is_defense = info.get("is_defense", False)
    dual_use = info.get("dual_use", False)

    # Check unresolvable assets first
    if not ticker and ("unlisted" in listing.lower() or sector == "Unresolvable"):
        if profile.investor_id == "D":
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=False,
                borderline=False,
                explanation="Asset has no US exchange listing or ticker (fails Investor D requirement).",
            )
        elif profile.investor_id == "B":
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=False,
                borderline=False,
                explanation="Asset is unlisted/non-equity and does not belong to the Information Technology sector.",
            )
        else:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=None,
                borderline=False,
                explanation="Asset issuer, sector, or listing cannot be definitively resolved from disclosure packet.",
            )

    # Investor A: Ethical / No-Military
    if profile.investor_id == "A":
        if is_defense:
            if dual_use:
                return ConstraintCheck(
                    resolved_ticker=resolved_ticker,
                    issuer_sector=sector,
                    issuer_listing=listing,
                    passes=False,
                    borderline=True,
                    explanation=(
                        f"{info.get('name', resolved_ticker)} operates dual-use civilian and military/defense contracts. "
                        "Per Part 0 guidelines, dual-use assets trigger borderline=true and lean to ABSTAIN."
                    ),
                )
            else:
                return ConstraintCheck(
                    resolved_ticker=resolved_ticker,
                    issuer_sector=sector,
                    issuer_listing=listing,
                    passes=False,
                    borderline=False,
                    explanation=(
                        f"{info.get('name', resolved_ticker)} is a prime defense contractor / aerospace defense issuer. "
                        "Violates Investor A hard constraint against military and weapons holdings."
                    ),
                )
        else:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=True,
                borderline=False,
                explanation=f"{info.get('name', resolved_ticker)} ({sector}) has no primary military or defense contracting business.",
            )

    # Investor B: Tech-Only
    elif profile.investor_id == "B":
        if sector == "Information Technology":
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=True,
                borderline=False,
                explanation=f"{resolved_ticker} is strictly classified within the Information Technology sector.",
            )
        elif "Technology" in sector or "Software" in sector:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=True,
                borderline=True,
                explanation=f"{resolved_ticker} has hybrid sector classification ({sector}). Plausible technology categorization.",
            )
        else:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=False,
                borderline=False,
                explanation=(
                    f"{resolved_ticker} is classified in {sector}, which is outside Information Technology. "
                    "Violates Investor B hard constraint."
                ),
            )

    # Investor C: Open / All Industries
    elif profile.investor_id == "C":
        return ConstraintCheck(
            resolved_ticker=resolved_ticker,
            issuer_sector=sector,
            issuer_listing=listing,
            passes=True,
            borderline=False,
            explanation="Investor C has no sector or geographic restrictions. Constraint check passes unconditionally.",
        )

    # Investor D: US-Market Only
    elif profile.investor_id == "D":
        is_adr = "ADR" in listing
        is_unlisted = "unlisted" in listing.lower() or "over-the-counter" in listing.lower()
        if is_unlisted:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=False,
                borderline=False,
                explanation=f"{resolved_ticker or 'Asset'} is unlisted or trades OTC. Lacks national US exchange listing.",
            )
        elif is_adr:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=True,
                borderline=True,
                explanation=f"{resolved_ticker} trades on a US exchange via American Depositary Receipt (ADR). Listed on US exchange.",
            )
        else:
            return ConstraintCheck(
                resolved_ticker=resolved_ticker,
                issuer_sector=sector,
                issuer_listing=listing,
                passes=True,
                borderline=False,
                explanation=f"{resolved_ticker} is listed and actively traded on a major US national exchange ({listing}).",
            )

    return ConstraintCheck(
        resolved_ticker=resolved_ticker,
        issuer_sector=sector,
        issuer_listing=listing,
        passes=None,
        borderline=False,
        explanation="Constraint verification unhandled profile.",
    )
