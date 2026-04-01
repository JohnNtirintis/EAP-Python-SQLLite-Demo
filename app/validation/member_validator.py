from __future__ import annotations

from ..dto import CreateMemberDTO

from .errors import FieldError, ValidationError
from .rules import optional_email, positive_int, required_str


class MemberValidator:
    """Entity-specific business validation for member operations."""

    def validate_create(self, dto: CreateMemberDTO) -> None:
        errors: list[FieldError] = []

        full_name_error = required_str(dto.full_name, "full_name", "Full name")
        if full_name_error:
            errors.append(full_name_error)

        # .strip() is redundant here
        # we have normalized the data earlier
        # but, we will keep it for defensive programming in case this validator is used elsewhere without normalization
        phone = (dto.phone or "").strip()
        email = (dto.email or "").strip()
        if not phone and not email:
            errors.append(FieldError(field="phone", message="Provide at least one contact method: phone or email."))

        email_error = optional_email(dto.email, "email")
        if email_error:
            errors.append(email_error)

        age_error = positive_int(dto.age, "age", "Age")
        if age_error:
            errors.append(age_error)

        if errors:
            raise ValidationError(errors)


