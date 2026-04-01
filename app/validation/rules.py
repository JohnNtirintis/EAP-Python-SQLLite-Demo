from __future__ import annotations

from .errors import FieldError


def required_str(value: str | None, field: str, label: str) -> FieldError | None:
    if value is None or not value.strip():
        return FieldError(field=field, message=f"{label} is required.")
    return None


def positive_int(value: int | None, field: str, label: str) -> FieldError | None:
    if value is not None and value <= 0:
        return FieldError(field=field, message=f"{label} must be a positive number.")
    return None


def optional_email(value: str | None, field: str, label: str = "Email") -> FieldError | None:
    if value is None or not value.strip():
        return None
    if "@" not in value or value.startswith("@") or value.endswith("@"):
        return FieldError(field=field, message=f"{label} is not valid.")
    return None

