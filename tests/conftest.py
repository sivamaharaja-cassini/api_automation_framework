# tests/conftest.py
import pytest
import yaml
from utils.http_client import HTTPClient
from utils.logger import get_logger
from utils.data_manager import DataManager
from dotenv import load_dotenv
import os

logger = get_logger("conftest")
load_dotenv()  # take environment variables from .env.

def pytest_configure(config):
    token = os.getenv("GOREST_TOKEN")
    if not token:
        config.addinivalue_line(
            "markers", "gorest: mark test requiring GOREST_TOKEN"
        )


#def load_config():
#    with open("config/config.yaml", "r", encoding="utf-8") as f:
#        return yaml.safe_load(f)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="session")
def envs(config):
    return config["envs"]

@pytest.fixture(scope="session")
def env(request, config):
    # choose environment via CLI -E or env var TEST_ENV
    env_name = os.environ.get("TEST_ENV") or request.config.getoption("--env") or config.get("default_env")
    if env_name not in config["envs"]:
        raise RuntimeError(f"Unknown environment: {env_name}")
    return { "name": env_name, **config["envs"][env_name] }

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Environment to run tests against")

@pytest.fixture
def http_client(request, envs, config):
    # Priority: test marker → CLI (--env) → TEST_ENV → default_env
    marker = request.node.get_closest_marker("env")
    if marker:
        env_name = marker.args[0]
    else:
        env_name = (
            request.config.getoption("--env")
            or os.environ.get("TEST_ENV")
            or config.get("default_env")
        )

    if env_name not in envs:
        raise RuntimeError(f"Unknown environment: {env_name}")
    return HTTPClient(base_url=envs[env_name]["base_url"])

#@pytest.fixture(scope="session")
#def http_client(env):
#    client = HTTPClient(base_url=env["base_url"])
#    #client = HTTPClient(base_url="https://reqres.in/api")
#    return client

#@pytest.fixture(scope="session")
#def gorest_client(envs):
#    from utils.http_client import HTTPClient
#    return HTTPClient(base_url=envs["gorest"]["base_url"])

#@pytest.fixture(scope="session")
#def jsonplaceholder_client(envs):
#    from utils.http_client import HTTPClient
#    return HTTPClient(base_url=envs["jsonplaceholder"]["base_url"])

@pytest.fixture(scope="session")
def gorest_token():
    # expects token in env var GOREST_TOKEN (per config)
    return os.environ.get("GOREST_TOKEN")

@pytest.fixture
def data_manager():
    dm = DataManager()
    yield dm
    errs = dm.cleanup()
    if errs:
        logger.warning("Errors during data cleanup: %s", errs)

# helper to attach test name to client requests
@pytest.fixture(autouse=True)
def attach_test_name(request):
    test_name = request.node.name
    # yield so tests can run
    yield
    # after test finishes: nothing extra here; logs already saved per request.