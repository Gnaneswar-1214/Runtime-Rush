"""
Simple test to verify challenge routes are properly configured.
This test checks that the routes are registered and the schemas are valid.
"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from app.routers.challenges import (
    ChallengeCreateSchema,
    ChallengeUpdateSchema,
    ChallengeResponse,
    CodeFragmentSchema,
    TestCaseSchema,
    router
)


def test_challenge_create_schema_validation():
    """Test that ChallengeCreateSchema validates correctly"""
    now = datetime.utcnow()
    
    # Valid challenge data
    data = {
        "title": "Test Challenge",
        "description": "A test challenge",
        "language": "python",
        "correct_solution": "print('test')",
        "start_time": now + timedelta(hours=1),
        "end_time": now + timedelta(hours=2),
        "fragments": [
            {"content": "print('", "original_order": 0},
            {"content": "test')", "original_order": 1}
        ],
        "test_cases": [
            {"input": "", "expected_output": "test", "visible": True}
        ]
    }
    
    schema = ChallengeCreateSchema(**data)
    assert schema.title == "Test Challenge"
    assert schema.language == "python"
    assert len(schema.fragments) == 2
    assert len(schema.test_cases) == 1


def test_challenge_update_schema_allows_partial():
    """Test that ChallengeUpdateSchema allows partial updates"""
    # Only title update
    data = {"title": "Updated Title"}
    schema = ChallengeUpdateSchema(**data)
    assert schema.title == "Updated Title"
    assert schema.description is None
    assert schema.language is None


def test_code_fragment_schema():
    """Test CodeFragmentSchema"""
    fragment = CodeFragmentSchema(content="print('hello')", original_order=0)
    assert fragment.content == "print('hello')"
    assert fragment.original_order == 0


def test_test_case_schema():
    """Test TestCaseSchema"""
    test_case = TestCaseSchema(
        input="test input",
        expected_output="test output",
        visible=True
    )
    assert test_case.input == "test input"
    assert test_case.expected_output == "test output"
    assert test_case.visible is True


def test_test_case_schema_default_visible():
    """Test TestCaseSchema default visible value"""
    test_case = TestCaseSchema(
        input="test input",
        expected_output="test output"
    )
    assert test_case.visible is True


def test_router_configuration():
    """Test that router is properly configured"""
    assert router.prefix == "/api/challenges"
    assert "challenges" in router.tags
    
    # Check that routes are registered
    route_paths = [route.path for route in router.routes]
    assert "" in route_paths  # POST and GET list
    assert "/{challenge_id}" in route_paths  # GET, PUT, DELETE by ID


def test_router_has_all_required_methods():
    """Test that all required HTTP methods are registered"""
    methods = set()
    for route in router.routes:
        methods.update(route.methods)
    
    assert "POST" in methods
    assert "GET" in methods
    assert "PUT" in methods
    assert "DELETE" in methods


def test_challenge_response_schema():
    """Test that ChallengeResponse schema is properly configured"""
    # This verifies the schema can be instantiated with the expected fields
    now = datetime.utcnow()
    
    # Note: We can't fully test this without a database object,
    # but we can verify the schema structure
    assert hasattr(ChallengeResponse, 'model_fields')
    fields = ChallengeResponse.model_fields
    
    assert 'id' in fields
    assert 'title' in fields
    assert 'description' in fields
    assert 'language' in fields
    assert 'correct_solution' in fields
    assert 'start_time' in fields
    assert 'end_time' in fields
    assert 'created_by' in fields
    assert 'created_at' in fields
    assert 'fragments' in fields
    assert 'test_cases' in fields
