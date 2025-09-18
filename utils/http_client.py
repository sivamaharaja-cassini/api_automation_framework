# utils/http_client.py
import requests
from requests.adapters import HTTPAdapter, Retry
from utils.logger import get_logger, dump_request_response
from tenacity import retry, stop_after_attempt, wait_exponential
import uuid
import time

logger = get_logger("http_client")

class HTTPClient:
    def __init__(self, base_url: str, timeout: int = 10, retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(total=retries, backoff_factor=0.3,
                                               status_forcelist=[429, 500, 502, 503, 504],
                                               allowed_methods=["GET","POST","PUT","PATCH","DELETE"]))
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.timeout = timeout

    def _full_url(self, path: str):
        return f"{self.base_url}/{path.lstrip('/')}"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4))
    def request(self, method: str, path: str, **kwargs):
        # ✅ Extract and remove test_name before calling requests
        test_name = kwargs.pop("test_name", "unknown")

        req_id = str(uuid.uuid4())
        url = self._full_url(path)
        start = time.perf_counter()

        # ✅ Only pass real kwargs (without test_name) to requests
        resp = self.session.request(method=method, url=url, timeout=self.timeout, **kwargs)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        # Logging metadata
        req_meta = {
            "id": req_id,
            "method": method,
            "url": url,
            "headers": dict(resp.request.headers),
            "body": kwargs.get("json") or kwargs.get("data")
        }

        try:
            resp_body = resp.json()
        except Exception:
            resp_body = resp.text

        resp_meta = {
            "id": req_id,
            "status_code": resp.status_code,
            "elapsed_ms": elapsed_ms,
            "headers": dict(resp.headers),
            "body": resp_body
        }

        # ✅ Use the extracted test_name for logging
        dump_request_response(test_name=test_name, req_meta=req_meta, resp_meta=resp_meta)

        logger.info("%s %s -> %s (%sms)", method, url, resp.status_code, elapsed_ms)
        return resp