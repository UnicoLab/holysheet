# Block Types Overview

HolySheet ships with **53 block types** organized into five categories. Each block is a Pydantic v2 model with full type safety and validation.

---

## :bar_chart: Quick Reference

### :chart_with_upwards_trend: Charts (18 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`LineChart`](charts.md#linechart) | `line_chart` | Multi-series line chart | `data`, `x`, `y`, `series`, `height` |
| [`AreaChart`](charts.md#areachart) | `area_chart` | Filled area chart | `data`, `x`, `y`, `series`, `height` |
| [`BarChart`](charts.md#barchart) | `bar_chart` | Grouped/stacked bar chart | `data`, `x`, `y`, `series`, `height` |
| [`PieChart`](charts.md#piechart) | `pie_chart` | Pie / donut chart | `data`, `name`, `value`, `height` |
| [`ScatterChart`](charts.md#scatterchart) | `scatter_chart` | Scatter / bubble plot | `data`, `x`, `y`, `size`, `category` |
| [`RadarChart`](charts.md#radarchart) | `radar_chart` | Radar / spider chart | `data`, `indicators`, `height` |
| [`GaugeChart`](charts.md#gaugechart) | `gauge` | Speedometer gauge | `value`, `min`, `max`, `thresholds` |
| [`FunnelChart`](charts.md#funnelchart) | `funnel_chart` | Conversion funnel | `data`, `name`, `value`, `height` |
| [`TreemapChart`](charts.md#treemapchart) | `treemap_chart` | Hierarchical treemap | `data`, `name`, `value`, `category` |
| [`HeatmapChart`](charts.md#heatmapchart) | `heatmap_chart` | 2D heatmap with color gradient | `data`, `x`, `y`, `value` |
| [`CandlestickChart`](charts.md#candlestickchart) | `candlestick_chart` | Financial OHLC chart | `data`, `x`, `open`, `close`, `low`, `high` |
| [`SankeyChart`](charts.md#sankeychart) | `sankey_chart` | Flow / energy diagram | `nodes`, `links` |
| [`WaterfallChart`](charts.md#waterfallchart) | `waterfall_chart` | Waterfall / bridge chart | `data`, `category`, `value` |
| [`BoxPlotChart`](charts.md#boxplotchart) | `boxplot_chart` | Statistical box plot | `data`, `categories` |
| [`MapChart`](charts.md#mapchart) | `map_chart` | Geographical scatter | `data`, `lat`, `lng`, `value`, `name` |
| [`GanttChart`](charts.md#ganttchart) | `gantt_chart` | Project timeline / Gantt chart | `tasks`, `height` |
| [`DAGChart`](charts.md#dagchart) | `dag_chart` | Directed acyclic graph | `nodes`, `edges`, `layout` |
| [`CorrelationMatrix`](charts.md#correlationmatrix) | `correlation_matrix` | Statistical correlation heatmap | `matrix`, `labels`, `height` |

### :chart_with_upwards_trend: KPI & Metrics (4 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`KPI`](kpi-metrics.md#kpi) | `kpi` | Key metric card with delta | `label`, `value`, `unit`, `delta`, `status` |
| [`Metric`](kpi-metrics.md#metric) | `metric` | Compact inline metric | `label`, `value`, `unit`, `icon` |
| [`StatComparison`](kpi-metrics.md#statcomparison) | `stat_comparison` | Side-by-side stat comparison | `title`, `items` |
| `ProgressBar` | `progress` | Progress indicator | `label`, `value`, `max`, `color` |

### :page_facing_up: Data & Content (14 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`DataTable`](data-content.md#datatable) | `data_table` | Searchable, paginated table | `data`, `columns`, `searchable`, `paginated` |
| [`Markdown`](data-content.md#markdown) | `markdown` | Rich text content | `content` |
| [`CodeBlock`](data-content.md#codeblock) | `code_block` | Syntax-highlighted code | `code`, `language`, `title` |
| [`Image`](data-content.md#image) | `image` | Image display | `src`, `alt`, `caption`, `width` |
| [`Alert`](data-content.md#alert) | `alert` | Callout / notification | `severity`, `title`, `message` |
| [`Timeline`](data-content.md#timeline) | `timeline` | Vertical event timeline | `events` |
| [`Callout`](data-content.md#callout) | `callout` | Styled quote / highlight | `content`, `author`, `variant` |
| [`JsonViewer`](data-content.md#jsonviewer) | `json_viewer` | Interactive JSON tree | `data`, `collapsed_depth` |
| [`UserCard`](data-content.md#usercard) | `user_card` | Team member card | `name`, `role`, `stats` |
| [`StatusList`](data-content.md#statuslist) | `status_list` | Status indicators list | `items` |
| [`InfoList`](data-content.md#infolist) | `info_list` | Key-value pair display | `items` |
| [`Sparkline`](data-content.md#sparkline) | `sparkline` | Tiny inline chart | `data`, `color` |
| [`Scorecard`](data-content.md#scorecard) | `scorecard` | Conditional color metric grid | `data`, `value_column`, `thresholds` |
| [`DataProfile`](data-content.md#dataprofile) | `data_profile` | Auto-EDA column statistics | `columns` |

### :bricks: Layout (8 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`Section`](layout.md#section) | `section` | Group blocks with heading | `title`, `description`, `children` |
| [`Columns`](layout.md#columns) | `columns` | Multi-column grid | `children`, `widths`, `layout` |
| [`Tabs`](layout.md#tabs) | `tabs` | Tabbed content panels | `tabs` (list of `{label, children}`) |
| [`Divider`](layout.md#divider) | `divider` | Visual separator line | `label`, `variant` |
| [`Accordion`](layout.md#accordion) | `accordion` | Collapsible panels | `panels` |
| [`Stepper`](data-content.md#stepper) | `stepper` | Process / wizard steps | `steps`, `current_step` |
| [`TagList`](data-content.md#taglist) | `tag_list` | Colored tag/badge chips | `tags` |
| [`Compare`](layout.md#compare) | `compare` | Side-by-side comparison container | `left_children`, `right_children`, `mode` |

### :video_game: Interactive (9 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`Slider`](interactive.md#slider) | `slider` | Interactive slider | `label`, `min`, `max`, `step`, `default_value` |
| [`NumberInput`](interactive.md#numberinput) | `number_input` | Number input with buttons | `label`, `min`, `max`, `step` |
| [`Toggle`](interactive.md#toggle) | `toggle` | On/off switch | `label`, `description`, `default_value` |
| [`Dropdown`](interactive.md#dropdown) | `dropdown` | Select from options | `label`, `options`, `default_value` |
| [`TextInput`](interactive.md#textinput) | `text_input` | Text / textarea input | `label`, `placeholder`, `multiline` |
| [`CheckboxGroup`](interactive.md#checkboxgroup) | `checkbox_group` | Multiple checkboxes | `label`, `options`, `default_values` |
| [`RadioGroup`](interactive.md#radiogroup) | `radio_group` | Single-select radio buttons | `label`, `options`, `default_value` |
| [`Embed`](data-content.md#embed) | `embed` | Iframe embed | `url`, `height` |
| [`Video`](data-content.md#video) | `video` | HTML5 video player | `src`, `poster`, `controls` |

---

## :jigsaw: How Blocks Work

Every block inherits from `Block` — a Pydantic v2 `BaseModel` with a `type` discriminator:

```python title="Basic block usage"
from holysheet import Report, KPI, LineChart

report = Report(title="Dashboard", theme="dark")

# Just instantiate and add
report.add(KPI(label="Revenue", value="$1.2M", delta="+12%", status="positive"))
report.add(LineChart(title="Trend", data=my_data, x="date", y="revenue"))  # (1)!

report.export_html("dashboard.html")
```

!!! tip "Method Chaining"
    `report.add()` returns `self`, so you can chain calls:

    ```python
    report.add(KPI(label="A", value=1)).add(KPI(label="B", value=2))
    ```

---

## :arrow_right: Detailed References

- **[KPI & Metrics](kpi-metrics.md)** — KPI cards, compact metrics, stat comparisons
- **[Charts](charts.md)** — All 18 chart types with data format examples
- **[Data & Content](data-content.md)** — Tables, markdown, code, images, alerts, timelines, scorecards, and more
- **[Layout](layout.md)** — Columns, sections, tabs, dividers, accordions, compare containers
- **[Interactive](interactive.md)** — Sliders, toggles, dropdowns, text inputs, checkboxes, and radio buttons
