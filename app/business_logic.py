from __future__ import annotations

from dataclasses import replace
from typing import Optional

from app.dal import LibraryDAL
from app.dto import CreateMemberDTO
from app.validation.member_validator import MemberValidator


class LibraryBusinessLogic:
    """Business layer that applies rules before persisting through DAL."""

    def __init__(self, dal: LibraryDAL, member_validator: Optional[MemberValidator] = None) -> None:
        self.dal = dal
        self.member_validator = member_validator or MemberValidator()

    def add_member(self, dto: CreateMemberDTO) -> int:
        normalized = self._normalize_member(dto)
        self.member_validator.validate_create(normalized)

        return self.dal.add_member(
            full_name=normalized.full_name,
            registration_number=self._next_registration_number(),
            address=normalized.address or "",
            phone=normalized.phone or "",
            email=normalized.email or "",
            age=normalized.age,
            profession=normalized.profession or "",
            gender=normalized.gender or "Other",
        )

    def _normalize_member(self, dto: CreateMemberDTO) -> CreateMemberDTO:
        return replace(
            dto,
            full_name=(dto.full_name or "").strip(),
            address=(dto.address or "").strip() or None,
            phone=(dto.phone or "").strip() or None,
            email=(dto.email or "").strip() or None,
            profession=(dto.profession or "").strip() or None,
            gender=(dto.gender or "").strip() or None,
        )

    def _next_registration_number(self) -> str:
        members = self.dal.list_members()
        max_id = max((int(member["id"]) for member in members), default=0)
        return f"M-{1000 + max_id + 1}"
