from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from .database import DatabaseManager


class LibraryDAL:
    """Data access layer with inline SQL queries for the DB-only export."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    @staticmethod
    def _to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
        return [dict(row) for row in rows]

    def add_member(
        self,
        full_name: str,
        registration_number: str,
        address: str = "",
        phone: str = "",
        email: str = "",
        age: int | None = None,
        profession: str = "",
        gender: str = "Other",
        notes: str = "",
    ) -> int:
        sql = (
            "INSERT INTO members (full_name, address, phone, email, registration_number, age, profession, gender, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        )
        with self.db.get_connection() as connection:
            cursor = connection.execute(
                sql,
                (full_name, address, phone, email, registration_number, age, profession, gender, notes),
            )
            return int(cursor.lastrowid)

    def update_member(
        self,
        member_id: int,
        full_name: str,
        address: str = "",
        phone: str = "",
        email: str = "",
        age: int | None = None,
        profession: str = "",
        gender: str = "Other",
        notes: str = "",
    ) -> None:
        sql = (
            "UPDATE members "
            "SET full_name = ?, address = ?, phone = ?, email = ?, age = ?, profession = ?, gender = ?, notes = ? "
            "WHERE id = ?;"
        )
        with self.db.get_connection() as connection:
            connection.execute(sql, (full_name, address, phone, email, age, profession, gender, notes, member_id))

    def delete_member(self, member_id: int) -> None:
        with self.db.get_connection() as connection:
            active_loan = connection.execute(
                "SELECT 1 FROM loans WHERE member_id = ? AND status = 'borrowed' LIMIT 1;",
                (member_id,),
            ).fetchone()
            if active_loan:
                raise ValueError("Cannot delete member with active loans.")
            connection.execute("DELETE FROM members WHERE id = ?;", (member_id,))

    def list_members(self) -> list[dict[str, Any]]:
        with self.db.get_connection() as connection:
            rows = connection.execute(
                "SELECT id, full_name, registration_number, age, profession, gender, status, email, phone "
                "FROM members ORDER BY full_name;"
            ).fetchall()
        return self._to_dicts(rows)

    def get_member(self, member_id: int) -> dict[str, Any] | None:
        with self.db.get_connection() as connection:
            row = connection.execute("SELECT * FROM members WHERE id = ?;", (member_id,)).fetchone()
        return dict(row) if row else None

    def add_category(self, name: str, description: str = "") -> int:
        with self.db.get_connection() as connection:
            cursor = connection.execute("INSERT INTO categories (name, description) VALUES (?, ?);", (name, description))
            return int(cursor.lastrowid)

    def list_categories(self) -> list[dict[str, Any]]:
        with self.db.get_connection() as connection:
            rows = connection.execute("SELECT id, name, description FROM categories ORDER BY name;").fetchall()
        return self._to_dicts(rows)

    def delete_category(self, category_id: int) -> None:
        with self.db.get_connection() as connection:
            existing_books = connection.execute(
                "SELECT 1 FROM books WHERE category_id = ? LIMIT 1;",
                (category_id,),
            ).fetchone()
            if existing_books:
                raise ValueError("Cannot delete category with books assigned to it.")
            connection.execute("DELETE FROM categories WHERE id = ?;", (category_id,))

    def add_book(
        self,
        title: str,
        author: str,
        isbn: str,
        category_id: int,
        total_copies: int,
        published_year: int | None = None,
    ) -> int:
        sql = (
            "INSERT INTO books (title, author, isbn, category_id, total_copies, available_copies, published_year) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);"
        )
        with self.db.get_connection() as connection:
            cursor = connection.execute(sql, (title, author, isbn, category_id, total_copies, total_copies, published_year))
            return int(cursor.lastrowid)

    def update_book(
        self,
        book_id: int,
        title: str,
        author: str,
        isbn: str,
        category_id: int,
        total_copies: int,
        published_year: int | None = None,
    ) -> None:
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

            if total_copies < borrowed_count:
                raise ValueError("Total copies cannot be less than currently borrowed copies.")

            new_available = total_copies - borrowed_count
            connection.execute(
                "UPDATE books SET title = ?, author = ?, isbn = ?, category_id = ?, total_copies = ?, available_copies = ?, published_year = ? "
                "WHERE id = ?;",
                (title, author, isbn, category_id, total_copies, new_available, published_year, book_id),
            )

    def delete_book(self, book_id: int) -> None:
        with self.db.get_connection() as connection:
            active_loan = connection.execute(
                "SELECT 1 FROM loans WHERE book_id = ? AND status = 'borrowed' LIMIT 1;",
                (book_id,),
            ).fetchone()
            if active_loan:
                raise ValueError("Cannot delete book with active loans.")

            any_loan_history = connection.execute("SELECT 1 FROM loans WHERE book_id = ? LIMIT 1;", (book_id,)).fetchone()
            if any_loan_history:
                raise ValueError("Cannot delete book that has loan history.")

            connection.execute("DELETE FROM ratings WHERE book_id = ?;", (book_id,))
            connection.execute("DELETE FROM books WHERE id = ?;", (book_id,))

    def list_books(self) -> list[dict[str, Any]]:
        sql = (
            "SELECT b.id, b.title, b.author, b.isbn, c.name AS category_name, b.available_copies, b.total_copies "
            "FROM books b JOIN categories c ON c.id = b.category_id ORDER BY b.title;"
        )
        with self.db.get_connection() as connection:
            rows = connection.execute(sql).fetchall()
        return self._to_dicts(rows)

    def search_books(self, keyword: str) -> list[dict[str, Any]]:
        pattern = f"%{keyword.strip()}%"
        sql = (
            "SELECT b.id, b.title, b.author, b.isbn, c.name AS category_name, b.available_copies, b.total_copies "
            "FROM books b JOIN categories c ON c.id = b.category_id "
            "WHERE b.title LIKE ? OR b.author LIKE ? OR b.isbn LIKE ? OR c.name LIKE ? "
            "ORDER BY b.title;"
        )
        with self.db.get_connection() as connection:
            rows = connection.execute(sql, (pattern, pattern, pattern, pattern)).fetchall()
        return self._to_dicts(rows)

    def borrow_book(self, member_id: int, book_id: int, days: int = 14) -> int:
        loan_date = date.today()
        due_date = loan_date + timedelta(days=days)

        with self.db.get_connection() as connection:
            member = connection.execute("SELECT status FROM members WHERE id = ?;", (member_id,)).fetchone()
            if not member:
                raise ValueError("Member does not exist.")
            if member["status"] != "active":
                raise ValueError("Member is inactive.")

            book = connection.execute("SELECT available_copies FROM books WHERE id = ?;", (book_id,)).fetchone()
            if not book:
                raise ValueError("Book does not exist.")
            if int(book["available_copies"]) <= 0:
                raise ValueError("Book is not available.")

            cursor = connection.execute(
                "INSERT INTO loans (member_id, book_id, loan_date, due_date, status) VALUES (?, ?, ?, ?, 'borrowed');",
                (member_id, book_id, loan_date.isoformat(), due_date.isoformat()),
            )
            connection.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = ?;", (book_id,))
            return int(cursor.lastrowid)

    def return_book(self, loan_id: int) -> None:
        with self.db.get_connection() as connection:
            loan = connection.execute("SELECT book_id, status FROM loans WHERE id = ?;", (loan_id,)).fetchone()
            if not loan:
                raise ValueError("Loan does not exist.")
            if loan["status"] != "borrowed":
                raise ValueError("Loan is already returned.")

            connection.execute("UPDATE loans SET return_date = DATE('now'), status = 'returned' WHERE id = ?;", (loan_id,))
            connection.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?;", (loan["book_id"],))

    def list_loans(self, active_only: bool = False) -> list[dict[str, Any]]:
        sql = (
            "SELECT l.id, m.full_name AS member_name, b.title AS book_title, l.loan_date, l.due_date, l.return_date, l.status "
            "FROM loans l "
            "JOIN members m ON m.id = l.member_id "
            "JOIN books b ON b.id = l.book_id "
        )
        if active_only:
            sql += "WHERE l.status = 'borrowed' "
        sql += "ORDER BY l.loan_date DESC;"

        with self.db.get_connection() as connection:
            rows = connection.execute(sql).fetchall()
        return self._to_dicts(rows)

    def add_or_update_rating(self, member_id: int, book_id: int, rating: int) -> None:
        with self.db.get_connection() as connection:
            connection.execute(
                "INSERT INTO ratings (member_id, book_id, rating) VALUES (?, ?, ?) "
                "ON CONFLICT(member_id, book_id) DO UPDATE SET rating = excluded.rating, rated_at = CURRENT_TIMESTAMP;",
                (member_id, book_id, rating),
            )


