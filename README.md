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
  Books_Page.py        Book catalog with search and category filters.
  Book_Edit_Page.py    Add / edit / delete a book.
  Categories_Page.py   Add / edit / delete categories.
  Loans_Page.py        Lend a book and return a book.
  Members_Page.py      Member CRUD and renewal / deactivation.
  Rating_Page.py       Rate a returned book.
  Recommend_Page.py    Per-member book recommendations.
  Statistics_Page.py   Five statistics sections (charts + tables).
  Assets/              Icons and images used in the GUI.

sql/
  schema.sql           CREATE TABLE IF NOT EXISTS schema script.
  library_erd_schema.png  ERD diagram of the schema.
```

## Architecture (top-down)

1. **GUI** (`gui/`) only talks to the `BusinessLogic` instance it receives as `service`.
2. **BusinessLogic** (`app/business_logic.py`) builds DTOs, runs them through validators, and delegates to the DAL.
3. **DAL** (`app/dal.py`) executes parameterised SQL through the `DatabaseManager`.
4. **DatabaseManager** (`app/database.py`) manages SQLite connections with `PRAGMA foreign_keys = ON`.

## To regenerate requirements

```
pip freeze > requirements.txt
```
