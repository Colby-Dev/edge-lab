def implied_probability(decimal_odds: float) -> float:
    """
    Convert decimal odds to implied probability.
    Example: 1.91 -> ~0.5236
    """
    return 1.0 / decimal_odds


def remove_vig(probabilities: list[float]) -> list[float]:
    """
    Normalize probabilities to remove sportsbook vig.
    """
    total = sum(probabilities)
    return [p / total for p in probabilities]


def expected_value(prob: float, decimal_odds: float) -> float:
    """
    Expected value for 1 unit stake.
    EV = (p * odds) - 1
    """
    return (prob * decimal_odds) - 1
