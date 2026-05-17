# Σύστημα Διαχείρισης Δανειστικής Βιβλιοθήκης
EAP - ΠΛΗΠΡΟ Project 31 (2025-2026)

A library management system built with Python, SQLite and tkinter.

## Installation

```
pip install -r requirements.txt
```

## Running the app

```
python main.py
```

On first run, the app creates `library.db` next to `main.py`, applies the schema
from `sql/schema.sql`, and seeds starter data (categories, books, members,
loans, ratings).

## Project structure

```
main.py                Entry point. Builds the DAL/BusinessLogic and launches the GUI.
requirements.txt       Pinned third-party dependencies.

app/                   Backend - DB, business logic, validation.
  database.py          SQLite connection manager (context-managed, FK on).
  dal.py               Data Access Layer. Inline SQL + CRUD methods.
  business_logic.py    BusinessLogic facade used by the GUI. Validates and delegates to dal.
  bootstrap.py         Wires the DAL and seeds starter data on first run.
  dto.py               Dataclasses used to pass data between layers.
  validation/          Stateless validation rules + per-entity validators.

gui/                   tkinter user interface. One module per page.
  MainTkWindow.py      Main window. Holds page instances and routes navigation.
  SideBar_Menu.py      Left-hand navigation menu.
  Styles.py            Colour, font and ttk style definitions.
  Dashboard_Page.py    Home page with KPI cards, loans chart, overdue table.
  Books_Page.py        Book catalog with search, category filters, rating sort.
  Book_Edit_Page.py    Add / edit / delete a book.
  Categories_Page.py   Add / edit / delete categories.
  Loans_Page.py        Lend a book and return a book.
  Members_Page.py      Member CRUD and renewal / deactivation.
  Rating_Page.py       Rate a returned book (1-5).
  Recommend_Page.py    Per-member book recommendations.
  Statistics_Page.py   Five statistics sections (charts + tables).
  Assets/              Icons and images used in the GUI.

sql/
  schema.sql           CREATE TABLE IF NOT EXISTS schema script.
  schema.png           ERD diagram of the schema.
```

## Architecture (top-down)

1. **GUI** (`gui/`) only talks to the `BusinessLogic` instance it receives as `service`. No SQL leaks into the GUI layer.
2. **BusinessLogic** (`app/business_logic.py`) builds DTOs, runs them through validators, and delegates to the DAL.
3. **Validation** (`app/validation/`) is a separate layer of stateless functions. They raise typed exceptions on bad input.
4. **DAL** (`app/dal.py`) executes parameterised SQL through the `DatabaseManager`. All multi-step operations run inside a `with` block so they form a single transaction.
5. **DatabaseManager** (`app/database.py`) manages SQLite connections with `PRAGMA foreign_keys = ON`.

## Database

5 tables: `members`, `categories`, `books`, `loans`, `ratings`. Foreign keys are enforced. The `ratings` table has `UNIQUE(member_id, book_id)` so a member can have at most one rating per book, with `ON DELETE CASCADE` on both references.

Indexes covering the hot query paths:

- `idx_loans_member_date` - loans filtered by member + date (Statistics sections 1, 2, 4)
- `idx_loans_book_date`   - book popularity by date (Statistics section 3)
- `idx_books_category`    - category distribution (Statistics sections 2, 3)
- `idx_loans_status`      - Dashboard's "currently borrowed" KPI
- `idx_ratings_book`      - average rating lookups on `books` list

## Notable implementation details

- **Borrow** is an atomic transaction: INSERT into `loans` + UPDATE of `books.available_copies` in the same `with` block. If either fails, the database rolls back.
- **Return** moves the loan to `status='returned'` and increments `available_copies`. If the GUI passes a rating, `return_book(loan_id, rating=N)` also runs the rating upsert in the same call.
- **Rate** uses SQLite UPSERT (`INSERT … ON CONFLICT(member_id, book_id) DO UPDATE`) so a member can rate the same book again and the row is updated rather than duplicated.
- **Search** does a single LEFT JOIN with the per-book ratings aggregate, so the catalog ships title, author, ISBN, category, availability, and average rating in one round-trip.
- **Recommendations** are computed entirely in SQL: a score of `1.5 * category_loans + avg_rating` per candidate book, with books the member has already borrowed excluded.

## To regenerate requirements

```
pip freeze > requirements.txt
```
