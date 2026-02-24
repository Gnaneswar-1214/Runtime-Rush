from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models import ParticipantSession
from uuid import UUID


class SessionManager:
    """Manages participant session operations with auto-save functionality"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_session(
        self, 
        participant_id: UUID, 
        challenge_id: UUID, 
        current_code: str
    ) -> ParticipantSession:
        """
        Save or update a participant session using upsert logic.
        
        This method uses PostgreSQL's INSERT ... ON CONFLICT UPDATE to handle
        concurrent saves gracefully. If a session already exists for the
        participant-challenge pair, it updates the code and timestamp.
        
        Args:
            participant_id: UUID of the participant
            challenge_id: UUID of the challenge
            current_code: The current code content to save
            
        Returns:
            ParticipantSession object with saved data
        """
        # Use PostgreSQL upsert (INSERT ... ON CONFLICT UPDATE)
        stmt = insert(ParticipantSession).values(
            participant_id=participant_id,
            challenge_id=challenge_id,
            current_code=current_code,
            last_saved=datetime.now(timezone.utc)
        ).on_conflict_do_update(
            index_elements=['participant_id', 'challenge_id'],
            set_={
                'current_code': current_code,
                'last_saved': datetime.now(timezone.utc)
            }
        )
        
        self.db.execute(stmt)
        self.db.commit()
        
        # Retrieve and return the saved session
        session = self.get_session(participant_id, challenge_id)
        return session
    
    def get_session(
        self, 
        participant_id: UUID, 
        challenge_id: UUID
    ) -> Optional[ParticipantSession]:
        """
        Retrieve a participant session.
        
        Args:
            participant_id: UUID of the participant
            challenge_id: UUID of the challenge
            
        Returns:
            ParticipantSession object or None if not found
        """
        return (
            self.db.query(ParticipantSession)
            .filter(
                ParticipantSession.participant_id == participant_id,
                ParticipantSession.challenge_id == challenge_id
            )
            .first()
        )
    
    def auto_save(
        self, 
        participant_id: UUID, 
        challenge_id: UUID, 
        code: str
    ) -> ParticipantSession:
        """
        Auto-save participant code during active editing.
        
        This is a convenience method that wraps save_session for use in
        background auto-save tasks. It provides the same upsert behavior.
        
        Args:
            participant_id: UUID of the participant
            challenge_id: UUID of the challenge
            code: The current code content to auto-save
            
        Returns:
            ParticipantSession object with saved data
        """
        return self.save_session(participant_id, challenge_id, code)
