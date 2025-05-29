from unittest.mock import patch


def test_root_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Furniture Search API"}


def test_search_endpoint(test_client, mock_search_service, sample_furniture_item):
    with patch("app.main.search_service", mock_search_service):
        mock_search_service.search.return_value = [sample_furniture_item]

        response = test_client.post(
            "/search",
            params={
                "query": "sofa",
                "category": "living room",
                "min_price": 1000,
                "max_price": 2000,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "filters" in data
        assert "results" in data
        assert "total" in data
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == sample_furniture_item["id"]
