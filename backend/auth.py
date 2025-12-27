from sqlalchemy.orm import Session
from sqlalchemy import text

def get_user_plan(db: Session, user_id: str) -> str:
    result = db.execute(
        text("SELECT plan FROM profiles WHERE id = :uid"),
        {"uid": user_id}
    ).fetchone()

    if not result:
        return "free"

    return result[0]

def increment_api_usage(db: Session, user_id: str):
    db.execute(
        text("""
        UPDATE profiles
        SET api_calls = COALESCE(api_calls, 0) + 1
        WHERE id = :uid
        """),
        {"uid": user_id}
    )
    db.commit()