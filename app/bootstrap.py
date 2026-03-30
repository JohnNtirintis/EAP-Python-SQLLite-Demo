from __future__ import annotations

from pathlib import Path

from .dal import LibraryDAL
from .database import DatabaseManager


def create_dal(db_path: Path) -> LibraryDAL:
    """Wire DB manager + DAL and seed demo data when DB is empty."""
    project_root = Path(__file__).resolve().parent.parent
    schema_path = project_root / "sql" / "schema.sql"

    db = DatabaseManager(db_path=db_path, schema_path=schema_path)
    db.initialize()

    dal = LibraryDAL(db)
    seed_if_empty(dal)
    return dal


def seed_if_empty(dal: LibraryDAL) -> None:
    """Insert starter records exactly once for quick testing."""
    if dal.list_categories():
        return

    sci_fi_id = dal.add_category("Science Fiction", "Futuristic and speculative stories")
    history_id = dal.add_category("History", "Historical studies and narratives")
    technology_id = dal.add_category("Technology", "Engineering and software topics")

    dune_id = dal.add_book("Dune", "Frank Herbert", "9780441172719", sci_fi_id, 4, 1965)
    dal.add_book("Foundation", "Isaac Asimov", "9780553293357", sci_fi_id, 3, 1951)
    clean_code_id = dal.add_book("Clean Code", "Robert C. Martin", "9780132350884", technology_id, 2, 2008)
    dal.add_book("Sapiens", "Yuval Noah Harari", "9780062316097", history_id, 5, 2011)

    member_1 = dal.add_member(
        full_name="Alice Johnson",
        registration_number="M-1001",
        age=24,
        profession="Student",
        gender="Female",
        email="alice@example.com",
        address="10 Main Street",
        notes="Interested in sci-fi",
    )
    member_2 = dal.add_member(
        full_name="Nikos Papas",
        registration_number="M-1002",
        age=31,
        profession="Engineer",
        gender="Male",
        email="nikos@example.com",
        address="21 Oak Avenue",
        notes="Prefers technology books",
    )

    dal.borrow_book(member_1, dune_id)
    dal.borrow_book(member_2, clean_code_id)
    dal.add_or_update_rating(member_1, dune_id, 5)
    dal.add_or_update_rating(member_2, clean_code_id, 4)


