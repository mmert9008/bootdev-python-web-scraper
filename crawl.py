from urllib.parse import urlsplit
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
