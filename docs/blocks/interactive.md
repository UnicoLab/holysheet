# Interactive Blocks

Interactive blocks add user controls to your dashboard — sliders, number inputs, toggles, dropdowns, text inputs, and more. These provide a way to include interactive UI elements with local state in your reports.

---

## Slider

Interactive slider control for selecting numeric values or ranges.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Slider label |
| `min` | `int \| float` | `0` | Minimum value |
| `max` | `int \| float` | `100` | Maximum value |
| `step` | `int \| float` | `1` | Step increment |
| `default_value` | `int \| float \| list \| None` | `None` | Initial value(s) |
| `unit` | `str \| None` | `None` | Optional unit label |
| `show_value` | `bool` | `True` | Display the current value |

### Single Value Slider

```python title="slider_single.py"
from holysheet import Slider

Slider(
    label="Budget Threshold",
    min=0,
    max=1_000_000,
    step=10_000,
    default_value=500_000,
    unit="$",
)
```

### Range Slider

Pass a **list of two values** to `default_value` for a range slider:

```python title="slider_range.py"
Slider(
    label="Date Range",
    min=2020,
    max=2026,
    step=1,
    default_value=[2023, 2025],  # Range selection
)
```

### Decimal Steps

```python title="slider_decimal.py"
Slider(
    label="Confidence Level",
    min=0.0,
    max=1.0,
    step=0.05,
    default_value=0.95,
    unit="%",
    show_value=True,
)
```

---

## NumberInput

Numeric input field with increment/decrement buttons for precise value entry.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Input label |
| `min` | `int \| float` | `0` | Minimum value |
| `max` | `int \| float` | `100` | Maximum value |
| `step` | `int \| float` | `1` | Step increment |
| `default_value` | `int \| float` | `0` | Initial value |
| `unit` | `str \| None` | `None` | Optional unit label |

### Example

```python title="number_input_example.py"
from holysheet import NumberInput

NumberInput(
    label="Target Revenue",
    min=0,
    max=10_000_000,
    step=100_000,
    default_value=2_000_000,
    unit="$",
)
```

### Multiple Inputs in a Row

```python title="number_inputs_row.py"
from holysheet import NumberInput, Columns

Columns(children=[
    NumberInput(
        label="Min Price",
        min=0, max=1000,
        step=10, default_value=100,
        unit="$",
    ),
    NumberInput(
        label="Max Price",
        min=0, max=1000,
        step=10, default_value=500,
        unit="$",
    ),
    NumberInput(
        label="Quantity",
        min=1, max=100,
        step=1, default_value=10,
    ),
])
```

---

## Toggle

On/off switch for boolean state.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Toggle label |
| `description` | `str \| None` | `None` | Optional description text |
| `default_value` | `bool` | `False` | Initial state |

### Example

```python title="toggle_example.py"
from holysheet import Toggle

Toggle(
    label="Show Advanced Metrics",
    description="Display detailed performance metrics and breakdowns",
    default_value=False,
)
```

### Multiple Toggles

```python title="toggles_multiple.py"
from holysheet import Toggle, Columns

Columns(children=[
    Toggle(
        label="Dark Mode",
        description="Switch to dark theme",
        default_value=True,
    ),
    Toggle(
        label="Show Targets",
        description="Overlay target lines on charts",
        default_value=False,
    ),
    Toggle(
        label="Include Forecasts",
        description="Show projected values",
        default_value=True,
    ),
])
```

---

## :brain: How Interactive State Works

Interactive blocks in HolySheet render as functional UI controls in the browser. Here's how they work:

### Current Behavior

1. **Visual Controls** — Sliders, number inputs, and toggles render as fully interactive React components
2. **Local State** — Each control maintains its own local state in the browser
3. **Display Only** — Currently, changing a control's value does not automatically filter or update other blocks in the dashboard

!!! info "Interactive Blocks Are Visual"
    In the current version (v0.3.0), interactive blocks serve as **visual input elements**. They display and respond to user interaction within the dashboard but do not yet trigger cross-block reactivity.

### Future Roadmap

Future versions of HolySheet plan to introduce:

- **Cross-block reactivity** — Slider changes filtering chart data in real-time
- **Event callbacks** — Python-defined logic for control interactions
- **Linked controls** — Multiple controls driving shared state
- **Dashboard filters** — Global filter bar with interactive controls

