# Device Log Summarizer — Prompt Notes

I used AI in small steps while working on the Device Log Summarizer. I kept the prompts focused so I could test each part before moving on.

> **Note:** I did not use AI for Section 1, the sensor-sanitization exercise.

## Prompt 1 — Core Data Processing Task
```
You are provided with a small CSV file named device_telemetry.csv containing these
columns:
●
device_id (String, e.g., DEV_A, DEV_B)
●
status (ACTIVE, WARNING, ERROR)
●
temperature (Float)

Requirements:
1. Data Ingestion: Read the CSV file using Python (you can use standard csv library or
pandas).
2. Aggregation: Group the data by device_id and compute:
●
Total number of records per device
●
Average (mean) temperature
●
Count of records where status is ERROR
3. Filtering: Filter out any devices that have an average temperature above 80.0.
4. Export: Save the final aggregated results into a clean JSON file and print a summary
table in the terminal.

When done update the readme.md file with the changes and done for the code
```

### Prompt 2 - 
```
Now, for the next step we have clear requirement the json file in the 
output folder i.e summary.json you need to convert that into a bar chart
make sure the bar chart are good in terms of theming and UX. 
For the functionality make completly sure that it can handle error data which is 
null data, error data etc, it should not break the code and must create the bar chart 
with remaining good data from the summary.json
```

### Prompt 3 -
```
Chart is being created but the UI is not looking good 
currently the texts are being overlapped on the bar charts 
check and fix this small issue 
```

## Final notes

- **Project files used:**
    * sanatization_template.py 
- **Chart checked:** found a small UI issue fixed
- **Changes I made myself:** section 1 was completed by myself
- **Remaining issues:** NONE

I kept this log as a record of the prompts I actually used and the results I observed. Update the notes after each step so the log reflects the real work, not just the intended workflow.
