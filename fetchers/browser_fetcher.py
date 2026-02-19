"""A module that contains functions that mimic browser requests."""

import os
from typing import Literal

import curl_cffi

CLIENT_IDENTIFIER = os.getenv("CLIENT_IDENTIFIER")


def mimic_browser_request(
    url: str,
    method: Literal["GET", "POST"],
    headers: dict | None = None,
    proxy: str | None = None,
    payload: dict | None = None,
    session: curl_cffi.Session | None = None,
) -> curl_cffi.Response:
    """_A function that mimics a browser requests either in GET or POST.

    Args:
        url (str): The url that needs to be fetched.
        method (str): The CURL method (GET or POST)
        headers (dict | None, optional): Headers for the request.
        proxy (str | None, optional): Using proxy or not.
        payload (dict | None, optional): Payload for the request.
        session (curl_cffi.Session | None, optional): A curl_cffi
        session.

    Returns:
        curl_cffi.Response: The response from the requested url.
    """
    if not session:
        session = create_client_session()

    response: curl_cffi.Response
    if method == "GET":
        response = session.get(
            url=url,
            headers=headers,
            params=payload,
            proxy=proxy,
        )
    elif method == "POST":
        response = session.post(
            url=url,
            headers=headers,
            params=payload,
            proxy=proxy,
        )
    return response


def create_client_session(
    client_identifier: str | None = CLIENT_IDENTIFIER,
) -> curl_cffi.Session:
    """A function to create a curl_cffi session.

    Args:
        client_identifier (str | None, optional): The client version
        (example: chrome142).

    Returns:
        curl_cffi.Session: A curl cffi
    """
    session: curl_cffi.Session = curl_cffi.Session(
        impersonate=client_identifier  # type: ignore[arg-type]
    )
    return session
