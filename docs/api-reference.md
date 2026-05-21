# API Reference

Complete API reference for HolySheet v0.3.0.

---

## Report

::: holysheet.report.Report

The main class for composing dashboards.

### Constructor

```python
Report(
    title: str = "Untitled Report",
    subtitle: str | None = None,
    theme: str = "light",
    logo_url: str | None = None,
    author: str | None = None,
    report_version: str | None = None,
    footer: str | None = None,
)
```

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `title` | `str` | `"Untitled Report"` | Report title displayed in the header |
| `subtitle` | `str \| None` | `None` | Optional subtitle below the title |
| `theme` | `str` | `"light"` | Theme name: `"light"`, `"dark"`, or `"executive"` |
| `logo_url` | `str \| None` | `None` | URL for a logo image in the header |
| `author` | `str \| None` | `None` | Report author name |
| `report_version` | `str \| None` | `None` | Report version string |
| `footer` | `str \| None` | `None` | Custom footer text |

### Methods

#### `add(block) → Report`

Append a block to the report. Returns `self` for method chaining.

```python
report.add(KPI(label="Revenue", value="$1.2M"))
report.add(KPI(label="A", value=1)).add(KPI(label="B", value=2))  # Chaining
```

#### `export_html(path) → Path`

Export as a standalone HTML file. Returns the resolved output path.

```python
path = report.export_html("report.html")
```

#### `export_folder(path) → Path`

Export as a folder with `index.html`, `assets/`, and `report.json`. Returns the resolved output directory path.

```python
path = report.export_folder("dist/")
```

#### `export_json(path) → Path`

Export just the JSON spec file. Returns the resolved output path.

```python
path = report.export_json("report.json")
```

#### `to_json(pretty=False) → str`

Serialize the report to a JSON string.

```python
json_str = report.to_json(pretty=True)
```

#### `to_schema() → ReportSchema`

Build a `ReportSchema` Pydantic model from the report.

```python
schema = report.to_schema()
print(schema.title, schema.theme, len(schema.blocks))
```

### Properties

#### `blocks → list[Block]`

Read-only list of current blocks.

```python
print(f"Report has {len(report.blocks)} blocks")
```

---

## Block Types

All blocks inherit from `Block` and are imported from `holysheet`:

```python
from holysheet import KPI, Metric, LineChart, BarChart, AreaChart, ...
```

---

### KPI

```python
KPI(
    label: str,
    value: str | int | float,
    unit: str | None = None,
    delta: str | None = None,
    status: Literal["positive", "negative", "neutral"] | None = None,
    description: str | None = None,
)
```

---

### Metric

```python
Metric(
    label: str,
    value: str | int | float,
    unit: str | None = None,
    icon: str | None = None,
)
```

---

### StatComparison

```python
StatComparison(
    title: str,
    items: list[dict[str, Any]] = [],
    # Each item: {"label": str, "current": val, "previous": val, "unit": str?}
)
```

---

### LineChart

```python
LineChart(
    title: str,
    data: Any = None,
    x: str | None = None,
    y: str | list[str] | None = None,
    series: list[str] | None = None,
    height: int = 360,
)
```

---

### AreaChart

```python
AreaChart(
    title: str,
    data: Any = None,
    x: str | None = None,
    y: str | list[str] | None = None,
    series: list[str] | None = None,
    height: int = 360,
)
```

---

### BarChart

```python
BarChart(
    title: str,
    data: Any = None,
    x: str | None = None,
    y: str | list[str] | None = None,
    series: list[str] | None = None,
    height: int = 360,
)
```

---

### PieChart

```python
PieChart(
    title: str,
    data: Any = None,
    name: str | None = None,
    value: str | None = None,
    height: int = 360,
)
```

---

### ScatterChart

```python
ScatterChart(
    title: str,
    data: Any = None,
    x: str | None = None,
    y: str | None = None,
    size: str | None = None,
    category: str | None = None,
    height: int = 360,
)
```

---

### RadarChart

```python
RadarChart(
    title: str,
    data: Any = None,
    indicators: list[str] = [],
    height: int = 360,
)
```

---

### GaugeChart

