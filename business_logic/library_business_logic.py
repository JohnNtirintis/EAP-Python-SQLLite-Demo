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



    
    
  
