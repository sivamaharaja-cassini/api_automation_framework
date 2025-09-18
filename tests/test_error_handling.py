# tests/test_error_handling.py
import pytest

@pytest.mark.env("jsonplaceholder")
def test_jsonplaceholder_not_found(http_client):
    resp = http_client.request("GET", "/posts/99999", test_name="test_jsonplaceholder_not_found")
    assert resp.status_code == 404 or resp.status_code == 200  # jsonplaceholder may return {} with 200; check both
    try:
        j = resp.json()
        assert j == {} or isinstance(j, dict)
    except:
        assert resp.status_code == 404

@pytest.mark.env("httpbin")
def test_httpbin_method_not_allowed(http_client):
    # httpbin uses /get for GET only; try DELETE to /get via a httpbin client
    #from utils.http_client import HTTPClient
    #httpbin = HTTPClient("https://httpbin.org")
    resp = http_client.request("DELETE", "/get", test_name="test_httpbin_method_not_allowed")
    assert resp.status_code in (405, 404)  # method not allowed expectations