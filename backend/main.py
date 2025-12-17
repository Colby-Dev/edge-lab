from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy import text
from sqlalchemy.orm import Session
from deps import get_db
from models import Odds
from probability import implied_probability, remove_vig, expected_value


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


##Comment to check RW