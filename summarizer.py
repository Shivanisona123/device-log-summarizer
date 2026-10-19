"""Summarize device telemetry from CSV to JSON and print a terminal table."""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = {"device_id", "status", "temperature"}
TEMPERATURE_LIMIT = 80.0


def parse_temperature(raw_value):
    """Parse a finite numeric temperature, returning None for invalid values."""
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return None
    # Reject NaN and infinities, which otherwise distort aggregation.
    if value != value or value in (float("inf"), float("-inf")):
        return None
    return value


def summarize_csv(csv_path):
    """Read a telemetry CSV and return aggregated device rows.

    A row contributes to record_count and average_temperature only when it has
    a non-empty device_id and a valid numeric temperature. ERROR status counts
    are computed among those same accepted rows.
    """
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    aggregates = defaultdict(lambda: {"temperature_sum": 0.0, "record_count": 0, "error_count": 0})

    try:
        with path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise ValueError("CSV is empty or has no header row.")

            headers = {header.strip() for header in reader.fieldnames if header}
            missing = REQUIRED_COLUMNS - headers
            if missing:
                raise ValueError("CSV is missing required column(s): " + ", ".join(sorted(missing)))

            for line_number, row in enumerate(reader, start=2):
                # Normalize keys and text fields to tolerate whitespace in headers/values.
                normalized = {(key.strip() if key else ""): value for key, value in row.items()}
                device_id = (normalized.get("device_id") or "").strip()
                status = (normalized.get("status") or "").strip().upper()
                temperature = parse_temperature(normalized.get("temperature"))

                if not device_id:
                    print(f"Warning: skipping line {line_number}: empty device_id.", file=sys.stderr)
                    continue
                if temperature is None:
                    print(f"Warning: skipping line {line_number}: invalid temperature.", file=sys.stderr)
                    continue

                item = aggregates[device_id]
                item["temperature_sum"] += temperature
                item["record_count"] += 1
                if status == "ERROR":
                    item["error_count"] += 1

    except UnicodeDecodeError as exc:
        raise ValueError(f"Could not decode CSV as UTF-8: {path}") from exc
    except OSError as exc:
        raise OSError(f"Could not read CSV file {path}: {exc}") from exc

    results = []
    for device_id, values in sorted(aggregates.items()):
        count = values["record_count"]
        average = values["temperature_sum"] / count
        if average > TEMPERATURE_LIMIT:
            continue
        results.append({
            "device_id": device_id,
            "record_count": count,
            "average_temperature": round(average, 2),
            "error_count": values["error_count"],
        })
    return results


def write_json(results, output_path):
    """Write aggregated results as readable JSON, creating parent folders."""
    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2)
            handle.write("\n")
    except OSError as exc:
        raise OSError(f"Could not write JSON output {path}: {exc}") from exc


def print_table(results):
    """Print a simple aligned table without third-party table dependencies."""
    headers = ("Device ID", "Records", "Avg temperature", "ERROR count")
    rows = [
        (
            item["device_id"],
            str(item["record_count"]),
            f'{item["average_temperature"]:.2f}',
            str(item["error_count"]),
        )
        for item in results
    ]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]

    def format_row(row):
        return "| " + " | ".join(value.ljust(widths[i]) for i, value in enumerate(row)) + " |"

    print(format_row(headers))
    print("|-" + "-|-".join("-" * width for width in widths) + "-|")
    if not rows:
        print("| No devices passed the filter.".ljust(sum(widths) + 10) + "|")
        return
    for row in rows:
        print(format_row(row))


def main():
    parser = argparse.ArgumentParser(description="Aggregate device telemetry from a CSV file.")
    parser.add_argument("csv_file", nargs="?", default="device_telemetry.csv",
                        help="Input CSV path (default: device_telemetry.csv)")
    parser.add_argument("--output", default="output/summary.json",
                        help="JSON output path (default: output/summary.json)")
    args = parser.parse_args()

    try:
        results = summarize_csv(args.csv_file)
        write_json(results, args.output)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_table(results)
    print(f"\nWrote {len(results)} device(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
