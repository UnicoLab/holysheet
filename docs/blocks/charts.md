# Charts

HolySheet includes **9 chart types** powered by Apache ECharts, providing rich interactive visualizations with tooltips, legends, and responsive sizing.

---

## Common Props

All chart blocks share these common props:

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title displayed above the chart |
| `data` | `Any` | `None` | Tabular data (list of dicts, dict of lists, pandas/polars DataFrame) |
| `height` | `int` | `360` | Chart height in pixels |

!!! info "Data Formats"
    All chart `data` props accept any of the [supported data formats](../data-sources.md) — lists of dicts, dict of lists, pandas DataFrames, or polars DataFrames. Data is automatically converted to records internally.

---

## LineChart

Multi-series line chart for time-series data and trends.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data |
| `x` | `str \| None` | `None` | Column name for X axis |
| `y` | `str \| list[str] \| None` | `None` | Column name(s) for Y axis |
| `series` | `list[str] \| None` | `None` | Optional grouping column for multi-series |
| `height` | `int` | `360` | Chart height in pixels |

### Single Series

```python title="line_single.py"
from holysheet import LineChart

LineChart(
    title="User Growth",
    data=[
        {"month": "Jan", "users": 1_200},
        {"month": "Feb", "users": 1_450},
        {"month": "Mar", "users": 1_830},
        {"month": "Apr", "users": 2_100},
    ],
    x="month",
    y="users",
)
```

### Multi-Series

Pass a **list** to `y` to plot multiple lines:

```python title="line_multi.py"
LineChart(
    title="Revenue, Costs & Profit",
    data=monthly_data,
    x="month",
    y=["revenue", "costs", "profit"],  # Multiple Y columns
    height=420,
)
```

!!! tip "Multi-Series Pattern"
    When `y` is a list, each column becomes its own line with a legend entry. This works the same way for `AreaChart` and `BarChart`.

---

## AreaChart

Filled area chart — visually identical to `LineChart` but with filled regions below the lines.

### Props

