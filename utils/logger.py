# utils/logger.py
import logging
import json
from datetime import datetime, UTC
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(LOG_DIR / "test_framework.log")
        fmt = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger

def dump_request_response(test_name: str, req_meta: dict, resp_meta: dict):
    """
    Save request/response JSON to logs/request_resp_<test_name>_<ts>.json
    req_meta, resp_meta are dicts (url, method, headers, body, status_code, response_body, elapsed_ms)
    """
    filename = LOG_DIR / f"req_resp_{test_name}_{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')}.json"
    payload = {"request": req_meta, "response": resp_meta}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)