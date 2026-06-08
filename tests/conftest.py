import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Keep a deep copy of the original activities to restore between tests
_original_activities = copy.deepcopy(activities)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Arrange: restore in-memory activities before each test to ensure isolation."""
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
    yield
    # Teardown: restore original state after the test as well
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
