from sqlalchemy import text 
from sqlalchemy.orm import Session

def get_user_tier(db: Session, user_id: str) -> str:
    row = db.execute(
        text("select plan from profiles where id = :uid"),
        {"uid": user_id}
    ).fetchone()

    return row[0] if row and row[0] else "free"