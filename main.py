from __future__ import annotations

from pathlib import Path

from db_app.bootstrap import create_dal

# TODO
#from app.bootstrap import create_business_logic


def main() -> None:
    """Start the application.

    Flow:
    1) Find where this project is on disk.
    2) Decide the SQLite file path.
    3) Build the business logic object (app "brain").
    4) Give that object to the GUI so buttons/forms can use it.
    5) Start the GUI loop.
    """
    # Get the folder where main.py lives (your project root here).
    project_root = Path(__file__).resolve().parent

    # Path to the SQLite database file.
    # If it does not exist, SQLite creates it when connecting.
    db_path = project_root / "library.db"
    
    # Test:
    dal = create_dal(db_path)

    members = dal.list_members()
    books = dal.list_books()
    loans = dal.list_loans()

    print("DB ready.")
    print(f"Members: {len(members)}")
    print(f"Books: {len(books)}")
    print(f"Loans: {len(loans)}")

    # Create the BUSINESS LOGIC layer.
    # Think of this as the app's "brain":
    # it knows the library rules
    # it validates input
    # it talks to DAL/DB
    # bootstrap also wires dependencies and initializes schema.
    #business_logic = create_business_logic(db_path)

    # TODO: Create the GUI and start the app.
    # Create the GUI
    # PASS business_logic into LibraryApp so the GUI can call
    # methods like create_member / borrow_book without writing SQL.
    # This keeps clean layering:
    # GUI -> BusinessLogic -> DAL -> DB
    # app = LibraryApp(business_logic)

    # Start Tkinter event loop (window stays open and listens for user actions).
    # app.mainloop()

if __name__ == "__main__":
    main()
