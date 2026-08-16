from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag


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
