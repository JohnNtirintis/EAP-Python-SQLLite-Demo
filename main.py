"""
main.py - Entry point for the Library Management System.

Initializes the SQLite database, seeds sample data,
and launches the tkinter GUI.
"""

#import database as db
#from gui import LibraryApp

def main():
    # Step 1: Create tables (if they don't exist yet)
    db.initialize_database()

    # Step 2: Populate with sample data (only if DB is empty)
    db.seed_data()

    # Step 3: Launch the GUI
    app = LibraryApp()
    app.mainloop()

if __name__ == "__main__":
    main()
