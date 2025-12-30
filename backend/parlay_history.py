from sqlalchemy.orm import Session
from models import Parlay
from uuid import UUID

def get_user_parlays(db: Session, user_id: UUID):
    return (
        db.query(Parlay)
        .filter(Parlay.user_id == user_id)
        .order_by(Parlay.created_at.desc())
        .all()
    )
