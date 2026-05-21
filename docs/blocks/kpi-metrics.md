# KPI & Metrics

KPI and Metric blocks are the headline numbers of your dashboard. They give stakeholders an instant snapshot of performance.

---

## KPI

The `KPI` block is a full-featured key performance indicator card with support for delta values (change indicators) and semantic status colors.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Display label (e.g. "Total Revenue") |
| `value` | `str \| int \| float` | *required* | The main metric value |
| `unit` | `str \| None` | `None` | Unit suffix (e.g. `"$"`, `"%"`, `"ms"`) |
| `delta` | `str \| None` | `None` | Change indicator (e.g. `"+12.3%"`, `"-$500"`) |
| `status` | `"positive" \| "negative" \| "neutral" \| None` | `None` | Semantic color: green, red, or gray |
| `description` | `str \| None` | `None` | Helper text below the value |

### Basic Example

```python title="kpi_basic.py"
from holysheet import Report, KPI

report = Report(title="Metrics", theme="dark")

report.add(KPI(
    label="Total Revenue",
    value="$2.26M",
    delta="+34.2%",
    status="positive",
))

report.add(KPI(
    label="Churn Rate",
    value="2.1%",
    delta="-0.6%",
    status="positive",
    description="Monthly logo churn",
))

report.add(KPI(
    label="Error Rate",
    value=0.03,
    unit="%",
    delta="+0.01%",
    status="negative",
))
```

### Status Colors

=== "Positive"

    ```python
    KPI(label="Revenue", value="$1.2M", delta="+12%", status="positive")
    ```
    Renders with a **green** accent — use for metrics where an increase is good.

=== "Negative"

    ```python
    KPI(label="Errors", value=142, delta="+23", status="negative")
    ```
    Renders with a **red** accent — use for metrics where an increase is bad.

=== "Neutral"

    ```python
    KPI(label="Response Time", value=142, unit="ms", status="neutral")
    ```
    Renders with a **gray** accent — use for informational metrics.

### With Units

```python title="kpi_units.py"
KPI(label="Uptime", value=99.97, unit="%", status="positive")
KPI(label="Response Time", value=142, unit="ms", status="neutral")
KPI(label="Revenue", value=1_250_000, unit="€", delta="+12%", status="positive")
```

!!! tip "Formatting"
    The `value` prop accepts strings, integers, and floats. For formatted values like `$2.26M`, pass a pre-formatted string. For raw numbers, use `int` or `float` with a `unit`.

---

## Metric

The `Metric` block is a lightweight, compact metric display — ideal for dense metric grids where you need many values at a glance.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Metric label |
| `value` | `str \| int \| float` | *required* | The metric value |
| `unit` | `str \| None` | `None` | Optional unit suffix |
| `icon` | `str \| None` | `None` | Optional icon name hint |

### Example

```python title="metric_example.py"
from holysheet import Report, Metric, Columns

report = Report(title="Metrics Grid", theme="light")

report.add(Columns(children=[
    Metric(label="Avg. Deal Size", value="$4,850", unit="USD"),
    Metric(label="LTV:CAC Ratio", value="5.2x"),
    Metric(label="Median Onboarding", value="3.4", unit="days"),
    Metric(label="NPS Score", value=72),
]))
```

### KPI vs Metric

| Feature | KPI | Metric |
|:--------|:----|:-------|
| Delta / change indicator | :material-check: Yes | :material-close: No |
| Status colors | :material-check: Yes | :material-close: No |
| Description text | :material-check: Yes | :material-close: No |
| Icon support | :material-close: No | :material-check: Yes |
| Visual weight | Heavy — hero card | Light — compact inline |
| **Best for** | Headline metrics | Supporting metrics in grids |

!!! tip "When to Use Which"
    Use **KPI** for 3–5 hero metrics at the top of your dashboard. Use **Metric** inside `Columns` for dense secondary metric grids.

---

## StatComparison

The `StatComparison` block provides a side-by-side comparison of current vs previous values across multiple metrics.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Block title |
| `items` | `list[dict]` | `[]` | List of comparison items |

Each item in `items` should be a dict with:

| Key | Type | Description |
|:----|:-----|:------------|
| `label` | `str` | Metric name |
| `current` | `str \| int \| float` | Current period value |
| `previous` | `str \| int \| float` | Previous period value |
| `unit` | `str` (optional) | Unit suffix |

### Example

```python title="stat_comparison.py"
from holysheet import Report, StatComparison

report = Report(title="Quarterly Review", theme="executive")

report.add(StatComparison(
    title="Q4 vs Q3 Performance",
    items=[
        {"label": "Revenue", "current": "$2.26M", "previous": "$1.68M", "unit": "USD"},
        {"label": "Users", "current": 42_000, "previous": 24_400},
        {"label": "NRR", "current": "127%", "previous": "119%"},
        {"label": "Churn", "current": "2.1%", "previous": "2.7%"},
    ],
))
```

---

## :bulb: Dashboard Tips

### KPI Row Pattern

The most common pattern is 3–5 KPIs at the top of your report:

```python title="kpi_row.py"
from holysheet import Report, KPI, Columns

report = Report(title="Dashboard", theme="dark")

report.add(Columns(children=[
    KPI(label="Revenue", value="$4.64M", delta="+23%", status="positive"),
    KPI(label="Deals Closed", value=127, delta="+18", status="positive"),
    KPI(label="Win Rate", value=68, unit="%", delta="+4.2%", status="positive"),
    KPI(label="Avg Deal Size", value="$36.5K", delta="+$2.1K", status="positive"),
]))
```

!!! tip "Use Columns for KPI rows"
    Wrap KPIs in a `Columns` block to display them side-by-side in a responsive grid.

### Combining KPI + Metric

```python title="combined_metrics.py"
# Hero KPIs
report.add(Columns(children=[
    KPI(label="Annual Revenue", value="$2.26M", delta="+34%", status="positive"),
    KPI(label="Active Users", value="42,000", delta="+72%", status="positive"),
    KPI(label="Churn Rate", value="2.1%", delta="-0.6%", status="positive"),
]))

# Supporting metrics
report.add(Columns(children=[
    Metric(label="Avg. Deal Size", value="$4,850"),
    Metric(label="LTV:CAC", value="5.2x"),
    Metric(label="Onboarding", value="3.4 days"),
    Metric(label="NPS", value=72),
]))
```