```python
GaugeChart(
    title: str,
    value: int | float = 0,
    min: int | float = 0,
    max: int | float = 100,
    unit: str | None = None,
    thresholds: list[dict[str, Any]] | None = None,
    height: int = 300,
)
```

---

### FunnelChart

```python
FunnelChart(
    title: str,
    data: Any = None,
    name: str | None = None,
    value: str | None = None,
    height: int = 360,
)
```

---

### TreemapChart

```python
TreemapChart(
    title: str,
    data: Any = None,
    name: str | None = None,
    value: str | None = None,
    category: str | None = None,
    height: int = 360,
)
```

---

### DataTable

```python
DataTable(
    title: str,
    data: Any = None,
    columns: list[str] | None = None,
    searchable: bool = True,
    paginated: bool = True,
)
```

---

### Markdown

```python
Markdown(
    content: str,
)
```

---

### CodeBlock

```python
CodeBlock(
    code: str,
    language: str | None = None,
    title: str | None = None,
)
```

---

### Image

```python
Image(
    src: str,
    alt: str | None = None,
    caption: str | None = None,
    width: str | int | None = None,
    height: str | int | None = None,
)
```

---

### Alert

```python
Alert(
    severity: Literal["info", "warning", "error", "success"] = "info",
    title: str | None = None,
    message: str = "",
)
```

---

### ProgressBar

```python
ProgressBar(
    label: str,
    value: int | float = 0,
    max: int | float = 100,
    color: str | None = None,
    description: str | None = None,
)
```

---

### Divider

```python
Divider(
    label: str | None = None,
    variant: Literal["solid", "dashed", "dotted"] = "solid",
)
```

---

### Section

```python
Section(
    title: str,
    description: str | None = None,
    children: list[Block] = [],
)
```

---

### Columns

```python
Columns(
    children: list[Block] = [],
    widths: list[int] | None = None,
    layout: Literal["equal", "bento", "custom"] = "equal",
)
```

---

### Tabs

```python
Tabs(
    tabs: list[dict[str, Any]] = [],
    # Each tab: {"label": str, "children": list[Block]}
)
```

---

### Accordion

```python
Accordion(
    panels: list[dict[str, Any]] = [],
    # Each panel: {"title": str, "subtitle": str?, "children": list[Block], "default_expanded": bool?}
)
```

---

### Slider

```python
Slider(
    label: str,
    min: int | float = 0,
    max: int | float = 100,
    step: int | float = 1,
    default_value: int | float | list[int | float] | None = None,
    unit: str | None = None,
    show_value: bool = True,
)
```

---

### NumberInput

```python
NumberInput(
    label: str,
    min: int | float = 0,
    max: int | float = 100,
    step: int | float = 1,
    default_value: int | float = 0,
    unit: str | None = None,
)
```

---

### Toggle

```python
Toggle(
    label: str,
    description: str | None = None,
    default_value: bool = False,
)
```

---

### HeatmapChart

```python
HeatmapChart(title: str, data: Any = None, x: str = "", y: str = "", value: str = "", height: int = 360)
```

---

### CandlestickChart

```python
CandlestickChart(title: str, data: Any = None, x: str = "", open: str = "open", close: str = "close", low: str = "low", high: str = "high", height: int = 400)
```

---

### SankeyChart

```python
SankeyChart(title: str, nodes: list[dict] = [], links: list[dict] = [], height: int = 400)
```

---

### WaterfallChart

```python
WaterfallChart(title: str, data: Any = None, category: str = "", value: str = "", height: int = 360)
```

---

### BoxPlotChart

```python
BoxPlotChart(title: str, data: list[list[float]] = [], categories: list[str] | None = None, height: int = 360)
```

---

### MapChart

```python
MapChart(title: str, data: Any = None, lat: str = "", lng: str = "", value: str = "", name: str | None = None, height: int = 400)
```

---

### Timeline

```python
Timeline(title: str | None = None, events: list[dict] = [])
# Event dict: {"date": str, "title": str, "description"?: str, "icon"?: str, "color"?: str}
```

---

### Callout

```python
Callout(content: str, author: str | None = None, icon: str | None = None, variant: Literal["quote", "highlight", "note"] = "quote")
```

---

### Embed

