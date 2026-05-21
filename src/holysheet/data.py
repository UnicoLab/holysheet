"""Data conversion utilities for HolySheet.

Converts various tabular data formats into ``list[dict[str, Any]]`` records
suitable for JSON serialization.  Handles:

- ``list[dict]`` (pass-through with value cleaning)
- ``dict[str, list]`` (column-oriented → row-oriented)
- ``pandas.DataFrame`` (optional dependency)
- ``polars.DataFrame`` (optional dependency)
- Datetime, numpy scalar, Decimal, and NaN sanitisation
"""

from __future__ import annotations

import math
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import orjson
from loguru import logger

from holysheet.exceptions import DataConversionError

# ---------------------------------------------------------------------------
# Optional dependency imports
# ---------------------------------------------------------------------------

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:  # pragma: no cover
    HAS_PANDAS = False

try:
    import polars as pl

    HAS_POLARS = True
except ImportError:  # pragma: no cover
    HAS_POLARS = False

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:  # pragma: no cover
    HAS_NUMPY = False


# ---------------------------------------------------------------------------
# Value sanitisation
# ---------------------------------------------------------------------------


def _clean_value(value: Any) -> Any:
    """Sanitise a single value for safe JSON serialisation.

    Args:
        value: Arbitrary Python value.

    Returns:
        A JSON-safe equivalent.
    """
    if value is None:
        return None

    # numpy scalar types → native Python
    if HAS_NUMPY and isinstance(value, np.generic):
        native = value.item()
        # Recurse to handle e.g. np.float64 NaN
        return _clean_value(native)

    # float NaN / Inf → None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None

    # Decimal → float
    if isinstance(value, Decimal):
        return float(value)

    # datetime / date → ISO string
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()

    # bytes → utf-8 string
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")

    return value


def _clean_record(record: dict[str, Any]) -> dict[str, Any]:
    """Apply :func:`_clean_value` to every value in *record*.

    Args:
        record: A single row dict.

    Returns:
        Cleaned dict with JSON-safe values.
    """
    return {k: _clean_value(v) for k, v in record.items()}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def to_records(data: Any) -> list[dict[str, Any]]:
    """Convert *data* to a list of record dicts.

    Supported input types:

    - ``list[dict[str, Any]]`` — returned as-is (values cleaned).
    - ``dict[str, list]`` — column-oriented mapping converted to rows.
    - ``pandas.DataFrame`` — uses ``.to_dict(orient='records')``.
    - ``polars.DataFrame`` — uses ``.to_dicts()``.

    Args:
        data: Tabular data in one of the supported formats.

    Returns:
        A ``list[dict[str, Any]]`` of cleaned records.

    Raises:
        DataConversionError: If *data* is not a supported type or conversion
            fails for any reason.
    """
    if data is None:
        return []

    try:
        # --- list[dict] ---
        if isinstance(data, list):
            if len(data) == 0:
                return []
            if isinstance(data[0], dict):
                logger.debug("Converting list[dict] with {} records", len(data))
                return [_clean_record(r) for r in data]
            raise DataConversionError(
                f"Expected list[dict], got list[{type(data[0]).__name__}]",
                source_type=f"list[{type(data[0]).__name__}]",
            )

        # --- dict[str, list] (column-oriented) ---
        if isinstance(data, dict):
            logger.debug("Converting dict[str, list] with {} columns", len(data))
            columns = list(data.keys())
            if not columns:
                return []
            n_rows = len(next(iter(data.values())))
            # Validate uniform length
            for col, values in data.items():
                if len(values) != n_rows:
                    raise DataConversionError(
                        f"Column '{col}' has {len(values)} rows, expected {n_rows}",
                        source_type="dict[str, list]",
                    )
            records = [{col: data[col][i] for col in columns} for i in range(n_rows)]
            return [_clean_record(r) for r in records]

        # --- pandas DataFrame ---
        if HAS_PANDAS and isinstance(data, pd.DataFrame):
            logger.debug(
                "Converting pandas DataFrame ({} rows, {} cols)", len(data), len(data.columns)
            )
            records = data.to_dict(orient="records")
            return [_clean_record(r) for r in records]

        # --- polars DataFrame ---
        if HAS_POLARS and isinstance(data, pl.DataFrame):
            logger.debug("Converting polars DataFrame ({} rows, {} cols)", data.height, data.width)
            records = data.to_dicts()
            return [_clean_record(r) for r in records]

        raise DataConversionError(
            f"Unsupported data type: {type(data).__name__}",
            source_type=type(data).__name__,
        )

    except DataConversionError:
        raise
    except Exception as exc:
        raise DataConversionError(
            f"Failed to convert data: {exc}",
            source_type=type(data).__name__,
        ) from exc


def records_to_json_bytes(records: list[dict[str, Any]]) -> bytes:
    """Serialise *records* to compact JSON bytes using orjson.

    Args:
        records: List of record dicts (should already be cleaned).

    Returns:
        UTF-8 encoded JSON bytes.
    """
    return orjson.dumps(records, option=orjson.OPT_NON_STR_KEYS)
