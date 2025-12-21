import math
from typing import List


def parlay_probability(probabilities: List[float]) -> float:
    """
    Multiply independent probabilities.
    """
    p = 1.0
    for prob in probabilities:
        p *= prob
    return p


def parlay_odds(decimal_odds: List[float]) -> float:
    """
    Multiply decimal odds.
    """
    o = 1.0
    for odd in decimal_odds:
        o *= odd
    return o


def parlay_expected_value(probabilities: List[float], decimal_odds: List[float]) -> float:
    """
    EV for 1 unit stake.
    """
    p = parlay_probability(probabilities)
    o = parlay_odds(decimal_odds)
    return (p * o) - 1


def marginal_ev(
    current_probs: List[float],
    current_odds: List[float],
    new_prob: float,
    new_odds: float
) -> float:
    """
    Change in EV from adding one leg.
    """
    ev_before = parlay_expected_value(current_probs, current_odds)
    ev_after = parlay_expected_value(
        current_probs + [new_prob],
        current_odds + [new_odds]
    )
    return ev_after - ev_before

def win_probability_decay(probabilities: List[float]) -> float:
    """
    How much total win probability has decayed
    compared to a single-leg average.
    """
    if not probabilities:
        return 0.0

    avg_prob = sum(probabilities) / len(probabilities)
    parlay_prob = 1.0
    for p in probabilities:
        parlay_prob *= p

    return parlay_prob / avg_prob


def parlay_variance(probabilities: List[float], decimal_odds: List[float]) -> float:
    """
    Variance proxy for parlay returns.
    """
    p = 1.0
    for prob in probabilities:
        p *= prob

    o = 1.0
    for odd in decimal_odds:
        o *= odd

    # Binary outcome: win or lose
    return p * (1 - p) * (o ** 2)


def risk_adjusted_return(
    probabilities: List[float],
    decimal_odds: List[float]
) -> float:
    """
    EV normalized by risk (Sharpe-like ratio).
    """
    from parlay import parlay_expected_value

    ev = parlay_expected_value(probabilities, decimal_odds)
    var = parlay_variance(probabilities, decimal_odds)

    if var <= 0:
        return 0.0

    return ev / math.sqrt(var)
