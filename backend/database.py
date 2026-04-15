from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres.isfrghjgbqsygpigvicz:ifvBlt56UClJxbtm@aws-1-us-east-1.pooler.supabase.com:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()