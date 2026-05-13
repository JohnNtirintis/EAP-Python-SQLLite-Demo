# validation/rules.py
# Stateless, pure validation functions — no DB calls, no side effects.
# Used internally by member_validator.py, book_validator.py, loan_validator.py.

import re
from datetime import datetime


def is_non_empty(value) -> bool:
    """Returns True if value is not None and not a blank string."""
    return value is not None and str(value).strip() != ""


def is_valid_email(email: str) -> bool:
    """Returns True if email matches a basic valid email format."""
    if not is_non_empty(email):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email.strip()) is not None


def is_valid_phone(phone: str) -> bool:
    """Returns True if phone contains only digits, spaces, +, -, and is 7-20 chars."""
    if not is_non_empty(phone):
        return False
    cleaned = re.sub(r"[\s\-\+]", "", phone.strip())
    return cleaned.isdigit() and 7 <= len(cleaned) <= 20


def is_valid_age(age) -> bool:
    """Returns True if age is an integer >= 0."""
    try:
        return int(age) >= 0
    except (TypeError, ValueError):
        return False


def is_valid_gender(gender) -> bool:
    """Returns True if gender is 'Male', 'Female', 'Other', or None."""
    return gender is None or gender in ("Male", "Female", "Other")


def is_valid_status(status: str) -> bool:
    """Returns True if status is 'active' or 'inactive'."""
    return status in ("active", "inactive")


def is_valid_rating(rating) -> bool:
    """Returns True if rating is an integer between 1 and 5 inclusive."""
    try:
        return 1 <= int(rating) <= 5
    except (TypeError, ValueError):
        return False


def is_valid_isbn(isbn: str) -> bool:
    """Returns True if ISBN is non-empty and between 10 and 17 characters."""
    if not is_non_empty(isbn):
        return False
    cleaned = isbn.strip().replace("-", "")
    return 10 <= len(cleaned) <= 17


def is_valid_date(date_str: str) -> bool:
    """Returns True if date_str matches the YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return True
    except (ValueError, AttributeError):
        return False


def is_positive_integer(value) -> bool:
    """Returns True if value is an integer strictly greater than 0."""
    try:
        return int(value) > 0
    except (TypeError, ValueError):
        return False


def is_non_negative_integer(value) -> bool:
    """Returns True if value is an integer >= 0."""
    try:
        return int(value) >= 0
    except (TypeError, ValueError):
        return False
