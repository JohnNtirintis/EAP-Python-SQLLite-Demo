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
        raise MemberValidationError("Απαιτείται πλήρες όνομα.")

    if not is_non_empty(dto.registration_number):
        raise MemberValidationError("Απαιτείται αριθμός μητρώου.")

    if dto.email and not is_valid_email(dto.email):
        raise MemberValidationError(f"Μη έγκυρη μορφή email: '{dto.email}'.")

    if dto.phone and not is_valid_phone(dto.phone):
        raise MemberValidationError(f"Μη έγκυρος αριθμός τηλεφώνου: '{dto.phone}'.")

    if dto.age is not None and not is_valid_age(dto.age):
        raise MemberValidationError("Η ηλικία πρέπει να είναι μη αρνητικός ακέραιος.")

    if not is_valid_gender(dto.gender):
        raise MemberValidationError(
            f"Μη έγκυρο φύλο '{dto.gender}'. Επιτρέπονται: 'Male', 'Female', 'Other' ή None."
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
        raise MemberValidationError("Το πλήρες όνομα δεν μπορεί να είναι κενό.")

    if dto.email and not is_valid_email(dto.email):
        raise MemberValidationError(f"Μη έγκυρη μορφή email: '{dto.email}'.")

    if dto.phone and not is_valid_phone(dto.phone):
        raise MemberValidationError(f"Μη έγκυρος αριθμός τηλεφώνου: '{dto.phone}'.")

    if dto.age is not None and not is_valid_age(dto.age):
        raise MemberValidationError("Η ηλικία πρέπει να είναι μη αρνητικός ακέραιος.")

    if dto.gender is not None and not is_valid_gender(dto.gender):
        raise MemberValidationError(
            f"Μη έγκυρο φύλο '{dto.gender}'. Επιτρέπονται: 'Male', 'Female', 'Other' ή None."
        )
