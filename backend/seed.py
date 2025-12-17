from database import SessionLocal
from models import Sportsbook, Game, Odds
from datetime import datetime

db = SessionLocal()

# Create sportsbook
dk = Sportsbook(name="DraftKings")
fd = Sportsbook(name="FanDuel")

db.add_all([dk, fd])
db.commit()

# Create game
game = Game(
    sport="NBA",
    home_team="Lakers",
    away_team="Celtics",
    start_time=datetime.utcnow()
)

db.add(game)
db.commit()

# Create odds
odds = [
    Odds(
        game_id=game.id,
        sportsbook_id=dk.id,
        market="moneyline",
        outcome="Lakers",
        odds_decimal=1.91
    ),
    Odds(
        game_id=game.id,
        sportsbook_id=fd.id,
        market="moneyline",
        outcome="Lakers",
        odds_decimal=1.95
    ),
]

db.add_all(odds)
db.commit()

db.close()

print("Seed data inserted")
