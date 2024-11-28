from logic.base import BaseCrawler
import asyncio
from collections import deque
from typing import Iterable, Collection
from asyncio import Future
from logic.objects.url import Url


class Crawler(BaseCrawler):

    def __init__(self, max_retries: int = 4, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def run_requests(
        self,
        *,
        urls: Collection[Url],
        user_agent: str,
        resolution: str,
        proxy_settings: dict | None = None
    ) -> list:
        """
        Send requests to the collection of urls.
        - :arg urls: Url objects to iterate over.
        """
        assert len(urls) > 0, 'There are no Url to request!'
        tasks: deque = deque()

        for url in urls:
            tasks.append(
                asyncio.create_task(
                    self.request(
                        url=url,
                        user_agent=user_agent,
                        resolution=resolution,
                        proxy_settings=proxy_settings,
                    )
                )
            )
        responses = await asyncio.gather(*tasks)
        print(responses)
        return responses
