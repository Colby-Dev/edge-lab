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
