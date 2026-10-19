# Device Log Summarizer CLI

A small Python CLI that reads `device_telemetry.csv`, aggregates telemetry by device, excludes devices whose average temperature is above 80.0, exports JSON, prints a terminal summary, and optionally creates a Matplotlib bar chart.

## Requirements
- Python 3.9+
- Matplotlib for charting (`python -m pip install matplotlib`)

The ingestion and aggregation code uses Python's standard library.

## Files
- `sanitization_template.py` — independent exercise template for Section 1. Complete the TODO yourself, as the assessment explicitly asks you not to use AI for this section.
- `summarizer.py` — CSV ingestion, validation, aggregation, filtering, JSON export, and terminal table.
- `chart.py` — chart generation from the JSON output.
- `device_telemetry.csv` — sample input data.
- `output/summary.json` — sample output.
- `output/average_temperature.png` — sample chart (generate it locally by running the command below).
- `PROMPT_LOG.md` — AI collaboration log template; edit it so it accurately reflects your actual prompting and debugging.

## Run
From this directory:

```bash
python summarizer.py device_telemetry.csv --output output/summary.json
python chart.py output/summary.json --output output/average_temperature.png
```

If no arguments are provided, `summarizer.py` defaults to `device_telemetry.csv` and `output/summary.json`.

## Aggregation behavior
- Records are grouped by `device_id`.
- `record_count` counts valid CSV records with a non-empty device ID and a parseable temperature.
- `average_temperature` is the arithmetic mean of parseable temperatures.
- `error_count` counts `ERROR` statuses among those same valid records.
- Devices with average temperature strictly greater than `80.0` are excluded.
- Bad rows are skipped with a warning; missing files and unreadable/invalid CSV headers produce a helpful error and a non-zero exit status.
- The output JSON contains only devices that pass the average-temperature filter.

## Note about the assessment
Section 1 is intentionally left as an exercise because its instructions say to complete it without AI. Implement the function yourself, then run its tests.
