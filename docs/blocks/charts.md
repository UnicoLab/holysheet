# Charts

HolySheet includes **18 chart types** powered by Apache ECharts, providing rich interactive visualizations with tooltips, legends, and responsive sizing.

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

## HeatmapChart

2D heatmap with color gradient visualization — ideal for showing patterns across two categorical dimensions.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data with x, y, and value columns |
| `x` | `str` | *required* | Column name for X axis categories |
| `y` | `str` | *required* | Column name for Y axis categories |
| `value` | `str` | *required* | Column name for the heat value |
| `height` | `int` | `360` | Chart height in pixels |

!!! example "Website Traffic Heatmap"

    ```python title="heatmap_example.py"
    from holysheet import HeatmapChart

    heatmap_data = []
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        for hour in ["9am", "10am", "11am", "12pm", "1pm", "2pm"]:
            heatmap_data.append({"day": day, "hour": hour, "visits": random.randint(10, 200)})

    HeatmapChart(
        title="Website Traffic by Day & Hour",
        data=heatmap_data,
        x="hour",
        y="day",
        value="visits",
    )
    ```

---

## CandlestickChart

Financial OHLC (Open-High-Low-Close) candlestick chart for stock price and financial data.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data with OHLC columns |
| `x` | `str` | *required* | Column for date/category axis |
| `open` | `str` | `"open"` | Column for open price |
| `close` | `str` | `"close"` | Column for close price |
| `low` | `str` | `"low"` | Column for low price |
| `high` | `str` | `"high"` | Column for high price |
| `height` | `int` | `400` | Chart height in pixels |

!!! example "Stock Price Chart"

    ```python title="candlestick_example.py"
    from holysheet import CandlestickChart

    CandlestickChart(
        title="AAPL Stock Price",
        data=[
            {"date": "2024-01", "open": 142.5, "close": 148.3, "low": 138.2, "high": 150.1},
            {"date": "2024-02", "open": 148.3, "close": 155.7, "low": 145.0, "high": 158.4},
            {"date": "2024-03", "open": 155.7, "close": 149.8, "low": 146.3, "high": 159.2},
        ],
        x="date",
    )
    ```

!!! tip "Custom Column Names"
    If your data uses different column names (e.g. `open_price` instead of `open`), specify them explicitly: `open="open_price"`, `close="close_price"`, etc.

---

## SankeyChart

Sankey / flow diagram for visualizing flows, energy transfers, or revenue attribution.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `nodes` | `list[dict]` | *required* | List of node dicts with `name` key |
| `links` | `list[dict]` | *required* | List of link dicts with `source`, `target`, `value` |
| `height` | `int` | `400` | Chart height in pixels |

!!! example "Revenue Flow"

    ```python title="sankey_example.py"
    from holysheet import SankeyChart

    SankeyChart(
        title="Revenue Flow",
        nodes=[
            {"name": "Product Sales"},
            {"name": "Services"},
            {"name": "North America"},
            {"name": "Europe"},
            {"name": "Net Revenue"},
        ],
        links=[
            {"source": "Product Sales", "target": "North America", "value": 450},
            {"source": "Product Sales", "target": "Europe", "value": 280},
            {"source": "Services", "target": "North America", "value": 200},
            {"source": "North America", "target": "Net Revenue", "value": 650},
            {"source": "Europe", "target": "Net Revenue", "value": 280},
        ],
    )
    ```

!!! info "Sankey vs Other Charts"
    Unlike most charts, `SankeyChart` does **not** use `data`/`x`/`y` props. Instead, it takes explicit `nodes` and `links` lists.

---

## WaterfallChart

Waterfall / bridge chart for financial analysis — shows how individual values contribute to a total.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data with category and value columns |
| `category` | `str` | *required* | Column name for categories |
| `value` | `str` | *required* | Column name for values (positive = green, negative = red) |
| `height` | `int` | `360` | Chart height in pixels |

!!! example "Revenue Bridge"

    ```python title="waterfall_example.py"
    from holysheet import WaterfallChart

    WaterfallChart(
        title="Revenue Bridge Q3 → Q4",
        data=[
            {"item": "Q3 Revenue", "amount": 1850},
            {"item": "New Customers", "amount": 420},
            {"item": "Upsells", "amount": 180},
            {"item": "Churn", "amount": -210},
            {"item": "Refunds", "amount": -45},
        ],
        category="item",
        value="amount",
    )
    ```

