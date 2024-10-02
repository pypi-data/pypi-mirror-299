# Login / authenticate function for the girder client.
from girder_client import GirderClient


def login(
    api_url: str,
    login_or_email: str | None = None,
    password: str | None = None,
    api_key: str | None = None,
) -> GirderClient:
    """Authenticate a girder client with the given credentials or interactively
    if none is given.

    Args:
        api_url (str): The DSA girder API url.
        login_or_email (str | None): The login or email. Defaults to None.
        password (str | None): Password for login / email. Defaults to None.
        api_key (str | None): The api key to authenticate with. Defaults to None.

    Returns:
        girder_client.GirderClient: The authenticated girder client.

    """
    gc = GirderClient(apiUrl=api_url)

    if api_key is None:
        if login_or_email is None:
            _ = gc.authenticate(interactive=True)
        elif password is None:
            _ = gc.authenticate(username=login_or_email, interactive=True)
        else:
            _ = gc.authenticate(username=login_or_email, password=password)
    else:
        _ = gc.authenticate(apiKey=api_key)

    return gc
