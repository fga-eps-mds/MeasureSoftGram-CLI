# examples

Copy of the sample data used by the `msgram demo` command.

The demo reads the copy packaged in `src/cli/resources/demo_data/` (shipped in
the wheel and sdist). This folder keeps an identical copy as a fallback when
running from a repository checkout; `tests/unit/test_demo_dataset.py` checks
that both copies stay the same.

## analytics-raw-data/

Contains one real SonarCloud export of this repository
(`fga-eps-mds-2026.2-MeasureSoftGram-CLI-25-10-2026-17-57-36-develop.json`),
collected by the "Export de métricas" workflow (`parser.py`) on 25/10/2026.
It includes `sqale_debt_ratio`, so the demo calculates `technical_debt_ratio`.
It has no GitHub data, so `team_throughput` and `ci_feedback_time` are not
calculated (the demo warns about them).

Run the full demo with:

```bash
msgram demo
```

This creates a `./msgram-demo/` working directory, generates `msgram.json`
(via `init`), extracts the metrics from the sample Sonar JSON (via `extract`)
and computes the four quality layers exporting a CSV (via `calculate`). No
external data or network access is required.

The file name keeps the `dd-mm-yyyy-hh-mm-ss` date pattern on purpose: the
`extract` and `calculate` commands read the version from that date. The
original export in the DOC repository (`Analytics/data`) is named with the
`mm-dd-yyyy` pattern used by `parser.py`; it was renamed here to match the
CLI convention.

To refresh the dataset, copy the latest CLI export from the DOC repository
into both folders (renaming the date to `dd-mm-yyyy`) and run the tests.
