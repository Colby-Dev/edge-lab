from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Header
from database import SessionLocal
from sqlalchemy import text
from sqlalchemy.orm import Session
from deps import get_db
from models import Odds
from probability import implied_probability, remove_vig, expected_value
from schemas import ParlayRequest
from enum import Enum
from optimizer import optimize_parlays
from schemas import ParlayRequest, SaveParlayRequest
from parlay import (
    parlay_probability,
    parlay_odds,
    parlay_expected_value,
    marginal_ev,
    parlay_variance,
    risk_adjusted_return
)
from parlay_history import get_user_parlays
from performance import roi
from auth import get_current_user


class UserTier(str, Enum):
    FREE = "free"
    PRO = "pro"

def get_user_tier(x_user_tier: str = Header(default="free")) -> UserTier:
    return UserTier(x_user_tier)

def get_current_user_id():
    # TEMP: replace with Supabase auth later
    return "00000000-0000-0000-0000-000000000000"

app = FastAPI(title="Edge Lab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-test")
def db_test():
    db = SessionLocal()
    try:
        result = db.execute(text("select 1")).fetchone()
        return {"db": result[0]}
    finally:
        db.close()

@app.get("/odds")
def get_odds(db: Session = Depends(get_db)):
    odds = db.query(Odds).limit(50).all()

    return [
        {
            "id": o.id,
            "game_id": o.game_id,
            "sportsbook_id": o.sportsbook_id,
            "market": o.market,
            "outcome": o.outcome,
            "odds_decimal": float(o.odds_decimal),
        }
        for o in odds
    ]

@app.get("/probability/{game_id}/{market}")
def get_probability(game_id: int, market: str, db: Session = Depends(get_db)):
    odds_rows = (
        db.query(Odds)
        .filter(Odds.game_id == game_id)
        .filter(Odds.market == market)
        .all()
    )

    if not odds_rows:
        return {"error": "No odds found"}

    implied_probs = [implied_probability(float(o.odds_decimal)) for o in odds_rows]
    fair_probs = remove_vig(implied_probs)

    results = []
    for o, fair_p in zip(odds_rows, fair_probs):
        ev = expected_value(fair_p, float(o.odds_decimal))
        results.append({
            "outcome": o.outcome,
            "sportsbook_id": o.sportsbook_id,
            "odds_decimal": float(o.odds_decimal),
            "implied_prob": implied_probability(float(o.odds_decimal)),
            "fair_prob": fair_p,
            "expected_value": ev
        })

    return results

@app.post("/parlay/evaluate")
def evaluate_parlay(
    payload: ParlayRequest, 
    db: Session = Depends(get_db), 
    user = (get_current_user),
    ):
        user_id = user["user_id"]
        tier = get_user_tier(db, user_id)
    
        legs = payload.legs

        if len(legs) < 1:
            return {"error": "Parlay must contain at least one leg"}

        # ---- BASIC METRICS (FREE TIER) ----
        probs = [leg.probability for leg in legs]
        odds = [leg.odds_decimal for leg in legs]

        total_prob = parlay_probability(probs)
        total_odds = parlay_odds(odds)
        ev = parlay_expected_value(probs, odds)

        response = {
            "leg_count": len(legs),
            "legs": [leg.label for leg in legs],
            "total_probability": total_prob,
            "total_odds": total_odds,
            "expected_value": ev
        }

        #----- Adv Tier -----
        if tier in ("pro", "premium"):
            response.update({
                "variance": parlay_variance(probs, odds),
                "risk_adjusted_return": risk_adjusted_return(probs, odds),
                "marginal_impacts":[
                    {
                        "label": leg.label,
                        "marginal_ev": marginal_ev(
                            probs[:i] + probs[i+1],
                            odds[:i] + odds[i+1:],
                            leg.probability,
                            leg.odds_decimal
                        )
                        
                    }
                    for i, leg in enumerate(legs)
                ]
            })

        return response

    # TEMP: hardcode user tier
    # user_tier = "free"  # later: derive from profiles table

    # if user_tier == "paid":
    #     response.update({
    #         "variance": parlay_variance(probs, odds),
    #         "risk_adjusted_return": risk_adjusted_return(probs, odds),
    #         "marginal_impacts": [
    #             {
    #                 "label": leg.label,
    #                 "marginal_ev": marginal_ev(
    #                     probs[:i] + probs[i+1:],
    #                     odds[:i] + odds[i+1:],
    #                     leg.probability,
    #                     leg.odds_decimal
    #                 )
    #             }
    #             for i, leg in enumerate(legs)
    #         ]
    #     })

    # return response
    
@app.post("/parlay/optimize")
def optimize(payload: ParlayRequest):
    legs = [
        {
            "label": leg.label,
            "probability": leg.probability,
            "odds_decimal": leg.odds_decimal
        }
        for leg in payload.legs
    ]

    suggestions = optimize_parlays(legs)

    return {
        "suggestions": suggestions
    }

@app.post("/parlay/save")
def save_parlay(payload: SaveParlayRequest, db = Depends(get_db)):

    user_id = get_current_user_id()

    db.execute(
        text("""
            insert into saved_parlays
            (user_id, legs, total_probability, total_odds, expected_value, risk_adjusted_return)
            values
            (:user_id, :legs, :tp, :to, :ev, :rar)
        """),
        {
            "user_id": user_id,
            "legs": payload.legs,
            "tp": payload.total_probability,
            "to": payload.total_odds,
            "ev": payload.expected_value,
            "rar": payload.risk_adjusted_return
        }
    )

    db.commit()

    return {"status": "saved"}

@app.get("/parlay/history")
def parlay_history(db = Depends(get_db)):
    user_id = get_current_user_id()

    rows = db.execute(
        text("""
            select *
            from saved_parlays
            where user_id = :user_id
            order by created_at desc
        """),
        {"user_id": user_id}
    ).fetchall()

    return [dict(row) for row in rows]

@app.get("/user/performance")
def user_performance(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    parlays = get_user_parlays(db, user.id)

    total_stake = sum(p.stake for p in parlays)
    total_return = sum(p.payout for p in parlays)
    total_expected = sum(p.expected_return for p in parlays)

    return {
        "roi": roi(total_stake, total_return),
        "expected_vs_actual": total_return - total_expected,
        "edge_capture": sum(p.expected_value for p in parlays) / max(len(parlays), 1),
        "parlay_count": len(parlays)
    }


# @app.post("/parlay/optimize")
# def optimize(payload: ParlayRequest):
#     legs = [leg.model_dump() for leg in payload.legs]
#     optimized = optimize_parlay(legs)
#     return {"optimized_legs": optimized}
