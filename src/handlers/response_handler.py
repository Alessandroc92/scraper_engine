"""A module that collects request handlers."""

from typing import Literal

import curl_cffi
import httpx  # type: ignore[import-not-found]
import requests  # type: ignore[import-untyped]


def response_handler(
    response_object: Literal[
        requests.Response,
        curl_cffi.Response,
        httpx.Response,
    ],
) -> dict:
    """A function that handle an HttpResponse and get back its elements.

    Args:
        response_object: (Literal[ requests.Response, curl_cffi.Response, httpx.Response]):
        a response http object which allows for different response types.

    Returns:
        dict: _description_
    """
    pass
