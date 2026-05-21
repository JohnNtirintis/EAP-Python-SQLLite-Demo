# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date, timedelta
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from gui.Styles import *


class Dashboard(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        #make Dashboard expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.dashboardData_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.dashboardData_frame.grid(row=0, column=0, sticky='nsew')

        self.dashboardData_frame.grid_columnconfigure(0, weight=1)
        self.dashboardData_frame.grid_columnconfigure(1, weight=1)
        self.dashboardData_frame.grid_columnconfigure(2, weight=1)
        self.dashboardData_frame.grid_rowconfigure(0, weight=0)
        self.dashboardData_frame.grid_rowconfigure(1, weight=1, minsize=200)
        self.dashboardData_frame.grid_rowconfigure(2, weight=1, minsize=200)

        #images
        self.books_icon = tk.PhotoImage(file='gui/Assets/books_icon.png')
        self.loaned_books_icon = tk.PhotoImage(file='gui/Assets/loaned_books_icon.png')
        self.members_icon = tk.PhotoImage(file='gui/Assets/members_icon.png')

        # KPI cards - placeholders, populated by refresh_kpis()
        self._kpi_value_labels = []  # tk.Label x 3, updated each refresh
        kpi_info = [
            {"icon": self.books_icon,        "label": "Συνολικά Βιβλία"},
            {"icon": self.members_icon,      "label": "Συνολικά Μέλη"},
            {"icon": self.loaned_books_icon, "label": "Δανεισμένα Βιβλία"},
        ]
        for col, item in enumerate(kpi_info):
            self.create_dashboard_card(col, item)

        # Figure (loans-per-day for the last 7 days)
        self._figure_container = None
        self.create_figure_container()

        # Overdue table
        self.create_overdue_table()

        # Populate everything from the service on first show.
        self.refresh_all()

    # =========================================
    # Dashboard KPI card
    # =========================================
    def create_dashboard_card(self, col, data):
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg=BG_CARD
                    )
        container.grid(row=0, column=col, padx=15, pady=(5, 10), sticky='nsew')

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)

        data_icon = tk.Label(
                    container,
                    anchor="w",
                    image=data["icon"],
                    bg=BG_CARD
                    )
        data_icon.grid(rowspan=2, column=0, sticky='w', padx=(20, 5))

        data_lbl = tk.Label(
                    container,
                    anchor="ne",
                    text=data["label"],
                    bd=0,
                    bg=BG_CARD,
                    fg=FG_MUTED,
                    font=FONT_SUBHEADER
                    )
        data_lbl.grid(row=0, column=1, sticky='e', padx=(0, 20), pady=(10, 0))

        value_lbl = tk.Label(
                    container,
                    anchor="ne",
                    text="—",
                    bd=0,
                    bg=BG_CARD,
                    fg=FG_DARK,
                    font=("Segoe UI", 20)
                    )
        value_lbl.grid(row=1, column=1, sticky='e', padx=(0, 20), pady=(0, 10))
        self._kpi_value_labels.append(value_lbl)

    # =========================================
    # Overdue Table
    # =========================================
    def create_overdue_table(self):
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg=BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=3, padx=15, pady=(10, 0), sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        table_title = tk.Label(
                        container,
                        anchor="center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font=FONT_TITLE,
                        text="Οφειλές"
                        )
        table_title.grid(row=0, column=0, sticky='w', padx=(15, 0), pady=10)

        self.return_btn = ttk.Button(
                        container,
                        text="ΕΠΙΣΤΡΟΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.go_to_return,
                        )
        self.return_btn.grid(row=0, column=1, sticky='e', padx=(0, 15), pady=10)
        self.return_btn.state(['disabled'])

        # No ISBN column here — we don't fetch books in the loans query.
        columns = ("ID", "Μέλος", "Βιβλίο", "Καθυστέρηση", "Ημ/νία Επιστροφής")
        self.overdue_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.overdue_table.grid(row=1, column=0, columnspan=2, sticky='nsew',
                                padx=(15,), pady=(0, 5))
        self.overdue_table.bind("<<TreeviewSelect>>", lambda e: self.selection_btn())

        v_scrollbar = ttk.Scrollbar(
                        container,
                        orient='vertical',
                        command=self.overdue_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=1, column=3, sticky='ns')
        self.overdue_table.config(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(
                        container,
                        orient='horizontal',
                        command=self.overdue_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2, 0.5)
        h_scrollbar.grid(row=2, column=0, columnspan=2, sticky='we', padx=(15, 0))
        self.overdue_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.overdue_table.heading(col, text=col, anchor='w')
            self.overdue_table.column(
                col,
                anchor="w",
                width=120 if col != "ID" else 80,
                minwidth=120 if col != "ID" else 80,
                stretch=True if col != "ID" else False,
                )

    # =========================================
    # Figure container (created once, redrawn on refresh)
    # =========================================
    def create_figure_container(self):
        self._figure_container = tk.Frame(
                    self.dashboardData_frame,
                    bg=BG_CARD
                    )
        self._figure_container.grid(row=1, columnspan=3, padx=15, pady=10, sticky='nsew')
        self._figure_container.grid_propagate(False)

    def _draw_figure(self, dates, counts):
        # Clear any existing chart
        for w in self._figure_container.winfo_children():
            w.destroy()

        dataframe = pd.DataFrame({'dates': dates, 'y': counts})

        figure = plt.Figure(figsize=(5, 1), dpi=100, frameon=False)
        figure_plot = figure.add_subplot(1, 1, 1)

        figure_plot.spines.right.set_visible(False)
        figure_plot.spines.top.set_visible(False)
        figure_plot.spines.left.set_linewidth(0.5)
        figure_plot.spines.bottom.set_linewidth(0.5)
        figure_plot.spines.bottom.set_color(BG_DARK)
        figure_plot.spines.left.set_color(BG_DARK)
        figure_plot.tick_params('both', colors=BG_DARK)

        figure_plot.xaxis.label.set_visible(False)
        figure_plot.yaxis.label.set_visible(False)

        figure_plot.axes.grid(axis='y', color=MPL_GRID, linewidth=0.5)
        figure.subplots_adjust(top=0.75, bottom=0.15, left=0.08, right=0.95)

        figure_plot.set_title(
            'Δανεισμοί (τελευταίες 7 ημέρες)',
            x=-0.06, y=1.1,
            fontdict={
                'fontsize': 18,
                'color': MPL_TEXT,
                'verticalalignment': 'center',
                'horizontalalignment': 'left',
            },
            loc='left',
            pad=10,
        )
        figure_plot.set_facecolor(MPL_BG)

        line_graph = FigureCanvasTkAgg(figure, self._figure_container)
        widget = line_graph.get_tk_widget()
        widget.configure(bg=MPL_BG)
        widget.pack(fill='both', expand=True)

        dataframe.plot(
            x='dates', y='y',
            kind='line', legend=False,
            ax=figure_plot, linewidth=2, linestyle='-',
            color=ACCENT
        )

    # =========================================
    # Refresh everything from the service
    # =========================================
    def refresh_all(self):
        # KPI counts
        if self.service:
            try:
                books = self.service.list_books() or []
                members = self.service.list_members() or []
                loans = self.service.list_loans() or []
            except Exception:
                books, members, loans = [], [], []
        else:
            books, members, loans = [], [], []

        total_books = sum(int(getattr(b, "total_copies", 0)) for b in books)
        total_members = len(members)
        borrowed_count = sum(1 for l in loans if getattr(l, "status", None) == "borrowed")

        for lbl, value in zip(self._kpi_value_labels,
                              [total_books, total_members, borrowed_count]):
            lbl.config(text=str(value))

        # Chart: loans per day for the last 7 days
        today = date.today()
        date_range = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # oldest -> newest
        date_strs = [d.strftime("%m-%d") for d in date_range]
        loans_per_day = Counter()
        for l in loans:
            ld = getattr(l, "loan_date", None)
            if not ld:
                continue
            try:
                # loan_date is stored as ISO YYYY-MM-DD
                ld_date = datetime.strptime(ld, "%Y-%m-%d").date()
            except ValueError:
                continue
            if ld_date in date_range:
                loans_per_day[ld_date] += 1
        counts = [loans_per_day.get(d, 0) for d in date_range]
        try:
            self._draw_figure(date_strs, counts)
        except Exception:
            # Best-effort: do not crash the dashboard if matplotlib hiccups
            pass

        # Overdue table
        self._populate_overdue(loans, today)

    def _populate_overdue(self, loans, today):
        self.overdue_table.delete(*self.overdue_table.get_children())
        for l in loans:
            if getattr(l, "status", None) != "borrowed":
                continue
            due = getattr(l, "due_date", None)
            if not due:
                continue
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
            except ValueError:
                continue
            if due_date >= today:
                continue
            delta = (today - due_date).days
            self.overdue_table.insert(
                "", "end", iid=str(l.id),
                values=(
                    f"{l.id:04d}",
                    getattr(l, "member_name", "") or "",
                    getattr(l, "book_title", "") or "",
                    f"{delta} ημέρες",
                    due,
                ),
            )
        autosize_content(self.overdue_table)

    # =========================================
    # ΕΠΙΣΤΡΟΦΗ from overdue table - route through Loans page
    # =========================================
    def go_to_return(self):
        selected = self.overdue_table.selection()
        if not selected:
            return
        try:
            loan_id = int(selected[0])
        except (ValueError, TypeError):
            return
        # Tell the Loans page to pre-select this loan, then jump to Rating directly
        # (Same flow as the Loans page's ΕΠΙΣΤΡΟΦΗ button.)
        from gui.Loans_Page import Loans
        loans_page = self.app.pages.get(Loans)
        if loans_page is not None:
            loans_page.pending_return_loan_id = loan_id
        self.app.change_page("Βαθμολογία")

    # =========================================
    # Table selection -> button state
    # =========================================
    def selection_btn(self):
        if not self.overdue_table.selection():
            self.return_btn.state(['disabled'])
        else:
            self.return_btn.state(['!disabled'])

    # =========================================
    # Reset on page change
    # =========================================
    def reset(self):
        try:
            self.overdue_table.selection_set(())
        except Exception:
            pass
        self.return_btn.state(['disabled'])
        # Refresh data so KPIs reflect any changes elsewhere.
        self.refresh_all()


# =========================================
# Helper: autosize tree columns to content. Kept module-level so other
# pages can `from gui.Dashboard_Page import autosize_content`.
# =========================================
def autosize_content(treeview):
    tree_font = tk.font.Font(font=FONT_BOLD)

    for col in treeview["columns"]:
        max_width = tree_font.measure(col) + 30

        for item in treeview.get_children():
            cell_text = treeview.set(item, col)
            cell_width = tree_font.measure(str(cell_text)) + 30
            if cell_width > max_width:
                max_width = cell_width

        treeview.column(col, width=max_width, minwidth=max_width)
