"""
Simple test to verify submission routes are properly configured.
This test checks that the routes are registered and the schemas are valid.
"""
import pytest
from uuid import uuid4

from app.routers.submissions import (
    SubmissionCreateSchema,
    SubmissionResponse,
    router
)


def test_submission_create_schema_validation():
    """Test that SubmissionCreateSchema validates correctly"""
    participant_id = uuid4()
    
    data = {
        "code": "print('hello world')",
        "participant_id": participant_id
    }
    
    schema = SubmissionCreateSchema(**data)
    assert schema.code == "print('hello world')"
    assert schema.participant_id == participant_id


def test_submission_create_schema_requires_code():
    """Test that code is required"""
    with pytest.raises(Exception):  # Pydantic validation error
        SubmissionCreateSchema(participant_id=uuid4())


def test_submission_create_schema_requires_participant_id():
    """Test that participant_id is required"""
    with pytest.raises(Exception):  # Pydantic validation error
        SubmissionCreateSchema(code="print('test')")


def test_submission_response_schema():
    """Test that SubmissionResponse schema is properly configured"""
    assert hasattr(SubmissionResponse, 'model_fields')
    fields = SubmissionResponse.model_fields
    
    assert 'id' in fields
    assert 'challenge_id' in fields
    assert 'participant_id' in fields
    assert 'code' in fields
    assert 'timestamp' in fields
    assert 'is_correct' in fields
    assert 'validation_result' in fields


def test_router_configuration():
    """Test that router is properly configured"""
    assert router.prefix == "/api"
    assert "submissions" in router.tags
    
    # Check that routes are registered
    route_paths = [route.path for route in router.routes]
    assert "/challenges/{challenge_id}/submit" in route_paths
    assert "/submissions/{submission_id}" in route_paths
    assert "/challenges/{challenge_id}/submissions" in route_paths
    assert "/participants/{participant_id}/submissions" in route_paths


def test_router_has_required_methods():
    """Test that required HTTP methods are registered"""
    methods = set()
    for route in router.routes:
        methods.update(route.methods)
    
    assert "POST" in methods
    assert "GET" in methods


def test_submit_endpoint_path():
    """Test that submit endpoint has correct path"""
    submit_routes = [r for r in router.routes if "submit" in r.path]
    assert len(submit_routes) == 1
    assert submit_routes[0].path == "/challenges/{challenge_id}/submit"
    assert "POST" in submit_routes[0].methods


def test_get_submission_endpoint_path():
    """Test that get submission endpoint has correct path"""
    get_routes = [r for r in router.routes if r.path == "/submissions/{submission_id}"]
    assert len(get_routes) == 1
    assert "GET" in get_routes[0].methods


def test_get_challenge_submissions_endpoint_path():
    """Test that get challenge submissions endpoint has correct path"""
    routes = [r for r in router.routes if r.path == "/challenges/{challenge_id}/submissions"]
    assert len(routes) == 1
    assert "GET" in routes[0].methods


def test_get_participant_submissions_endpoint_path():
    """Test that get participant submissions endpoint has correct path"""
    routes = [r for r in router.routes if r.path == "/participants/{participant_id}/submissions"]
    assert len(routes) == 1
    assert "GET" in routes[0].methods
