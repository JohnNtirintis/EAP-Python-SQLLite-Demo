from __future__ import annotations

from pathlib import Path

from .dal import LibraryDAL
from .database import DatabaseManager
from .business_logic import BusinessLogic
from .dto import (
    CreateCategoryDTO,
    CreateBookDTO,
    CreateMemberDTO,
    CreateLoanDTO,
)


def create_business_logic(dal: LibraryDAL) -> BusinessLogic:
    return BusinessLogic(dal)


def create_dal(db_path: Path) -> LibraryDAL:
    project_root = Path(__file__).resolve().parent.parent
    schema_path = project_root / "sql" / "schema.sql"

    db = DatabaseManager(db_path=db_path, schema_path=schema_path)
    db.initialize()

    dal = LibraryDAL(db)
    seed_if_empty(dal)
    return dal


def seed_if_empty(dal: LibraryDAL) -> None:
    if dal.list_categories():
        return

    # ---------------------------------------------------------
    # CATEGORIES
    # ---------------------------------------------------------
    sci_fi = dal.add_category(CreateCategoryDTO(
        name="Science Fiction",
        description="Futuristic and speculative stories"
    ))
    history = dal.add_category(CreateCategoryDTO(
        name="History",
        description="Historical studies and narratives"
    ))
    technology = dal.add_category(CreateCategoryDTO(
        name="Technology",
        description="Engineering and software topics"
    ))

    # ---------------------------------------------------------
    # BOOKS
    # ---------------------------------------------------------
    dune = dal.add_book(CreateBookDTO(
        title="Dune",
        author="Frank Herbert",
        isbn="9780441172719",
        category_id=sci_fi.id,
        total_copies=4,
        published_year=1965,
    ))

    dal.add_book(CreateBookDTO(
        title="Foundation",
        author="Isaac Asimov",
        isbn="9780553293357",
        category_id=sci_fi.id,
        total_copies=3,
        published_year=1951,
    ))

    clean_code = dal.add_book(CreateBookDTO(
        title="Clean Code",
        author="Robert C. Martin",
        isbn="9780132350884",
        category_id=technology.id,
        total_copies=2,
        published_year=2008,
    ))

    dal.add_book(CreateBookDTO(
        title="Sapiens",
        author="Yuval Noah Harari",
        isbn="9780062316097",
        category_id=history.id,
        total_copies=5,
        published_year=2011,
    ))

    # ---------------------------------------------------------
    # MEMBERS
    # ---------------------------------------------------------
    member_1 = dal.add_member(CreateMemberDTO(
        full_name="Alice Johnson",
        registration_number="M-1001",
        address="10 Main Street",
        phone="",
        email="alice@example.com",
        age=24,
        profession="Student",
        gender="Female",
        notes="Interested in sci-fi",
    ))

    member_2 = dal.add_member(CreateMemberDTO(
        full_name="Nikos Papas",
        registration_number="M-1002",
        address="21 Oak Avenue",
        phone="",
        email="nikos@example.com",
        age=31,
        profession="Engineer",
        gender="Male",
        notes="Prefers technology books",
    ))

    # ---------------------------------------------------------
    # LOANS
    # ---------------------------------------------------------
    dal.borrow_book(CreateLoanDTO(
        member_id=member_1.id,
        book_id=dune.id,
    ))

    dal.borrow_book(CreateLoanDTO(
        member_id=member_2.id,
        book_id=clean_code.id,
    ))

    # ---------------------------------------------------------
    # RATINGS
    # ---------------------------------------------------------
    dal.add_or_update_rating(member_1.id, dune.id, 5)
    dal.add_or_update_rating(member_2.id, clean_code.id, 4)
