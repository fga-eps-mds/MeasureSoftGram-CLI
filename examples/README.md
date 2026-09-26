# examples

Embedded sample data used by the `msgram demo` command.

## analytics-raw-data/

Contains one real SonarQube analysis export in JSON format
(`fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json`).
It is the same fixture used by the test suite and is known to run through the
whole pipeline (extract, then calculate).

Run the full demo with:

```bash
msgram demo
```

This creates a `./msgram-demo/` working directory, generates `msgram.json`
(via `init`), extracts the metrics from the sample Sonar JSON (via `extract`)
and computes the four quality layers exporting a CSV (via `calculate`). No
external data or network access is required.

The file name keeps the `dd-mm-yyyy-hh-mm-ss` date pattern on purpose: the
`extract` command derives the output `.metrics` file name from that date.
