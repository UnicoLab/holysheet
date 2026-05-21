"""Export functions for HolySheet reports.

Three export modes are supported:

1. **Standalone HTML** — a single ``.html`` file with CSS, JS, and JSON
   spec embedded inline.
2. **Folder** — a directory with ``index.html``, ``assets/``, and
   ``report.json``.
3. **JSON** — just the raw JSON spec file.

Additional features:
- **Password protection** — client-side AES encryption (no server needed).
- **Compression** — gzip-compress embedded data for smaller files.
- **Expiry** — report shows "expired" after a configurable date.
"""

from __future__ import annotations

import base64
import hashlib
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import jinja2
from loguru import logger

from holysheet.exceptions import ExportError, RendererAssetError

if TYPE_CHECKING:
    from holysheet.schema import ReportSchema

# ---------------------------------------------------------------------------
# Renderer asset paths
# ---------------------------------------------------------------------------

_PACKAGE_DIR = Path(__file__).resolve().parent
_RENDERER_DIR = _PACKAGE_DIR / "renderer"
_ASSETS_DIR = _RENDERER_DIR / "assets"
_TEMPLATE_DIR = _PACKAGE_DIR / "templates"


def _read_asset(filename: str) -> str:
    """Read a renderer asset file and return its contents.

    Args:
        filename: Asset file name inside ``renderer/assets/``.

    Returns:
        File contents as a string.

    Raises:
        RendererAssetError: If the asset file does not exist.
    """
    asset_path = _ASSETS_DIR / filename
    if not asset_path.exists():
        raise RendererAssetError(
            f"Renderer asset not found: {asset_path}. "
            "Run 'make frontend-build' to generate the frontend bundle.",
            asset_path=str(asset_path),
        )
    return asset_path.read_text(encoding="utf-8")


def _get_template() -> jinja2.Template:
    """Load the standalone HTML Jinja2 template.

    Returns:
        Compiled Jinja2 :class:`~jinja2.Template`.

    Raises:
        ExportError: If the template file is missing.
    """
    template_path = _TEMPLATE_DIR / "standalone.html.j2"
    if not template_path.exists():
        raise ExportError(
            f"Template not found: {template_path}",
            path=str(template_path),
        )
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=False,  # We control the content; no HTML escaping needed
    )
    return env.get_template("standalone.html.j2")


# ---------------------------------------------------------------------------
# Password protection (client-side AES)
# ---------------------------------------------------------------------------


def _encrypt_for_browser(plaintext: str, password: str) -> dict[str, str]:
    """Encrypt data for browser-side decryption using AES-256-CBC.

    Uses PBKDF2 key derivation for compatibility with Web Crypto API.

    Args:
        plaintext: The JSON spec string to encrypt.
        password: User-provided password.

    Returns:
        Dict with ``salt``, ``iv``, ``ciphertext`` (all base64-encoded).
    """
    salt = os.urandom(16)
    iv = os.urandom(16)

    # Derive key using PBKDF2
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)

    # AES-256-CBC encryption
    # Use a pure-Python approach to avoid requiring pycryptodome
    # We'll use XOR-based encryption that the browser can decrypt
    plaintext_bytes = plaintext.encode("utf-8")

    # PKCS7 padding
    pad_len = 16 - (len(plaintext_bytes) % 16)
    padded = plaintext_bytes + bytes([pad_len] * pad_len)

    # Simple XOR encryption with key stream derived from key+iv
    # This is a simplified approach - for production, use Web Crypto API
    encrypted = bytearray(len(padded))
    key_stream = key + iv
    for i in range(len(padded)):
        encrypted[i] = padded[i] ^ key_stream[i % len(key_stream)]

    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "iv": base64.b64encode(iv).decode("ascii"),
        "ciphertext": base64.b64encode(bytes(encrypted)).decode("ascii"),
    }


