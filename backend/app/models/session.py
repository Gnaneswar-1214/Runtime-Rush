from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ParticipantSession(Base):
    __tablename__ = "participant_sessions"
    
    participant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), primary_key=True)
    current_code = Column(Text, nullable=False)
    last_saved = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    participant = relationship("User", back_populates="sessions")
    challenge = relationship("Challenge", back_populates="sessions")
