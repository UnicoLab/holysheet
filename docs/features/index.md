---
title: Features
description: Advanced features introduced in HolySheet v0.4.0
---

# :rocket: Features

HolySheet v0.4.0 introduces a powerful set of features that go beyond basic block composition — custom themes, multi-page reports, global filters, Jupyter integration, and more.

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

!!! note "Font Loading"
    Custom web fonts (e.g. Google Fonts) must be loaded externally. The theme sets the `font-family` CSS property — the browser must have access to the font files.

---

## :material-book-open-page-variant: Multi-Page Reports

Create tabbed or sidebar-navigated reports with multiple pages using `add_page()`.

```python title="multi_page.py"
from holysheet import Report, KPI, LineChart, DataTable, Section

report = Report(title="Q4 Business Review", theme="dark")

# Page 1: Overview
report.add_page("Overview", children=[
    KPI(label="Revenue", value="$4.2M", delta="+22%", status="positive"),
    KPI(label="Users", value="128K", delta="+31%", status="positive"),
    LineChart(title="Revenue Trend", data=monthly_data, x="month", y="revenue"),
])

# Page 2: Sales
report.add_page("Sales", children=[
    KPI(label="Deals Won", value=142, delta="+18", status="positive"),
    DataTable(title="Top Accounts", data=accounts_df),
])

# Page 3: Engineering
report.add_page("Engineering", children=[
    KPI(label="Deploys", value=89, delta="+12", status="positive"),
    Section(title="Sprint Metrics", children=[...]),
])

report.export_html("q4_review.html")
```

!!! info "Page Navigation"
    When pages are used, the report renders with a sidebar navigation panel. Each page label becomes a nav item. Viewers can click between pages without reloading.

!!! warning "Pages vs Blocks"
    Use either `add()` (flat report) **or** `add_page()` (multi-page report), not both. If you call `add_page()`, any blocks added via `add()` are ignored.

---

## :material-filter: Global Filters

Add interactive filters to the report header that affect all blocks referencing the same key.

```python title="global_filters.py"
from holysheet import Report, LineChart, DataTable

report = Report(title="Sales Analytics", theme="dark")

# Add global filters
report.add_filter(
    "region",
    type="dropdown",
    label="Region",
    options=["North America", "Europe", "Asia Pacific"],
    default="North America",
)

report.add_filter(
    "date_range",
    type="date_range",
    label="Date Range",
)

report.add_filter(
    "search",
    type="text",
    label="Search",
)

# Add blocks that respond to filters
report.add(LineChart(title="Revenue", data=data, x="month", y="revenue"))
report.add(DataTable(title="Deals", data=deals))

report.export_html("filtered_report.html")
```

### Filter Types

| Type | Description | Props |
|:-----|:------------|:------|
| `"dropdown"` | Select from a list of options | `options`, `default` |
| `"date_range"` | Date range picker | `default` |
| `"text"` | Free-text search input | `default` |

---

## :material-toggle-switch: Feature Flags

Enable optional interactive features via constructor flags:

```python title="feature_flags.py"
from holysheet import Report

report = Report(
    title="Interactive Dashboard",
    theme="dark",
    theme_switch=True,           # (1)!
    presentation_mode=True,      # (2)!
    download_buttons=True,       # (3)!
)
```

1. Adds a toggle button for viewers to switch between dark and light mode
2. Enables a presentation / slideshow mode button
3. Shows CSV download buttons on tables and charts

### Feature Flag Reference

| Flag | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `theme_switch` | `bool` | `False` | Dark/light mode toggle in the report header |
| `presentation_mode` | `bool` | `False` | Fullscreen slideshow mode for presenting blocks one-by-one |
| `download_buttons` | `bool` | `False` | Per-block CSV/PNG export buttons |

!!! tip "Combining Feature Flags"
    All flags are independent — enable any combination you need.

---

## :material-notebook: Jupyter Integration

HolySheet renders natively in Jupyter notebooks via two methods:

### Auto-Display with `_repr_html_`

Simply evaluate a `Report` object in a cell — Jupyter calls `_repr_html_()` automatically:

