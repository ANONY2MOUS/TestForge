import pytest
from api.utils.helpers import (
    assert_status,
    assert_headers_present,
    assert_json_field,
    assert_response_time,
)

class TestGetUser:
    def test_get_valid_user_returns_200(self, api_client, schema_validator, known_users):
        response = api_client.get(f"/users/{known_users['valid']}")
        assert_status(response, 200)
        schema_validator.validate(response.json(), "user_schema.json")

    def test_valid_user_login_matches_requested_username(self, api_client, known_users):
        username = known_users["valid"]
        response = api_client.get(f"/users/{username}")
        assert_status(response, 200)
        data = response.json()
        assert data["login"].lower() == username.lower()

    def test_valid_user_has_positive_id(self, api_client, known_users):
        response = api_client.get(f"/users/{known_users['valid']}")
        assert_status(response, 200)
        assert_json_field(response.json(), "id", field_type=int, min_value=1)

    def test_response_includes_rate_limit_headers(self, api_client, known_users):
        response = api_client.get(f"/users/{known_users['valid']}")
        assert_headers_present(response, [
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
        ])

    def test_user_endpoint_responds_within_3_seconds(self, api_client, known_users):
        response = api_client.get(f"/users/{known_users['valid']}")
        assert_status(response, 200)
        assert_response_time(response, max_ms=3000)

    def test_nonexistent_user_returns_404(self, api_client, known_users):
        response = api_client.get(f"/users/{known_users['nonexistent']}")
        assert_status(response, 404)

    def test_list_users_returns_200(self, api_client):
        response = api_client.get("/users", params={"per_page": 10})
        assert_status(response, 200)

    def test_list_users_returns_array(self, api_client):
        response = api_client.get("/users", params={"per_page": 10})
        assert_status(response, 200)
        data = response.json()
        assert isinstance(data, list)

    def test_list_users_respects_per_page_param(self, api_client):
        response = api_client.get("/users", params={"per_page": 5})
        assert_status(response, 200)
        data = response.json()
        assert len(data) == 5
