import asyncio
from typing import TypedDict
from urllib.parse import urljoin, urlsplit
import aiohttp
import requests
from bs4 import BeautifulSoup, Tag


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    full_path = f"{parsed.netloc.lower()}{parsed.path}"
    return full_path.rstrip("/")


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_tag = soup.find("main")
    if isinstance(main_tag, Tag):
        p_tag = main_tag.find("p")
        if isinstance(p_tag, Tag):
            return p_tag.get_text(strip=True)
    p_tag = soup.find("p")
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")
        if href is not None:
            urls.append(urljoin(base_url, href))
    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    images: list[str] = []
    for img_tag in soup.find_all("img"):
        src = img_tag.get("src")
        if src is not None:
            images.append(urljoin(base_url, src))
    return images


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


def get_html(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if response.status_code >= 400:
        raise Exception(f"HTTP error: {response.status_code}")
    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"Expected text/html content-type, got: {content_type}")
    return response.text


class AsyncCrawler:
    def __init__(
        self,
        base_url: str,
        max_concurrency: int = 5,
        max_pages: int = 100,
    ):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc.lower()
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks: set[asyncio.Task] = set()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return False
            if normalized_url in self.page_data:
                return False
            return True

    async def get_html(self, url: str) -> str:
        if self.session is None:
            raise Exception("ClientSession is not initialized")
        headers = {"User-Agent": "BootCrawler/1.0"}
        async with self.session.get(url, headers=headers) as response:
            if response.status >= 400:
                raise Exception(f"HTTP error: {response.status}")
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                raise Exception(f"Expected text/html content-type, got: {content_type}")
            return await response.text()

    async def crawl_page(self, current_url: str):
        if self.should_stop:
            return

        current_domain = urlsplit(current_url).netloc.lower()
        if self.base_domain != current_domain:
            return

        normalized_current = normalize_url(current_url)
        is_new = await self.add_page_visit(normalized_current)
        if not is_new:
            return

        print(f"crawling: {current_url}")
        try:
            async with self.semaphore:
                html = await self.get_html(current_url)
        except asyncio.CancelledError:
            return
        except Exception as e:
            print(f"error crawling {current_url}: {e}")
            return

        if self.should_stop:
            return

        data = extract_page_data(html, current_url)
        async with self.lock:
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return
            self.page_data[normalized_current] = data

        tasks = []
        for next_url in data["outgoing_links"]:
            if self.should_stop:
                break
            task = asyncio.create_task(self.crawl_page(next_url))
            self.all_tasks.add(task)
            tasks.append(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(
    base_url: str,
    max_concurrency: int = 5,
    max_pages: int = 100,
) -> dict[str, PageData]:
    async with AsyncCrawler(
        base_url, max_concurrency=max_concurrency, max_pages=max_pages
    ) as crawler:
        return await crawler.crawl()
