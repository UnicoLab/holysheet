---
title: CLI Reference
description: HolySheet command-line interface documentation
---

# :material-console: CLI Reference

HolySheet provides a command-line interface for validating, serving, developing, linting, and comparing reports.

```bash
holysheet [OPTIONS] COMMAND [ARGS]...
```

### Global Options

| Option | Description |
|:-------|:------------|
| `--verbose`, `-v` | Enable debug logging |
| `--help` | Show help and exit |

---

## validate

Validate a HolySheet JSON spec file for structural correctness.

```bash
holysheet validate REPORT_JSON
```

### Arguments

| Argument | Description |
|:---------|:------------|
| `REPORT_JSON` | Path to a JSON spec file |

### Example

```bash
$ holysheet validate report.json
Validating report.json...
✓ Valid HolySheet spec
  Title:          Q4 Review
  Schema version: 1.0.0
  Theme:          dark
  Blocks:         12
  Created at:     2026-05-21T08:00:00+00:00
```

---

## serve

Start a local HTTP server and open the report in your default browser.

```bash
holysheet serve REPORT_JSON [OPTIONS]
```

### Arguments

| Argument | Description |
|:---------|:------------|
| `REPORT_JSON` | Path to a JSON spec file |

### Options

| Option | Default | Description |
|:-------|:--------|:------------|
| `--port`, `-p` | `8765` | Port to serve on |
| `--no-open` | `False` | Don't auto-open browser |

### Example

```bash
# Default port
$ holysheet serve report.json
Serving report.json at http://localhost:8765
Press Ctrl+C to stop.

# Custom port, no browser
$ holysheet serve report.json --port 3000 --no-open
```

!!! info "How Serve Works"
    The `serve` command:

    1. Reads and validates the JSON spec
    2. Exports to a temporary folder
    3. Starts a Python HTTP server
    4. Opens the browser (unless `--no-open`)
    5. Cleans up the temp folder on exit

---

## version

Display the installed HolySheet version.

```bash
holysheet version
```

### Example

```bash
$ holysheet version
holysheet 0.4.0
```

---

## dev :material-new-box:{ .new-badge }

Start a **hot-reload development server** that watches a Python report script for changes and automatically rebuilds and refreshes the browser.

```bash
holysheet dev SCRIPT [OPTIONS]
```

### Arguments

| Argument | Description |
|:---------|:------------|
| `SCRIPT` | Path to a Python script that generates a HolySheet report |

### Options

| Option | Default | Description |
|:-------|:--------|:------------|
| `--port`, `-p` | `8000` | Port to serve on |
| `--no-open` | `False` | Don't auto-open browser |

### Example

```bash
$ holysheet dev my_report.py
🔥 HolySheet Dev Server
   Watching: /Users/you/project/my_report.py
   Serving:  http://localhost:8000
   Press Ctrl+C to stop.

  Building from my_report.py...
  ✓ Build #1 ready
```

When you save changes to `my_report.py`, the server automatically rebuilds:

```
↻ Change detected in my_report.py
  Building from my_report.py...
  ✓ Build #2 ready
```

### How It Works

1. Executes the Python script via subprocess
2. Locates the generated HTML output
3. Injects a live-reload JavaScript snippet (polls `/api/version`)
4. Serves the output via a local HTTP server
5. Watches the script file for `mtime` changes (polling every 500ms)
6. Re-executes and reloads the browser on change

!!! tip "Development Workflow"
    The `dev` command is the fastest way to iterate on a report. Open your script in an editor, save changes, and see the result instantly in the browser.

!!! note "Script Requirements"
    Your script should call `report.export_html()` or similar. The dev server looks for HTML output in the `HOLYSHEET_DEV_OUTPUT` directory or the script's directory.

---

## lint :material-new-box:{ .new-badge }

Run a linter against a HolySheet report to catch common issues, missing best practices, and potential problems.

```bash
holysheet lint SOURCE [OPTIONS]
```

