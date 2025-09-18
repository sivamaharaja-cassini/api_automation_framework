# tests/test_crud.py
import pytest
from utils.schema_validator import assert_response_schema

@pytest.mark.env("jsonplaceholder")
def test_jsonplaceholder_create_post(http_client):
    payload = {"title":"Test Post Title","body":"This is a test post body content for automation testing","userId":1}
    resp = http_client.request("POST", "/posts", json=payload, test_name="test_jsonplaceholder_create_post")
    assert resp.status_code == 201
    j = resp.json()
    # API returns id=101 in the assessment expectation - assert presence and types
    assert "id" in j and isinstance(j["id"], int)
    assert j["title"] == payload["title"]

@pytest.mark.env("jsonplaceholder")
def test_jsonplaceholder_get_post1(http_client):
    resp = http_client.request("GET", "/posts/1", test_name="test_jsonplaceholder_get_post1")
    assert resp.status_code == 200
    j = resp.json()
    assert isinstance(j["id"], int)
    assert isinstance(j["userId"], int)
    assert isinstance(j["title"], str)