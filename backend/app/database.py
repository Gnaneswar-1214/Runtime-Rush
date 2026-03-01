from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ SQLite database (works on Railway)
DATABASE_URL = "sqlite:///./runtime_rush.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ THIS IS REQUIRED by your routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()