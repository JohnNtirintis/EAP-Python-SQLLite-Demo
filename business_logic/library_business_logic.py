from __future__ import annotations
from dataclasses import replace
from typing import Optional
from app.dal import LibraryDAL
from app.dto import (
    CreateMemberDTO,
    UpdateMemberDTO,
    CreateLoanDTO,
    ReturnLoanDTO,
    CreateBookDTO,
    UpdateBookDTO,
    CreateCategoryDTO,
)
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
    normalized = self._normalize_member(dto)
    # 2. Validation
    self.member_validator.validate_create(normalized)
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
    )
        
    # 5. Επιστροφή αποτελέσματος
    return member_id




  def _normalize_member(self, dto: CreateMemberDTO | UpdateMemberDTO) -> CreateMemberDTO | UpdateMemberDTO:
    return replace(
        dto,
        full_name=(dto.full_name or "").strip() if dto.full_name is not None else None,
        address=(dto.address or "").strip() or None,
        phone=(dto.phone or "").strip() or None,
        email=(dto.email or "").strip() or None,
        profession=(dto.profession or "").strip() or None,
        gender=(dto.gender or "").strip() or None,
    )

        
        
 def _next_registration_number(self) -> str:
   """Δημιουργεί νέο μοναδικό αριθμό μέλους."""
   members = self.dal.list_members()
   max_id = max((int(member["id"]) for member in memebrs), default=0)
   return f"M-{1000 + max_id + 1}"


 def update_member(self, member_id: int, dto: UpdateMemberDTO) -> None:
     
     
    normalized = self._normalize_member(dto)
    self.dal.update_member(
    member_id=member_id,
    full_name=normalized.full_name or "",
    address=normalized.address or "",
    phone=normalized.phone or "",
    email=normalized.email or "",
    age=normalized.age,
    profession=normalized.profession or "",
    gender=normalized.gender or "Other",
  )

def deactivate_member(self, member_id: int) -> None:
  self.dal.deactivate_member(member_id)

def renew_membership(self, member_id: int) -> None:
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
  self.dal.return_book(loan_id=dto.loan_id,
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

def add_book(self, dto: CreateBookDTO) -> int:
  book_id = self.dal.add_book(
    title=dto.title,
    author=dto.author,
    isbn=dto.isbn,
    category_id=dto.category_id,
    total_copies=dto.stock,
    published_year=None
  )
  return book_id

def update_book(self,book_id:int,dto:UpdateBookDTO)->None:
  """
  Ενημερώνει στοιχεια βιβλίου.
  Αν καποιο πεδίο στο dto είναι None,
  κρατάμε την παλιά τιμή από το βιβλίο.
  """
  # Παίρνουμε όλα τα βιβλία
  books=self.dal.list_books()

  # Βρίσκουμε το συγκεκριμένο βιβλίο 
  book=next((b for b in books if b["id"]==book_id), None)

  # Αν δεν υπάρχει, σταματάμε
  if book is None:
    raise ValueError("Book does not exist.")

  # Κρατάμε νέα τιμή αν υπάρχει,αλλιώς την παλιά
  title = dto.title if dto.title is not None else book["title"]
  author = dto.author if dto.author is not None else book["author"]
  category_id = dto.category_id if dto.category_id is not None else book["category_id"]
  total_copies = dto.stock if dto.stock is not None else book["total_copies"]

  # Το ISBN δεν υπάρχει στο UpdateBookDTO, άρα κρατάμε το παλίο
  isbn = book["isbn"]

  # published_year δεν το έχουμε στο DTO,άρα για τώρα None
  published_year = None

  # Κλήση DAL
  self.dal.update_book(
    book_id=book_id,
    title=title,
    author=author,
    isbn=isbn,
    category_id=category_id,
    total_copies=total_copies,
    published_year=published_year
  )

def add_category(self, dto:CreateCategoryDTO)-> int:
  """
  Προσθέτει νέα κατηγορια βιβλίου.
  """
  category_name = dto.name.strip()
  if not category_name:
    raise ValueError("Category name is required.")

  category_id = self.dal.add_category(
    name=category_name
  )
  return category_id

def list_available_books_by_category(self,category_name:str):
  """
  Επιστρέφει διαθεσιμα βιβλία συγκεκριμένης κατηγορίας.
  """
  category_name = category_name.strip().lower()
  if not category_name:
    return[]
  books = self.dal.list_books()
  available_books = [
    book for book in books
    if book["category_name"].lower()==category_name
    and book["available_copies"]>0
  ]
  return available_books

def check_availability(self,book_id:int)-> bool:
  """
  Ελεγχει αν ένα βιβλίο ειναι διαθεσιμο.
  """
  books = self.dal.list_books()
  book = next((b for b in books if b["id"]==book_id),None)
  if book is None:
    raise ValueError("Book does not exist.")

  return book["available_copies"]>0




  
  

  



  








    
    

  


  


  


    



    
     
     
 
    

 
     



     



     
  
  




    


  
   
  


    
    
  
