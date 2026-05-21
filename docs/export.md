# Export & Deployment

HolySheet supports three export modes and includes a CLI for validation and local serving.

---

## :page_facing_up: Standalone HTML

The recommended and default export mode. Generates a **single self-contained HTML file** with all CSS, JavaScript, and data embedded inline.

```python title="export_html.py"
report.export_html("report.html")
```

### Characteristics

| Property | Value |
|:---------|:------|
| **File size** | ~1.5 MB (mostly React + ECharts bundles) |
| **Dependencies** | None — fully self-contained |
| **Offline support** | :material-check: Yes |
| **Server required** | :material-close: No |

### How It Works

1. Reads the prebuilt React bundle (`app.js`) and styles (`app.css`) from the package
2. Serializes your report to a JSON specification
3. Renders everything into a Jinja2 HTML template with inline `<script>` and `<style>` tags
4. Writes a single `.html` file

### Usage

```python title="html_export_full.py"
from holysheet import Report, KPI, LineChart

report = Report(title="Q4 Review", theme="dark")
report.add(KPI(label="Revenue", value="$2.26M", delta="+34%", status="positive"))
report.add(LineChart(title="Trend", data=data, x="month", y="revenue"))

# Export to current directory
path = report.export_html("report.html")
print(f"Written to: {path}")

# Export to a subdirectory (created automatically)
path = report.export_html("output/reports/q4_review.html")
```

!!! tip "Opening in Browser"
    ```python
    import webbrowser
    path = report.export_html("report.html")
    webbrowser.open(f"file://{path}")
    ```

---

## :file_folder: Folder Export

Generates a deployable folder with separate files — ideal for web hosting.

```python title="export_folder.py"
report.export_folder("dist/")
```

### Output Structure

```
dist/
├── index.html          ← Entry point (loads assets)
├── report.json         ← Dashboard specification
├── spec-loader.js      ← Auto-generated loader script
└── assets/
    ├── app.js          ← React application bundle
    └── app.css         ← Stylesheet
```

### Characteristics

| Property | Value |
|:---------|:------|
| **Total size** | ~1.5 MB (split across files) |
| **Server required** | :material-check: Yes (for local file:// CORS) |
| **CDN-friendly** | :material-check: Yes |
| **Cacheable assets** | :material-check: Yes |

!!! example "Deployment Options"
    === "AWS S3"

        ```bash
        aws s3 sync dist/ s3://my-bucket/reports/q4/ --acl public-read
        ```

    === "GitHub Pages"

        ```bash
        # Add dist/ contents to your gh-pages branch
        cp -r dist/* docs/
        git add docs/
        git commit -m "Update report"
        git push
        ```

    === "Nginx"

        ```nginx
        server {
            listen 80;
            root /var/www/reports;
            location / {
                try_files $uri $uri/ =404;
            }
        }
        ```

    === "Python HTTP"

        ```bash
        cd dist/
        python -m http.server 8000
        ```

---

## :material-code-json: JSON Export

Exports just the raw dashboard specification as JSON. Useful for debugging, version control, or feeding into external renderers.

```python title="export_json.py"
report.export_json("report.json")
```

### Output Example

```json title="report.json (simplified)"
{
  "schema_version": "1.0.0",
  "title": "Q4 Review",
  "subtitle": null,
  "theme": "dark",
  "created_at": "2026-05-21T08:00:00+00:00",
  "blocks": [
    {
      "id": "block_001",
      "type": "kpi",
      "props": {
        "label": "Revenue",
        "value": "$2.26M",
        "delta": "+34%",
        "status": "positive"
      }
    }
  ]
}
```

### Getting JSON as a String

You can also get the JSON string directly without writing to a file:

```python title="json_string.py"
# Compact JSON
json_str = report.to_json()

# Pretty-printed JSON
json_str = report.to_json(pretty=True)
```

### Schema Object

Access the full schema object for programmatic manipulation:

```python title="schema_object.py"
schema = report.to_schema()
print(schema.title)           # "Q4 Review"
print(schema.schema_version)  # "1.0.0"
print(schema.theme)           # "dark"
print(len(schema.blocks))     # Number of blocks

# Convert to dict
data = schema.to_dict()

# Convert to JSON bytes (orjson)
json_bytes = schema.to_json_bytes()
```

---

## :material-console: CLI Usage

HolySheet includes a command-line interface for validation and local serving.

### Validate a JSON Spec

```bash
holysheet validate report.json
```

Output:

```
Validating report.json...
✓ Valid HolySheet spec
  Title:          Q4 Review
  Schema version: 1.0.0
  Theme:          dark
  Blocks:         12
  Created at:     2026-05-21T08:00:00+00:00
```

### Serve Locally

Start a local HTTP server and open the report in your default browser:

```bash
holysheet serve report.json
```

Options:

| Flag | Default | Description |
|:-----|:--------|:------------|
| `--port`, `-p` | `8765` | Port to serve on |
| `--no-open` | `False` | Don't auto-open browser |

```bash
# Custom port
holysheet serve report.json --port 3000

# Don't open browser automatically
holysheet serve report.json --no-open
```

!!! info "How Serve Works"
    The `serve` command:

    1. Reads and validates the JSON spec
    2. Exports to a temporary folder
    3. Starts a Python HTTP server
    4. Opens the browser (unless `--no-open`)
    5. Cleans up the temp folder on exit

### Version

```bash
holysheet version
# holysheet 0.2.0
```

### Verbose Mode

Add `-v` for debug logging on any command:

```bash
holysheet -v validate report.json
holysheet -v serve report.json
```

---

## :globe_with_meridians: Embedding in Web Apps

### Iframe Embedding

Embed a standalone HTML report in any web page:

```html title="embed.html"
<iframe
  src="report.html"
  width="100%"
  height="800"
  frameborder="0"
  style="border: 1px solid #e5e7eb; border-radius: 8px;"
></iframe>
```

### Dynamic Loading (JSON)

For dynamic web apps, export as JSON and load the spec at runtime:

```javascript title="loader.js"
// Fetch the report spec
const response = await fetch('/api/reports/q4.json');
const spec = await response.json();

// Set the spec for the HolySheet renderer
window.__HOLYSHEET_SPEC__ = spec;
```

### Integration with Flask/FastAPI

```python title="app.py"
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from holysheet import Report, KPI

app = FastAPI()

@app.get("/report", response_class=HTMLResponse)
def generate_report():
    report = Report(title="Live Report", theme="dark")
    report.add(KPI(label="Active Users", value=42_000))

    # Export to HTML string via schema
    schema = report.to_schema()
    # ... render with your template
```

---

## :bulb: Export Tips

!!! tip "File Size"
    Standalone HTML files are ~1.5 MB regardless of data size (the bulk is the React + ECharts bundle). Adding more data increases the size proportionally — a report with 10,000 table rows might be ~2–3 MB.

!!! tip "Path Handling"
    All export methods accept `str` or `pathlib.Path` and automatically create parent directories:

    ```python
    from pathlib import Path

    report.export_html(Path("output") / "reports" / "q4.html")
    # Creates output/reports/ if it doesn't exist
    ```

!!! warning "Renderer Assets"
    If you see a `RendererAssetError`, it means the prebuilt React bundle is missing. This typically happens in development. Run:

    ```bash
    make frontend-build
    ```
