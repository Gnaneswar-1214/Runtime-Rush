# SQLite-compatible models
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Index, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='participant')  # 'admin' or 'participant'
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    
    created_challenges = relationship("Challenge", foreign_keys="Challenge.created_by", back_populates="creator")
    submissions = relationship("Submission", back_populates="participant")
    sessions = relationship("ParticipantSession", back_populates="participant")
    progress = relationship("UserProgress", back_populates="user", uselist=False)

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    current_level = Column(Integer, default=1)
    level1_completed = Column(Boolean, default=False)
    level2_completed = Column(Boolean, default=False)
    level3_completed = Column(Boolean, default=False)
    level1_score = Column(Integer, default=0)
    level2_score = Column(Integer, default=0)
    level3_score = Column(Integer, default=0)
    level1_time_taken = Column(Integer, default=0)  # seconds
    level2_time_taken = Column(Integer, default=0)
    level3_time_taken = Column(Integer, default=0)
    level1_submission_order = Column(Integer, default=0)  # 1st, 2nd, 3rd...
    level2_submission_order = Column(Integer, default=0)
    level3_submission_order = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="progress")

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    level = Column(Integer, default=1)  # 1, 2, or 3
    correct_solution = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_challenges")
    fragments = relationship("CodeFragment", back_populates="challenge", cascade="all, delete-orphan")
    test_cases = relationship("TestCase", back_populates="challenge", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="challenge")

class CodeFragment(Base):
    __tablename__ = "code_fragments"
    
    id = Column(String(36), primary_key=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    original_order = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    challenge = relationship("Challenge", back_populates="fragments")

class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(String(36), primary_key=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    visible = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    challenge = relationship("Challenge", back_populates="test_cases")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(String(36), primary_key=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id"), nullable=False)
    participant_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    code = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    is_correct = Column(Boolean, nullable=False)
    validation_result = Column(JSON, nullable=False)
    
    challenge = relationship("Challenge", back_populates="submissions")
    participant = relationship("User", back_populates="submissions")
    
    __table_args__ = (
        Index('idx_submissions_challenge', 'challenge_id', 'timestamp'),
        Index('idx_submissions_participant', 'participant_id', 'challenge_id'),
        Index('idx_submissions_correct', 'challenge_id', 'is_correct', 'timestamp'),
    )

class Winner(Base):
    __tablename__ = "winners"
    
    challenge_id = Column(String(36), ForeignKey("challenges.id"), primary_key=True)
    participant_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    submission_id = Column(String(36), ForeignKey("submissions.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    declared_at = Column(DateTime, server_default=func.now())

class ParticipantSession(Base):
    __tablename__ = "participant_sessions"
    
    participant_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id"), primary_key=True)
    current_code = Column(Text, nullable=False)
    last_saved = Column(DateTime, server_default=func.now())
    
    participant = relationship("User", back_populates="sessions")
