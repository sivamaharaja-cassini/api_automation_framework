# features/environment.py
from utils.http_client import HTTPClient

def before_feature(context, feature):
    """
    Hook that runs before each feature file.
    Here you can set up shared things like the API client.
    """
    if "ReqRes" in feature.name:
        context.base_url = "https://reqres.in/api"
    else:
        context.base_url = "https://jsonplaceholder.typicode.com"

    # Create an HTTP client instance for the feature
    context.client = HTTPClient(context.base_url)

def after_feature(context, feature):
    """
    Hook that runs after each feature.
    Could be used for cleanup if needed.
    """
    pass
