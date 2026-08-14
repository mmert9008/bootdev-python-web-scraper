from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    full_path = f"{parsed.netloc.lower()}{parsed.path}"
    return full_path.rstrip("/")
