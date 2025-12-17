import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL="postgresql://postgres.mxvjxkrhuvsckftmnizs:KwV%y?.b_weC8&U@aws-0-us-west-2.pooler.supabase.com:6543/postgres"

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