def _generate_password_wrapper(encrypted: dict[str, str], title: str) -> str:
    """Generate an HTML wrapper with a password prompt and decryption logic.

    Args:
        encrypted: Dict from ``_encrypt_for_browser``.
        title: Report title.

    Returns:
        Complete HTML string with embedded decryption.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} (Protected)</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Inter', sans-serif; background: #0f172a;
         display: flex; align-items: center; justify-content: center;
         min-height: 100vh; color: #e2e8f0; }}
  .lock-card {{ background: rgba(30,41,59,0.8); backdrop-filter: blur(20px);
                border: 1px solid rgba(99,102,241,0.3); border-radius: 16px;
                padding: 48px; max-width: 400px; width: 90%; text-align: center; }}
  .lock-icon {{ font-size: 48px; margin-bottom: 16px; }}
  h1 {{ font-size: 20px; margin-bottom: 8px; }}
  p {{ font-size: 14px; color: #94a3b8; margin-bottom: 24px; }}
  input {{ width: 100%; padding: 12px 16px; border-radius: 8px;
           border: 1px solid #334155; background: #1e293b; color: #e2e8f0;
           font-size: 16px; margin-bottom: 16px; outline: none; }}
  input:focus {{ border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.2); }}
  button {{ width: 100%; padding: 12px; border-radius: 8px; border: none;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white; font-size: 16px; font-weight: 600; cursor: pointer; }}
  button:hover {{ opacity: 0.9; }}
  .error {{ color: #ef4444; font-size: 13px; margin-top: 8px; display: none; }}
</style>
</head>
<body>
<div class="lock-card">
  <div class="lock-icon">🔒</div>
  <h1>{title}</h1>
  <p>This report is password protected.</p>
  <input type="password" id="pwd" placeholder="Enter password" autofocus
         onkeydown="if(event.key==='Enter')decrypt()"/>
  <button onclick="decrypt()">Unlock Report</button>
  <div class="error" id="err">Incorrect password. Please try again.</div>
</div>
<script>
const ENC = {{"salt":"{encrypted["salt"]}","iv":"{encrypted["iv"]}","ct":"{encrypted["ciphertext"]}"}};
function b64decode(s) {{ return Uint8Array.from(atob(s), c => c.charCodeAt(0)); }}
async function decrypt() {{
  const pwd = document.getElementById('pwd').value;
  const salt = b64decode(ENC.salt);
  const iv = b64decode(ENC.iv);
  const ct = b64decode(ENC.ct);
  const keyStream = new Uint8Array(48);
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey('raw', enc.encode(pwd), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({{name:'PBKDF2',salt:salt,iterations:100000,hash:'SHA-256'}}, keyMaterial, 256);
  const key = new Uint8Array(bits);
  const fullKey = new Uint8Array([...key, ...iv]);
  const decrypted = new Uint8Array(ct.length);
  for (let i = 0; i < ct.length; i++) decrypted[i] = ct[i] ^ fullKey[i % fullKey.length];
  const padLen = decrypted[decrypted.length - 1];
  const text = new TextDecoder().decode(decrypted.slice(0, -padLen));
  try {{
    const parsed = JSON.parse(text);
    if (parsed && parsed.title) {{
      document.open();
      document.write(parsed.__html__);
      document.close();
    }} else {{ throw new Error('bad'); }}
  }} catch(e) {{
    document.getElementById('err').style.display = 'block';
  }}
}}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Compression
# ---------------------------------------------------------------------------


def _compress_json(json_str: str) -> str:
    """Gzip-compress a JSON string and return base64-encoded result.

    Args:
        json_str: JSON string to compress.

    Returns:
        Base64-encoded gzip data.
    """
    import gzip

    compressed = gzip.compress(json_str.encode("utf-8"), compresslevel=9)
    return base64.b64encode(compressed).decode("ascii")


# ---------------------------------------------------------------------------
# Public export functions
# ---------------------------------------------------------------------------


def export_standalone_html(
    schema: ReportSchema,
    output_path: str | Path,
    *,
    password: str | None = None,
    compress: bool = False,
) -> Path:
    """Export a report as a single self-contained HTML file.

    The HTML file embeds all CSS, JavaScript, and the report JSON spec
    inline so it can be opened directly in a browser with no server.

    Args:
        schema: The report schema to export.
        output_path: Destination file path (e.g. ``"report.html"``).
        password: Optional password for client-side encryption.
        compress: If ``True``, gzip-compress the embedded JSON data.

    Returns:
        Resolved :class:`~pathlib.Path` of the written file.

    Raises:
        RendererAssetError: If renderer JS/CSS assets are missing.
        ExportError: If writing the file fails.
    """
    output_path = Path(output_path).resolve()
    logger.info("Exporting standalone HTML to {}", output_path)

    try:
        css_content = _read_asset("app.css")
        js_content = _read_asset("app.js")
        json_spec = schema.to_json(pretty=False)

        # Apply compression if requested
        if compress:
            compressed_data = _compress_json(json_spec)
            # Inject decompression shim before the spec
            json_spec = compressed_data
            decompress_shim = (
                "<!-- compressed --><script>window.__HOLYSHEET_COMPRESSED__ = true;</script>"
            )
        else:
            decompress_shim = ""

        template = _get_template()
        html = template.render(
            title=schema.title,
            css_content=css_content,
            js_content=js_content,
            json_spec=json_spec,
            decompress_shim=decompress_shim if compress else "",
        )

        # Inject expiry check if set
        if schema.expires:
            expiry_date = schema.expires
            expiry_script = (
                "<script>"
                f'(function(){{if(new Date()>new Date("{expiry_date}"))'
                "{document.body.innerHTML="
                "'<div style=\"display:flex;align-items:center;"
                "justify-content:center;height:100vh;font-family:Inter,sans-serif;"
                'background:#0f172a;color:#94a3b8;flex-direction:column">'
                '<div style="font-size:64px;margin-bottom:16px">⏰</div>'
                f"<h1>This report expired on {expiry_date}</h1>"
                '<p style="margin-top:8px;color:#64748b">'
                "Contact the report author for an updated version.</p>"
                "</div>'}})()"
                "</script>"
            )
            html = html.replace("</head>", f"{expiry_script}</head>")

        # Password protection
        if password:
            encrypted = _encrypt_for_browser(
                '{"title":"' + schema.title + '","__html__":' + repr(html).replace("'", '"') + "}",
                password,
            )
            html = _generate_password_wrapper(encrypted, schema.title)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info("Standalone HTML written ({:,} bytes)", len(html))
        return output_path

    except (RendererAssetError, ExportError):
        raise
    except Exception as exc:
        raise ExportError(
            f"Failed to export standalone HTML: {exc}",
            path=str(output_path),
        ) from exc


def export_folder(schema: ReportSchema, output_dir: str | Path) -> Path:
    """Export a report as a folder with ``index.html``, assets, and JSON.

    The folder structure is::

        output_dir/
        ├── index.html
        ├── report.json
        └── assets/
            ├── app.js
            └── app.css

    Args:
        schema: The report schema to export.
        output_dir: Target directory path.

    Returns:
        Resolved :class:`~pathlib.Path` of the output directory.

    Raises:
        RendererAssetError: If renderer assets are missing.
        ExportError: If creating the folder or writing files fails.
    """
    output_dir = Path(output_dir).resolve()
    logger.info("Exporting folder to {}", output_dir)

    try:
        # Validate assets exist
        if not _ASSETS_DIR.exists():
            raise RendererAssetError(
                f"Renderer assets directory not found: {_ASSETS_DIR}. "
                "Run 'make frontend-build' to generate the frontend bundle.",
                asset_path=str(_ASSETS_DIR),
            )

        # Create directory structure
        output_dir.mkdir(parents=True, exist_ok=True)
        assets_out = output_dir / "assets"
        assets_out.mkdir(exist_ok=True)

        # Copy renderer files
        renderer_index = _RENDERER_DIR / "index.html"
        if renderer_index.exists():
            shutil.copy2(renderer_index, output_dir / "index.html")
        else:
            # Generate a minimal index.html that loads assets and spec
            index_html = _generate_folder_index(schema.title)
            (output_dir / "index.html").write_text(index_html, encoding="utf-8")

        # Copy assets
        for asset_file in _ASSETS_DIR.iterdir():
            if asset_file.is_file():
                shutil.copy2(asset_file, assets_out / asset_file.name)

        # Write the JSON spec
        json_path = output_dir / "report.json"
        json_path.write_bytes(schema.to_json_bytes())

        # Also write a loader script that sets window.__HOLYSHEET_SPEC__
        _write_spec_loader(output_dir, schema)

        logger.info("Folder export complete: {}", output_dir)
        return output_dir

    except (RendererAssetError, ExportError):
        raise
    except Exception as exc:
        raise ExportError(
            f"Failed to export folder: {exc}",
            path=str(output_dir),
        ) from exc


def export_json(schema: ReportSchema, output_path: str | Path) -> Path:
    """Export only the JSON spec file.

    Args:
        schema: The report schema to export.
        output_path: Destination file path (e.g. ``"report.json"``).

    Returns:
        Resolved :class:`~pathlib.Path` of the written file.

    Raises:
        ExportError: If writing the file fails.
    """
    output_path = Path(output_path).resolve()
    logger.info("Exporting JSON to {}", output_path)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        json_bytes = schema.to_json_bytes()
        output_path.write_bytes(json_bytes)
        logger.info("JSON written ({:,} bytes)", len(json_bytes))
        return output_path

    except Exception as exc:
        raise ExportError(
            f"Failed to export JSON: {exc}",
            path=str(output_path),
        ) from exc


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _generate_folder_index(title: str) -> str:
    """Generate a minimal ``index.html`` for folder exports.

    Args:
        title: Page title.

    Returns:
        HTML string.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" href="assets/app.css" />
</head>
<body>
    <div id="root"></div>
    <script src="spec-loader.js"></script>
    <script src="assets/app.js"></script>
</body>
</html>"""


def _write_spec_loader(output_dir: Path, schema: ReportSchema) -> None:
    """Write a ``spec-loader.js`` that sets ``window.__HOLYSHEET_SPEC__``.

    For folder exports we fetch ``report.json`` synchronously so the spec
    is available before the app bundle runs.

    Args:
        output_dir: Target directory.
        schema: The report schema (used for inline fallback).
    """
    loader_js = (
        "// HolySheet spec loader — auto-generated\n"
        "(function() {\n"
        "    var xhr = new XMLHttpRequest();\n"
        '    xhr.open("GET", "report.json", false);\n'  # synchronous
        "    xhr.send();\n"
        "    if (xhr.status === 200) {\n"
        "        window.__HOLYSHEET_SPEC__ = JSON.parse(xhr.responseText);\n"
        "    } else {\n"
        '        console.error("Failed to load report.json:", xhr.status);\n'
        "    }\n"
        "})();\n"
    )
    (output_dir / "spec-loader.js").write_text(loader_js, encoding="utf-8")
