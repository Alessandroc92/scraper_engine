import os
import tls_client


def mimic_browser_request(
    url: str, method: str, headers: dict | None = None, proxy: bool | None = None
) -> str:
    pass


def create_client_session(client_identifier: str | None = None) -> tls_client.Session:
    """_summary_

    Args:
        client_identifier (str | None, optional): _description_. Defaults to None.

    Returns:
        tls_client.Session: _description_
    """
    if not client_identifier:
        client_identifier = os.getenv("CLIENT_IDENTIFIER")
    session = tls_client.Session(
        client_identifier=client_identifier,
        random_tls_extension_order=True,
    )
    return session
