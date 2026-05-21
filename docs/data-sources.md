# Data Sources

HolySheet auto-detects and converts data from multiple Python data formats. You never need to manually transform data — just pass it directly to any block that accepts `data`.

---

## Supported Formats

### :material-format-list-bulleted: List of Dicts

The most common format. Each dict is a row, keys are column names.

```python title="list_of_dicts.py"
data = [
    {"month": "Jan", "revenue": 124_500, "costs": 78_200},
    {"month": "Feb", "revenue": 138_200, "costs": 82_100},
    {"month": "Mar", "revenue": 152_800, "costs": 85_600},
]

LineChart(title="Revenue Trend", data=data, x="month", y=["revenue", "costs"])
```

!!! tip "This is the internal format"
    Internally, HolySheet converts all data to `list[dict[str, Any]]`. If your data is already in this format, it passes through with minimal overhead (just value sanitization).

---

### :material-code-braces: Dict of Lists

Column-oriented format where keys are column names and values are lists.

```python title="dict_of_lists.py"
data = {
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "revenue": [124_500, 138_200, 152_800, 149_300],
    "costs": [78_200, 82_100, 85_600, 83_900],
}

LineChart(title="Revenue Trend", data=data, x="month", y="revenue")
```

!!! warning "Uniform Length Required"
    All lists must have the same length. If column lengths differ, a `DataConversionError` is raised:

    ```python
    # This will raise DataConversionError
    data = {
        "month": ["Jan", "Feb", "Mar"],
        "revenue": [100, 200],  # Only 2 values!
    }
    ```

---

### :simple-pandas: Pandas DataFrames

```python title="pandas_data.py"
import pandas as pd

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "revenue": [124_500, 138_200, 152_800, 149_300],
    "costs": [78_200, 82_100, 85_600, 83_900],
})

LineChart(title="Revenue Trend", data=df, x="month", y=["revenue", "costs"])
DataTable(title="Raw Data", data=df)
```

!!! info "Optional Dependency"
    Pandas is an optional dependency. Install with:
    ```bash
    pip install holysheet[pandas]
    ```

**How it works:** Internally calls `df.to_dict(orient='records')` and then sanitizes each value.

---

### :simple-polars: Polars DataFrames

```python title="polars_data.py"
import polars as pl

df = pl.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "revenue": [124_500, 138_200, 152_800, 149_300],
    "costs": [78_200, 82_100, 85_600, 83_900],
})

LineChart(title="Revenue Trend", data=df, x="month", y=["revenue", "costs"])
DataTable(title="Raw Data", data=df)
```

!!! info "Optional Dependency"
    Polars is an optional dependency. Install with:
    ```bash
    pip install holysheet[polars]
    ```

**How it works:** Internally calls `df.to_dicts()` and then sanitizes each value.

---

## :broom: Value Sanitization

HolySheet automatically cleans values for safe JSON serialization. This happens transparently on all data formats.

| Input Type | Output | Example |
|:-----------|:-------|:--------|
| `None` | `None` | — |
| `float` NaN | `None` | `float('nan')` → `None` |
| `float` Inf | `None` | `float('inf')` → `None` |
| `Decimal` | `float` | `Decimal("3.14")` → `3.14` |
| `datetime` | ISO string | `datetime(2024, 1, 15)` → `"2024-01-15T00:00:00"` |
| `date` | ISO string | `date(2024, 1, 15)` → `"2024-01-15"` |
| `bytes` | UTF-8 string | `b"hello"` → `"hello"` |
| NumPy scalar | Native Python | `np.float64(3.14)` → `3.14` |
| NumPy NaN | `None` | `np.nan` → `None` |

!!! example "Automatic NaN Handling"
    ```python
    import pandas as pd
    import numpy as np

    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "score": [95, np.nan, 87],       # NaN is auto-converted to None
        "date": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
    })

    # Just pass it — HolySheet handles the NaN and datetime conversion
    DataTable(title="Scores", data=df)
    ```

---

## :gear: The `to_records()` Function

Under the hood, all data conversion goes through `holysheet.data.to_records()`:

```python title="to_records_usage.py"
from holysheet.data import to_records

# Convert any supported format to list[dict]
records = to_records(my_dataframe)
records = to_records(my_dict_of_lists)
records = to_records(my_list_of_dicts)

# Returns: [{"col1": val1, "col2": val2}, ...]
```

### Conversion Flow

```
Input Data (any format)
    │
    ├── list[dict] ──→ Clean values ──→ list[dict]
    ├── dict[str, list] ──→ Transpose ──→ Clean values ──→ list[dict]
    ├── pd.DataFrame ──→ .to_dict("records") ──→ Clean values ──→ list[dict]
    └── pl.DataFrame ──→ .to_dicts() ──→ Clean values ──→ list[dict]
```

### Error Handling

If data cannot be converted, a `DataConversionError` is raised:

```python
from holysheet.exceptions import DataConversionError

try:
    records = to_records("not valid data")
except DataConversionError as e:
    print(e.message)      # "Unsupported data type: str"
    print(e.source_type)  # "str"
```

---

## :bulb: Tips

### Mixing Data Sources

You can use different data formats across blocks in the same report:

```python title="mixed_data.py"
import pandas as pd

# Some data as dicts
kpi_data = {"revenue": 2_260_000, "users": 42_000}

# Chart data from pandas
chart_df = pd.read_csv("monthly_revenue.csv")

# Table data as list of dicts
customers = [
    {"name": "Acme Corp", "mrr": "$12,400"},
    {"name": "GlobalTech", "mrr": "$9,800"},
]

report = Report(title="Mixed Sources", theme="dark")
report.add(KPI(label="Revenue", value=f"${kpi_data['revenue']:,.0f}"))
report.add(LineChart(title="Trend", data=chart_df, x="month", y="revenue"))
report.add(DataTable(title="Top Customers", data=customers))
```

### Large DataFrames

!!! warning "Performance Note"
    All data is embedded in the HTML file as JSON. Very large datasets (100K+ rows) will increase file size and may impact browser performance. Consider:

    - Aggregating data before passing to charts
    - Limiting DataTable rows to a reasonable size
    - Using `paginated=True` (default) for large tables

### Data is Serialized at Export Time

Data conversion happens when you call `export_html()`, `export_json()`, or `export_folder()` — not when you create the block. This means you can modify your DataFrames after adding them to blocks:

```python
df = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})
chart = LineChart(title="Chart", data=df, x="x", y="y")
report.add(chart)

# ⚠️ This modification WILL be reflected in the export
# because 'data' holds a reference to df
df["y"] = [100, 200, 300]

report.export_html("report.html")  # Uses the modified data
```
