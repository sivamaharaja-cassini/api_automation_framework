# tests/test_auth.py
import pytest
from utils.schema_validator import assert_response_schema

@pytest.mark.env("httpbin")
@pytest.mark.parametrize("payload", [
    {"username": "alice", "password": "wonderland"},
    {"username": "bob", "password": "builder"},
])
def test_httpbin_post_login_success(http_client, payload):
    """
    Test POST /post with login-like payloads
    httpbin echoes the JSON back under 'json'
    """
    resp = http_client.request(
        "POST",
        "/post",
        json=payload,
        test_name="test_httpbin_post_login_success"
    )
    assert resp.status_code == 200
    j = resp.json()
    assert j["json"] == payload


@pytest.mark.env("httpbin")
def test_httpbin_post_missing_password(http_client):
    """
    Simulate a login attempt with missing password
    """
    payload = {"username": "alice"}
    resp = http_client.request(
        "POST",
        "/post",
        json=payload,
        test_name="test_httpbin_post_missing_password"
    )
    assert resp.status_code == 200
    j = resp.json()
    # httpbin won’t validate, it just echoes back
    # So we check that password is missing in echoed payload
    assert "password" not in j["json"]
    assert j["json"]["username"] == "alice"


@pytest.mark.skip(reason="/login endpoint is deprecated")
@pytest.mark.env("requires")
@pytest.mark.parametrize("payload, expected_status", [
    ({"email":"eve.holt@reqres.in","password":"cityslicka"}, 200),
    ({"email":"eve.holt@reqres.in","password":"wrongpassword"}, 400),
])
def test_reqres_login_variants(http_client, payload, expected_status):
    resp = http_client.request("POST", "/login", json=payload, test_name="test_reqres_login_variants")
    assert resp.status_code == expected_status
    j = None
    try:
        j = resp.json()
    except:
        pytest.skip("Non-json response")
    if expected_status == 200:
        assert "token" in j and isinstance(j["token"], str) and j["token"].strip() != ""
    else:
        assert "error" in j or "error" in str(j)

@pytest.mark.skip(reason="/login endpoint is deprecated")
@pytest.mark.env("requires")
def test_reqres_missing_password(http_client):
    resp = http_client.request("POST", "/login", json={"email":"eve.holt@reqres.in"}, test_name="test_reqres_missing_password")
    assert resp.status_code == 400
    j = resp.json()
    assert "error" in j and "Missing" in str(j["error"])