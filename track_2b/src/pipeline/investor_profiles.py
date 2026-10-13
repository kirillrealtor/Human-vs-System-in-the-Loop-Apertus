"""
Investor Profiles A-D definition for Congressional Trade Evaluation (v2).
"""

from typing import Dict
from .models import InvestorProfile

INVESTOR_PROFILES: Dict[str, InvestorProfile] = {
    "A": InvestorProfile(
        investor_id="A",
        investor_name="Ethical No-Military",
        hard_constraint=(
            "Must NOT hold companies in the military / defense sector. "
            "If the issuer is in aerospace and defense, weapons, ammunition, military vehicles or "
            "defense-contractor business, the signal MUST be ABSTAIN with constraint_check.passes = false."
        ),
        risk_appetite="Conservative",
        target_horizon="6M",
        max_single_position_pct=5.0,
    ),
    "B": InvestorProfile(
        investor_id="B",
        investor_name="Tech-Only",
        hard_constraint=(
            "Only Technology sector. If the issuer is not in the Technology sector, "
            "the signal MUST be ABSTAIN with constraint_check.passes = false."
        ),
        risk_appetite="Aggressive",
        target_horizon="3M",
        max_single_position_pct=10.0,
    ),
    "C": InvestorProfile(
        investor_id="C",
        investor_name="Open All Industries",
        hard_constraint=(
            "No sector or geography restriction. Evaluate the trade on its merits. "
            "Constraint check always passes."
        ),
        risk_appetite="Moderate",
        target_horizon="6M",
        max_single_position_pct=7.5,
    ),
    "D": InvestorProfile(
        investor_id="D",
        investor_name="US-Market Only",
        hard_constraint=(
            "Only companies listed on a US exchange (NYSE, Nasdaq, NYSE American, Cboe). "
            "If the issuer has no US exchange listing, the signal MUST be ABSTAIN with constraint_check.passes = false."
        ),
        risk_appetite="Moderate",
        target_horizon="9M",
        max_single_position_pct=5.0,
    ),
}


def get_investor_profile(investor_id: str) -> InvestorProfile:
    """Retrieve an investor profile by ID ('A', 'B', 'C', or 'D')."""
    inv_id = investor_id.upper()
    if inv_id not in INVESTOR_PROFILES:
        raise ValueError(f"Unknown investor ID: {investor_id}. Expected one of {list(INVESTOR_PROFILES.keys())}")
    return INVESTOR_PROFILES[inv_id]
