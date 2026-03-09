from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ✅ Use PostgreSQL on Railway, SQLite locally
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./runtime_rush.db")

# Fix for Railway PostgreSQL URL (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # needed for SQLite
    )
else:
    # PostgreSQL settings
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ THIS IS REQUIRED by your routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()