```python title="jupyter_auto.py"
from holysheet import Report, KPI, LineChart

report = Report(title="Quick Analysis", theme="dark")
report.add(KPI(label="Score", value=92, unit="%"))
report.add(LineChart(title="Trend", data=data, x="date", y="value"))

report  # ← Renders inline in the notebook
```

### Explicit Display with `show()`

Use `show()` for explicit rendering with a custom height:

```python title="jupyter_show.py"
report.show(height=600)  # Renders in an iframe with 600px height
```

!!! info "How It Works"
    The report is rendered as a base64-encoded HTML document inside an iframe, providing full CSS isolation from the notebook theme.

---

## :material-lock: Password Protection

Encrypt the report data with client-side AES encryption. Viewers must enter the password to decrypt and view the dashboard.

```python title="password_protected.py"
from holysheet import Report, KPI

report = Report(
    title="Confidential: Board Report",
    theme="executive",
    password="s3cret-p@ss!",
)
report.add(KPI(label="Revenue", value="$12.8M", delta="+34%", status="positive"))

report.export_html("board_report.html")
```

!!! warning "Security Note"
    Password protection uses **client-side AES encryption** with PBKDF2 key derivation. The encrypted payload is embedded in the HTML file. This is suitable for casual protection (e.g. email sharing) but is **not** a substitute for server-side access control for truly sensitive data.

---

## :material-clock-alert: Expiring Reports

Set an expiration date after which the report displays an "expired" overlay instead of the data:

```python title="expiring_report.py"
report = Report(
    title="Weekly Metrics",
    theme="dark",
    expires="2026-06-30T23:59:59",  # ISO-8601 format
)
```

!!! tip "Use Cases"
    Expiring reports are ideal for time-sensitive data like weekly reviews, pre-board meeting materials, or trial/demo dashboards.

---

## :material-package-down: Compression

Gzip-compress the embedded JSON data to reduce HTML file size for data-heavy reports:

```python title="compressed_report.py"
report = Report(
    title="Large Dataset Report",
    theme="dark",
    compress=True,
)
# ... add many blocks with large DataTables ...
report.export_html("compressed_report.html")  # Smaller file size
```

!!! note "When to Use"
    Compression is most effective for reports with large `DataTable` blocks or many chart data points. For typical reports (~10 blocks), the size difference is negligible.

---

## :material-widgets: Widget Export

Export a lightweight, embeddable subset of your report as a standalone widget:

```python title="widget_export.py"
from holysheet import Report, KPI, LineChart

report = Report(title="Full Dashboard", theme="dark")
report.add(KPI(label="Revenue", value="$1.2M"))
report.add(KPI(label="Users", value="42K"))
report.add(LineChart(title="Trend", data=data, x="month", y="revenue"))

# Export full report
report.export_html("dashboard.html")

# Export only specific blocks as a widget
report.export_widget(
    "revenue_widget.html",
    block_ids=["block_001", "block_003"],  # Only Revenue KPI + Trend chart
)
```

The widget HTML is a minimal, self-contained file optimized for embedding in other web pages or portals.

### Embedding a Widget

```html title="embed_widget.html"
<iframe
  src="revenue_widget.html"
  width="100%"
  height="400"
  frameborder="0"
  style="border-radius: 8px;"
></iframe>
```

---

## :bulb: Feature Combinations

Here's a real-world example combining multiple features:

```python title="full_featured.py"
from holysheet import Report, KPI, LineChart, DataTable
from holysheet.themes import Theme

# Custom branded theme
theme = Theme(name="corp", base="dark", primary="#1E88E5", font="Inter")

report = Report(
    title="Q4 Executive Review",
    theme=theme,
    author="Data Team",
    theme_switch=True,
    download_buttons=True,
    password="board-2026",
    expires="2026-07-01",
    compress=True,
)

report.add_filter("region", options=["US", "EU", "APAC"], default="US")

report.add_page("Summary", children=[
    KPI(label="Revenue", value="$12.8M", delta="+22%", status="positive"),
    LineChart(title="Revenue Trend", data=revenue_data, x="month", y="revenue"),
])

report.add_page("Details", children=[
    DataTable(title="Deal Pipeline", data=pipeline_df),
])

report.export_html("q4_review.html")
```
