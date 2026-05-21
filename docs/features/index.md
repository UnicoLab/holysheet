---
title: Features
description: Advanced features in HolySheet v0.5.0
---

# :rocket: Features

HolySheet v0.5.0 includes a powerful set of features that go beyond basic block composition — custom themes, multi-page reports, global filters, Jupyter integration, AI insights, anomaly detection, PDF export, and more.

---

## :material-palette-swatch: Custom Theme API

Create fully branded dashboards by extending any built-in theme with your own colors, fonts, and chart palette.

### Creating a Custom Theme

```python title="custom_theme.py"
from holysheet import Report, KPI
from holysheet.themes import Theme

brand = Theme(
    name="acme",
    base="dark",                          # Extend the dark theme
    primary="#FF6B00",                     # Brand orange
    secondary="#00D4AA",                   # Teal accent
    background="#0A0A0F",                  # Deep background
    surface="#1A1A2E",                     # Card surface
    font="Satoshi",                        # Custom font
    chart_palette=["#FF6B00", "#00D4AA", "#6366F1", "#F59E0B"],
)

report = Report(title="Acme Corp Dashboard", theme=brand)
report.add(KPI(label="Revenue", value="$4.2M", delta="+18%", status="positive"))
report.export_html("acme_dashboard.html")
```

### Theme Parameters

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `name` | `str` | `"custom"` | Theme identifier |
| `base` | `str` | `"dark"` | Base theme to extend (`"dark"`, `"light"`, `"executive"`) |
| `primary` | `str \| None` | `None` | Primary brand color |
| `secondary` | `str \| None` | `None` | Secondary accent color |
| `background` | `str \| None` | `None` | Page background color |
| `surface` | `str \| None` | `None` | Card / surface color |
| `text` | `str \| None` | `None` | Primary text color |
| `text_secondary` | `str \| None` | `None` | Muted text color |
| `border` | `str \| None` | `None` | Border color |
| `success` | `str \| None` | `None` | Success status color |
| `warning` | `str \| None` | `None` | Warning status color |
| `danger` | `str \| None` | `None` | Danger / error color |
| `info` | `str \| None` | `None` | Info color |
| `font` | `str \| None` | `None` | Body + heading font family |
| `mono_font` | `str \| None` | `None` | Monospace font family |
| `chart_palette` | `list[str] \| None` | `None` | Chart series color palette |

!!! tip "Only Override What You Need"
    The `Theme` class deep-copies the base theme and only overrides the properties you specify. Unset properties inherit from the base.

---

## :material-book-open-page-variant: Multi-Page Reports

Create tabbed or sidebar-navigated reports with multiple pages using `add_page()`.

```python title="multi_page.py"
from holysheet import Report, KPI, LineChart, DataTable, Section

report = Report(title="Q4 Business Review", theme="dark")

report.add_page("Overview", children=[
    KPI(label="Revenue", value="$4.2M", delta="+22%", status="positive"),
    LineChart(title="Revenue Trend", data=monthly_data, x="month", y="revenue"),
])

report.add_page("Sales", children=[
    KPI(label="Deals Won", value=142, delta="+18", status="positive"),
    DataTable(title="Top Accounts", data=accounts_df),
])

report.export_html("q4_review.html")
```

---

## :material-filter: Global Filters

Add interactive filters to the report header that affect all blocks.

```python title="global_filters.py"
from holysheet import Report, LineChart, DataTable

report = Report(title="Sales Analytics", theme="dark")

report.add_filter("region", type="dropdown", label="Region",
    options=["North America", "Europe", "Asia Pacific"], default="North America")

report.add_filter("date_range", type="date_range", label="Date Range")
report.add_filter("search", type="text", label="Search")

report.add(LineChart(title="Revenue", data=data, x="month", y="revenue"))
report.add(DataTable(title="Deals", data=deals))

report.export_html("filtered_report.html")
```

| Type | Description | Props |
|:-----|:------------|:------|
| `"dropdown"` | Select from a list of options | `options`, `default` |
| `"date_range"` | Date range picker | `default` |
| `"text"` | Free-text search input | `default` |
| `"checkbox"` | Multi-select with checkboxes | `options`, `default` |

---

## :material-toggle-switch: Feature Flags

```python title="feature_flags.py"
report = Report(
    title="Interactive Dashboard",
    theme="dark",
    theme_switch=True,           # Dark/light mode toggle
    presentation_mode=True,      # Slideshow mode
    download_buttons=True,       # CSV download buttons
)
```

---

## :material-notebook: Jupyter Integration

