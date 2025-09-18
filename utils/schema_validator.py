# utils/schema_validator.py
from jsonschema import validate, ValidationError
import json
from pathlib import Path

SCHEMAS_DIR = Path("schemas")

def load_schema(name: str):
    p = SCHEMAS_DIR / name
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def assert_response_schema(response_json: dict, schema_name: str):
    schema = load_schema(schema_name)
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")