"""
Library Management System - SQLite3 Demo
Demonstrates why SQLite3 is superior to .txt file storage for a book rental system
Documentation: https://docs.python.org/3/library/sqlite3.html
"""

import sqlite3
from datetime import datetime

def demo():
    # =============================================================================
    # SECTION 1: Initialize Database Connection
    # =============================================================================
    # Connect to an on-disk database file (creates it if it doesn't exist)
    con = sqlite3.connect('library.db')
    cur = con.cursor()

    # Enable foreign keys for referential integrity
    cur.execute("PRAGMA foreign_keys = ON")

    # =============================================================================
    # SECTION 2: Define Schema - Proper Data Types
    # =============================================================================
    print("=" * 60)
    print("Creating library database schema...")
    print("=" * 60)

    # Users/Members table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            registration_date TEXT
        )
    """)

    # Books table with proper data types
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            isbn TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_available INTEGER DEFAULT 1,  -- 1=available, 0=rented
            rating REAL CHECK(rating >= 1 AND rating <= 5)
        )
    """)

    # Rental history - tracks who rented what and when
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            isbn TEXT NOT NULL,
            rental_date TEXT,
            return_date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(isbn) REFERENCES books(isbn)
        )
    """)

    con.commit()
    print("Database schema created successfully!\n")

    # =============================================================================
    # SECTION 3: Insert Sample Users
    # =============================================================================
    print("=" * 60)
    print("Adding sample users...")
    print("=" * 60)

    users_data = [
        ("Alice Johnson", "alice@email.com", "555-0101"),
        ("Bob Smith", "bob@email.com", "555-0102"),
        ("Carol White", "carol@email.com", "555-0103"),
    ]

    for name, email, phone in users_data:
        cur.execute("""
            INSERT INTO users (name, email, phone, registration_date)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, datetime.now().isoformat()))

    con.commit()
    print(f"Inserted {len(users_data)} users\n")

    # =============================================================================
    # SECTION 4: Insert Sample Books (with proper column mapping)
    # =============================================================================
    print("=" * 60)
    print("Adding sample books...")
    print("=" * 60)

    books_data = [
        ('978-0451524935', '1984', 'George Orwell', 1, 4.5),
        ('978-0380016647', 'The Animal Farm', 'George Orwell', 1, 4.3),
        ('978-0393067491', 'The State', 'Plato', 0, 3.8),
        ('978-0201379624', 'Design Patterns', 'Gang of Four', 1, 4.7),
        ('978-0262033848', 'Introduction to Algorithms', 'CLRS', 1, 4.8),
    ]

    # Using executemany - all columns properly mapped
    cur.executemany("""
        INSERT INTO books (isbn, title, author, is_available, rating)
        VALUES (?, ?, ?, ?, ?)
    """, books_data)

    con.commit()
    print(f"Inserted {len(books_data)} books\n")

    # =============================================================================
    # SECTION 5: Demonstrate Powerful Queries (Why SQLite3 Wins!)
    # =============================================================================
    print("=" * 60)
    print("QUERYING EXAMPLES - What .txt Files CAN'T Do!")
    print("=" * 60)

    # Query 1: List all available books
    print("\n1. Find all AVAILABLE books (instant, even with 1M rows):")
    print("-" * 60)
    for isbn, title, author, is_available, rating in cur.execute(
        "SELECT isbn, title, author, is_available, rating FROM books WHERE is_available = 1"
    ):
        print(f"   [{isbn}] {title} by {author} | Rating: {rating}")

    # Query 2: Find books by a specific author
    print("\n2. Find all books by George Orwell:")
    print("-" * 60)
    for isbn, title, rating in cur.execute(
        "SELECT isbn, title, rating FROM books WHERE author = ?", ("George Orwell",)
    ):
        print(f"   • {title} ({isbn}): {rating}")

    # Query 3: Get all users and their rentals (JOIN query - .txt files would be NIGHTMARE)
    print("\n3. User rental history (with JOIN - impossible in .txt):")
    print("-" * 60)

    # First, let's record some rental activity
    cur.execute("""
        INSERT INTO rentals (user_id, isbn, rental_date, return_date)
        VALUES (1, '978-0451524935', '2026-02-01', NULL)
    """)
    cur.execute("""
        INSERT INTO rentals (user_id, isbn, rental_date, return_date)
        VALUES (2, '978-0380016647', '2026-02-05', '2026-02-12')
    """)
    con.commit()

    # Complex query joining three tables
    for user_name, book_title, rental_date, return_date in cur.execute("""
        SELECT u.name, b.title, r.rental_date, r.return_date
        FROM rentals r
        JOIN users u ON r.user_id = u.user_id
        JOIN books b ON r.isbn = b.isbn
        WHERE r.return_date IS NULL
    """):
        status = "Still renting" if return_date is None else "Returned"
        print(f"   • {user_name}: {book_title} (since {rental_date}) - {status}")

    # Query 4: Statistics - Get average rating
    print("\n4. Library statistics (Calculate in seconds, not hours):")
    print("-" * 60)
    avg_rating = cur.execute("SELECT AVG(rating) FROM books").fetchone()[0]
    total_books = cur.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    available_books = cur.execute("SELECT COUNT(*) FROM books WHERE is_available = 1").fetchone()[0]

    print(f"   • Total books: {total_books}")
    print(f"   • Available for rent: {available_books}")
    print(f"   • Average rating: {avg_rating:.2f}")

    # Query 5: Find high-rated books (rating >= 4.5)
    print("\n5. Premium collection (rating >= 4.5):")
    print("-" * 60)
    for title, rating, is_available in cur.execute(
        "SELECT title, rating, is_available FROM books WHERE rating >= 4.5 ORDER BY rating DESC"
    ):
        status = "Available" if is_available else "Rented"
        print(f"   • {title}: {rating} - {status}")

    # =============================================================================
    # SECTION 6: Why .txt Files Would Be a Disaster
    # =============================================================================
    print("\n" + "=" * 60)
    print("WHY .txt FILES ARE A BAD IDEA FOR THIS PROJECT:")
    print("=" * 60)

    comparison = """
    .txt File Approach Problems:
    ─────────────────────────────────────────────────────────────
    Data Corruption Risk
    - One person accidentally deletes/modifies a line → entire record lost
    - No undo or rollback capability
    
    Query Nightmare
    - Need available books? Parse entire file, check each line manually
    - Need user rental history? Search multiple files, somehow correlate data
    - Want statistics? Parse everything, calculate in Python loops
    
    Concurrency Issues
    - 2 people access file simultaneously → Data gets corrupted
    - No locking mechanism = race conditions
    
    Data Validation
    - Can't enforce data types (is rating REALLY a number between 1-5?)
    - Can't prevent duplicate user emails
    - Can't prevent missing required fields
    
    Relationships
    - Which user rented which book? Manual correlation across files
    - Book categories? Author relationships? Foreign keys? IMPOSSIBLE

    ────────────────────────────────────────────────────────────── 
    SQLite3 Handles All This Automatically!
    """

    print(comparison)

    # =============================================================================
    # SECTION 7: Clean Up
    # =============================================================================
    print("\n" + "=" * 60)
    con.close()
    print("Database connection closed")
    print("Database saved to: library.db")
    print("=" * 60)

    # =============================================================================
    # Additional Notes for Your Team
    # =============================================================================
    print("""
    SQLite3 ADVANTAGES FOR YOUR PROJECT:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Zero configuration - just import sqlite3
    Portable - library.db is one file, copy it anywhere
    Perfect for small-medium systems (100K+ records)
    Built into Python - no external dependencies
    Industry standard - used by Firefox, Chrome, SQL databases
    Future proof - easy upgrade to PostgreSQL/MySQL later
    Crash recovery - transactions ensure data safety
    SQL standard - whoever learns it knows most databases
    """)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    demo()
