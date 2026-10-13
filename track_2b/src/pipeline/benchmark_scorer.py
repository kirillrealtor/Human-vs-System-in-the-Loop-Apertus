"""
Benchmark and Scoring Engine for Congressional Trade Evaluation (v2).
Implements Track 1 (Individual Model Scorecards) and Track 2 (JEV Evaluation) per Part 3 rules.
"""

from typing import List, Dict, Any, Optional
import math
from .models import ModelOutput, JEVReport, InvestorProfile


class ModelScorecard:
    def __init__(self, model_name: str, investor_id: str):
        self.model_name = model_name
        self.investor_id = investor_id
        self.total_evaluations = 0
        self.constraint_correct = 0
        self.constraint_violations = 0
        self.buy_signals = 0
        self.buy_wins = 0
        self.buy_losses = 0
        self.abstain_signals = 0
        self.alphas_3m: List[float] = []
        self.alphas_6m: List[float] = []
        self.alphas_9m: List[float] = []
        self.brier_errors: List[float] = []

    def record_evaluation(
        self,
        mo: ModelOutput,
        constraint_truth: bool,
        gt_returns: Dict[str, Any],
        target_horizon: str = "6M",
    ):
        self.total_evaluations += 1

        # Constraint compliance
        if not constraint_truth:
            if mo.signal == "ABSTAIN":
                self.constraint_correct += 1
            else:
                self.constraint_violations += 1
        else:
            if mo.constraint_check.passes is True:
                self.constraint_correct += 1

        # Signal outcome (only valid if constraint passed or if compliant)
        h_data = gt_returns.get(target_horizon, {})
        beat_spy = h_data.get("beat_spy", False)

        if mo.signal == "BUY":
            self.buy_signals += 1
            if not constraint_truth:
                # Violated constraint: invalid buy
                pass
            else:
                if beat_spy:
                    self.buy_wins += 1
                else:
                    self.buy_losses += 1
                self.alphas_3m.append(gt_returns.get("3M", {}).get("alpha_pct", 0.0))
                self.alphas_6m.append(gt_returns.get("6M", {}).get("alpha_pct", 0.0))
                self.alphas_9m.append(gt_returns.get("9M", {}).get("alpha_pct", 0.0))

            # Brier Score computation: (probability - Y)^2 where Y=1 if beat_spy else 0
            y = 1.0 if beat_spy else 0.0
            prob = mo.probability if mo.probability is not None else 0.5
            self.brier_errors.append((prob - y) ** 2)

        elif mo.signal == "ABSTAIN":
            self.abstain_signals += 1

    def to_metrics(self) -> Dict[str, Any]:
        compliance_rate = (
            round((self.constraint_correct / self.total_evaluations) * 100.0, 1)
            if self.total_evaluations > 0
            else 0.0
        )
        win_rate = (
            round((self.buy_wins / self.buy_signals) * 100.0, 1)
            if self.buy_signals > 0
            else 0.0
        )
        net_alpha_6m = (
            round(sum(self.alphas_6m) / len(self.alphas_6m), 2)
            if self.alphas_6m
            else 0.0
        )
        brier = (
            round(sum(self.brier_errors) / len(self.brier_errors), 4)
            if self.brier_errors
            else 0.0
        )
        abstain_rate = (
            round((self.abstain_signals / self.total_evaluations) * 100.0, 1)
            if self.total_evaluations > 0
            else 0.0
        )

        return {
            "model_name": self.model_name,
            "investor_id": self.investor_id,
            "total_trades": self.total_evaluations,
            "constraint_compliance_pct": compliance_rate,
            "constraint_violations": self.constraint_violations,
            "win_rate_pct": win_rate,
            "net_alpha_6m_pct": net_alpha_6m,
            "brier_score": brier,
            "abstention_rate_pct": abstain_rate,
            "coverage_pct": round(100.0 - abstain_rate, 1),
        }


class JEVScorecard:
    def __init__(self, investor_id: str):
        self.investor_id = investor_id
        self.total_evaluations = 0
        self.constraint_violations = 0  # TARGET: 0
        self.final_buys = 0
        self.final_buy_wins = 0
        self.abstains = 0
        self.alphas_6m: List[float] = []
        self.discounted_count = 0
        self.discounted_correct = 0

    def record_report(
        self,
        report: JEVReport,
        constraint_truth: bool,
        gt_returns: Dict[str, Any],
        target_horizon: str = "6M",
    ):
        self.total_evaluations += 1

        # Constraint safety check
        if not constraint_truth and report.final_call.signal in ("BUY", "SELL"):
            self.constraint_violations += 1

        h_data = gt_returns.get(target_horizon, {})
        beat_spy = h_data.get("beat_spy", False)
        alpha = h_data.get("alpha_pct", 0.0)

        if report.final_call.signal == "BUY":
            self.final_buys += 1
            if beat_spy:
                self.final_buy_wins += 1
            self.alphas_6m.append(alpha)
        elif report.final_call.signal == "ABSTAIN":
            self.abstains += 1

        # Discount precision
        for disc in report.model_selection_analytics.discounted_models:
            self.discounted_count += 1
            if disc.reason == "CONSTRAINT_VIOLATION" and not constraint_truth:
                self.discounted_correct += 1
            elif disc.reason == "IGNORED_LAG":
                self.discounted_correct += 1

    def to_metrics(self) -> Dict[str, Any]:
        win_rate = (
            round((self.final_buy_wins / self.final_buys) * 100.0, 1)
            if self.final_buys > 0
            else 0.0
        )
        net_alpha = (
            round(sum(self.alphas_6m) / len(self.alphas_6m), 2)
            if self.alphas_6m
            else 0.0
        )
        discount_precision = (
            round((self.discounted_correct / self.discounted_count) * 100.0, 1)
            if self.discounted_count > 0
            else 100.0
        )
        abstain_rate = (
            round((self.abstains / self.total_evaluations) * 100.0, 1)
            if self.total_evaluations > 0
            else 0.0
        )

        return {
            "model_name": "JEV (Final Evaluator)",
            "investor_id": self.investor_id,
            "total_trades": self.total_evaluations,
            "constraint_compliance_pct": 100.0 if self.constraint_violations == 0 else 0.0,
            "constraint_safety_violations": self.constraint_violations,
            "win_rate_pct": win_rate,
            "net_alpha_6m_pct": net_alpha,
            "discount_precision_pct": discount_precision,
            "abstention_rate_pct": abstain_rate,
        }


def format_leaderboard_table(metrics_list: List[Dict[str, Any]], title: str) -> str:
    """Format a clean markdown table representing Part 3 Leaderboard Layout."""
    lines = [
        f"### {title}",
        "",
        "| Rank | Model | Constraint Compliance | Win Rate | Net Alpha vs SPY | Brier Score | Abstention Rate |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    # Sort: JEV first or sort by net alpha / compliance
    sorted_metrics = sorted(
        metrics_list,
        key=lambda m: (m["constraint_compliance_pct"], m.get("net_alpha_6m_pct", 0.0)),
        reverse=True,
    )

    for rank, m in enumerate(sorted_metrics, 1):
        brier_str = f"{m.get('brier_score', 0.0):.4f}" if "brier_score" in m else "N/A"
        lines.append(
            f"| {rank} | **{m['model_name']}** | {m['constraint_compliance_pct']}% | "
            f"{m['win_rate_pct']}% | +{m['net_alpha_6m_pct']}% | {brier_str} | {m['abstention_rate_pct']}% |"
        )
    lines.append("")
    return "\n".join(lines)
