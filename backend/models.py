from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Sportsbook(Base):
    __tablename__ = "sportsbooks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    sport = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)


class Odds(Base):
    __tablename__ = "odds"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    sportsbook_id = Column(Integer, ForeignKey("sportsbooks.id"))
    market = Column(String, nullable=False)
    outcome = Column(String, nullable=False)
    odds_decimal = Column(Numeric, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
