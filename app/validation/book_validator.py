# validation/book_validator.py
# Validates BookDTO data before it is passed to dal.py.
# Called by business_logic.py — never directly from the GUI.

from app.validation.errors import BookValidationError
from app.validation.rules import (
    is_non_empty,
    is_valid_isbn,
    is_positive_integer,
)


def validate_new_book(dto) -> None:
    """
    Validates all required fields for adding a new book.
    Raises BookValidationError with a descriptive message if any check fails.
    dto: BookDTO
    """
    if not is_non_empty(dto.title):
        raise BookValidationError("Book title is required.")

    if not is_non_empty(dto.author):
        raise BookValidationError("Author name is required.")

    if not is_valid_isbn(dto.isbn):
        raise BookValidationError(
            f"Invalid ISBN '{dto.isbn}'. Must be 10-17 characters."
        )

    if not dto.category_id:
        raise BookValidationError("A valid category must be selected.")

    if not is_positive_integer(dto.total_copies):
        raise BookValidationError("Total copies must be a positive integer.")

    if dto.published_year is not None:
        try:
            year = int(dto.published_year)
            if not (1000 <= year <= 9999):
                raise BookValidationError(
                    "Published year must be a valid 4-digit year."
                )
        except (TypeError, ValueError):
            raise BookValidationError("Published year must be a valid integer.")


def validate_update_book(dto) -> None:
    """
    Validates fields for updating an existing book.
    Raises BookValidationError if any provided field is invalid.
    dto: BookDTO
    """
    if not is_non_empty(dto.title):
        raise BookValidationError("Book title cannot be blank.")

    if not is_non_empty(dto.author):
        raise BookValidationError("Author name cannot be blank.")

    if not is_valid_isbn(dto.isbn):
        raise BookValidationError(
            f"Invalid ISBN '{dto.isbn}'. Must be 10-17 characters."
        )

    if not is_positive_integer(dto.total_copies):
        raise BookValidationError("Total copies must be a positive integer.")

    if dto.published_year is not None:
        try:
            year = int(dto.published_year)
            if not (1000 <= year <= 9999):
                raise BookValidationError(
                    "Published year must be a valid 4-digit year."
                )
        except (TypeError, ValueError):
            raise BookValidationError("Published year must be a valid integer.")
