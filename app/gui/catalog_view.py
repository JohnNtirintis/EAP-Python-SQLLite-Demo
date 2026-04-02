import tkinter as tk
from tkinter import ttk, messagebox


class CatalogView(ttk.Frame):
    """
    Catalog tab — now fully compatible with DTO-based DAL/BusinessLogic.
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # SECTION: Category creation
        # ---------------------------------------------------------
        cat_frame = ttk.LabelFrame(self, text="Add category")
        cat_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(cat_frame, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.entry_cat_name = ttk.Entry(cat_frame, width=30)
        self.entry_cat_name.grid(row=0, column=1, sticky="w")

        ttk.Label(cat_frame, text="Description:").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_cat_desc = ttk.Entry(cat_frame, width=40)
        self.entry_cat_desc.grid(row=0, column=3, sticky="w")

        ttk.Button(cat_frame, text="Add category", command=self.add_category).grid(row=0, column=4, padx=10)

        # ---------------------------------------------------------
        # SECTION: Book creation / edit
        # ---------------------------------------------------------
        book_frame = ttk.LabelFrame(self, text="Book details")
        book_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(book_frame, text="Title:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.entry_title = ttk.Entry(book_frame, width=40)
        self.entry_title.grid(row=0, column=1, sticky="w")

        ttk.Label(book_frame, text="Author:").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_author = ttk.Entry(book_frame, width=30)
        self.entry_author.grid(row=0, column=3, sticky="w")

        ttk.Label(book_frame, text="ISBN:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_isbn = ttk.Entry(book_frame, width=40)
        self.entry_isbn.grid(row=1, column=1, sticky="w")

        ttk.Label(book_frame, text="Category:").grid(row=1, column=2, sticky="e", padx=5)
        self.entry_category = ttk.Combobox(
            book_frame,
            values=[c.name for c in self.logic.list_categories()],
            width=28,
            state="readonly"
        )
        self.entry_category.grid(row=1, column=3, sticky="w")

        ttk.Label(book_frame, text="Total copies:").grid(row=2, column=0, sticky="e", padx=5)
        self.entry_copies = ttk.Entry(book_frame, width=20)
        self.entry_copies.grid(row=2, column=1, sticky="w")

        ttk.Label(book_frame, text="Published year:").grid(row=2, column=2, sticky="e", padx=5)
        self.entry_year = ttk.Entry(book_frame, width=20)
        self.entry_year.grid(row=2, column=3, sticky="w")

        ttk.Button(book_frame, text="Add book", command=self.add_book).grid(row=3, column=0, padx=10, pady=5)
        ttk.Button(book_frame, text="Update book", command=self.update_book).grid(row=3, column=1, padx=10, pady=5)
        ttk.Button(book_frame, text="Delete book", command=self.delete_book).grid(row=3, column=2, padx=10, pady=5)
        ttk.Button(book_frame, text="Reset Form", command=self.reset_form).grid(row=3, column=3, padx=10, pady=5)

        # ---------------------------------------------------------
        # SECTION: Search
        # ---------------------------------------------------------
        search_frame = ttk.LabelFrame(self, text="Search books")
        search_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(search_frame, text="Keyword:").pack(side="left", padx=5)
        self.entry_search = ttk.Entry(search_frame, width=40)
        self.entry_search.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Show all", command=self.refresh).pack(side="left", padx=5)

        # ---------------------------------------------------------
        # SECTION: Books table
        # ---------------------------------------------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "author", "isbn", "category", "available", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col, text in zip(columns, ["ID", "Title", "Author", "ISBN", "Category", "Available", "Total copies"]):
            self.tree.heading(col, text=text)

        self.tree.column("id", width=40)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("isbn", width=120)
        self.tree.column("category", width=120)
        self.tree.column("available", width=80)
        self.tree.column("total", width=100)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_book)

        self.refresh()

    # ---------------------------------------------------------
    # CATEGORY
    # ---------------------------------------------------------
    def add_category(self):
        try:
            name = self.entry_cat_name.get().strip()
            desc = self.entry_cat_desc.get().strip()

            if not name:
                raise ValueError("Category name cannot be empty.")

            self.logic.add_category(name=name, description=desc)

            messagebox.showinfo("Success", "Category added.")

            # Refresh category dropdown
            self.entry_category["values"] = [c.name for c in self.logic.list_categories()]

            self.entry_cat_name.delete(0, "end")
            self.entry_cat_desc.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # BOOKS: ADD
    # ---------------------------------------------------------
    def add_book(self):
        try:
            title = self.entry_title.get().strip()
            author = self.entry_author.get().strip()
            isbn = self.entry_isbn.get().strip()
            category_name = self.entry_category.get().strip()
            copies = int(self.entry_copies.get())
            year = int(self.entry_year.get()) if self.entry_year.get() else None

            if not title or not author or not isbn or not category_name:
                raise ValueError("All fields except year are required.")

            categories = self.logic.list_categories()
            category_id = next(c.id for c in categories if c.name == category_name)

            self.logic.add_book(
                title=title,
                author=author,
                isbn=isbn,
                category_id=category_id,
                total_copies=copies,
                published_year=year,
            )

            messagebox.showinfo("Success", "Book added.")
            self.refresh()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # BOOKS: UPDATE
    # ---------------------------------------------------------
    def update_book(self):
        try:
            selected = self.tree.selection()
            if not selected:
                raise ValueError("No book selected.")

            book_id = self.tree.item(selected[0])["values"][0]

            title = self.entry_title.get().strip()
            author = self.entry_author.get().strip()
            isbn = self.entry_isbn.get().strip()
            category_name = self.entry_category.get().strip()
            copies = int(self.entry_copies.get())
            year = int(self.entry_year.get()) if self.entry_year.get() else None

            if not title or not author or not isbn or not category_name:
                raise ValueError("All fields except year are required.")

            categories = self.logic.list_categories()
            category_id = next(c.id for c in categories if c.name == category_name)

            self.logic.update_book(
                book_id=book_id,
                title=title,
                author=author,
                isbn=isbn,
                category_id=category_id,
                total_copies=copies,
                published_year=year,
            )

            messagebox.showinfo("Success", "Book updated.")
            self.refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # BOOKS: DELETE
    # ---------------------------------------------------------
    def delete_book(self):
        try:
            selected = self.tree.selection()
            if not selected:
                raise ValueError("No book selected.")

            book_id = self.tree.item(selected[0])["values"][0]

            confirm = messagebox.askyesno(
                "Confirm delete",
                "Are you sure you want to delete this book?\nThis action cannot be undone."
            )
            if not confirm:
                return

            self.logic.delete_book(book_id)

            messagebox.showinfo("Success", "Book deleted.")
            self.refresh()
            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    def search_books(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.refresh()
            return

        results = self.logic.search_books(keyword)
        self._populate_table(results)

    # ---------------------------------------------------------
    # REFRESH TABLE
    # ---------------------------------------------------------
    def refresh(self):
        books = self.logic.list_books()
        self._populate_table(books)

    def _populate_table(self, books):
        self.tree.delete(*self.tree.get_children())

        for b in books:  # b is BookResponseDTO
            self.tree.insert(
                "",
                "end",
                values=(
                    b.id,
                    b.title,
                    b.author,
                    b.isbn,
                    b.category_name,
                    b.available_copies,
                    b.total_copies,
                ),
            )

    # ---------------------------------------------------------
    # AUTO-FILL HANDLER
    # ---------------------------------------------------------
    def on_select_book(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        book_id = self.tree.item(selected[0])["values"][0]

        books = self.logic.list_books()
        book = next((b for b in books if b.id == book_id), None)
        if not book:
            return

        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, book.title)

        self.entry_author.delete(0, "end")
        self.entry_author.insert(0, book.author)

        self.entry_isbn.delete(0, "end")
        self.entry_isbn.insert(0, book.isbn)

        self.entry_category.set(book.category_name)

        self.entry_copies.delete(0, "end")
        self.entry_copies.insert(0, book.total_copies)

        self.entry_year.delete(0, "end")
        if book.published_year:
            self.entry_year.insert(0, book.published_year)

    # ---------------------------------------------------------
    # RESET FORM
    # ---------------------------------------------------------
    def reset_form(self):
        self.entry_title.delete(0, "end")
        self.entry_author.delete(0, "end")
        self.entry_isbn.delete(0, "end")
        self.entry_category.set("")
        self.entry_copies.delete(0, "end")
        self.entry_year.delete(0, "end")
        self.tree.selection_remove(self.tree.selection())
