from __future__ import annotations
from pathlib import Path
from gui.MainTkWindow import MainTkWindow

from app.bootstrap import create_dal, create_business_logic


def main() -> None:
    """Start the application."""
    project_root = Path(__file__).resolve().parent
    db_path = project_root / "library.db"

    dal = create_dal(db_path)
    business_logic = create_business_logic(dal)

    print("DB ready.")
    print(f"Members: {len(dal.list_members())}")
    print(f"Books: {len(dal.list_books())}")
    print(f"Loans: {len(dal.list_loans())}")

    app = MainTkWindow(business_logic)
    app.mainloop()


if __name__ == "__main__":
    main()