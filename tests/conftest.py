from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app
from app.services.search_service import SearchService


@pytest.fixture
def test_settings():
    """Create test settings for Azure services."""
    return Settings(
        azure_search_service_name="testsearchservice",
        azure_search_api_key="test-key",
        azure_search_index_name="test-index",
        azure_storage_connection_string="test-connection",
        azure_vision_key="test-vision-key",
        azure_vision_endpoint="https://test-vision.cognitiveservices.azure.com/",
    )


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_search_service():
    """Create a mock search service for testing."""
    mock_service = Mock(spec=SearchService)
    return mock_service


@pytest.fixture
def sample_furniture_item():
    """Create a sample furniture item for testing."""
    return {
        "id": "test-001",
        "name": "Test Sofa",
        "description": "A comfortable test sofa",
        "category": "sofa",
        "style": "modern",
        "color": "brown",
        "material": "leather",
        "price": 1299.99,
        "dimensions": {"length": 220, "width": 90, "height": 85, "unit": "cm"},
        "images": ["https://example.com/sofa1.jpg"],
        "features": ["reclining", "storage"],
        "availability": True,
        "rating": 4.5,
        "reviews": 120,
        "brand": "FurnitureCo",
        "warranty": "2 years",
        "assembly_required": False,
        "weight": 150.0,
        "shipping_info": {
            "country": "US",
            "state": "CA",
            "city": "San Francisco",
            "zip": "94103",
            "address": "123 Main St",
        },
        "tags": ["living room", "leather", "modern"],
    }
