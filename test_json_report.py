import json
import os
import tempfile
import unittest
from json_report import write_json_report


class TestJsonReport(unittest.TestCase):
    def test_write_json_report_sorting_and_content(self):
        sample_data = {
            "example.com/b": {
                "url": "https://example.com/b",
                "heading": "Page B",
                "first_paragraph": "Paragraph B",
                "outgoing_links": [],
                "image_urls": [],
            },
            "example.com/a": {
                "url": "https://example.com/a",
                "heading": "Page A",
                "first_paragraph": "Paragraph A",
                "outgoing_links": ["https://example.com/b"],
                "image_urls": ["https://example.com/img.png"],
            },
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "test_report.json")
            write_json_report(sample_data, out_file)
            self.assertTrue(os.path.exists(out_file))

            with open(out_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(len(data), 2)
            # Must be sorted by URL: 'a' comes before 'b'
            self.assertEqual(data[0]["url"], "https://example.com/a")
            self.assertEqual(data[1]["url"], "https://example.com/b")

    def test_write_json_report_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "empty_report.json")
            write_json_report({}, out_file)
            with open(out_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()
