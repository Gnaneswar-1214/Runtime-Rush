"""Basic setup verification tests"""
import pytest
from app.database import Base, engine
from app.models import User, Challenge, CodeFragment, TestCase, Submission, Winner, ParticipantSession


def test_database_models_import():
    """Verify all database models can be imported"""
    assert User is not None
    assert Challenge is not None
    assert CodeFragment is not None
    assert TestCase is not None
    assert Submission is not None
    assert Winner is not None
    assert ParticipantSession is not None


def test_database_base_metadata():
    """Verify database metadata is properly configured"""
    assert Base.metadata is not None
    tables = Base.metadata.tables
    
    # Verify all expected tables are registered
    expected_tables = {
        'users',
        'challenges',
        'code_fragments',
        'test_cases',
        'submissions',
        'winners',
        'participant_sessions'
    }
    
    assert expected_tables.issubset(set(tables.keys()))


def test_config_loads():
    """Verify configuration loads properly"""
    from app.config import settings
    
    assert settings.database_url is not None
    assert settings.redis_url is not None
    assert settings.secret_key is not None
