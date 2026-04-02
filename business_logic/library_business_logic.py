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
    """
    Προσθέτει νέο μέλος στο σύστημα
    Flow:
    1. Normalize δεδομένα
    2. Validation μεσω validator
    3. Δημιουργία registration_number
    4. Κλήση DAL για αποθήκευση
    5. Επιστροφή member_id
    """
    # 1. Καθαρισμός δεδομένων
    normalized = self._normalized_member(dto)
    # 2. Validation
    self.member_validation.validate_create(normalized)
    # 3. Δημιουργία registration number
    registration_number = self._next_registration_number()
    # 4. Κλήση DAL
    member_id = self.dal.add_member(
      full_name=normalized.full_name,
      registration_number=registration_number,
      address=normalized.address or "",
      phone=normalized.phone or "",
      email=normalized.email or "",
      age=normalized.age,
      profession=normalized.profession or "",
      gender=normalized.gender or "Other",
    # 5. Επιστροφή αποτελέσματος
    return member_id

 def _next_registration_number(self) -> str:
   """Δημιουργεί νέο μοναδικό αριθμό μέλους."""
   members = self.dal.list_numbers()
   max_id = max((int(member["id"]) for member in memebrs), default=0)
   return f"M-{1000 + max_id + 1}"



    
    
  
