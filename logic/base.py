import asyncio
from logging import Logger
from urllib.parse import urlsplit

from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from playwright.async_api import async_playwright

from logic.log import logger
from logic.objects.url import Url


class BaseCrawler:
    """
    Base crawler class containing logic for data extracting while crawling domains.
    Each spider inheriting from this class expects to receive UserAgent and Proxy,
    as well as initial Url object.
    """
    def __init__(
        self,
        root_url: Url,
        headless: bool = False,
    ) -> None:
        self.root_url: Url = root_url
        self.headless: bool = headless
        self.logger: Logger = logger
        self._domain: str | None = None

    @property
    def domain(self) -> str:
        """
        Set domain from `initial_url.
        """
        if self._domain is None:
            self._domain = urlsplit(self.root_url.value).netloc
        return self._domain

    @staticmethod
    def viewport(*, resolution: str):
        """
        Set a viewport for next request.
        """
        resolution_params = resolution.split('x')
        return {'width': int(resolution_params[0]), 'height': int(resolution_params[1])}

    @staticmethod
    def html(*, page_source: str, base_url: str) -> HtmlElement | None:
        """
        Parse page source and return HtmlElement on success.
        - :arg page_source: Result of page.content()
        - :arg base_url: Current url
        """
        try:
            hp = HTMLParser(encoding='utf-8')
            element: HtmlElement = fromstring(
                page_source,
                parser=hp,
                base_url=base_url,
            )
            return element
        except Exception:
            return None

    @staticmethod
    def extract_urls_with_texts(html_element: HtmlElement) -> list[dict[str, str]] | None:
        """
        Search for urls in body of provided HtmlElement.
        - :arg html_element: Lxml HtmlElement representing <body> of current webpage.
        """
        urls: list[HtmlElement] = html_element.xpath('/html/body//a[@href and not(@href="") and not(@href=" ")]')
        return [
            {'value': url.xpath('./@href')[0], 'anchor': url.text_content().strip()} for url in urls
        ] if urls else None

    async def parse_page(self, html: HtmlElement) -> dict | None:
        """"""
        await asyncio.sleep(10)
        print(f'parse: {html.base_url}')
        return

    async def request(
        self,
        *,
        url: Url,
        user_agent: str,
        resolution: str,
        proxy_settings: dict | None = None):
        """
        Send request to specified url.
        Parse page and return dictionary with url object and
        a result of calling a parse_page method on requested page.
        :param url: Url object that will be requested.
        :param user_agent: UserAgent that will be used for this request.
        :param resolution: String representing a resolution ie: `1920x1080`
        :param proxy_settings: Additional proxy settings if request should be made with proxy.
        :return: Dictionary with keys `url` and `result`.
        """
        try:
            async with async_playwright() as pw:
                # Increase number of requests on the Url object.
                url.number_of_requests += 1

                # Prepare browser initial parameters
                launch_params = {'headless': self.headless}
                if proxy_settings is not None:
                    launch_params['proxy'] = proxy_settings

                # Launch browser.
                browser = await pw.chromium.launch(
                    headless=self.headless
                )

                # Prepare and start new context.
                viewport = self.viewport(resolution=resolution)
                context = await browser.new_context(
                    viewport=viewport,
                    user_agent=user_agent,
                )
                page = await  context.new_page()

                # Navigate to a website
                await page.goto(url.value, wait_until='domcontentloaded')

                # Prepare lxml HtmlElement and do whatever you want with it.
                html = self.html(page_source=await page.content(), base_url=page.url)

                return {'url': Url, 'result': await self.parse_page(html=html)}
        except Exception as exc:
            self.logger.error(
                f'({self.request.__qualname__}): exception="{exc.__class__}", '
                f'message="{exc}", url="{url.value}"', exc_info=True
            )
            return {'url': Url, 'result': None}
