import asyncio
from collections import deque
from typing import Collection

from logic.base import BaseCrawler
from logic.objects.url import Url


class Crawler(BaseCrawler):

    def __init__(
        self,
        urls_to_crawl: Collection[Url],
        sleep_time: float | int,
        max_retries: int = 4,
        *args,
        **kwargs
    ) -> None:
        self.urls_to_crawl: Collection[Url] = urls_to_crawl
        self.sleep_time: float | int = sleep_time
        self.max_retries: int = max_retries
        self.queue: deque[Url] = deque()
        self.found_internal_urls: set[Url] = set()
        self.requested_urls: set[Url] = set()
        self.external_domains: set[Url] = set()
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
        assert len(urls) > 0, 'There are no Urls to request!'
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
