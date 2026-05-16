# validation/member_validator.py
# Validates MemberDTO data before it is passed to dal.py.
# Called by business_logic.py — never directly from the GUI.

from app.validation.errors import MemberValidationError
from app.validation.rules import (
    is_non_empty,
    is_valid_email,
    is_valid_phone,
    is_valid_age,
    is_valid_gender,
)


def validate_new_member(dto) -> None:
    """
    Validates all required fields for creating a new member.
    Raises MemberValidationError with a descriptive message if any check fails.
    dto: MemberDTO
    """
    if not is_non_empty(dto.full_name):
        raise MemberValidationError("Full name is required.")

    if not is_non_empty(dto.registration_number):
        raise MemberValidationError("Registration number is required.")

    if dto.email and not is_valid_email(dto.email):
        raise MemberValidationError(f"Invalid email format: '{dto.email}'.")

    if dto.phone and not is_valid_phone(dto.phone):
        raise MemberValidationError(f"Invalid phone number: '{dto.phone}'.")

    if dto.age is not None and not is_valid_age(dto.age):
        raise MemberValidationError("Age must be a non-negative integer.")

    if not is_valid_gender(dto.gender):
        raise MemberValidationError(
            f"Invalid gender '{dto.gender}'. Must be 'Male', 'Female', 'Other', or None."
        )


def validate_update_member(dto) -> None:
    """
    Validates fields for updating an existing member.
    Raises MemberValidationError if any provided field is invalid.
    Empty strings are treated as "no value provided" for optional fields,
    matching the behaviour of validate_new_member.
    dto: MemberDTO
    """
    if dto.full_name is not None and not is_non_empty(dto.full_name):
        raise MemberValidationError("Full name cannot be blank.")

    # email/phone: only validate if a non-empty value is actually present
    if dto.email and not is_valid_email(dto.email):
        raise MemberValidationError(f"Invalid email format: '{dto.email}'.")

    if dto.phone and not is_valid_phone(dto.phone):
        raise MemberValidationError(f"Invalid phone number: '{dto.phone}'.")

    if dto.age is not None and not is_valid_age(dto.age):
        raise MemberValidationError("Age must be a non-negative integer.")

    if dto.gender is not None and not is_valid_gender(dto.gender):
        raise MemberValidationError(
            f"Invalid gender '{dto.gender}'. Must be 'Male', 'Female', 'Other', or None."
        )