---

## BoxPlotChart

Statistical box-and-whisker plot for visualizing data distributions.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `list[list[float]]` | *required* | Each inner list: `[min, Q1, median, Q3, max]` |
| `categories` | `list[str] \| None` | `None` | Labels for each box |
| `height` | `int` | `360` | Chart height in pixels |

!!! example "Response Time Distribution"

    ```python title="boxplot_example.py"
    from holysheet import BoxPlotChart

    BoxPlotChart(
        title="API Response Time (ms)",
        data=[
            [12, 45, 68, 120, 250],   # API v1
            [8, 32, 55, 95, 180],     # API v2
            [15, 52, 82, 145, 310],   # GraphQL
        ],
        categories=["API v1", "API v2", "GraphQL"],
    )
    ```

!!! info "Data Format"
    Each inner list represents one box: `[min, Q1, median, Q3, max]`. This is **not** raw data — you need to pre-compute the statistics.

---

## MapChart

Geographical scatter chart for visualizing data points on a coordinate grid.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `data` | `Any` | `None` | Tabular data with lat/lng/value columns |
| `lat` | `str` | *required* | Column name for latitude |
| `lng` | `str` | *required* | Column name for longitude |
| `value` | `str` | *required* | Column name for bubble size |
| `name` | `str \| None` | `None` | Column name for point labels |
| `height` | `int` | `400` | Chart height in pixels |

!!! example "Global User Distribution"

    ```python title="map_example.py"
    from holysheet import MapChart

    MapChart(
        title="Global Users",
        data=[
            {"lat": 40.7, "lng": -74.0, "users": 45000, "city": "New York"},
            {"lat": 51.5, "lng": -0.1, "users": 38000, "city": "London"},
            {"lat": 35.7, "lng": 139.7, "users": 32000, "city": "Tokyo"},
        ],
        lat="lat",
        lng="lng",
        value="users",
        name="city",
    )
    ```

---

## GanttChart

Project timeline / Gantt chart for visualizing task schedules, durations, and progress.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `tasks` | `list[dict]` | `[]` | List of task dicts with `name`, `start`, `end`, and optional `progress`, `color`, `group` |
| `height` | `int` | `400` | Chart height in pixels |

**Task dict keys:** `name` (str, required), `start` (str, required — date like `"2026-01-15"`), `end` (str, required), `progress` (float 0–1, optional), `color` (str, optional hex color), `group` (str, optional — for row grouping)

!!! example "Sprint Planning"

    ```python title="gantt_example.py"
    from holysheet import GanttChart

    GanttChart(
        title="Q1 Project Timeline",
        tasks=[
            {"name": "Requirements", "start": "2026-01-06", "end": "2026-01-17",
             "progress": 1.0, "group": "Phase 1"},
            {"name": "Design", "start": "2026-01-13", "end": "2026-01-31",
             "progress": 0.8, "group": "Phase 1"},
            {"name": "Backend Dev", "start": "2026-01-27", "end": "2026-03-07",
             "progress": 0.45, "group": "Phase 2"},
            {"name": "Frontend Dev", "start": "2026-02-03", "end": "2026-03-14",
             "progress": 0.3, "group": "Phase 2"},
            {"name": "Testing", "start": "2026-03-02", "end": "2026-03-21",
             "progress": 0.0, "group": "Phase 3"},
            {"name": "Launch", "start": "2026-03-21", "end": "2026-03-28",
             "progress": 0.0, "group": "Phase 3"},
        ],
        height=350,
    )
    ```

!!! tip "Progress Values"
    The `progress` field is a float between `0.0` (not started) and `1.0` (complete). It controls the filled portion of each task bar.

---

## DAGChart

Directed acyclic graph (DAG) for visualizing workflows, dependency trees, and pipeline architectures.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `nodes` | `list[dict]` | `[]` | List of node dicts with `id`, `label`, and optional `color`, `icon` |
| `edges` | `list[dict]` | `[]` | List of edge dicts with `from`, `to`, and optional `label` |
| `height` | `int` | `400` | Chart height in pixels |
| `layout` | `"force" \| "circular"` | `"force"` | Graph layout algorithm |

