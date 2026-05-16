# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox

from gui.Styles import *
from gui.Dashboard_Page import autosize_content


# Map DB loan.status -> Greek display in the Δανεισμένα Βιβλία table.
STATUS_DISPLAY = {
    "borrowed": "Ενεργό",
    "returned": "Επιστράφηκε",
}


class Loans(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        #cached copies of all books / members / loans
        self._all_books = []
        self._all_members = []
        self._all_loans = []

        #last loan id user selected for return (consumed by Rating page)
        self.pending_return_loan_id = None

        #make Loans expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.loans_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.loans_frame.grid(row=0, column=0, sticky='nswe')

        self.loans_frame.grid_columnconfigure(0, weight=1)
        self.loans_frame.grid_columnconfigure(1, weight=1)
        self.loans_frame.grid_rowconfigure(0, weight=0)
        self.loans_frame.grid_rowconfigure(1, weight=1, minsize=200)
        self.loans_frame.grid_rowconfigure(2, weight=1, minsize=200)
        self.loans_frame.grid_rowconfigure(3, weight=0)
        self.loans_frame.grid_rowconfigure(4, weight=1, minsize=200)

        #loans title
        loans_label = tk.Label(
                            self.loans_frame,
                            anchor='w',
                            text='Δανεισμός Βιβλίων',
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE
                            )
        loans_label.grid(row=0, column=0, padx=15, pady=(5, 10), sticky='nsew')

        #loans button
        self.loan_button = ttk.Button(
                        self.loans_frame,
                        text="ΔΑΝΕΙΣΜΟΣ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.borrow_book,
                        )
        self.loan_button.grid(row=0, column=1, sticky='e', padx=(0, 15), pady=10)
        self.loan_button.state(['disabled'])

        #table title
        loans_table_title = tk.Label(
                            self.loans_frame,
                            anchor='w',
                            text='Δανεισμένα Βιβλία',
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE
                            )
        loans_table_title.grid(row=3, column=0, padx=15, pady=(5, 10), sticky='nsew')

        #return button
        self.return_button = ttk.Button(
                        self.loans_frame,
                        text="ΕΠΙΣΤΡΟΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.go_to_rating,
                        )
        self.return_button.grid(row=3, column=1, sticky='e', padx=(0, 15), pady=10)
        self.return_button.state(['disabled'])

        self.selectbook_loan()
        self.selectmember_loan()
        self.return_table()

        # initial data load
        self.refresh_all()

    # =========================================
    # Loan/Return button activation
    # =========================================
    def update_loan_btn(self):
        has_book = bool(self.searchbooks_table.selection())
        has_member = bool(self.searchmember_table.selection())
        if has_book and has_member:
            self.loan_button.state(['!disabled'])
        else:
            self.loan_button.state(['disabled'])

    def update_return_btn(self, button, table):
        selected = table.selection()
        if not selected:
            button.state(['disabled'])
        else:
            button.state(['!disabled'])

    # =========================================
    # Select Book table
    # =========================================
    def selectbook_loan(self):
        container = tk.Frame(
                    self.loans_frame,
                    bd=0,
                    bg=BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=1, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        title_lbl = tk.Label(
                        container,
                        anchor="center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font=FONT_SUBHEADER_BOLD,
                        text="Επιλογή Βιβλίου:"
                        )
        title_lbl.grid(row=0, column=0, sticky='w', padx=(15, 0), pady=10)

        #searchbar
        self.searchbar_book_var = tk.StringVar()
        self.searchbar_book = ttk.Entry(
                    container,
                    font=FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    textvariable=self.searchbar_book_var
                    )
        self.searchbar_book.grid(row=0, column=1, sticky='ew', padx=15, pady=10)
        self.searchbar_book_var.set("Αναζήτηση...")
        self.searchbar_book.bind("<FocusIn>",
                                 lambda e: remove_placeholder_var(self.searchbar_book_var))
        self.searchbar_book.bind("<FocusOut>",
                                 lambda e: add_placeholder_var(self.searchbar_book_var))
        self.searchbar_book.bind("<Return>", lambda e: self._filter_books_table())
        # live filter
        self.searchbar_book_var.trace_add("write", lambda *a: self._filter_books_table())

        #table
        columns = ("ID", "Τίτλος", "Συγγραφέας", "Έτος έκδοσης", "ISBN", "Διαθέσιμα")
        self.searchbooks_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.searchbooks_table.grid(row=1, column=0, columnspan=2, sticky='nsew',
                                    padx=(15, 5), pady=(0, 5))
        self.searchbooks_table.bind("<<TreeviewSelect>>",
                                    lambda e: self.update_loan_btn())

        #scrollbars
        self._book_v_scroll = ttk.Scrollbar(
                        container, orient='vertical',
                        command=self.searchbooks_table.yview,
                        style="Vertical.TScrollbar"
                        )
        self._book_v_scroll.grid(row=1, column=3, sticky='ns')
        self.searchbooks_table.config(yscrollcommand=self._book_v_scroll.set)

        self._book_h_scroll = ttk.Scrollbar(
                        container, orient='horizontal',
                        command=self.searchbooks_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        self._book_h_scroll.set(0.2, 0.5)
        self._book_h_scroll.grid(row=2, column=0, columnspan=2, sticky='we', padx=(15, 0))
        self.searchbooks_table.config(xscrollcommand=self._book_h_scroll.set)

        for col in columns:
            self.searchbooks_table.heading(col, text=col, anchor='w')
            self.searchbooks_table.column(
                col, anchor="w",
                width=120 if col != "ID" else 80,
                minwidth=120 if col != "ID" else 80,
                stretch=True if col != "ID" else False,
                )

    # =========================================
    # Select Member table
    # =========================================
    def selectmember_loan(self):
        container = tk.Frame(
                    self.loans_frame,
                    bd=0,
                    bg=BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        title_lbl = tk.Label(
                        container,
                        anchor="center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font=FONT_SUBHEADER_BOLD,
                        text="Επιλογή Mέλους:"
                        )
        title_lbl.grid(row=0, column=0, sticky='w', padx=(15, 0), pady=10)

        #searchbar
        self.searchbar_member_var = tk.StringVar()
        self.searchbar_member = ttk.Entry(
                    container,
                    font=FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    textvariable=self.searchbar_member_var
                    )
        self.searchbar_member.grid(row=0, column=1, sticky='ew', padx=15, pady=10)
        self.searchbar_member_var.set("Αναζήτηση...")
        self.searchbar_member.bind("<FocusIn>",
                                   lambda e: remove_placeholder_var(self.searchbar_member_var))
        self.searchbar_member.bind("<FocusOut>",
                                   lambda e: add_placeholder_var(self.searchbar_member_var))
        self.searchbar_member.bind("<Return>", lambda e: self._filter_members_table())
        self.searchbar_member_var.trace_add("write", lambda *a: self._filter_members_table())

        #table
        columns = ("ID", "Ονοματεπώνυμο", "Αρ. Μητρώου", "Email", "Τηλέφωνο", "Κατάσταση")
        self.searchmember_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.searchmember_table.grid(row=1, column=0, columnspan=2, sticky='nsew',
                                     padx=(15, 5), pady=(0, 5))
        self.searchmember_table.bind("<<TreeviewSelect>>",
                                     lambda e: self.update_loan_btn())

        #scrollbars
        self._member_v_scroll = ttk.Scrollbar(
                        container, orient='vertical',
                        command=self.searchmember_table.yview,
                        style="Vertical.TScrollbar"
                        )
        self._member_v_scroll.grid(row=1, column=3, sticky='ns')
        self.searchmember_table.config(yscrollcommand=self._member_v_scroll.set)

        self._member_h_scroll = ttk.Scrollbar(
                        container, orient='horizontal',
                        command=self.searchmember_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        self._member_h_scroll.set(0.2, 0.5)
        self._member_h_scroll.grid(row=2, column=0, columnspan=2, sticky='we', padx=(15, 0))
        self.searchmember_table.config(xscrollcommand=self._member_h_scroll.set)

        for col in columns:
            self.searchmember_table.heading(col, text=col, anchor='w')
            self.searchmember_table.column(
                col, anchor="w",
                width=120 if col != "ID" else 80,
                minwidth=120 if col != "ID" else 80,
                stretch=True if col != "ID" else False,
                )

    # =========================================
    # Return Book table
    # =========================================
    def return_table(self):
        container = tk.Frame(
                    self.loans_frame,
                    bd=0,
                    bg=BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=4, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)

        columns = ("ID", "Μέλος", "Βιβλίο", "Ημ/νία Δανεισμού",
                   "Προθεσμία Επιστροφής", "Κατάσταση")
        self.loans_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.loans_table.grid(row=0, column=0, sticky='nsew', padx=(15, 5), pady=(0, 5))
        self.loans_table.bind(
            "<<TreeviewSelect>>",
            lambda e: self.update_return_btn(self.return_button, self.loans_table))

        v_scrollbar = ttk.Scrollbar(
                        container, orient='vertical',
                        command=self.loans_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.loans_table.config(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(
                        container, orient='horizontal',
                        command=self.loans_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2, 0.5)
        h_scrollbar.grid(row=1, column=0, sticky='we', padx=(15, 0))
        self.loans_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.loans_table.heading(col, text=col, anchor='w')
            self.loans_table.column(
                col, anchor="w",
                width=120 if col != "ID" else 80,
                minwidth=120 if col != "ID" else 80,
                stretch=True if col != "ID" else False,
                )

    # =========================================
    # Data refresh - called from reset()
    # =========================================
    def refresh_all(self):
        if not self.service:
            return
        try:
            self._all_books = list(self.service.list_books() or [])
            self._all_members = list(self.service.list_members() or [])
            self._all_loans = list(self.service.list_loans() or [])
        except Exception as e:
            messagebox.showerror("Σφάλμα φόρτωσης", str(e))
            return
        self._filter_books_table()
        self._filter_members_table()
        self._populate_loans_table()

    # =========================================
    # Populate filtered books table (available only)
    # =========================================
    def _filter_books_table(self):
        term = self.searchbar_book_var.get().strip()
        if term == "Αναζήτηση...":
            term = ""
        term_l = term.lower()

        self.searchbooks_table.delete(*self.searchbooks_table.get_children())
        for b in self._all_books:
            # only show books with at least 1 available copy
            available = getattr(b, "available_copies", 0)
            if available <= 0:
                continue
            title = getattr(b, "title", "") or ""
            author = getattr(b, "author", "") or ""
            isbn = getattr(b, "isbn", "") or ""
            category = getattr(b, "category_name", "") or ""
            if term_l:
                hay = " ".join([title, author, isbn, category]).lower()
                if term_l not in hay:
                    continue
            self.searchbooks_table.insert(
                "", "end", iid=str(b.id),
                values=(
                    f"{b.id:04d}",
                    title,
                    author,
                    getattr(b, "published_year", "") or "",
                    isbn,
                    f"{available}/{getattr(b, 'total_copies', 0)}",
                ),
            )
        autosize_content(self.searchbooks_table)

    # =========================================
    # Populate filtered members table
    # =========================================
    def _filter_members_table(self):
        term = self.searchbar_member_var.get().strip()
        if term == "Αναζήτηση...":
            term = ""
        term_l = term.lower()

        self.searchmember_table.delete(*self.searchmember_table.get_children())
        for m in self._all_members:
            name = m.get("full_name", "") or ""
            reg  = m.get("registration_number", "") or ""
            email = m.get("email", "") or ""
            if term_l:
                hay = " ".join([name, reg, email]).lower()
                if term_l not in hay:
                    continue
            status_display = "Ενεργό" if m.get("status") == "active" else "Ανενεργό"
            self.searchmember_table.insert(
                "", "end", iid=str(m["id"]),
                values=(
                    f"{m['id']:04d}",
                    name,
                    reg,
                    email,
                    m.get("phone", "") or "",
                    status_display,
                ),
            )
        autosize_content(self.searchmember_table)

    # =========================================
    # Populate loans table - shows borrowed (active) loans only
    # =========================================
    def _populate_loans_table(self):
        self.loans_table.delete(*self.loans_table.get_children())
        for ln in self._all_loans:
            if getattr(ln, "status", None) != "borrowed":
                continue
            self.loans_table.insert(
                "", "end", iid=str(ln.id),
                values=(
                    f"{ln.id:04d}",
                    getattr(ln, "member_name", "") or "",
                    getattr(ln, "book_title", "") or "",
                    getattr(ln, "loan_date", "") or "",
                    getattr(ln, "due_date", "") or "",
                    STATUS_DISPLAY.get(getattr(ln, "status", ""), getattr(ln, "status", "")),
                ),
            )
        autosize_content(self.loans_table)

    # =========================================
    # ΔΑΝΕΙΣΜΟΣ button
    # =========================================
    def borrow_book(self):
        if not self.service:
            return
        book_sel = self.searchbooks_table.selection()
        member_sel = self.searchmember_table.selection()
        if not book_sel or not member_sel:
            return
        book_id = int(book_sel[0])
        member_id = int(member_sel[0])
        try:
            self.service.borrow_book(member_id, book_id)
            messagebox.showinfo("Επιτυχία", "Ο δανεισμός καταχωρήθηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return
        self.refresh_all()
        self.loan_button.state(['disabled'])

    # =========================================
    # ΕΠΙΣΤΡΟΦΗ button - go to Rating page; Rating submits the return
    # =========================================
    def go_to_rating(self):
        sel = self.loans_table.selection()
        if not sel:
            return
        loan_id = int(sel[0])
        self.pending_return_loan_id = loan_id
        self.app.change_page("Βαθμολογία")

    # =========================================
    # Reset on navigation
    # =========================================
    def reset(self):
        try:
            self.loans_table.selection_set(())
            self.searchbooks_table.selection_set(())
            self.searchmember_table.selection_set(())
        except Exception:
            pass
        self.searchbar_member_var.set("Αναζήτηση...")
        self.searchbar_book_var.set("Αναζήτηση...")
        self.refresh_all()
        self.loan_button.state(['disabled'])
        self.return_button.state(['disabled'])


# =========================================
# Placeholder helpers (kept module-level so other pages can import them)
# =========================================
def add_placeholder_var(searchbar_var):
    if searchbar_var.get() == "":
        searchbar_var.set("Αναζήτηση...")

def remove_placeholder_var(searchbar_var):
    if searchbar_var.get() == "Αναζήτηση...":
        searchbar_var.set("")
