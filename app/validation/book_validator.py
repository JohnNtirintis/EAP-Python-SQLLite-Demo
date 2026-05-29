# validation/book_validator.py
# Validates BookDTO data before it is passed to dal.py.
# Called by business_logic.py — never directly from the GUI.

from app.validation.errors import BookValidationError
from app.validation.rules import (
    is_non_empty,
    is_valid_isbn,
    is_positive_integer,
    is_non_negative_integer,
)


def validate_new_book(dto) -> None:
    """
    Validates all required fields for adding a new book.
    Raises BookValidationError with a descriptive message if any check fails.
    dto: BookDTO
    """
    if not is_non_empty(dto.title):
        raise BookValidationError("Ο τίτλος του βιβλίου είναι απαραίτητος.")

    if not is_non_empty(dto.author):
        raise BookValidationError("Το όνομα συγγραφέα είναι απαραίτητο.")

    if not is_valid_isbn(dto.isbn):
        raise BookValidationError(
            f"Μη έγκυρο ISBN '{dto.isbn}'. Πρέπει να έχει 10–17 χαρακτήρες."
        )

    if not dto.category_id:
        raise BookValidationError("Πρέπει να επιλεγεί έγκυρη κατηγορία.")

    if not is_positive_integer(dto.total_copies):
        raise BookValidationError("Ο συνολικός αριθμός αντιτύπων πρέπει να είναι θετικός ακέραιος.")

    if dto.published_year is not None:
        try:
            year = int(dto.published_year)
            if not (1000 <= year <= 9999):
                raise BookValidationError(
                    "Το έτος έκδοσης πρέπει να είναι έγκυρο τετραψήφιο έτος."
                )
        except (TypeError, ValueError):
            raise BookValidationError("Το έτος έκδοσης πρέπει να είναι έγκυρος ακέραιος αριθμός.")


def validate_update_book(dto) -> None:
    """
    Validates fields for updating an existing book.
    Raises BookValidationError if any provided field is invalid.
    dto: BookDTO
    """
    if not is_non_empty(dto.title):
        raise BookValidationError("Ο τίτλος του βιβλίου δεν μπορεί να είναι κενός.")

    if not is_non_empty(dto.author):
        raise BookValidationError("Το όνομα συγγραφέα δεν μπορεί να είναι κενό.")

    if not is_valid_isbn(dto.isbn):
        raise BookValidationError(
            f"Μη έγκυρο ISBN '{dto.isbn}'. Πρέπει να έχει 10–17 χαρακτήρες."
        )

    if not is_positive_integer(dto.total_copies):
        raise BookValidationError("Ο συνολικός αριθμός αντιτύπων πρέπει να είναι θετικός ακέραιος.")

    if dto.available_copies is not None:
        if not is_non_negative_integer(dto.available_copies):
            raise BookValidationError("Τα διαθέσιμα αντίτυπα πρέπει να είναι μη αρνητικός ακέραιος.")
        if int(dto.available_copies) > int(dto.total_copies):
            raise BookValidationError("Τα διαθέσιμα αντίτυπα δεν μπορούν να υπερβαίνουν τα συνολικά.")

    if dto.published_year is not None:
        try:
            year = int(dto.published_year)
            if not (1000 <= year <= 9999):
                raise BookValidationError(
                    "Το έτος έκδοσης πρέπει να είναι έγκυρο τετραψήφιο έτος."
                )
        except (TypeError, ValueError):
            raise BookValidationError("Το έτος έκδοσης πρέπει να είναι έγκυρος ακέραιος αριθμός.")
