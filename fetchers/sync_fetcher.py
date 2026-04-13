"""A module that contains functions that mimic browser requests."""

from __future__ import annotations

import logging
import os
from typing import Any, Literal, Protocol

import curl_cffi
from loggers.configs import setup_logging
from handlers.response_handler import HttpResponse

CLIENT_IDENTIFIER = os.getenv("CLIENT_IDENTIFIER")
setup_logging.create_dictconfig()
logger = logging.getLogger(__name__)


class SyncFetcher:
    """A Class that creates objects to make sync web requests.

    SyncFetcher expects a session implementing HttpSession.
    Use adapters for third-party libraries.
    """

    def __init__(
        self,
        proxy: str | None = None,
        session: HttpSession | None = None,
    ):
        self.proxy = proxy
        self.session = session or self._default_session()

    def _default_session(self) -> HttpSession:
        """An internal methdo to create the default client session.

        Returns:
            HttpClientSession: An HTTP Client Session.
        """
        return CurlCffiAdapter(session=curl_cffi.Session(impersonate=CLIENT_IDENTIFIER))

    def request(
        self,
        url: str,
        method: Literal["get", "post", "delete", "put"],
        headers: dict | None = None,
        proxy: str | None = None,
        params: dict | None = None,
        payload: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        """A function that mimics a browser requests.

        Args:
            url (str): The url that needs to be fetched.
            method (str): The CURL method (get or post)
            headers (dict | None, optional): Headers for the request.
            proxy (str | None, optional): Using proxy or not.
            params (str | None, optional): Params for the request.
            payload (dict | None, optional): Payload for the request.
            session (HttpClientSession | None, optional): A curl_cffi
            session.

        Returns:
            HttpResponse: The response from the requested url.
        """
        logger.debug('Incoming Request',extra={'url':url})
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=payload,
            proxy=proxy or self.proxy,
        )
        return response


class HttpSession(Protocol):
    def request(self, method: str, url: str, **kwargs: Any) -> Any: ...


class CurlCffiAdapter:
    def __init__(self, session):
        self.session = session

    def request(self, method: str, url: str, proxy=None, **kwargs: Any) -> Any:
        method = method.strip().lower()
        if method not in ["get", "post", "delete", "put"]:
            raise ValueError(f"The method={method} your requested is not allowed.")
        if proxy:
            kwargs["proxy"] = proxy
        request_attribute = getattr(self.session, method)
        response = request_attribute(url=url, **kwargs)
        return response


class RequestsAdapter:
    def __init__(self, session):
        self.session = session

    def request(self, method: str, url: str, proxy=None, **kwargs: Any) -> Any:
        method = method.strip().lower()
        if method not in ["get", "post", "delete", "put"]:
            raise ValueError(f"The method={method} your requested is not allowed.")
        if proxy:
            kwargs["proxies"] = {"http": proxy, "https": proxy}
        request_attribute = getattr(self.session, method)
        response = request_attribute(url=url, **kwargs)
        return response
