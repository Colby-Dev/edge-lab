from typing import List, Dict
from parlay import (
    parlay_expected_value,
    risk_adjusted_return,
    marginal_ev
)

def implied_probability(decimal_odds: float) -> float:
    return 1.0 / decimal_odds


def edge_percentage(fair_prob: float, decimal_odds: float) -> float:
    implied = implied_probability(decimal_odds)
    return fair_prob - implied


def edge_strength(edge: float) -> str:
    if edge > 0.05:
        return "strong"
    if edge > 0.02:
        return "medium"
    if edge > 0:
        return "weak"
    return "negative"


def is_positive_ev(prob: float, odds: float) -> bool:
    return (prob * odds) - 1 > 0


def detect_parlay_edge(
    probabilities: List[float],
    odds: List[float],
    ev_threshold: float = 0.02,
    risk_adj_threshold: float = 0.01
) -> Dict:
    ev = parlay_expected_value(probabilities, odds)
    risk_adj = risk_adjusted_return(probabilities, odds)

    return {
        "is_edge": ev >= ev_threshold and risk_adj >= risk_adj_threshold,
        "expected_value": ev,
        "risk_adjusted_return": risk_adj
    }


def detect_marginal_edge(
    current_probs: List[float],
    current_odds: List[float],
    new_prob: float,
    new_odds: float,
    min_delta_ev: float = 0.0
) -> Dict:
    delta = marginal_ev(
        current_probs,
        current_odds,
        new_prob,
        new_odds
    )

    return {
        "is_edge": delta > min_delta_ev,
        "delta_ev": delta
    }
