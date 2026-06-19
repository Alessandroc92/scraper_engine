import asyncio

from curl_cffi import AsyncSession


class AsyncFetcher:

    def __init__(
        self,
        proxy: str| None = None,
        max_clients: int = 10,
        headers: dict | None = None,
        cookies: dict | None = None,
        timeout: int = 30,
        impersonate: str = 'chrome'
        ):
        self.proxy = proxy
        self.max_clients = max_clients
        self.headers = headers
        self.cookies = cookies
        self.impersonate = impersonate


    async def fetch_all(self, urls: list):
        async with AsyncSession(
            proxy=self.proxy,
            max_clients=self.max_clients,
            headers=self.headers,
            cookies=self.cookies,
            impersonate=self.impersonate,
            ) as session:
            tasks = [session.get(url) for url in urls]
            return await asyncio.gather(*tasks)
