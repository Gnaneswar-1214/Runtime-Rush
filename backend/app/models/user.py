from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), nullable=False)  # 'organizer' or 'participant'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    created_challenges = relationship("Challenge", foreign_keys="Challenge.created_by", back_populates="creator")
    submissions = relationship("Submission", back_populates="participant")
    sessions = relationship("ParticipantSession", back_populates="participant")
