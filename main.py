from logic.base import BaseCrawler
from logic.crawler import Crawler
from logic.config import USER_AGENTS, RESOLUTIONS
import asyncio
from logic.objects.url import Url


def create_urls_collection(urls):
    return [Url(value=url) for url in urls]

def create_url(url):
    return Url(value=url)

if __name__ == '__main__':
    # proxy_config = {
    #     "server": "http://your-proxy-server:port",
    #     "username": "your-username",  # Optional, remove if not required
    #     "password": "your-password"  # Optional, remove if not required
    # }

    test_url = 'https://meowbaby.eu/'
    test_urls = [
        'https://meowbaby.eu/pl/c/Sofy-i-Pufy/284',
        'https://meowbaby.eu/PL-Suche-Baseny',
        'https://meowbaby.eu/pl/c/Zabawki-Montessori/224',
        'https://meowbaby.eu/pl/c/Misie/330',
        'https://meowbaby.eu/PL-Akcesoria',
        'https://meowbaby.eu/pl/c/Skomponuj-Zestaw/245',
    ]


    url_root = create_url(test_url)
    urls_to_crawl = create_urls_collection(urls=test_urls)

    crawler = Crawler(root_url=url_root, sleep_time=2, urls_to_crawl=urls_to_crawl)

    asyncio.run(
        crawler.run_requests(
            urls=urls_to_crawl,
            user_agent=USER_AGENTS[2],
            resolution=RESOLUTIONS[0]
        )
    )