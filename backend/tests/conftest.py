import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from urllib.parse import quote_plus

# URL-encode the password to handle special characters like @
password = quote_plus("gnandow@2006")
TEST_DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/runtime_rush_test"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
