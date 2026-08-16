import unittest
from crawl import (
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
    normalize_url,
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url_basic(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_strip_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_protocol(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_and_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_root_path(self):
        input_url = "https://www.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_root_no_slash(self):
        input_url = "https://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_uppercase_scheme_and_domain(self):
        input_url = "HTTPS://WWW.BOOT.DEV/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    # Tests for get_heading_from_html
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_fallback_h2(self):
        input_body = "<html><body><h2>Fallback Subtitle</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Subtitle"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1_priority_over_h2(self):
        input_body = "<html><body><h2>Sub Heading</h2><h1>Main Heading</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Main Heading"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_missing(self):
        input_body = "<html><body><p>Just a paragraph</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # Tests for get_first_paragraph_from_html
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
        </main>
    </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_fallback_no_main(self):
        input_body = """<html><body>
        <p>First paragraph without main.</p>
        <p>Second paragraph.</p>
    </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph without main."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_missing(self):
        input_body = "<html><body><h1>Only a heading</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty_main_fallback(self):
        input_body = """<html><body>
        <main></main>
        <p>Fallback paragraph outside empty main.</p>
    </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Fallback paragraph outside empty main."
        self.assertEqual(actual, expected)

    # Tests for get_urls_from_html
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/to/page">Link</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/to/page"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a href="https://crawler-test.com/home">Home</a>
            <div>
                <a href="/about">About</a>
            </div>
            <a href="https://external.com/faq">FAQ</a>
        </body></html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/home",
            "https://crawler-test.com/about",
            "https://external.com/faq",
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_missing_href(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><a>No href attribute</a></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # Tests for get_images_from_html
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://cdn.example.com/image.jpg" alt="CDN Image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://cdn.example.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <img src="/assets/header.png" alt="Header">
            <div>
                <img src="https://cdn.example.com/pic.png">
                <img src="/assets/footer.jpg">
            </div>
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/assets/header.png",
            "https://cdn.example.com/pic.png",
            "https://crawler-test.com/assets/footer.jpg",
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><img alt='Missing src'></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
