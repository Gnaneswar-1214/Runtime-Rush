from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Winner(Base):
    __tablename__ = "winners"
    
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), primary_key=True)
    participant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    declared_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    challenge = relationship("Challenge", back_populates="winner")
    participant = relationship("User")
    submission = relationship("Submission")
