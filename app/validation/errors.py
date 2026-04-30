# validation/errors.py
# Custom exception classes for the validation layer.
# Raised by validators, caught in business_logic.py.
# Never caught directly in the GUI layer.


class ValidationError(Exception):
    """Base class for all validation errors in the application."""
    pass


class MemberValidationError(ValidationError):
    """Raised when member data fails validation rules."""
    pass


class BookValidationError(ValidationError):
    """Raised when book data fails validation rules."""
    pass


class LoanValidationError(ValidationError):
    """Raised when loan data fails validation rules."""
    pass


class CategoryValidationError(ValidationError):
    """Raised when category data fails validation rules."""
    pass
