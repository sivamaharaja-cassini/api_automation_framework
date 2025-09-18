# tests/test_performance.py
import pytest
import time
from concurrent.futures import ThreadPoolExecutor

@pytest.mark.performance
@pytest.mark.env("jsonplaceholder")
def test_jsonplaceholder_get_single_perf(http_client):
    start = time.perf_counter()
    resp = http_client.request("GET", "/posts/1", test_name="test_jsonplaceholder_get_single_perf")
    elapsed = (time.perf_counter() - start) * 1000
    assert resp.status_code == 200
    assert elapsed < 500  # ms

@pytest.mark.performance
@pytest.mark.env("httpbin")
def test_httpbin_concurrent_delay(http_client):
    httpbin = http_client.__class__(base_url="https://httpbin.org")
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(httpbin.request, "GET", "/delay/1", test_name="test_httpbin_concurrent_delay") for _ in range(10)]
        results = [f.result(timeout=30) for f in futures]
    assert all(r.status_code == 200 for r in results)