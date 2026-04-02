import tkinter as tk
from tkinter import ttk, messagebox


class BooksView(ttk.Frame):
    """
    GUI for managing books.
    Fully compatible with DTO-based DAL/BusinessLogic.
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # BOOKS TABLE
        # ---------------------------------------------------------
        self.tree = ttk.Treeview(
            self,
            columns=("title", "author", "isbn", "category", "available", "total"),
            show="headings",
        )
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("category", text="Category")
        self.tree.heading("available", text="Available")
        self.tree.heading("total", text="Total Copies")

        self.tree.pack(fill="both", expand=True, pady=10)

        # ---------------------------------------------------------
        # BOOK FORM
        # ---------------------------------------------------------
        form = ttk.Frame(self)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Title:").grid(row=0, column=0)
        self.entry_title = ttk.Entry(form)
        self.entry_title.grid(row=0, column=1)

        ttk.Label(form, text="Author:").grid(row=1, column=0)
        self.entry_author = ttk.Entry(form)
        self.entry_author.grid(row=1, column=1)

        ttk.Label(form, text="ISBN:").grid(row=2, column=0)
        self.entry_isbn = ttk.Entry(form)
        self.entry_isbn.grid(row=2, column=1)

        ttk.Label(form, text="Category:").grid(row=3, column=0)
        self.entry_category = ttk.Combobox(form, values=self._get_categories())
        self.entry_category.grid(row=3, column=1)

        ttk.Label(form, text="Total Copies:").grid(row=4, column=0)
        self.entry_total = ttk.Entry(form)
        self.entry_total.grid(row=4, column=1)

        ttk.Label(form, text="Published Year:").grid(row=5, column=0)
        self.entry_year = ttk.Entry(form)
        self.entry_year.grid(row=5, column=1)

        # ---------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------
        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=10)

        ttk.Button(btns, text="Add Book", command=self.add_book).pack(side="left", padx=5)
        ttk.Button(btns, text="Refresh", command=self.refresh).pack(side="left", padx=5)

        # Load initial data
        self.refresh()

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _get_categories(self):
        """Return category names for dropdown."""
        return [c.name for c in self.logic.list_categories()]

    def _get_category_id(self, name):
        """Return category ID from name."""
        for c in self.logic.list_categories():
            if c.name == name:
                return c.id
        return None

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------
    def refresh(self):
        """Load books into the table."""
        self.tree.delete(*self.tree.get_children())

        for b in self.logic.list_books():  # b is BookResponseDTO
            self.tree.insert(
                "",
                "end",
                values=(
                    b.title,
                    b.author,
                    b.isbn,
                    b.category_name,
                    b.available_copies,
                    b.total_copies,
                ),
            )

    def add_book(self):
        """Add a new book."""
        try:
            title = self.entry_title.get()
            author = self.entry_author.get()
            isbn = self.entry_isbn.get()
            category_name = self.entry_category.get()
            total = int(self.entry_total.get())
            year = int(self.entry_year.get()) if self.entry_year.get() else None

            category_id = self._get_category_id(category_name)
            if category_id is None:
                raise ValueError("Invalid category selected.")

            self.logic.add_book(
                title=title,
                author=author,
                isbn=isbn,
                category_id=category_id,
                total_copies=total,
                published_year=year,
            )

            messagebox.showinfo("Success", "Book added successfully!")
            self.refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))