Same as [LineChart](#linechart) — `title`, `data`, `x`, `y`, `series`, `height`.

### Example

```python title="area_example.py"
from holysheet import AreaChart

AreaChart(
    title="Active Users & New Sign-ups",
    data=user_growth,
    x="month",
    y=["active_users", "new_signups"],
    height=380,
)
```

---

## BarChart

Grouped or stacked bar chart for categorical comparisons.

### Props

Same as [LineChart](#linechart) — `title`, `data`, `x`, `y`, `series`, `height`.

### Example

```python title="bar_example.py"
from holysheet import BarChart

# Single series
BarChart(
    title="Sales by Region",
    data=[
        {"region": "North America", "sales": 1_840_000},
        {"region": "Europe", "sales": 1_250_000},
        {"region": "Asia Pacific", "sales": 920_000},
    ],
    x="region",
    y="sales",
)
```

### Multi-Series Bar Chart

```python title="bar_multi.py"
BarChart(
    title="Revenue by Product — Q3 vs Q4",
    data=[
        {"product": "Analytics Pro", "q3": 245_000, "q4": 312_000},
        {"product": "Data Pipeline", "q3": 189_000, "q4": 228_000},
        {"product": "Dashboard Hub", "q3": 156_000, "q4": 198_000},
    ],
    x="product",
    y=["q3", "q4"],
    height=400,
)
```

---

## PieChart

Pie or donut chart for showing proportional composition.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data |
| `name` | `str \| None` | `None` | Column name for slice labels |
| `value` | `str \| None` | `None` | Column name for slice values |
| `height` | `int` | `360` | Chart height in pixels |

### Example

```python title="pie_example.py"
from holysheet import PieChart

PieChart(
    title="Revenue by Segment",
    data=[
        {"segment": "Enterprise", "revenue": 980_000},
        {"segment": "Mid-Market", "revenue": 620_000},
        {"segment": "SMB", "revenue": 340_000},
        {"segment": "Startup", "revenue": 185_000},
    ],
    name="segment",
    value="revenue",
)
```

!!! note "`name` / `value` vs `x` / `y`"
    PieChart uses `name` and `value` instead of `x` and `y` because pie slices don't have axes. The same pattern applies to `FunnelChart` and `TreemapChart`.

---

## ScatterChart

Scatter or bubble plot for correlation analysis.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data |
| `x` | `str \| None` | `None` | Column for X axis |
| `y` | `str \| None` | `None` | Column for Y axis |
| `size` | `str \| None` | `None` | Column for bubble size (optional) |
| `category` | `str \| None` | `None` | Column for point color grouping (optional) |
| `height` | `int` | `360` | Chart height in pixels |

### Example

```python title="scatter_example.py"
from holysheet import ScatterChart

ScatterChart(
    title="Feature Usage vs Satisfaction",
    data=[
        {"feature": "Alerts", "usage": 89, "satisfaction": 4.7, "users": 3200},
        {"feature": "Charts", "usage": 76, "satisfaction": 4.5, "users": 2800},
        {"feature": "API", "usage": 62, "satisfaction": 4.2, "users": 1900},
        {"feature": "Export", "usage": 71, "satisfaction": 3.9, "users": 2400},
    ],
    x="usage",
    y="satisfaction",
    size="users",  # Bubble size based on user count
)
```

!!! tip "Bubble Charts"
    Pass the `size` parameter to create a bubble chart where point sizes represent a third dimension of data.

---

## RadarChart

Radar (spider) chart for multi-dimensional comparison across categories.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Data where each record is one series |
| `indicators` | `list[str]` | `[]` | List of dimension names to display on axes |
| `height` | `int` | `360` | Chart height in pixels |

### Example

```python title="radar_example.py"
from holysheet import RadarChart

RadarChart(
    title="Team Performance Comparison",
    data=[
        {"team": "Engineering", "velocity": 92, "quality": 88,
         "collaboration": 76, "innovation": 95, "delivery": 84},
        {"team": "Product", "velocity": 78, "quality": 91,
         "collaboration": 94, "innovation": 87, "delivery": 82},
    ],
    indicators=["velocity", "quality", "collaboration", "innovation", "delivery"],
)
```

---

## GaugeChart

Speedometer-style gauge for displaying a single value within a range.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `value` | `int \| float` | `0` | Current value to display |
| `min` | `int \| float` | `0` | Minimum scale value |
| `max` | `int \| float` | `100` | Maximum scale value |
| `unit` | `str \| None` | `None` | Optional unit label |
| `thresholds` | `list[dict] \| None` | `None` | Color stops: `[{"value": 80, "color": "#10B981"}, ...]` |
| `height` | `int` | `300` | Chart height in pixels |

### Example

```python title="gauge_example.py"
from holysheet import GaugeChart, Columns

Columns(children=[
    GaugeChart(
        title="API Uptime (SLA)",
        value=99.97,
        min=99.0,
        max=100.0,
        unit="%",
    ),
    GaugeChart(
        title="Avg Response Time",
        value=142,
        min=0,
        max=500,
        unit="ms",
    ),
    GaugeChart(
        title="Error Rate",
        value=0.12,
        min=0,
        max=5,
        unit="%",
    ),
])
```

### With Thresholds

```python title="gauge_thresholds.py"
GaugeChart(
    title="System Load",
    value=73,
    min=0,
    max=100,
    unit="%",
    thresholds=[
        {"value": 50, "color": "#10B981"},  # Green zone
        {"value": 80, "color": "#F59E0B"},  # Warning zone
        {"value": 100, "color": "#EF4444"}, # Danger zone
    ],
)
```

---

## FunnelChart

Conversion funnel for pipeline and process visualization.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data |
| `name` | `str \| None` | `None` | Column for stage labels |
| `value` | `str \| None` | `None` | Column for stage values |
| `height` | `int` | `360` | Chart height in pixels |

### Example

```python title="funnel_example.py"
from holysheet import FunnelChart

FunnelChart(
    title="Sign-up to Paid Conversion",
    data=[
        {"stage": "Website Visitors", "count": 148_200},
        {"stage": "Sign-ups", "count": 24_500},
        {"stage": "Activated", "count": 14_800},
        {"stage": "Trial Started", "count": 8_200},
        {"stage": "Paid Conversion", "count": 3_400},
    ],
    name="stage",
    value="count",
)
```

---

## TreemapChart

Hierarchical treemap for proportional area visualization.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data |
| `name` | `str \| None` | `None` | Column for node labels |
| `value` | `str \| None` | `None` | Column for node sizes |
| `category` | `str \| None` | `None` | Optional column for grouping |
| `height` | `int` | `360` | Chart height in pixels |

### Example

```python title="treemap_example.py"
from holysheet import TreemapChart

TreemapChart(
    title="Cloud Infrastructure Costs",
    data=[
        {"service": "Compute (GKE)", "cost": 42_300},
        {"service": "Cloud SQL", "cost": 28_700},
        {"service": "BigQuery", "cost": 18_500},
        {"service": "Cloud Storage", "cost": 12_800},
        {"service": "Networking", "cost": 9_600},
        {"service": "Pub/Sub", "cost": 6_200},
    ],
    name="service",
    value="cost",
)
```

---

## :bulb: Chart Tips

### Setting Chart Height

All charts default to `360px` height. Override with the `height` prop:

```python
LineChart(title="Trend", data=data, x="date", y="value", height=500)
```

### Multi-Series with `y` as a List

For charts that support `y` as a list (`LineChart`, `AreaChart`, `BarChart`), each column in the list becomes its own series in the chart:

```python title="multi_series.py"
# Each column in y becomes a separate line with its own legend entry
LineChart(
    title="Financial Overview",
    data=monthly_data,
    x="month",
    y=["revenue", "costs", "profit"],
)
```

### Data Format Quick Reference

| Chart | X/Category | Y/Value | Optional |
|:------|:-----------|:--------|:---------|
| `LineChart` | `x` (str) | `y` (str or list) | `series` |
| `AreaChart` | `x` (str) | `y` (str or list) | `series` |
| `BarChart` | `x` (str) | `y` (str or list) | `series` |
| `PieChart` | `name` (str) | `value` (str) | — |
| `ScatterChart` | `x` (str) | `y` (str) | `size`, `category` |
| `RadarChart` | `indicators` (list) | values in data | — |
| `GaugeChart` | — | `value` (number) | `thresholds` |
| `FunnelChart` | `name` (str) | `value` (str) | — |
| `TreemapChart` | `name` (str) | `value` (str) | `category` |

!!! warning "Data Required"
    Most charts require `data` to be provided. If `data` is `None`, the chart will render with no data points. The exception is `GaugeChart`, which uses a direct `value` prop instead of tabular data.