!!! tip "Use Case: Presentation Dashboards"
    Interactive blocks are already useful in **presentation contexts** — for example, a slider showing different scenarios, or toggles indicating which options are selected. They add polish and interactivity even without cross-block reactivity.

---

## :jigsaw: Control Panel Pattern

A common pattern is grouping interactive controls in a "control panel" section at the top of the dashboard:

```python title="control_panel.py"
from holysheet import (
    Report, Section, Columns,
    Slider, NumberInput, Toggle, Divider,
    KPI, LineChart,
)

report = Report(title="Interactive Dashboard", theme="dark")

# Control panel
report.add(Section(
    title="Dashboard Controls",
    description="Adjust parameters to explore the data",
    children=[
        Columns(children=[
            Slider(label="Time Range", min=2020, max=2026, default_value=[2023, 2026]),
            NumberInput(label="Target Revenue", min=0, max=10_000_000,
                       step=100_000, default_value=2_000_000, unit="$"),
            Toggle(label="Show Forecasts", default_value=True),
        ]),
    ],
))

report.add(Divider())

# Dashboard content
report.add(KPI(label="Revenue", value="$4.64M", delta="+23%", status="positive"))
report.add(LineChart(title="Revenue Trend", data=data, x="month", y="revenue"))

report.export_html("interactive_dashboard.html")
```

---

## Dropdown

Interactive select/dropdown for choosing from predefined options.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Dropdown label |
| `options` | `list[dict]` | *required* | List of `{label, value}` dicts |
| `default_value` | `Any \| None` | `None` | Initially selected value |
| `description` | `str \| None` | `None` | Helper text |

```python title="dropdown_example.py"
from holysheet import Dropdown

Dropdown(
    label="Select Region",
    options=[
        {"label": "🇺🇸 North America", "value": "na"},
        {"label": "🇪🇺 Europe", "value": "eu"},
        {"label": "🌏 Asia Pacific", "value": "apac"},
    ],
    default_value="na",
    description="Filter dashboard data by region",
)
```

---

## TextInput

Text or textarea input field with placeholder support.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Input label |
| `placeholder` | `str \| None` | `None` | Placeholder text |
| `default_value` | `str \| None` | `None` | Initial value |
| `multiline` | `bool` | `False` | Enable multi-line textarea |
| `rows` | `int` | `3` | Number of rows (when `multiline=True`) |
| `description` | `str \| None` | `None` | Helper text |

```python title="text_input_example.py"
from holysheet import TextInput, Columns

Columns(children=[
    TextInput(
        label="Search Reports",
        placeholder="Type to search...",
        description="Search across all reports and dashboards",
    ),
    TextInput(
        label="Notes",
        placeholder="Add your observations...",
        multiline=True,
        rows=5,
    ),
])
```

---

## CheckboxGroup

Multiple checkbox selection — for multi-select filters and option toggles.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Group label |
| `options` | `list[dict]` | *required* | List of `{label, value}` dicts |
| `default_values` | `list \| None` | `None` | Initially checked values |
| `description` | `str \| None` | `None` | Helper text |

!!! example "Module Selection"

    ```python title="checkbox_example.py"
    from holysheet import CheckboxGroup

    CheckboxGroup(
        label="Dashboard Modules",
        options=[
            {"label": "Revenue Analytics", "value": "revenue"},
            {"label": "User Metrics", "value": "users"},
            {"label": "Infrastructure", "value": "infra"},
            {"label": "Security Alerts", "value": "security"},
        ],
        default_values=["revenue", "users"],
        description="Select modules to display",
    )
    ```

---

## RadioGroup

Single-select radio button group for choosing one option from a set.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Group label |
| `options` | `list[dict]` | *required* | List of `{label, value}` dicts |
| `default_value` | `Any \| None` | `None` | Initially selected value |
| `description` | `str \| None` | `None` | Helper text |

!!! example "Time Range Selection"

    ```python title="radio_example.py"
    from holysheet import RadioGroup

    RadioGroup(
        label="Time Range",
        options=[
            {"label": "Last 7 days", "value": "7d"},
            {"label": "Last 30 days", "value": "30d"},
            {"label": "Last 90 days", "value": "90d"},
            {"label": "Year to date", "value": "ytd"},
        ],
        default_value="30d",
        description="Select analysis period",
    )
    ```
