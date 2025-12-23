from itertools import combinations
from typing import List
from parlay import (
    parlay_probability,
    parlay_odds,
    parlay_expected_value,
    risk_adjusted_return
)


def optimize_parlays(
    legs: List[dict],
    min_legs: int = 2,
    max_legs: int = 4,
    top_n: int = 5
):
    results = []

    for r in range(min_legs, max_legs + 1):
        for combo in combinations(legs, r):
            probs = [leg["probability"] for leg in combo]
            odds = [leg["odds_decimal"] for leg in combo]

            ev = parlay_expected_value(probs, odds)
            rar = risk_adjusted_return(probs, odds)

            results.append({
                "legs": [leg["label"] for leg in combo],
                "expected_value": ev,
                "risk_adjusted_return": rar,
                "leg_count": r
            })

    results.sort(key=lambda x: x["expected_value"], reverse=True)

    return results[:top_n]