!!! example "Data Pipeline"

    ```python title="dag_example.py"
    from holysheet import DAGChart

    DAGChart(
        title="ML Pipeline",
        nodes=[
            {"id": "ingest", "label": "Data Ingestion"},
            {"id": "clean", "label": "Cleaning"},
            {"id": "features", "label": "Feature Engineering"},
            {"id": "train", "label": "Model Training"},
            {"id": "eval", "label": "Evaluation"},
            {"id": "deploy", "label": "Deployment"},
        ],
        edges=[
            {"from": "ingest", "to": "clean"},
            {"from": "clean", "to": "features"},
            {"from": "features", "to": "train"},
            {"from": "train", "to": "eval"},
            {"from": "eval", "to": "deploy"},
            {"from": "eval", "to": "train", "label": "retrain"},
        ],
        layout="force",
    )
    ```

### Layout Options

=== "Force (default)"

    Physics-based force-directed layout — nodes repel each other and edges act as springs. Best for general-purpose graphs.

    ```python
    DAGChart(title="Graph", nodes=nodes, edges=edges, layout="force")
    ```

=== "Circular"

    Nodes arranged in a circle. Best for small graphs where you want to emphasize connectivity.

    ```python
    DAGChart(title="Graph", nodes=nodes, edges=edges, layout="circular")
    ```

!!! info "DAGChart vs SankeyChart"
    Use `DAGChart` when you want to show **structural relationships** (dependencies, workflows). Use `SankeyChart` when you want to show **flow quantities** (revenue attribution, energy transfers).

---

## CorrelationMatrix

Statistical correlation heatmap for visualizing pairwise relationships between variables.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Chart title |
| `matrix` | `list[list[float]]` | `[]` | 2D array of correlation values (typically in `[-1, 1]`) |
| `labels` | `list[str]` | `[]` | Row/column labels (must match matrix dimensions) |
| `height` | `int` | `400` | Chart height in pixels |

!!! example "Feature Correlations"

    ```python title="correlation_example.py"
    from holysheet import CorrelationMatrix

    CorrelationMatrix(
        title="Feature Correlation Matrix",
        labels=["Revenue", "Users", "NPS", "Churn", "ARPU"],
        matrix=[
            [ 1.00,  0.85,  0.62, -0.45,  0.91],
            [ 0.85,  1.00,  0.71, -0.38,  0.76],
            [ 0.62,  0.71,  1.00, -0.55,  0.58],
            [-0.45, -0.38, -0.55,  1.00, -0.42],
            [ 0.91,  0.76,  0.58, -0.42,  1.00],
        ],
    )
    ```

### With Pandas

```python title="correlation_pandas.py"
import pandas as pd
from holysheet import CorrelationMatrix

df = pd.DataFrame({
    "revenue": [100, 200, 150, 300, 250],
    "users": [1000, 2000, 1500, 3000, 2500],
    "nps": [72, 78, 75, 82, 80],
    "churn": [5.2, 4.1, 4.8, 3.2, 3.8],
})

corr = df.corr()

CorrelationMatrix(
    title="Metric Correlations",
    labels=corr.columns.tolist(),
    matrix=corr.values.tolist(),
)
```

!!! tip "Pre-computed Matrix"
    Unlike most chart blocks, `CorrelationMatrix` does **not** accept raw `data`. You need to pre-compute the correlation matrix (e.g. via `df.corr()` in pandas).

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
| `HeatmapChart` | `x`, `y` (str) | `value` (str) | — |
| `CandlestickChart` | `x` (str) | `open`, `close`, `low`, `high` | — |
| `SankeyChart` | `nodes` (list) | `links` (list) | — |
| `WaterfallChart` | `category` (str) | `value` (str) | — |
| `BoxPlotChart` | `categories` (list) | `data` (nested lists) | — |
| `MapChart` | `lat`, `lng` (str) | `value` (str) | `name` |
| `GanttChart` | — | `tasks` (list) | `height` |
| `DAGChart` | `nodes` (list) | `edges` (list) | `layout` |
| `CorrelationMatrix` | `labels` (list) | `matrix` (nested lists) | — |

!!! warning "Data Required"
    Most charts require `data` to be provided. If `data` is `None`, the chart will render with no data points. The exceptions are `GaugeChart` (uses a direct `value` prop), `SankeyChart` (uses `nodes`/`links`), `BoxPlotChart` (uses nested lists), `GanttChart` (uses `tasks`), `DAGChart` (uses `nodes`/`edges`), and `CorrelationMatrix` (uses `matrix`/`labels`).
