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

def update_member(self, member_id: int, dto: UpdateMemberDTO):
  normalized = self._normalized_member(dto)
  self.dal.update_member(
    member_id=member_id,
    full_name=normalized.full_name,
    address=normalized.address or "",
    phone=normalized.phone or "",
    email=normalized.email or "",
    age=normalized.age,
    profession=normalized.profession or "",
    gender=normalized.gender or "Other",
  )

def deactivate_member(self, member_id: int):
  self.dal.deactivate_member(member_id)

def renew_membership(self, member_id: int):
  self.dal.renew_membership(member_id)

def borrow_book(self, dto: CreateLoanDTO) -> int:
  """
  Δημιουργεί νέο δανεισμό βιβλιου.
  Flow:
  1. Κληση DAL για δανεισμό
  2. Επιστροφή loan_id
  """
  loan_id = self.dal.borrow_book(
    member_id=dto.member_id,
    book_id=dto.book_id
  )
  return loan_id

def return_book(self, dto: ReturnLoanDTO) -> None:
  """
  Επιστρέφει βιβλίο και (προαιρετικά) καταγραφει rating.
  Flow:
  1. Κλήση DAL για επιστροφή βιβλίου
  2. Αν υπάρχει rating -> προσπαθουμε να το καταγράψουμε
  # 1. Επιστροφή βιβλιου
  self.dal.return_book(loan_id=dto.loan_id
  )
  # 2. Αν υπάρχει rating
  if dto.rating is not None:
  
     # TODO: χρειαζεται member_id και book_id απο το Loan
     # για να καλέσουμε:
     # self.dal.add_or_update_rating(member_id, book_id, dto.rating)
     pass
  ####   
 

def list_members(self):
  """
  Επιστρέφει όλα τα μέλη.
  """"
  members = self.dal.list_members()
  return members

def list_books(self):
  """
  Επιστρέφει όλα τα βιβλία.
  """
  books = self.dal.list_books()
  return books

def search_books(self, keyword: str):
  """
  Αναζητά βιβλία με βάση λέξη-κλειδί.
  """
  # Καθαρισμός input
  keyword = keyword.strip().lower()
  # Αν είναι άδειο -> δεν ψάχνουμε
  if not keyword:
    return []

  # Κλήση DAL
  books = self.dal.search_books(keyword)
  return books

def list_loans(self, active_only: bool = False):
  """
  Επιστρέφει τη λιστα δανεισμών.
  active_only=True -> μόνο ενεργοί δανεισμοί
  active_only=False -> όλοι οι δανεισμοί
  """
  loans = self.dal.list_loans(active_only=active_only)
  return loans


  


  


    



    
     
     
 
    

 
     



     



     
  
  




    


  
   
  


    
    
  
