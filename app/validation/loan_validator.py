# validation/loan_validator.py
# Validates loan operations before they are passed to dal.py.
# Called by business_logic.py — never directly from the GUI.
# Note: Some checks require DB lookups — those are done in business_logic.py
#       before calling these validators. These functions validate data shape only.

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

    Checks performed in business_logic.py (require DB):
    - member exists and status = 'active'
    - book exists and available_copies > 0
    - no existing active loan for the same member + book

    dto: LoanDTO
    """
    if not dto.member_id:
        raise LoanValidationError("A valid member must be selected.")

    if not dto.book_id:
        raise LoanValidationError("A valid book must be selected.")

    if not is_valid_date(dto.loan_date):
        raise LoanValidationError(
            f"Invalid loan date '{dto.loan_date}'. Use YYYY-MM-DD format."
        )

    if not is_valid_date(dto.due_date):
        raise LoanValidationError(
            f"Invalid due date '{dto.due_date}'. Use YYYY-MM-DD format."
        )

    # due_date must be strictly after loan_date
    loan_dt = datetime.strptime(dto.loan_date, "%Y-%m-%d")
    due_dt  = datetime.strptime(dto.due_date, "%Y-%m-%d")
    if due_dt <= loan_dt:
        raise LoanValidationError(
            "Due date must be after the loan date."
        )


def validate_return(loan) -> None:
    """
    Validates that a loan can be returned.
    Raises LoanValidationError if the loan is already returned.

    loan: LoanDTO (fetched from DB by business_logic.py before calling this)
    """
    if loan is None:
        raise LoanValidationError("Loan record not found.")

    if loan.status == "returned":
        raise LoanValidationError(
            f"Loan ID {loan.id} has already been returned on {loan.return_date}."
        )
