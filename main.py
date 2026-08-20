import asyncio
import sys
from crawl import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")
    page_data = await crawl_site_async(base_url, max_concurrency=5)

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
