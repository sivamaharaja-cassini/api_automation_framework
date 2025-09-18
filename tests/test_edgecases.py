# tests/test_edgecases.py
import pytest

@pytest.mark.env("requires")
def test_empty_request_body_users(http_client):
    resp = http_client.request("POST", "/users", json={}, test_name="test_empty_request_body_users")
    # For many services this maps to 400/422; assert not 2xx
    assert resp.status_code >= 400

@pytest.mark.env("jsonplaceholder")
def test_unicode_and_special_characters_jsonplaceholder(http_client):
    payload = {"email":"josé@müller.com","first_name":"José","last_name":"muller"}
    resp = http_client.request("POST", "/users", json=payload, test_name="test_unicode_special_chars_jsonplaceholder")
    assert resp.status_code == 201
    j = resp.json()
    assert "José" in j.get("title", "") or "José" in str(j)