"""Tests for holysheet.data — data conversion utilities."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest

from holysheet.data import _clean_value, to_records
from holysheet.exceptions import DataConversionError

# ---------------------------------------------------------------------------
# list[dict] conversion
# ---------------------------------------------------------------------------


class TestListDictConversion:
    """Tests for list[dict] input."""

    def test_passthrough(self, sample_records: list[dict[str, Any]]) -> None:
        """list[dict] should pass through with values cleaned."""
        result = to_records(sample_records)
        assert len(result) == len(sample_records)
        assert result[0]["month"] == "Jan"
        assert result[0]["revenue"] == 1200

    def test_empty_list(self) -> None:
        """Empty list returns empty list."""
        assert to_records([]) == []

    def test_none_input(self) -> None:
        """None returns empty list."""
        assert to_records(None) == []

    def test_invalid_list_contents(self) -> None:
        """list of non-dicts raises DataConversionError."""
        with pytest.raises(DataConversionError, match="Expected list\\[dict\\]"):
            to_records([1, 2, 3])


# ---------------------------------------------------------------------------
# dict[str, list] conversion
# ---------------------------------------------------------------------------


class TestDictListConversion:
    """Tests for column-oriented dict[str, list] input."""

    def test_basic_conversion(self, sample_column_data: dict[str, list[Any]]) -> None:
        """dict[str, list] converts to row-oriented records."""
        result = to_records(sample_column_data)
        assert len(result) == 3
        assert result[0] == {"name": "Alice", "score": 95, "grade": "A"}
        assert result[2]["name"] == "Charlie"

    def test_empty_dict(self) -> None:
        """Empty dict returns empty list."""
        assert to_records({}) == []

    def test_uneven_columns(self) -> None:
        """Mismatched column lengths raise DataConversionError."""
        with pytest.raises(DataConversionError, match="rows, expected"):
            to_records({"a": [1, 2], "b": [3]})


# ---------------------------------------------------------------------------
# Value cleaning
# ---------------------------------------------------------------------------


class TestValueCleaning:
    """Tests for individual value sanitisation."""

    def test_none(self) -> None:
        assert _clean_value(None) is None

    def test_float_nan(self) -> None:
        assert _clean_value(float("nan")) is None

    def test_float_inf(self) -> None:
        assert _clean_value(float("inf")) is None
        assert _clean_value(float("-inf")) is None

    def test_decimal(self) -> None:
        result = _clean_value(Decimal("3.14"))
        assert isinstance(result, float)
        assert result == pytest.approx(3.14)

    def test_datetime(self) -> None:
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = _clean_value(dt)
        assert result == "2024-01-15T10:30:00"

    def test_date(self) -> None:
        d = date(2024, 1, 15)
        result = _clean_value(d)
        assert result == "2024-01-15"

    def test_bytes(self) -> None:
        result = _clean_value(b"hello")
        assert result == "hello"

    def test_normal_values_pass_through(self) -> None:
        assert _clean_value(42) == 42
        assert _clean_value("hello") == "hello"
        assert _clean_value(True) is True

    def test_nan_in_records(self) -> None:
        """NaN values in records are cleaned to None."""
        records = [{"a": 1, "b": float("nan")}]
        result = to_records(records)
        assert result[0]["b"] is None

    def test_datetime_in_records(self) -> None:
        """Datetime values in records are serialised to ISO strings."""
        records = [{"ts": datetime(2024, 6, 15)}]
        result = to_records(records)
        assert result[0]["ts"] == "2024-06-15T00:00:00"


# ---------------------------------------------------------------------------
# pandas DataFrame
# ---------------------------------------------------------------------------


class TestPandasConversion:
    """Tests for pandas DataFrame input (skipped if pandas not installed)."""

    @pytest.fixture(autouse=True)
    def _require_pandas(self) -> None:
        pytest.importorskip("pandas")

    def test_basic_dataframe(self) -> None:
        import pandas as pd

        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        result = to_records(df)
        assert len(result) == 3
        assert result[0] == {"x": 1, "y": 4}

    def test_dataframe_with_nan(self) -> None:
        import pandas as pd

        df = pd.DataFrame({"a": [1.0, float("nan"), 3.0]})
        result = to_records(df)
        assert result[1]["a"] is None

    def test_empty_dataframe(self) -> None:
        import pandas as pd

        df = pd.DataFrame()
        result = to_records(df)
        assert result == []


# ---------------------------------------------------------------------------
# polars DataFrame
# ---------------------------------------------------------------------------


class TestPolarsConversion:
    """Tests for polars DataFrame input (skipped if polars not installed)."""

    @pytest.fixture(autouse=True)
    def _require_polars(self) -> None:
        pytest.importorskip("polars")

    def test_basic_dataframe(self) -> None:
        import polars as pl

        df = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        result = to_records(df)
        assert len(result) == 3
        assert result[0] == {"x": 1, "y": 4}

    def test_empty_dataframe(self) -> None:
        import polars as pl

        df = pl.DataFrame()
        result = to_records(df)
        assert result == []


# ---------------------------------------------------------------------------
# Unsupported types
# ---------------------------------------------------------------------------


class TestUnsupportedTypes:
    """Tests for unsupported input types."""

    def test_string_raises(self) -> None:
        with pytest.raises(DataConversionError, match="Unsupported data type"):
            to_records("not a table")

    def test_int_raises(self) -> None:
        with pytest.raises(DataConversionError, match="Unsupported data type"):
            to_records(42)

    def test_set_raises(self) -> None:
        with pytest.raises(DataConversionError, match="Unsupported data type"):
            to_records({1, 2, 3})


# ---------------------------------------------------------------------------
# numpy integration
# ---------------------------------------------------------------------------


class TestNumpyIntegration:
    """Test numpy scalar handling (skipped if numpy not installed)."""

    @pytest.fixture(autouse=True)
    def _require_numpy(self) -> None:
        pytest.importorskip("numpy")

    def test_numpy_int(self) -> None:
        import numpy as np

        result = _clean_value(np.int64(42))
        assert result == 42
        assert isinstance(result, int)

    def test_numpy_float(self) -> None:
        import numpy as np

        result = _clean_value(np.float64(3.14))
        assert isinstance(result, float)

    def test_numpy_nan(self) -> None:
        import numpy as np

        result = _clean_value(np.float64("nan"))
        assert result is None

    def test_numpy_in_records(self) -> None:
        import numpy as np

        records = [{"val": np.int64(99)}]
        result = to_records(records)
        assert result[0]["val"] == 99
