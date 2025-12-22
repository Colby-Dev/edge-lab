from typing import List
from parlay import (
    parlay_expected_value,
    risk_adjusted_return,
    marginal_ev
)

def optimize_parlay(
        legs: List[dict],
        min_risk_adjusted: float = -0.05,
        max_legs: int = 6
):
    selected = []
    remaining = legs.copy()

    remaining.sort(
        key=lambda l: (l["probability"] * l["odds_decimal"]) - 1,
        reverse=True
    )

    if not remaining:
        return selected
    
    selected.append(remaining.pop(0))

    while remaining and len(selected) < max_legs:
        best_candidate = None
        best_score = 0

        current_probs = [l["probability"] for l in selected]
        current_odds = [l["odds_decimal"] for l in selected]

        current_risk_adj = risk_adjusted_return(current_probs, current_odds)

        for leg in remaining:
            delta_ev = marginal_ev(
                current_probs,
                current_odds,
                leg["probability"],
                leg["odds_decimal"]
            )

            new_risk_adj = risk_adjusted_return(
                current_probs + [leg["probability"]],
                current_odds + [leg["odds_decimal"]]
            )

            if delta_ev > 0 and new_risk_adj >= min_risk_adjusted:
                score = delta_ev + new_risk_adj

                if score > best_score:
                    best_score = score
                    best_candidate = leg
            
        if best_candidate:
            selected.append(best_candidate)
            remaining.remove(best_candidate)
        
        else: 
            break
        
    return selected