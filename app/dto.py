from __future__ import annotations

"""
dto.py - *Data Transfer Objects* for the Library Management System.

DTOs separate the data flowing IN (from the user / GUI) from the data
flowing OUT (from the database to the GUI).  They serve three purposes:

  1. Validation  – ensure required fields are present before hitting the DB.
  2. Decoupling  – the GUI never touches raw SQL rows; it works with typed objects.
  3. Clarity     – each operation advertises exactly which fields it needs.

Naming convention
─────────────────
  CreateXxxDTO   → fields the caller must supply to INSERT a new row.
  UpdateXxxDTO   → fields the caller may change on an existing row (all optional).
  XxxResponseDTO → fields returned to the caller after a read / write.
"""

"""
dto.py - Data Transfer Objects for the Library Management System.

DTOs separate:
  - data flowing IN (Create/Update DTOs)
  - data flowing OUT (Response DTOs)

They ensure:
  1. Validation before DB access
  2. Decoupling GUI from SQL rows
  3. Clear contracts between layers
"""


from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------
# MEMBERS
# ---------------------------------------------------------
@dataclass
class CreateMemberDTO:
    full_name: str
    registration_number: str
    address: str
    phone: str
    email: str
    age: Optional[int]
    profession: str
    gender: str
    notes: str


@dataclass
class UpdateMemberDTO:
    full_name: str
    address: str
    phone: str
    email: str
    age: Optional[int]
    profession: str
    gender: str
    notes: str


@dataclass
class MemberResponseDTO:
    id: int
    full_name: str
    registration_number: str
    address: str
    phone: str
    email: str
    age: Optional[int]
    profession: str
    gender: str
    status: str
    notes: str


# ---------------------------------------------------------
# CATEGORIES
# ---------------------------------------------------------
@dataclass
class CreateCategoryDTO:
    name: str
    description: str


@dataclass
class CategoryResponseDTO:
    id: int
    name: str
    description: str


# ---------------------------------------------------------
# BOOKS
# ---------------------------------------------------------
@dataclass
class CreateBookDTO:
    title: str
    author: str
    isbn: str
    category_id: int
    total_copies: int
    published_year: Optional[int]


@dataclass
class UpdateBookDTO:
    title: str
    author: str
    isbn: str
    category_id: int
    total_copies: int
    published_year: Optional[int]


@dataclass
class BookResponseDTO:
    id: int
    title: str
    author: str
    isbn: str
    category_id: int
    category_name: str
    total_copies: int
    available_copies: int
    published_year: Optional[int]


# ---------------------------------------------------------
# LOANS
# ---------------------------------------------------------
@dataclass
class CreateLoanDTO:
    member_id: int
    book_id: int


@dataclass
class ReturnLoanDTO:
    loan_id: int


@dataclass
class LoanResponseDTO:
    id: int
    member_id: int
    book_id: int
    member_name: str
    book_title: str
    loan_date: str
    due_date: str
    return_date: Optional[str]
    status: str


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------
@dataclass
class RecommendationDTO:
    book: BookResponseDTO
    score: float
