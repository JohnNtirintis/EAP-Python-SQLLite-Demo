# validation/loan_validator.py
# Validates loan operations before they are passed to dal.py.
# Called by business_logic.py — never directly from the GUI.

from datetime import datetime
from app.validation.errors import LoanValidationError
from app.validation.rules import is_valid_date


def validate_new_loan(dto) -> None:
    """
    Validates a new loan transaction.
    Raises LoanValidationError if any check fails.

    Checks performed here (data shape only):
    - member_id and book_id are present
    - loan_date and due_date are valid YYYY-MM-DD strings
    - due_date is strictly after loan_date
    """
    if not dto.member_id:
        raise LoanValidationError("A valid member must be selected.")

    if not dto.book_id:
        raise LoanValidationError("A valid book must be selected.")

    if not is_valid_date(dto.loan_date):
        raise LoanValidationError(
            f"Invalid loan date '{dto.loan_date}'. Use YYYY-MM-DD format.")

    if not is_valid_date(dto.due_date):
        raise LoanValidationError(
            f"Invalid due date '{dto.due_date}'. Use YYYY-MM-DD format.")

    loan_dt = datetime.strptime(dto.loan_date, "%Y-%m-%d")
    due_dt  = datetime.strptime(dto.due_date,  "%Y-%m-%d")
    if due_dt <= loan_dt:
        raise LoanValidationError("Due date must be after the loan date.")


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
