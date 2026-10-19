import csv
import json
import tempfile
import unittest
from pathlib import Path

from summarizer import summarize_csv, write_json


class SummarizerTests(unittest.TestCase):
    def test_aggregates_and_filters_hot_device(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "input.csv"
            path.write_text(
                "device_id,status,temperature\n"
                "A,ACTIVE,20\nA,ERROR,40\nB,ERROR,90\nB,ACTIVE,90\n",
                encoding="utf-8",
            )
            result = summarize_csv(path)
            self.assertEqual(result, [{
                "device_id": "A",
                "record_count": 2,
                "average_temperature": 30.0,
                "error_count": 1,
            }])

    def test_bad_temperature_is_skipped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "input.csv"
            path.write_text(
                "device_id,status,temperature\nA,ACTIVE,invalid\nA,ERROR,50\n",
                encoding="utf-8",
            )
            self.assertEqual(summarize_csv(path), [{
                "device_id": "A",
                "record_count": 1,
                "average_temperature": 50.0,
                "error_count": 0,
            }])

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            summarize_csv("does-not-exist-xyz.csv")

    def test_json_export(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested" / "summary.json"
            rows = [{"device_id": "A", "record_count": 1,
                     "average_temperature": 20.0, "error_count": 0}]
            write_json(rows, path)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), rows)


if __name__ == "__main__":
    unittest.main()
