from unittest.mock import Mock, patch

import pytest

from app.services.search_service import SearchService


@pytest.mark.asyncio
async def test_search_success(test_settings):
    """Test successful search operation."""
    with patch("app.core.config.get_settings", return_value=test_settings), patch(
        "app.services.search_service.SearchClient"
    ) as mock_client_class:
        # Setup mock
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        # Create mock search results that mimic Azure Search's iterator
        mock_results = [
            {"id": "test-1", "name": "Test Item 1"},
            {"id": "test-2", "name": "Test Item 2"},
        ]
        # Create an iterator that yields our mock results
        mock_iterator = iter(mock_results)
        mock_client.search.return_value = mock_iterator

        # Create service instance
        service = SearchService()

        # Perform search
        results = await service.search("test query")

        # Assertions
        assert len(results) == 2
        assert results[0]["id"] == "test-1"
        assert results[1]["id"] == "test-2"
        mock_client.search.assert_called_once()


@pytest.mark.asyncio
async def test_search_with_filters(test_settings):
    """Test search with filter parameters."""
    with patch("app.core.config.get_settings", return_value=test_settings), patch(
        "app.services.search_service.SearchClient"
    ) as mock_client_class:
        # Setup mock
        mock_client = mock_client_class.return_value
        mock_results = [{"id": "test-1", "name": "Test Item 1"}]
        mock_client.search.return_value = iter(mock_results)

        # Create service instance
        service = SearchService()

        # Perform search with filters
        results = await service.search(
            query="test query", filters="category eq 'sofa'", top=5, skip=0
        )

        # Assertions
        assert len(results) == 1
        assert results[0]["id"] == "test-1"
        mock_client.search.assert_called_once()


@pytest.mark.asyncio
async def test_search_error_handling(test_settings):
    """Test search error handling."""
    with patch("app.core.config.get_settings", return_value=test_settings), patch(
        "app.services.search_service.SearchClient"
    ) as mock_client_class:
        # Setup mock to raise an exception
        mock_client = mock_client_class.return_value
        mock_client.search.side_effect = Exception("Search failed")

        # Create service instance
        service = SearchService()

        # Perform search
        results = await service.search("test query")

        # Assertions
        assert len(results) == 0  # Should return empty list on error
        mock_client.search.assert_called_once()
