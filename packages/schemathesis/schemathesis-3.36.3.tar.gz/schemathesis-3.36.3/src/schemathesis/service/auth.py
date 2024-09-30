from . import metadata
from .constants import DEFAULT_HOSTNAME, DEFAULT_PROTOCOL


def login(token: str, hostname: str = DEFAULT_HOSTNAME, protocol: str = DEFAULT_PROTOCOL, verify: bool = True) -> str:
    from .client import ServiceClient

    """Make a login request to SaaS."""
    client = ServiceClient(f"{protocol}://{hostname}", token, verify=verify)
    response = client.login(metadata=metadata.Metadata())
    return response.username
