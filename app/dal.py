from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .database import DatabaseManager
from .dto import (
    CreateMemberDTO, UpdateMemberDTO, MemberResponseDTO,
    CreateCategoryDTO, CategoryResponseDTO,
    CreateBookDTO, UpdateBookDTO, BookResponseDTO,
    CreateLoanDTO, ReturnLoanDTO, LoanResponseDTO
)


class LibraryDAL:
    """Data access layer with inline SQL queries."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    # ---------------------------------------------------------
    # MEMBERS
    # ---------------------------------------------------------
    def add_member(self, dto: CreateMemberDTO) -> MemberResponseDTO:
        sql = (
            "INSERT INTO members (full_name, address, phone, email, registration_number, age, profession, gender, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        )
        with self.db.get_connection() as connection:
            cursor = connection.execute(
                sql,
                (
                    dto.full_name,
                    dto.address,
                    dto.phone,
                    dto.email,
                    dto.registration_number,
                    dto.age,
                    dto.profession,
                    dto.gender,
                    dto.notes,
                ),
            )
            new_id = int(cursor.lastrowid)

        return self.get_member(new_id)

    def update_member(self, member_id: int, dto: UpdateMemberDTO) -> MemberResponseDTO:
        sql = (
            "UPDATE members "
            "SET full_name = ?, address = ?, phone = ?, email = ?, age = ?, profession = ?, gender = ?, notes = ? "
            "WHERE id = ?;"
        )
        with self.db.get_connection() as connection:
            connection.execute(
                sql,
                (
                    dto.full_name,
                    dto.address,
                    dto.phone,
                    dto.email,
                    dto.age,
                    dto.profession,
                    dto.gender,
                    dto.notes,
                    member_id,
                ),
            )

        return self.get_member(member_id)

    def delete_member(self, member_id: int) -> None:
        with self.db.get_connection() as connection:
            active_loan = connection.execute(
                "SELECT 1 FROM loans WHERE member_id = ? AND status = 'borrowed' LIMIT 1;",
                (member_id,),
            ).fetchone()
            if active_loan:
                raise ValueError("Cannot delete member with active loans.")

            connection.execute("DELETE FROM members WHERE id = ?;", (member_id,))

    def list_members(self) -> list[MemberResponseDTO]:
        with self.db.get_connection() as connection:
            rows = connection.execute(
                "SELECT id, full_name, registration_number, address, phone, email, age, profession, gender, status, notes "
                "FROM members ORDER BY full_name;"
            ).fetchall()

        return [
            MemberResponseDTO(
                id=row["id"],
                full_name=row["full_name"],
                registration_number=row["registration_number"],
                address=row["address"],
                phone=row["phone"],
                email=row["email"],
                age=row["age"],
                profession=row["profession"],
                gender=row["gender"],
                status=row["status"],
                notes=row["notes"],
            )
            for row in rows
        ]

    def get_member(self, member_id: int) -> MemberResponseDTO | None:
        with self.db.get_connection() as connection:
            row = connection.execute(
                "SELECT id, full_name, registration_number, address, phone, email, age, profession, gender, status, notes "
                "FROM members WHERE id = ?;",
                (member_id,),
            ).fetchone()

        if not row:
            return None

        return MemberResponseDTO(
            id=row["id"],
            full_name=row["full_name"],
            registration_number=row["registration_number"],
            address=row["address"],
            phone=row["phone"],
            email=row["email"],
            age=row["age"],
            profession=row["profession"],
            gender=row["gender"],
            status=row["status"],
            notes=row["notes"],
        )

    # ---------------------------------------------------------
    # CATEGORIES
    # ---------------------------------------------------------
    def add_category(self, dto: CreateCategoryDTO) -> CategoryResponseDTO:
        with self.db.get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO categories (name, description) VALUES (?, ?);",
                (dto.name, dto.description),
            )
            new_id = int(cursor.lastrowid)

        return CategoryResponseDTO(id=new_id, name=dto.name, description=dto.description)

    def list_categories(self) -> list[CategoryResponseDTO]:
        with self.db.get_connection() as connection:
            rows = connection.execute(
                "SELECT id, name, description FROM categories ORDER BY name;"
            ).fetchall()

        return [
            CategoryResponseDTO(
                id=row["id"],
                name=row["name"],
                description=row["description"],
            )
            for row in rows
        ]

    def delete_category(self, category_id: int) -> None:
        with self.db.get_connection() as connection:
            existing_books = connection.execute(
                "SELECT 1 FROM books WHERE category_id = ? LIMIT 1;",
                (category_id,),
            ).fetchone()
            if existing_books:
                raise ValueError("Cannot delete category with books assigned to it.")

            connection.execute("DELETE FROM categories WHERE id = ?;", (category_id,))

    # ---------------------------------------------------------
    # BOOKS
    # ---------------------------------------------------------
    def add_book(self, dto: CreateBookDTO) -> BookResponseDTO:
        sql = (
            "INSERT INTO books (title, author, isbn, category_id, total_copies, available_copies, published_year) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);"
        )
        with self.db.get_connection() as connection:
            cursor = connection.execute(
                sql,
                (
                    dto.title,
                    dto.author,
                    dto.isbn,
                    dto.category_id,
                    dto.total_copies,
                    dto.total_copies,
                    dto.published_year,
                ),
            )
            new_id = int(cursor.lastrowid)

        return self.get_book(new_id)

    def update_book(self, book_id: int, dto: UpdateBookDTO) -> BookResponseDTO:
        with self.db.get_connection() as connection:
            book = connection.execute(
                "SELECT total_copies, available_copies FROM books WHERE id = ?;",
                (book_id,),
            ).fetchone()

            if not book:
                raise ValueError("Book does not exist.")

            old_total = int(book["total_copies"])
            old_available = int(book["available_copies"])
            borrowed_count = old_total - old_available

            if dto.total_copies < borrowed_count:
                raise ValueError("Total copies cannot be less than currently borrowed copies.")

            new_available = dto.total_copies - borrowed_count

            connection.execute(
                "UPDATE books SET title = ?, author = ?, isbn = ?, category_id = ?, total_copies = ?, available_copies = ?, published_year = ? "
                "WHERE id = ?;",
                (
                    dto.title,
                    dto.author,
                    dto.isbn,
                    dto.category_id,
                    dto.total_copies,
                    new_available,
                    dto.published_year,
                    book_id,
                ),
            )

        return self.get_book(book_id)

    def delete_book(self, book_id: int) -> None:
        with self.db.get_connection() as connection:
            active_loan = connection.execute(
                "SELECT 1 FROM loans WHERE book_id = ? AND status = 'borrowed' LIMIT 1;",
                (book_id,),
            ).fetchone()
            if active_loan:
                raise ValueError("Cannot delete book with active loans.")

            any_loan_history = connection.execute(
                "SELECT 1 FROM loans WHERE book_id = ? LIMIT 1;",
                (book_id,),
            ).fetchone()
            if any_loan_history:
                raise ValueError("Cannot delete book that has loan history.")

            connection.execute("DELETE FROM ratings WHERE book_id = ?;", (book_id,))
            connection.execute("DELETE FROM books WHERE id = ?;", (book_id,))

    def list_books(self) -> list[BookResponseDTO]:
        sql = (
            "SELECT b.id, b.title, b.author, b.isbn, b.category_id, c.name AS category_name, "
            "b.available_copies, b.total_copies, b.published_year "
            "FROM books b JOIN categories c ON c.id = b.category_id ORDER BY b.title;"
        )
        with self.db.get_connection() as connection:
            rows = connection.execute(sql).fetchall()

        return [
            BookResponseDTO(
                id=row["id"],
                title=row["title"],
                author=row["author"],
                isbn=row["isbn"],
                category_id=row["category_id"],
                category_name=row["category_name"],
                total_copies=row["total_copies"],
                available_copies=row["available_copies"],
                published_year=row["published_year"],
            )
            for row in rows
        ]

    def search_books(self, keyword: str) -> list[BookResponseDTO]:
        pattern = f"%{keyword.strip()}%"
        sql = (
            "SELECT b.id, b.title, b.author, b.isbn, b.category_id, c.name AS category_name, "
            "b.available_copies, b.total_copies, b.published_year "
            "FROM books b JOIN categories c ON c.id = b.category_id "
            "WHERE b.title LIKE ? OR b.author LIKE ? OR b.isbn LIKE ? OR c.name LIKE ? "
            "ORDER BY b.title;"
        )
        with self.db.get_connection() as connection:
            rows = connection.execute(sql, (pattern, pattern, pattern, pattern)).fetchall()

        return [
            BookResponseDTO(
                id=row["id"],
                title=row["title"],
                author=row["author"],
                isbn=row["isbn"],
                category_id=row["category_id"],
                category_name=row["category_name"],
                total_copies=row["total_copies"],
                available_copies=row["available_copies"],
                published_year=row["published_year"],
            )
            for row in rows
        ]

    # ---------------------------------------------------------
    # LENDING
    # ---------------------------------------------------------
    def borrow_book(self, dto: CreateLoanDTO) -> LoanResponseDTO:
        loan_date = date.today()
        due_date = loan_date + timedelta(days=14)

        with self.db.get_connection() as connection:
            member = connection.execute(
                "SELECT status FROM members WHERE id = ?;",
                (dto.member_id,),
            ).fetchone()
            if not member:
                raise ValueError("Member does not exist.")
            if member["status"] != "active":
                raise ValueError("Member is inactive.")

            book = connection.execute(
                "SELECT available_copies FROM books WHERE id = ?;",
                (dto.book_id,),
            ).fetchone()
            if not book:
                raise ValueError("Book does not exist.")
            if int(book["available_copies"]) <= 0:
                raise ValueError("Book is not available.")

            cursor = connection.execute(
                "INSERT INTO loans (member_id, book_id, loan_date, due_date, status) "
                "VALUES (?, ?, ?, ?, 'borrowed');",
                (
                    dto.member_id,
                    dto.book_id,
                    loan_date.isoformat(),
                    due_date.isoformat(),
                ),
            )

            connection.execute(
                "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?;",
                (dto.book_id,),
            )

            new_id = int(cursor.lastrowid)

        return self.get_loan(new_id)

    def return_book(self, dto: ReturnLoanDTO) -> LoanResponseDTO:
        with self.db.get_connection() as connection:
            loan = connection.execute(
                "SELECT book_id, status FROM loans WHERE id = ?;",
                (dto.loan_id,),
            ).fetchone()

            if not loan:
                raise ValueError("Loan does not exist.")
            if loan["status"] != "borrowed":
                raise ValueError("Loan is already returned.")

            connection.execute(
                "UPDATE loans SET return_date = DATE('now'), status = 'returned' WHERE id = ?;",
                (dto.loan_id,),
            )

            connection.execute(
                "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?;",
                (loan["book_id"],),
            )

        return self.get_loan(dto.loan_id)

    def list_loans(self) -> list[LoanResponseDTO]:
        sql = (
            "SELECT l.id, l.member_id, l.book_id, m.full_name AS member_name, "
            "b.title AS book_title, l.loan_date, l.due_date, l.return_date, l.status "
            "FROM loans l "
            "JOIN members m ON m.id = l.member_id "
            "JOIN books b ON b.id = l.book_id "
            "ORDER BY l.loan_date DESC;"
        )
        with self.db.get_connection() as connection:
            rows = connection.execute(sql).fetchall()

        return [
            LoanResponseDTO(
                id=row["id"],
                member_id=row["member_id"],
                book_id=row["book_id"],
                member_name=row["member_name"],
                book_title=row["book_title"],
                loan_date=row["loan_date"],
                due_date=row["due_date"],
                return_date=row["return_date"],
                status=row["status"],
            )
            for row in rows
        ]

    def get_loan(self, loan_id: int) -> LoanResponseDTO | None:
        sql = (
            "SELECT l.id, l.member_id, l.book_id, m.full_name AS member_name, "
            "b.title AS book_title, l.loan_date, l.due_date, l.return_date, l.status "
            "FROM loans l "
            "JOIN members m ON m.id = l.member_id "
            "JOIN books b ON b.id = l.book_id "
            "WHERE l.id = ?;"
        )
        with self.db.get_connection() as connection:
            row = connection.execute(sql, (loan_id,)).fetchone()

        if not row:
            return None

        return LoanResponseDTO(
            id=row["id"],
            member_id=row["member_id"],
            book_id=row["book_id"],
            member_name=row["member_name"],
            book_title=row["book_title"],
            loan_date=row["loan_date"],
            due_date=row["due_date"],
            return_date=row["return_date"],
            status=row["status"],
        )

    # ---------------------------------------------------------
    # RATINGS
    # ---------------------------------------------------------
    def add_or_update_rating(self, member_id: int, book_id: int, rating: int) -> None:
        with self.db.get_connection() as connection:
            connection.execute(
                "INSERT INTO ratings (member_id, book_id, rating) VALUES (?, ?, ?) "
                "ON CONFLICT(member_id, book_id) DO UPDATE SET rating = excluded.rating, rated_at = CURRENT_TIMESTAMP;",
                (member_id, book_id, rating),
            )
