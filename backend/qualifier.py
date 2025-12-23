from probability import expected_value


def qualifies_leg(
    probability: float,
    odds_decimal: float,
    min_ev: float = 0.01,
    min_prob: float = 0.45
) -> dict:
    """
    Determine whether a leg is eligible for parlay inclusion.
    """

    ev = expected_value(probability, odds_decimal)

    qualifies = (
        ev >= min_ev and
        probability >= min_prob
    )

    return {
        "qualifies": qualifies,
        "expected_value": ev,
        "probability": probability,
        "odds_decimal": odds_decimal,
        "reason": (
            "OK" if qualifies else
            "EV too low" if ev < min_ev else
            "Probability too low"
        )
    }