```python
Embed(url: str, title: str | None = None, height: int = 400, aspect_ratio: str | None = None)
```

---

### JsonViewer

```python
JsonViewer(data: Any = None, title: str | None = None, collapsed_depth: int = 2)
```

---

### UserCard

```python
UserCard(name: str, role: str | None = None, avatar_url: str | None = None, email: str | None = None, stats: list[dict] | None = None)
# Stats dict: {"label": str, "value": str}
```

---

### StatusList

```python
StatusList(title: str | None = None, items: list[dict] = [])
# Item dict: {"label": str, "status": "success"|"warning"|"error"|"info"|"pending", "description"?: str, "value"?: str}
```

---

### InfoList

```python
InfoList(title: str | None = None, items: list[dict] = [])
# Item dict: {"key": str, "value": str, "icon"?: str}
```

---

### Stepper

```python
Stepper(title: str | None = None, steps: list[dict] = [], current_step: int | None = None)
# Step dict: {"label": str, "description"?: str, "status"?: "complete"|"active"|"pending"}
```

---

### TagList

```python
TagList(title: str | None = None, tags: list[dict] = [])
# Tag dict: {"label": str, "color"?: str, "variant"?: str}
```

---

### Sparkline

```python
Sparkline(data: list[int | float] = [], color: str | None = None, height: int = 60, show_area: bool = True)
```

---

### Video

```python
Video(src: str, title: str | None = None, poster: str | None = None, autoplay: bool = False, controls: bool = True)
```

---

### Dropdown

```python
Dropdown(label: str, options: list[dict] = [], default_value: Any = None, description: str | None = None)
# Option dict: {"label": str, "value": Any}
```

---

### TextInput

```python
TextInput(label: str, placeholder: str | None = None, default_value: str | None = None, multiline: bool = False, rows: int = 3, description: str | None = None)
```

---

### CheckboxGroup

```python
CheckboxGroup(label: str, options: list[dict] = [], default_values: list | None = None, description: str | None = None)
# Option dict: {"label": str, "value": Any}
```

---

### RadioGroup

```python
RadioGroup(label: str, options: list[dict] = [], default_value: Any = None, description: str | None = None)
# Option dict: {"label": str, "value": Any}
```

---

## Schema Types

### ReportSchema

```python
from holysheet.schema import ReportSchema

ReportSchema(
    schema_version: str = "1.0.0",
    title: str = "Untitled Report",
    subtitle: str | None = None,
    theme: str = "light",
    logo_url: str | None = None,
    author: str | None = None,
    report_version: str | None = None,
    footer: str | None = None,
    created_at: str = <auto>,     # ISO-8601 timestamp
    blocks: list[dict] = [],       # Serialized block dicts
)
```

#### Methods

| Method | Returns | Description |
|:-------|:--------|:------------|
| `to_dict()` | `dict` | Convert to plain dict |
| `to_json(pretty=False)` | `str` | Serialize to JSON string |
| `to_json_bytes()` | `bytes` | Serialize to JSON bytes (orjson) |

---

## Utility Functions

### `to_records(data) → list[dict]`

```python
from holysheet.data import to_records
```

Convert any supported data format to `list[dict[str, Any]]`. Handles pandas, polars, dicts, and lists.

### `validate_theme(name) → dict`

```python
from holysheet.themes import validate_theme
```

Return the theme dict for the given name, or raise `HolySheetError`.

### `list_themes() → list[str]`

```python
from holysheet.themes import list_themes
```

Return sorted list of available theme names: `['dark', 'executive', 'light']`.

---

## Exceptions

All exceptions inherit from `HolySheetError`:

| Exception | When |
|:----------|:-----|
| `HolySheetError` | Base exception for all HolySheet errors |
| `SchemaValidationError` | Report schema fails Pydantic validation |
| `ExportError` | Writing files fails during export |
| `RendererAssetError` | Prebuilt React JS/CSS bundles are missing |
| `DataConversionError` | Data cannot be converted to records |

```python title="error_handling.py"
from holysheet.exceptions import HolySheetError, DataConversionError

try:
    report.export_html("report.html")
except HolySheetError as e:
    print(f"HolySheet error: {e.message}")
```
