from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldError:
    field: str
    message: str


class ValidationError(ValueError):
    """Raised when one or more validation checks fail."""

    def __init__(self, errors: list[FieldError]) -> None:
        self.errors = errors
        details = "; ".join(f"{error.field}: {error.message}" for error in errors)
        super().__init__(details or "Validation failed")

