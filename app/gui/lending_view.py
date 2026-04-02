import tkinter as tk
from tkinter import ttk, messagebox


class LendingView(ttk.Frame):
    """
    Lending tab — fully compatible with DTO-based DAL/BusinessLogic.
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # SECTION: Borrow book
        # ---------------------------------------------------------
        borrow_frame = ttk.LabelFrame(self, text="Borrow book")
        borrow_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(borrow_frame, text="Member:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.entry_member = ttk.Combobox(
            borrow_frame,
            values=[f"{m.id} - {m.full_name}" for m in self.logic.list_members()],
            width=40,
            state="readonly"
        )
        self.entry_member.grid(row=0, column=1, sticky="w")

        ttk.Label(borrow_frame, text="Book:").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_book = ttk.Combobox(
            borrow_frame,
            values=[f"{b.id} - {b.title}" for b in self.logic.list_books()],
            width=40,
            state="readonly"
        )
        self.entry_book.grid(row=0, column=3, sticky="w")

        ttk.Button(borrow_frame, text="Borrow", command=self.borrow_book).grid(row=0, column=4, padx=10)

        # ---------------------------------------------------------
        # SECTION: Return book
        # ---------------------------------------------------------
        return_frame = ttk.LabelFrame(self, text="Return book")
        return_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(return_frame, text="Loan ID:").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_return_id = ttk.Entry(return_frame, width=20)
        self.entry_return_id.grid(row=0, column=1, sticky="w")

        ttk.Button(return_frame, text="Return", command=self.return_book).grid(row=0, column=2, padx=10)

        # ---------------------------------------------------------
        # SECTION: Loans table
        # ---------------------------------------------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "member", "book", "loan_date", "due_date", "return_date", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("id", text="Loan ID")
        self.tree.heading("member", text="Member")
        self.tree.heading("book", text="Book")
        self.tree.heading("loan_date", text="Loan date")
        self.tree.heading("due_date", text="Due date")
        self.tree.heading("return_date", text="Return date")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=60)
        self.tree.column("member", width=180)
        self.tree.column("book", width=180)
        self.tree.column("loan_date", width=120)
        self.tree.column("due_date", width=120)
        self.tree.column("return_date", width=120)
        self.tree.column("status", width=100)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_loan)

        self.refresh()

    # ---------------------------------------------------------
    # BORROW
    # ---------------------------------------------------------
    def borrow_book(self):
        try:
            member_text = self.entry_member.get()
            book_text = self.entry_book.get()

            if not member_text or not book_text:
                raise ValueError("Select both member and book.")

            member_id = int(member_text.split(" - ")[0])
            book_id = int(book_text.split(" - ")[0])

            self.logic.borrow_book(member_id, book_id)

            messagebox.showinfo("Success", "Book borrowed.")
            self.refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # RETURN
    # ---------------------------------------------------------
    def return_book(self):
        try:
            loan_id = int(self.entry_return_id.get())
            self.logic.return_book(loan_id)

            messagebox.showinfo("Success", "Book returned.")
            self.refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # REFRESH TABLE
    # ---------------------------------------------------------
    def refresh(self):
        self.tree.delete(*self.tree.get_children())

        loans = self.logic.list_loans()  # list of LoanResponseDTO

        for l in loans:
            self.tree.insert(
                "",
                "end",
                values=(
                    l.id,
                    l.member_name,
                    l.book_title,
                    l.loan_date,
                    l.due_date,
                    l.return_date,
                    l.status,
                ),
            )

        # Refresh dropdowns with DTOs
        self.entry_member["values"] = [f"{m.id} - {m.full_name}" for m in self.logic.list_members()]
        self.entry_book["values"] = [f"{b.id} - {b.title}" for b in self.logic.list_books()]

    # ---------------------------------------------------------
    # AUTO-FILL HANDLER
    # ---------------------------------------------------------
    def on_select_loan(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        loan_id = values[0]
        member_name = values[1]
        book_title = values[2]

        # Auto-fill Loan ID
        self.entry_return_id.delete(0, "end")
        self.entry_return_id.insert(0, loan_id)

        # Auto-select member
        for item in self.entry_member["values"]:
            if member_name in item:
                self.entry_member.set(item)
                break

        # Auto-select book
        for item in self.entry_book["values"]:
            if book_title in item:
                self.entry_book.set(item)
                break
