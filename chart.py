"""Create a bar chart of average device temperatures from summary JSON."""

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Supports running on machines without a graphical desktop.
import matplotlib.pyplot as plt


def load_summary(json_path):
    path = Path(json_path)
    if not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("Expected the JSON root to be a list of device summaries.")

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Entry {index} must be a JSON object.")
        if "device_id" not in item or "average_temperature" not in item:
            raise ValueError(f"Entry {index} must include device_id and average_temperature.")
        try:
            item["average_temperature"] = float(item["average_temperature"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Entry {index} has an invalid average_temperature.") from exc
    return data


def create_chart(data, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    device_ids = [item["device_id"] for item in data]
    averages = [item["average_temperature"] for item in data]

    # A wider figure and rotated labels reduce overlap when there are many devices.
    width = max(8, len(device_ids) * 1.1)
    fig, ax = plt.subplots(figsize=(width, 5.5))

    if device_ids:
        bars = ax.bar(device_ids, averages)
        ax.bar_label(bars, fmt="%.1f", padding=3)
        ax.set_ylim(0, max(90, max(averages) * 1.15))
        ax.tick_params(axis="x", labelrotation=30)
        for label in ax.get_xticklabels():
            label.set_horizontalalignment("right")
    else:
        ax.text(0.5, 0.5, "No devices passed the filter", ha="center", va="center",
                transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])

    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average temperature (°C)")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    fig.tight_layout()
    try:
        fig.savefig(output, dpi=160, bbox_inches="tight")
    finally:
        plt.close(fig)
    return output


def main():
    parser = argparse.ArgumentParser(description="Chart average temperatures from summary JSON.")
    parser.add_argument("json_file", nargs="?", default="output/summary.json",
                        help="Input summary JSON path (default: output/summary.json)")
    parser.add_argument("--output", default="output/average_temperature.png",
                        help="Chart output path (default: output/average_temperature.png)")
    args = parser.parse_args()

    try:
        data = load_summary(args.json_file)
        output = create_chart(data, args.output)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Chart saved to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
