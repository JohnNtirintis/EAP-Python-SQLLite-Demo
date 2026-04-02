import tkinter as tk
from tkinter import ttk, messagebox


class StatisticsView(ttk.Frame):
    """
    Statistics tab — DTO compatible.
    Displays:
    - Start date
    - End date
    - Member ID (optional)
    - Buttons for each statistic
    - Output area
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # SECTION: Filters
        # ---------------------------------------------------------
        filter_frame = ttk.LabelFrame(self, text="Filters")
        filter_frame.pack(fill="x", padx=10, pady=10)

        # Start date
        ttk.Label(filter_frame, text="Start date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.entry_start = ttk.Entry(filter_frame, width=20)
        self.entry_start.grid(row=0, column=1, sticky="w")
        self.entry_start.insert(0, "2026-01-01")

        # End date
        ttk.Label(filter_frame, text="End date (YYYY-MM-DD):").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_end = ttk.Entry(filter_frame, width=20)
        self.entry_end.grid(row=0, column=3, sticky="w")
        self.entry_end.insert(0, "2026-12-31")

        # Member ID
        ttk.Label(filter_frame, text="Member ID (for member-specific stats):").grid(
            row=1, column=0, sticky="e", padx=5, pady=3
        )
        self.entry_member_id = ttk.Entry(filter_frame, width=20)
        self.entry_member_id.grid(row=1, column=1, sticky="w")

        # ---------------------------------------------------------
        # SECTION: Buttons
        # ---------------------------------------------------------
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Borrow count/member", command=self.stat_borrow_count).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Category/member", command=self.stat_category_member).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Category/global", command=self.stat_category_global).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="History/member", command=self.stat_history_member).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="By author", command=self.stat_by_author).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="By age", command=self.stat_by_age).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="By gender", command=self.stat_by_gender).pack(side="left", padx=5)

        # ---------------------------------------------------------
        # SECTION: Output
        # ---------------------------------------------------------
        output_frame = ttk.LabelFrame(self, text="Results")
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_output = tk.Text(output_frame, height=20, wrap="none")
        self.text_output.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _get_dates(self):
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        return start, end

    def _get_member_id(self):
        text = self.entry_member_id.get().strip()
        return int(text) if text else None

    def _show(self, title, data):
        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", f"{title}\n")
        self.text_output.insert("end", "-" * 40 + "\n\n")

        if isinstance(data, list):
            for row in data:
                self.text_output.insert("end", f"{row}\n")
        else:
            self.text_output.insert("end", str(data))

    # ---------------------------------------------------------
    # Statistics actions
    # ---------------------------------------------------------
    def stat_borrow_count(self):
        start, end = self._get_dates()
        data = self.logic.stats_borrow_count_per_member(start, end)
        self._show("Borrow count per member", data)

    def stat_category_member(self):
        start, end = self._get_dates()
        member_id = self._get_member_id()
        if not member_id:
            messagebox.showerror("Error", "Member ID required.")
            return
        data = self.logic.stats_category_per_member(member_id, start, end)
        self._show("Category stats for member", data)

    def stat_category_global(self):
        start, end = self._get_dates()
        data = self.logic.stats_category_global(start, end)
        self._show("Category stats (global)", data)

    def stat_history_member(self):
        start, end = self._get_dates()
        member_id = self._get_member_id()
        if not member_id:
            messagebox.showerror("Error", "Member ID required.")
            return
        data = self.logic.stats_history_member(member_id, start, end)
        self._show("Borrowing history for member", data)

    def stat_by_author(self):
        start, end = self._get_dates()
        data = self.logic.stats_by_author(start, end)
        self._show("Borrow count by author", data)

    def stat_by_age(self):
        start, end = self._get_dates()
        data = self.logic.stats_by_age(start, end)
        self._show("Borrow count by age group", data)

    def stat_by_gender(self):
        start, end = self._get_dates()
        data = self.logic.stats_by_gender(start, end)
        self._show("Borrow count by gender", data)