```python title="jupyter.py"
report  # ← Auto-renders inline via _repr_html_()

report.show(height=600)  # Explicit render with custom height
```

---

## :material-file-pdf-box: PDF Export

Export any report as a PDF file using a headless browser:

```python title="pdf_export.py"
report.export_pdf("report.pdf", landscape=True, margin="0.5in")
```

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `path` | `str \| Path` | — | Output PDF file path |
| `width` | `str` | `"A4"` | Paper format |
| `landscape` | `bool` | `False` | Landscape orientation |
| `margin` | `str` | `"1cm"` | Page margins |

!!! note "Requirements"
    Requires Playwright or Chrome:
    ```bash
    pip install playwright && playwright install chromium
    ```

---

## :material-chart-bell-curve: Anomaly Detection

Automatically detect and annotate statistical outliers on charts:

```python title="anomaly_detection.py"
report.add(LineChart(
    title="Response Time",
    data=metrics_data,
    x="timestamp",
    y="latency_ms",
    anomaly_detection=True,  # IQR-based outlier detection
))
```

Supported on `LineChart`, `AreaChart`, and `BarChart`. Uses IQR method with MAD fallback for near-uniform distributions.

---

## :material-brain: AI Insight Block

Generate LLM-powered data narratives at build time:

```python title="ai_insight.py"
from holysheet import AIInsight

report.add(AIInsight(
    title="Revenue Insight",
    data=revenue_df,
    provider="openai",      # or "anthropic" or "google"
))
```

| Provider | SDK Required | API Key Env Var |
|:---------|:-------------|:----------------|
| `"openai"` | `pip install openai` | `OPENAI_API_KEY` |
| `"anthropic"` | `pip install anthropic` | `ANTHROPIC_API_KEY` |
| `"google"` | `pip install google-generativeai` | `GOOGLE_API_KEY` |

---

## :material-google-spreadsheet: Google Sheets Data Source

Pull data directly from Google Sheets:

```python title="google_sheets.py"
from holysheet import GoogleSheet

report.add(GoogleSheet(
    spreadsheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    sheet_name="Q4 Data",
    title="Revenue by Region",
))
```

!!! note "Requirements"
    `pip install gspread google-auth` and set `GOOGLE_APPLICATION_CREDENTIALS`.

---

## :material-database-search: SQL Block

Run SQL queries against in-report data client-side:

```python title="sql_block.py"
from holysheet import SqlBlock

report.add(SqlBlock(
    title="Revenue Analysis",
    query="SELECT region, SUM(revenue) as total FROM data GROUP BY region",
    data=sales_df,
))
```

Supports `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`, and aggregates (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).

---

## :material-microphone: Narration & Voice Readback

```python title="narration.py"
from holysheet import NarrationBlock

report.add(NarrationBlock(
    text="Revenue grew 22% quarter-over-quarter.",
    autoplay=False,
))

# Auto-generate narration from KPIs
narration = report.auto_narrate()
```

---

## :material-cloud-upload: Cloud Publish

Upload reports to S3 or GCS from the CLI:

```bash
holysheet publish report.html -t s3://my-bucket/reports/q4.html --public
holysheet publish report.html -t gs://my-bucket/reports/q4.html --public
```

---

## :material-lock: Password Protection & Expiry

```python title="security.py"
report = Report(
    title="Confidential",
    theme="executive",
    password="s3cret-p@ss!",       # AES encryption
    expires="2026-06-30T23:59:59",  # Auto-expiry
    compress=True,                  # Gzip compression
)
```

---

## :bulb: Full Example

```python title="full_featured.py"
from holysheet import Report, KPI, LineChart, DataTable, AIInsight, NarrationBlock
from holysheet.themes import Theme

theme = Theme(name="corp", base="dark", primary="#1E88E5", font="Inter")

report = Report(
    title="Q4 Executive Review",
    theme=theme,
    theme_switch=True,
    download_buttons=True,
    password="board-2026",
    expires="2026-07-01",
    compress=True,
)

report.add_filter("region", options=["US", "EU", "APAC"], default="US")

report.add_page("Summary", children=[
    KPI(label="Revenue", value="$12.8M", delta="+22%", status="positive"),
    LineChart(title="Trend", data=data, x="month", y="revenue", anomaly_detection=True),
    AIInsight(title="Key Findings", data=data, provider="openai"),
])

report.add_page("Details", children=[
    DataTable(title="Pipeline", data=pipeline_df),
    NarrationBlock(text=report.auto_narrate()),
])

report.export_html("q4_review.html")
report.export_pdf("q4_review.pdf", landscape=True)
```
