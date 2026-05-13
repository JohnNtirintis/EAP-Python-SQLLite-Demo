from __future__ import annotations

from datetime import date, timedelta
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
    categories = {
        "Science Fiction": "Futuristic and speculative stories",
        "History": "Historical studies and narratives",
        "Technology": "Engineering and software topics",
        "Literature": "Classic and modern literary works",
        "Art": "Art history and creative techniques",
        "Science": "Physics, biology, and general science",
        "Mystery": "Detective and thriller novels",
    }
    category_ids = {}
    for name, desc in categories.items():
        category = dal.add_category(CreateCategoryDTO(name=name, description=desc))
        category_ids[name] = category.id

    # ---------------------------------------------------------
    # BOOKS
    # ---------------------------------------------------------
    books = [
        ("Dune", "Frank Herbert", "9780441172719", "Science Fiction", 6, 1965),
        ("Foundation", "Isaac Asimov", "9780553293357", "Science Fiction", 5, 1951),
        ("Neuromancer", "William Gibson", "9780441569595", "Science Fiction", 4, 1984),
        ("Sapiens", "Yuval Noah Harari", "9780062316097", "History", 6, 2011),
        ("The Silk Roads", "Peter Frankopan", "9781101912379", "History", 4, 2015),
        ("Clean Code", "Robert C. Martin", "9780132350884", "Technology", 6, 2008),
        ("The Pragmatic Programmer", "Andrew Hunt", "9780201616224", "Technology", 5, 1999),
        ("Designing Data-Intensive Applications", "Martin Kleppmann", "9781449373320", "Technology", 4, 2017),
        ("Pride and Prejudice", "Jane Austen", "9780141439518", "Literature", 5, 1813),
        ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Literature", 5, 1925),
        ("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Literature", 4, 1960),
        ("The Story of Art", "E. H. Gombrich", "9780714832470", "Art", 3, 1950),
        ("Ways of Seeing", "John Berger", "9780140135152", "Art", 3, 1972),
        ("A Brief History of Time", "Stephen Hawking", "9780553380163", "Science", 5, 1988),
        ("The Selfish Gene", "Richard Dawkins", "9780198788607", "Science", 4, 1976),
        ("The Hound of the Baskervilles", "Arthur Conan Doyle", "9780141032435", "Mystery", 4, 1902),
        ("Gone Girl", "Gillian Flynn", "9780307588371", "Mystery", 4, 2012),
        ("The Girl with the Dragon Tattoo", "Stieg Larsson", "9780307949486", "Mystery", 3, 2005),
    ]

    book_ids = {}
    for title, author, isbn, cat, total, year in books:
        book = dal.add_book(CreateBookDTO(
            title=title,
            author=author,
            isbn=isbn,
            category_id=category_ids[cat],
            total_copies=total,
            published_year=year,
        ))
        book_ids[title] = book.id

    # ---------------------------------------------------------
    # MEMBERS
    # ---------------------------------------------------------
    members = [
        ("Alice Johnson", "M-1001", "10 Main Street", "alice@example.com", 24, "Student", "Female"),
        ("Nikos Papas", "M-1002", "21 Oak Avenue", "nikos@example.com", 31, "Engineer", "Male"),
        ("Maria Costa", "M-1003", "5 Pine Road", "maria@example.com", 29, "Designer", "Female"),
        ("Kostas Dimitriou", "M-1004", "44 River St", "kostas@example.com", 41, "Teacher", "Male"),
        ("Eleni Markou", "M-1005", "7 Hill Blvd", "eleni@example.com", 37, "Researcher", "Female"),
        ("George Allen", "M-1006", "89 Lake View", "george@example.com", 52, "Accountant", "Male"),
        ("Sofia Petrova", "M-1007", "12 Sun Ave", "sofia@example.com", 22, "Student", "Female"),
        ("Alex Martin", "M-1008", "3 Maple St", "alex@example.com", 27, "Developer", "Other"),
        ("Irene Doukas", "M-1009", "18 Cedar Rd", "irene@example.com", 34, "Artist", "Female"),
        ("Panos Vass", "M-1010", "90 Green Ln", "panos@example.com", 46, "Manager", "Male"),
    ]

    member_ids = {}
    for full_name, reg_no, address, email, age, profession, gender in members:
        member = dal.add_member(CreateMemberDTO(
            full_name=full_name,
            registration_number=reg_no,
            address=address,
            phone="",
            email=email,
            age=age,
            profession=profession,
            gender=gender,
            notes="",
        ))
        member_ids[full_name] = member.id

    # ---------------------------------------------------------
    # LOANS (varied dates for statistics)
    # ---------------------------------------------------------
    today = date.today()

    loan_specs = [
        ("Alice Johnson", "Dune", -120, "returned"),
        ("Alice Johnson", "Foundation", -90, "returned"),
        ("Alice Johnson", "Neuromancer", -10, "borrowed"),
        ("Nikos Papas", "Clean Code", -60, "returned"),
        ("Nikos Papas", "The Pragmatic Programmer", -20, "borrowed"),
        ("Maria Costa", "Pride and Prejudice", -45, "returned"),
        ("Maria Costa", "The Great Gatsby", -12, "borrowed"),
        ("Kostas Dimitriou", "Sapiens", -75, "returned"),
        ("Kostas Dimitriou", "The Silk Roads", -30, "returned"),
        ("Eleni Markou", "A Brief History of Time", -50, "returned"),
        ("Eleni Markou", "The Selfish Gene", -8, "borrowed"),
        ("George Allen", "The Hound of the Baskervilles", -40, "returned"),
        ("George Allen", "Gone Girl", -6, "borrowed"),
        ("Sofia Petrova", "Ways of Seeing", -25, "returned"),
        ("Sofia Petrova", "The Story of Art", -4, "borrowed"),
        ("Alex Martin", "Designing Data-Intensive Applications", -18, "returned"),
        ("Alex Martin", "Clean Code", -2, "borrowed"),
        ("Irene Doukas", "To Kill a Mockingbird", -55, "returned"),
        ("Irene Doukas", "The Girl with the Dragon Tattoo", -15, "borrowed"),
        ("Panos Vass", "Sapiens", -22, "returned"),
        ("Panos Vass", "The Silk Roads", -5, "borrowed"),
        ("Alice Johnson", "The Great Gatsby", -70, "returned"),
        ("Nikos Papas", "Designing Data-Intensive Applications", -32, "returned"),
        ("Maria Costa", "Gone Girl", -9, "borrowed"),
        ("George Allen", "A Brief History of Time", -14, "borrowed"),
    ]

    def insert_loan(member_name, book_title, offset_days, status):
        loan_date = today + timedelta(days=offset_days)
        due_date = loan_date + timedelta(days=14)
        return_date = (loan_date + timedelta(days=7)) if status == "returned" else None
        with dal.db.get_connection() as connection:
            connection.execute(
                "INSERT INTO loans (member_id, book_id, loan_date, due_date, return_date, status) "
                "VALUES (?, ?, ?, ?, ?, ?);",
                (
                    member_ids[member_name],
                    book_ids[book_title],
                    loan_date.isoformat(),
                    due_date.isoformat(),
                    return_date.isoformat() if return_date else None,
                    status,
                ),
            )
            if status == "borrowed":
                connection.execute(
                    "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?;",
                    (book_ids[book_title],),
                )

    for member_name, book_title, offset_days, status in loan_specs:
        insert_loan(member_name, book_title, offset_days, status)

    # ---------------------------------------------------------
    # RATINGS
    # ---------------------------------------------------------
    dal.add_or_update_rating(member_ids["Alice Johnson"], book_ids["Dune"], 5)
    dal.add_or_update_rating(member_ids["Alice Johnson"], book_ids["Foundation"], 4)
    dal.add_or_update_rating(member_ids["Nikos Papas"], book_ids["Clean Code"], 5)
    dal.add_or_update_rating(member_ids["Maria Costa"], book_ids["Pride and Prejudice"], 4)
    dal.add_or_update_rating(member_ids["Kostas Dimitriou"], book_ids["Sapiens"], 5)
    dal.add_or_update_rating(member_ids["Eleni Markou"], book_ids["A Brief History of Time"], 4)
    dal.add_or_update_rating(member_ids["George Allen"], book_ids["Gone Girl"], 3)
    dal.add_or_update_rating(member_ids["Sofia Petrova"], book_ids["Ways of Seeing"], 4)
    dal.add_or_update_rating(member_ids["Alex Martin"], book_ids["Designing Data-Intensive Applications"], 5)
    dal.add_or_update_rating(member_ids["Irene Doukas"], book_ids["To Kill a Mockingbird"], 4)
    dal.add_or_update_rating(member_ids["Panos Vass"], book_ids["The Silk Roads"], 3)
