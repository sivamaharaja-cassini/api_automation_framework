# tests/test_validation.py
#Required GOREST Token
import os
import pytest

#@pytest.mark.skipif(not (os.environ.get("GOREST_TOKEN")), reason="GOREST_TOKEN not set")
#def test_gorest_missing_required_fields(http_client, gorest_token, data_manager, gorest_client):
#    headers = {"Authorization": f"Bearer {gorest_token}"}
#    payload = {"name":"John Doe"}  # missing email, gender, status
#    resp = gorest_client.request("POST", "/users", json=payload, headers=headers, test_name="test_gorest_missing_required_fields")
#    assert resp.status_code == 422
#    j = resp.json()
#    assert isinstance(j, list)
#    required_fields = {"email","gender","status"}
#    found = set([e.get("field") for e in j if "field" in e])
#    assert required_fields.issubset(found)

@pytest.mark.skipif(not (os.environ.get("GOREST_TOKEN")), reason="GOREST_TOKEN not set")
@pytest.mark.env("gorest")   # <-- Pick API here
def test_gorest_missing_required_fields(http_client, gorest_token, data_manager):
    headers = {"Authorization": f"Bearer {gorest_token}"}
    payload = {"name":"John Doe"}  # missing email, gender, status
    resp = http_client.request("POST", "/users", json=payload, headers=headers)
    assert resp.status_code == 422
    j = resp.json()
    required_fields = {"email","gender","status"}
    found = {e.get("field") for e in j if "field" in e}
    assert required_fields.issubset(found)

@pytest.mark.skipif(not (os.environ.get("GOREST_TOKEN")), reason="GOREST_TOKEN not set")
@pytest.mark.env("gorest")
def test_gorest_invalid_email_format(http_client, gorest_token, data_manager):
    headers = {"Authorization": f"Bearer {gorest_token}"}
    payload = {"name":"John Doe","email":"invalid-email-format","gender":"male","status":"active"}
    resp = http_client.request("POST", "/users", json=payload, headers=headers)
    assert resp.status_code == 422
    j = resp.json()
    assert any("email" in (e.get("field") or "") for e in j)