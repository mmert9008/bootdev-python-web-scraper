import unittest
from crawl import (
    get_first_paragraph_from_html,
    get_heading_from_html,
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


if __name__ == "__main__":
    unittest.main()
