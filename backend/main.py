from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from sqlalchemy import text
from sqlalchemy.orm import Session
from deps import get_db
from models import Odds

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

