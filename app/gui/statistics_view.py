import tkinter as tk
from tkinter import ttk, messagebox


class StatisticsView(ttk.Frame):
    """
    Statistics tab — δείχνει διάφορα στατιστικά δανεισμών.
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # PERIOD FILTER
        # ---------------------------------------------------------
        period_frame = ttk.LabelFrame(self, text="Period filter (YYYY-MM-DD)")
        period_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(period_frame, text="Start date:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.entry_start = ttk.Entry(period_frame, width=12)
        self.entry_start.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        ttk.Label(period_frame, text="End date:").grid(row=0, column=2, padx=5, pady=3, sticky="e")
        self.entry_end = ttk.Entry(period_frame, width=12)
        self.entry_end.grid(row=0, column=3, padx=5, pady=3, sticky="w")

        # ---------------------------------------------------------
        # MEMBER SELECTION
        # ---------------------------------------------------------
        member_frame = ttk.LabelFrame(self, text="Member")
        member_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(member_frame, text="Member:").grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.entry_member = ttk.Combobox(
            member_frame,
            values=[f"{m.id} - {m.full_name}" for m in self.logic.list_members()],
            width=40,
            state="readonly"
        )
        self.entry_member.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        ttk.Button(
            member_frame,
            text="Loans count in period",
            command=self.show_member_loans_in_period
        ).grid(row=0, column=2, padx=5, pady=3)

        ttk.Button(
            member_frame,
            text="Member category distribution",
            command=self.show_member_category_distribution
        ).grid(row=0, column=3, padx=5, pady=3)

        ttk.Button(
            member_frame,
            text="Member loan history",
            command=self.show_member_loan_history
        ).grid(row=0, column=4, padx=5, pady=3)

        # ---------------------------------------------------------
        # GLOBAL STATS BUTTONS
        # ---------------------------------------------------------
        global_frame = ttk.LabelFrame(self, text="Global statistics")
        global_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            global_frame,
            text="Category distribution (all members)",
            command=self.show_global_category_distribution
        ).grid(row=0, column=0, padx=5, pady=3)

        ttk.Button(
            global_frame,
            text="Loans per author",
            command=self.show_loans_per_author
        ).grid(row=0, column=1, padx=5, pady=3)

        ttk.Button(
            global_frame,
            text="Loans per age",
            command=self.show_loans_per_age
        ).grid(row=0, column=2, padx=5, pady=3)

        ttk.Button(
            global_frame,
            text="Loans per gender",
            command=self.show_loans_per_gender
        ).grid(row=0, column=3, padx=5, pady=3)

        # ---------------------------------------------------------
        # RESULTS TABLE
        # ---------------------------------------------------------
        table_frame = ttk.LabelFrame(self, text="Results")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("c1", "c2", "c3"), show="headings", height=18)
        self.tree.heading("c1", text="Column 1")
        self.tree.heading("c2", text="Column 2")
        self.tree.heading("c3", text="Column 3")

        self.tree.column("c1", width=250)
        self.tree.column("c2", width=150)
        self.tree.column("c3", width=150)

        self.tree.pack(fill="both", expand=True)

        self.refresh_members()

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _get_period(self):
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        if not start or not end:
            raise ValueError("Please enter both start and end date (YYYY-MM-DD).")
        return start, end

    def _get_selected_member_id(self):
        text = self.entry_member.get().strip()
        if not text:
            raise ValueError("Please select a member.")
        return int(text.split(" - ")[0])

    def _set_table(self, headers, rows):
        self.tree.delete(*self.tree.get_children())
        # adjust headings
        for i, h in enumerate(headers, start=1):
            col = f"c{i}"
            self.tree.heading(col, text=h)
        # clear unused headings
        for i in range(len(headers) + 1, 4):
            col = f"c{i-1}"
            self.tree.heading(col, text="")
        # insert rows
        for r in rows:
            self.tree.insert("", "end", values=r)

    def refresh_members(self):
        self.entry_member["values"] = [f"{m.id} - {m.full_name}" for m in self.logic.list_members()]

    # ---------------------------------------------------------
    # MEMBER STATS
    # ---------------------------------------------------------
    def show_member_loans_in_period(self):
        try:
            member_id = self._get_selected_member_id()
            start, end = self._get_period()
            total = self.logic.count_loans_by_member_in_period(member_id, start, end)
            self._set_table(
                ["Member ID", "Period", "Loans count"],
                [(member_id, f"{start} → {end}", total)]
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_member_category_distribution(self):
        try:
            member_id = self._get_selected_member_id()
            start, end = self._get_period()
            data = self.logic.member_category_distribution_in_period(member_id, start, end)
            rows = [(member_id, category, total) for category, total in data]
            self._set_table(
                ["Member ID", "Category", "Loans"],
                rows
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_member_loan_history(self):
        try:
            member_id = self._get_selected_member_id()
            data = self.logic.member_loan_history(member_id)
            rows = [(title, loan_date, return_date or "") for title, loan_date, return_date in data]
            self._set_table(
                ["Title", "Loan date", "Return date"],
                rows
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # GLOBAL STATS
    # ---------------------------------------------------------
    def show_global_category_distribution(self):
        try:
            start, end = self._get_period()
            data = self.logic.category_distribution_in_period(start, end)
            rows = [(category, total, "") for category, total in data]
            self._set_table(
                ["Category", "Loans", ""],
                rows
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_loans_per_author(self):
        try:
            data = self.logic.loans_per_author()
            rows = [(author, total, "") for author, total in data]
            self._set_table(
                ["Author", "Loans", ""],
                rows
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_loans_per_age(self):
        try:
            data = self.logic.loans_per_age()
            rows = [(age, total, "") for age, total in data]
            self._set_table(
                ["Age", "Loans", ""],
                rows
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_loans_per_gender(self):
        try:
            data = self.logic.loans_per_gender()
            rows = [(gender, total, "") for gender, total in data]
            self._set_table(
                ["Gender", "Loans", ""],
                rows
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