### Arguments

| Argument | Description |
|:---------|:------------|
| `SOURCE` | Path to a Python script (`.py`) or JSON spec file (`.json`) |

### Options

| Option | Default | Description |
|:-------|:--------|:------------|
| `--strict` | `False` | Treat warnings as errors (exit code 1) |

### Example

```bash
$ holysheet lint my_report.py
Linting my_report.py...

  💡 SUGGESTION [block_001]: KPI has no delta — consider adding a change indicator for context.
  ⚠️  WARNING [block_004]: Chart (line_chart) has no title — add a descriptive title for clarity.
  ✅ INFO [block_006]: DataTable has no explicit columns — columns will be auto-inferred from data.

  Found 1 warning(s), 1 suggestion(s), 1 info(s)
```

### Lint Rules

The linter checks for the following patterns:

| Level | Rule | Description |
|:------|:-----|:------------|
| :material-lightbulb: Suggestion | KPI without delta | KPI cards without change indicators lack context |
| :material-lightbulb: Suggestion | Section > 8 children | Large sections should use Tabs for organization |
| :material-lightbulb: Suggestion | Consecutive same-type blocks | Sequential blocks of the same type could use Columns |
| :material-alert: Warning | Chart without title | Charts need descriptive titles for clarity |
| :material-close-circle: Error | Empty chart data | Charts with empty `data=[]` render blank |
| :material-information: Info | DataTable without columns | Auto-inferred columns may be unstable |
| :material-information: Info | Missing theme | No explicit theme defaults to `"light"` |

### Strict Mode

```bash
# Exit with error code 1 if any warnings are found
$ holysheet lint my_report.py --strict
```

!!! tip "CI Integration"
    Add `holysheet lint --strict` to your CI pipeline to catch report issues before deployment.

---

## diff :material-new-box:{ .new-badge }

Compare two HolySheet JSON spec files and show the differences in metadata, blocks, and props.

```bash
holysheet diff FILE_A FILE_B
```

### Arguments

| Argument | Description |
|:---------|:------------|
| `FILE_A` | Path to the first JSON spec file |
| `FILE_B` | Path to the second JSON spec file |

### Example

```bash
$ holysheet diff report_v1.json report_v2.json
Comparing report_v1.json ↔ report_v2.json

Metadata changes:
  title: 'Q3 Review' → 'Q4 Review'
  theme: 'light' → 'dark'

Removed blocks (1):
  - kpi (block_003) "Old Metric"

Added blocks (2):
  + kpi (block_005) "New Revenue"
  + line_chart (block_006) "Revenue Trend"

Changed blocks (1):
  ~ kpi (block_001) "Revenue": props changed [delta, value]

Summary: 1 removed, 2 added, 1 changed (A: 4 blocks → B: 5 blocks)
```

### What It Compares

| Category | Details |
|:---------|:--------|
| **Metadata** | title, subtitle, theme, logo_url, author, report_version, footer, schema_version |
| **Removed blocks** | Blocks in A that are not in B (matched by block ID) |
| **Added blocks** | Blocks in B that are not in A |
| **Changed blocks** | Blocks present in both but with different type or props |

!!! tip "Version Control"
    Export your reports as JSON (`report.export_json("report.json")`) and commit them to Git. Use `holysheet diff` to review changes before deploying updated reports.

---

## :bulb: CLI Tips

### Verbose Mode

Add `-v` to any command for detailed debug output:

```bash
holysheet -v validate report.json
holysheet -v serve report.json
holysheet -v dev my_report.py
holysheet -v lint my_report.py
```

### Combining with Scripts

```bash
# Build, lint, and serve in one go
python my_report.py && holysheet lint report.json && holysheet serve report.json
```

### Makefile Integration

```makefile title="Makefile"
.PHONY: report dev lint

report:
	python reports/quarterly.py

dev:
	holysheet dev reports/quarterly.py

lint:
	holysheet lint reports/quarterly.py --strict
```
