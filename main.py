import asyncio
import sys
from crawl import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) < 4:
        print("missing required arguments: max_concurrency and max_pages")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    try:
        max_concurrency = int(sys.argv[2])
        max_pages = int(sys.argv[3])
    except ValueError:
        print("max_concurrency and max_pages must be integers")
        sys.exit(1)

    print(f"starting crawl of: {base_url}")
    page_data = await crawl_site_async(
        base_url, max_concurrency=max_concurrency, max_pages=max_pages
    )

    print(f"\nCrawling complete! Found {len(page_data)} page(s):\n")
    for data in page_data.values():
        if data is None:
            continue
        print(f"URL: {data['url']}")
        print(f"  Heading: {data['heading']}")
        print(f"  First Paragraph: {data['first_paragraph']}")
        print(f"  Outgoing Links ({len(data['outgoing_links'])}):")
        for link in data["outgoing_links"]:
            print(f"    - {link}")
        print(f"  Images ({len(data['image_urls'])}):")
        for img in data["image_urls"]:
            print(f"    - {img}")
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())
