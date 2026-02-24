from sqlalchemy import Column, Text, DateTime, Boolean, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False)
    participant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    code = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_correct = Column(Boolean, nullable=False)
    validation_result = Column(JSON, nullable=False)
    
    # Relationships
    challenge = relationship("Challenge", back_populates="submissions")
    participant = relationship("User", back_populates="submissions")
    
    # Indexes
    __table_args__ = (
        Index('idx_submissions_challenge', 'challenge_id', 'timestamp'),
        Index('idx_submissions_participant', 'participant_id', 'challenge_id'),
        Index('idx_submissions_correct', 'challenge_id', 'is_correct', 'timestamp'),
    )
