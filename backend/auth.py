from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends, HTTPException, Header
import jwt
import os

SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")

    try:
        scheme, token = authorization.split()
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )
        return payload  # contains sub = user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

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