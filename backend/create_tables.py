from app.database import engine, Base
from app.models_sqlite import Challenge, CodeFragment, TestCase, Submission, Winner, ParticipantSession, User, UserProgress

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
