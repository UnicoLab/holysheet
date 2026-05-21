"""HolySheet custom exceptions.

All exceptions inherit from :class:`HolySheetError` so callers can catch
the entire family with a single ``except HolySheetError`` clause.
"""

from __future__ import annotations


class HolySheetError(Exception):
    """Base exception for all HolySheet errors.

    Args:
        message: Human-readable error description.
    """

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class SchemaValidationError(HolySheetError):
    """Raised when a report schema fails validation.

    Args:
        message: Details about what failed validation.
        errors: Optional list of individual validation error dicts.
    """

    def __init__(
        self, message: str = "Schema validation failed", errors: list[dict] | None = None
    ) -> None:
        self.errors = errors or []
        super().__init__(message)


class ExportError(HolySheetError):
    """Raised when exporting a report fails.

    Args:
        message: Details about the export failure.
        path: The target path that caused the error.
    """

    def __init__(self, message: str = "Export failed", path: str | None = None) -> None:
        self.path = path
        super().__init__(message)


class RendererAssetError(HolySheetError):
    """Raised when renderer assets (JS/CSS bundles) are missing.

    This typically means the frontend has not been built yet.

    Args:
        message: Details about which asset is missing.
        asset_path: Path to the missing asset.
    """

    def __init__(
        self, message: str = "Renderer assets not found", asset_path: str | None = None
    ) -> None:
        self.asset_path = asset_path
        super().__init__(message)


class DataConversionError(HolySheetError):
    """Raised when data cannot be converted to the expected format.

    Args:
        message: Details about the conversion failure.
        source_type: The type of the input data that failed conversion.
    """

    def __init__(
        self, message: str = "Data conversion failed", source_type: str | None = None
    ) -> None:
        self.source_type = source_type
        super().__init__(message)
