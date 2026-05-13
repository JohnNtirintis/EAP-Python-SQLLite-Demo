# validation/loan_validator.py
# Validates loan operations before they are passed to dal.py.
# Called by business_logic.py — never directly from the GUI.

from app.validation.errors import LoanValidationError


def validate_new_loan(dto) -> None:
    """
    Validates a new loan transaction.
    Raises LoanValidationError if any check fails.

    Checks performed here (data shape only):
    - member_id and book_id are present
    """
    if not dto.member_id:
        raise LoanValidationError("A valid member must be selected.")

    if not dto.book_id:
        raise LoanValidationError("A valid book must be selected.")


def validate_return(loan: dict) -> None:
    """
    Validates a return operation against the loan dict from dal.get_loan().
    loan is a plain dict — uses bracket access, NOT dot notation.
    """
    if loan is None:
        raise LoanValidationError("Loan record not found.")

    if loan["status"] != "borrowed":
        raise LoanValidationError(
            "This loan has already been returned and cannot be processed again."
        )
