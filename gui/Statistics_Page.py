# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime,timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator, NullLocator
import mplcursors
import numpy as np


from app.dto import DateRangeDTO

from gui.Styles import *
from gui.Dashboard_Page import autosize_content

TODAY = date.today().isoformat()
DATE_MIN  = "2000-01-01"   # default "from" for Section 5 (all-time)

# =====================================================================
class Statistics(tk.Frame):
    def __init__(self, parent, controller, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.service = service

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        stats_frame = tk.Frame(self,
                               bg=BG_MAIN,
                               padx=30,
                               pady=20
                               )
        stats_frame.grid(row=0, column=0, sticky='nsew')
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(0, weight=0)
        stats_frame.grid_rowconfigure(1, weight=1)

        stats_title = tk.Label(
            stats_frame,
            text="Στατιστικά",
            anchor='w',
            bd=0,
            bg=BG_MAIN,
            fg=FG_MUTED,
            font=FONT_TITLE
        )
        stats_title.grid(row=0, column=0, padx=15, pady=(5, 10), sticky='nsew')

        # Scrollable canvas
        canvas_frame = tk.Frame(stats_frame, bg=BG_MAIN)
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(1, weight=0)

        self.cvs = tk.Canvas(canvas_frame, bg=BG_MAIN, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.cvs.yview)
        self.cvs.configure(yscrollcommand=v_scrollbar.set)
        self.cvs.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.cvs_content_frame = tk.Frame(self.cvs, bg=BG_MAIN)
        self.cvs_content_frame.grid_columnconfigure([0], weight=1)
        for i in range(5):
            self.cvs_content_frame.grid_rowconfigure(i, weight=1)

        win_id = self.cvs.create_window(
            (0, 0), window=self.cvs_content_frame, anchor="nw")

        self.cvs_content_frame.bind(
            "<Configure>",
            lambda e: self.cvs.configure(
                scrollregion=self.cvs.bbox("all")))
        self.cvs.bind(
            "<Configure>",
            lambda e: self.cvs.itemconfig(win_id, width=e.width))

        self.cvs.bind_all(
            "<MouseWheel>",
            self._on_mousewheel)

        self._build_s1()
        self._build_s2()
        self._build_s3()
        self._build_s4()

    # ================================================================
    # Navigation hook
    # ================================================================

    def on_show(self, **kwargs):
        """Called by MainTkWindow.show_frame() — refresh member combos."""
        self._s1_refresh_members("")
        self._s2_refresh_members("")
        self._s3_refresh_members("")

    # ================================================================
    # SECTION 1 — Daily loan summary per member in a time period
    # ================================================================

    def _build_s1(self):
        self._s1_card, self._s1_content = self.card_create(self.cvs_content_frame,
                                        0,"Δανεισμοί ανά Μέλος")

        #Data filter frame
        filter_frame_s1 = tk.Frame(self._s1_content, bg=BG_CARD)
        filter_frame_s1.grid(row=0, column=0, sticky="nsew", pady=(0,10))
        filter_frame_s1.grid_rowconfigure(0, weight=1)
        for i in range (7):
            filter_frame_s1.grid_columnconfigure(i, weight=1 if i==5 else 0)

        #Date filters
        _s1_from_lbl = tk.Label(
                filter_frame_s1,
                text="Από:",
                bg=BG_CARD,
                fg=FG_MUTED,
                font=FONT_MAIN)
        _s1_from_lbl.grid(row=0,column=0,padx=10, pady=10, sticky='nsew')
        self._s1_from = self.date_entry(filter_frame_s1)
        self._s1_from.grid(row=0,column=1, padx=(5, 10))

        _s1_to_lbl = tk.Label(
                filter_frame_s1,
                text="Έως:",
                bg=BG_CARD,
                fg=FG_MUTED,
                font=FONT_MAIN)
        _s1_to_lbl.grid(row=0,column=2,padx=10, pady=10, sticky='nsew')
        self._s1_to = self.date_entry(filter_frame_s1)
        self._s1_to.grid(row=0,column=3, padx=(5, 10))

        _s1_member_lbl = tk.Label(
                filter_frame_s1,
                text="Μέλος:",
                bg=BG_CARD,
                fg=FG_MUTED,
                font=FONT_MAIN)
        _s1_member_lbl.grid(row=0,column=4,padx=10, pady=10, sticky='nsew')
        self._s1_combo = ttk.Combobox(
                filter_frame_s1,
                state="readonly",
                font=FONT_MAIN,
                width=28,
                style="CustomCombobox.TCombobox",
        )
        self._s1_combo.grid(row=0,column=5, padx=10,pady=10,sticky='w')
        self._s1_member_map: dict = {}

        #search btn
        self._s1_search_btn = self.make_btn(parent=filter_frame_s1,text="Αναζήτηση",command=self._run_s1)
        self._s1_search_btn.grid(row=0,column=6,padx=10, pady=10, sticky='nsw')

        self._s1_result = tk.Frame(self._s1_content, bg=BG_CARD)
        self._s1_result.grid(row=1, column=0, sticky="nsew")

    def _s1_refresh_members(self, term=""):
        members = self.service.list_members()
        self._s1_member_map = {
            f"[{m['id']}] {m['full_name']}": m["id"]
            for m in members
        }
        self._s1_combo["values"] = list(self._s1_member_map.keys())
        if self._s1_combo["values"]:
            self._s1_combo.current(0)

    def _run_s1(self):
        self._s1_result.grid()
        d_from = self._s1_from.get().strip()
        d_to   = self._s1_to.get().strip()
        sel    = self._s1_combo.get()

        if not self._valid_range(d_from, d_to):
            return
        if not sel:
            messagebox.showwarning("Επιλογή", "Παρακαλώ επιλέξτε μέλος.")
            return

        member_id = self._s1_member_map.get(sel)

        date_range = DateRangeDTO(date_from=d_from, date_to=d_to)
        self._clear(self._s1_result)

        try:
            rows = self.service.get_daily_loan_summary(member_id, date_range)
        except Exception as ex:
            self._no_data(self._s1_result, str(ex))
            return

        if not rows:
            self._no_data(self._s1_result,
                          "Δεν βρέθηκαν δανεισμοί για την περίοδο.")
            return

        dates  = [r["loan_date"]   for r in rows]
        counts = [r["total_books"] for r in rows]

        dates_dt = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

        #get full date range from entries
        start_date = datetime.strptime(d_from, "%Y-%m-%d")
        end_date = datetime.strptime(d_to, "%Y-%m-%d")

        full_dates=[]
        full_counts=[]

        #row pointer
        row = 0

        d= start_date
        while d<=end_date:
            full_dates.append(d.strftime("%Y-%m-%d"))
            if row<len(dates_dt) and dates_dt[row]==d:
                full_counts.append(counts[row])
                row +=1
            else:
                full_counts.append(0)
            d += timedelta(days=1)

        self._draw_area(self._s1_result, full_dates, full_counts)

    # ================================================================
    # SECTION 2 — Category preferences per member (Donut)
    # ================================================================

    def _build_s2(self):
        self._s2_card, self._s2_content = self.card_create(
            self.cvs_content_frame, row=1,
            title="Δανεισμοί ανά Κατηγορία")

        # Data filter frame
        _s2_filter_frame = tk.Frame(self._s2_content, bg=BG_CARD)
        _s2_filter_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        _s2_filter_frame.grid_rowconfigure(0, weight=1)
        for i in range(7):
            _s2_filter_frame.grid_columnconfigure(i, weight=1 if i == 5 else 0)

        # Date filters
        _s2_from_lbl = tk.Label(
            _s2_filter_frame,
            text="Από:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s2_from_lbl.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._s2_from = self.date_entry(_s2_filter_frame)
        self._s2_from.grid(row=0, column=1, padx=(5, 10))

        _s2_to_lbl = tk.Label(
            _s2_filter_frame,
            text="Έως:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s2_to_lbl.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        self._s2_to = self.date_entry(_s2_filter_frame)
        self._s2_to.grid(row=0, column=3, padx=(5, 10))

        _s2_member_lbl = tk.Label(
            _s2_filter_frame,
            text="Μέλος:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s2_member_lbl.grid(row=0, column=4, padx=10, pady=10, sticky='nsew')
        self._s2_combo = ttk.Combobox(
            _s2_filter_frame,
            state="readonly",
            font=FONT_MAIN,
            width=28,
            style="CustomCombobox.TCombobox",
        )
        self._s2_combo.grid(row=0, column=5, padx=10, pady=10, sticky='w')
        self._s2_member_map: dict = {}

        # search btn
        self._s2_search_btn = self.make_btn(parent=_s2_filter_frame, text="Αναζήτηση", command=self._run_s2)
        self._s2_search_btn.grid(row=0, column=6, padx=10, pady=10, sticky='nsw')

        self._s2_result = tk.Frame(self._s2_content, bg=BG_CARD)
        self._s2_result.grid(row=1, column=0, sticky="nsew")

    def _s2_refresh_members(self, term=""):
        members = self.service.list_members()
        self._s2_member_map = {"Όλα τα μέλη": None}
        for m in members:
            key = f"[{m['id']}] {m['full_name']}"
            self._s2_member_map[key]= m["id"]

        self._s2_combo["values"] = list(self._s2_member_map.keys())
        if self._s2_combo["values"]:
            self._s2_combo.current(0)

    def _run_s2(self):
        self._s2_result.grid()
        d_from = self._s2_from.get().strip()
        d_to   = self._s2_to.get().strip()
        sel    = self._s2_combo.get()

        if not self._valid_range(d_from, d_to):
            return
        if not sel:
            messagebox.showwarning("Επιλογή", "Παρακαλώ επιλέξτε μέλος.")
            return

        member_id = self._s2_member_map.get(sel)

        date_range = DateRangeDTO(date_from=d_from, date_to=d_to)
        self._clear(self._s2_result)

        try:
            if member_id is None:
                rows = self.service.get_all_category_stats(date_range)
            else:
                rows = self.service.get_member_category_stats(member_id, date_range)
        except Exception as ex:
            self._no_data(self._s2_result, str(ex))
            return

        if not rows:
            self._no_data(self._s2_result,
                          "Δεν βρέθηκαν δανεισμοί για το μέλος.")
            return

        self._draw_donut(
            self._s2_result,
            [(r["category"], r["total"]) for r in rows])

    # # ================================================================
    # # SECTION 3 — Full loan history per member (table)
    # # ================================================================

    def _build_s3(self):
        self._s3_card, self._s3_content = self.card_create(
            self.cvs_content_frame, row=2,
            title="Ιστορικό δανεισμών")

        # Data filter frame
        _s3_filter_frame = tk.Frame(self._s3_content, bg=BG_CARD)
        _s3_filter_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        _s3_filter_frame.grid_rowconfigure(0, weight=1)
        for i in range (3):
            _s3_filter_frame.grid_columnconfigure(i, weight=1 if i==1 else 0)

        # Date filters
        _s3_member_lbl = tk.Label(
            _s3_filter_frame,
            text="Μέλος:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s3_member_lbl.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._s3_combo = ttk.Combobox(
            _s3_filter_frame,
            state="readonly",
            font=FONT_MAIN,
            width=28,
            style="CustomCombobox.TCombobox",
        )
        self._s3_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self._s3_member_map: dict = {}

        # search btn
        self._s3_search_btn = self.make_btn(parent=_s3_filter_frame, text="Αναζήτηση", command=self._run_s3)
        self._s3_search_btn.grid(row=0, column=2, padx=10, pady=10, sticky='nsw')

        self._s3_result = tk.Frame(self._s3_content, bg=BG_CARD)
        self._s3_result.grid(row=1, column=0, sticky="nsew")

    def _s3_refresh_members(self, term=""):
        members = self.service.list_members()
        self._s3_member_map = {
            f"[{m['id']}] {m['full_name']}": m["id"]
            for m in members
        }
        self._s3_combo["values"] = list(self._s3_member_map.keys())
        if self._s3_combo["values"]:
            self._s3_combo.current(0)

    def _run_s3(self):
        self._s3_result.grid()
        sel = self._s3_combo.get()
        if not sel:
            messagebox.showwarning("Επιλογή", "Παρακαλώ επιλέξτε μέλος.")
            return

        member_id = self._s3_member_map.get(sel)
        self._clear(self._s3_result)

        try:
            loans = self.service.get_member_loan_history(member_id)
        except Exception as ex:
            self._no_data(self._s3_result, str(ex))
            return

        if not loans:
            self._no_data(self._s3_result, "Δεν υπάρχουν δανεισμοί.")
            return

        columns = ["Τίτλος", "Συγγραφέας",
                 "Κατηγορία", "Ημ/νία Δανεισμού",
                 "Λήξη Δανεισμού", "Ημ/νία Επιστροφής"
                 ]
        frame = self._make_tree(self._s3_result, columns)
        frame.grid(row=0,column=0, sticky="nsew")
        self._s3_result.grid_rowconfigure(2, weight=1)
        self._s3_result.grid_columnconfigure(0, weight=1)

        tree = frame.winfo_children()[0]

        for ln in loans:
            ret  = ln.get("return_date") or ""
            due  = ln.get("due_date", "")

            tree.insert("", "end",
                        values=(
                            ln.get("book_title", ""),
                            ln.get("book_author", ""),
                            ln.get("category", ""),    # ← DAL returns "category"
                            ln.get("loan_date", ""),
                            due,
                            ret or "N/A"
                        ))
        tree.grid(row=0,column=0, sticky="nsew")

        autosize_content(tree)

    # ================================================================
    # SECTION 5 — Loans per filter (author / age / gender)
    # ================================================================

    def _build_s4(self):
        self._s4_card, self._s4_content = self.card_create(
            self.cvs_content_frame,
            3, "Δανεισμοί ανά Φίλτρο")

        # Data filter frame
        _s4_filter_frame = tk.Frame(self._s4_content, bg=BG_CARD)
        _s4_filter_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        _s4_filter_frame.grid_rowconfigure(0, weight=1)
        for i in range(7):
            _s4_filter_frame.grid_columnconfigure(i, weight=1 if i == 5 else 0)

        # Date filters
        _s4_from_lbl = tk.Label(
            _s4_filter_frame,
            text="Από:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s4_from_lbl.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self._s4_from = self.date_entry(_s4_filter_frame)
        self._s4_from.grid(row=0, column=1, padx=(5, 10))

        _s4_to_lbl = tk.Label(
            _s4_filter_frame,
            text="Έως:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s4_to_lbl.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        self._s4_to = self.date_entry(_s4_filter_frame)
        self._s4_to.grid(row=0, column=3, padx=(5, 10))

        _s4_member_lbl = tk.Label(
            _s4_filter_frame,
            text="Μέλος:",
            bg=BG_CARD,
            fg=FG_MUTED,
            font=FONT_MAIN)
        _s4_member_lbl.grid(row=0, column=4, padx=10, pady=10, sticky='nsew')
        self._s4_combo = ttk.Combobox(
            _s4_filter_frame,
            state="readonly",
            font=FONT_MAIN,
            width=28,
            values=["Συγγραφέας", "Ηλικία", "Φύλο"],
            style="CustomCombobox.TCombobox",
        )
        self._s4_combo.grid(row=0, column=5, padx=10, pady=10, sticky='w')

        # search btn
        self._s4_search_btn = self.make_btn(parent=_s4_filter_frame, text="Αναζήτηση", command=self._run_s4)
        self._s4_search_btn.grid(row=0, column=6, padx=10, pady=10, sticky='nsw')

        self._s4_result = tk.Frame(self._s4_content, bg=BG_CARD)
        self._s4_result.grid(row=1, column=0, sticky="nsew")


    def _run_s4(self):
        self._s4_result.grid()
        d_from = self._s4_from.get().strip()
        d_to   = self._s4_to.get().strip()
        flt = self._s4_combo.get()
        if not self._valid_range(d_from, d_to):
            return
        if not flt:
            messagebox.showwarning("Επιλογή", "Παρακαλώ επιλέξτε φίλτρο.")
            return

        date_range = DateRangeDTO(date_from=d_from, date_to=d_to)
        self._clear(self._s4_result)

        try:
            if flt == "Συγγραφέας":
                rows  = self.service.get_loans_per_author(date_range)
                title = "Πλήθος δανεισμών ανά Συγγραφέα"
                pairs = [(r["author"], r["total"]) for r in rows]
            elif flt == "Ηλικία":
                rows  = self.service.get_loans_per_age_group(date_range)
                title = "Πλήθος δανεισμών ανά Ηλικιακή Ομάδα"
                pairs = [(r["age_group"], r["total"]) for r in rows]
            else:
                rows  = self.service.get_loans_per_gender(date_range)
                title = "Πλήθος δανεισμών ανά Φύλο"
                pairs = [(r["gender"], r["total"]) for r in rows]
        except Exception as ex:
            self._no_data(self._s4_result, str(ex))
            return

        if not pairs:
            self._no_data(self._s4_result, "Δεν βρέθηκαν δεδομένα.")
            return

        self._draw_bar_h(self._s4_result, pairs, title)

    # ================================================================
    # Matplotlib helpers
    # ================================================================

    def _draw_area(self, parent, x_labels, y_values):
        """Straight-line filled area chart (light theme)."""
        x_pos = list(range(len(x_labels)))
        fig, ax = plt.subplots(figsize=(8, 3),facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)

        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.left.set_linewidth(0.5)
        ax.spines.bottom.set_linewidth(0.5)
        ax.spines.bottom.set_color(BG_DARK)
        ax.spines.left.set_color(BG_DARK)

        ax.plot(x_pos, y_values,
                color=CHART_COLORS[0], linewidth=2,
                linestyle="-")
        ax.fill_between(x_pos, y_values, alpha=0.20,
                        color=ACCENT)
        points = ax.scatter(
            x_pos, y_values,
            color=CHART_COLORS[0],
            s=1,  # μέγεθος marker
        )

        rotation = 45 if len(x_labels) > 6 else 0
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels, rotation=rotation,
                           ha="right" if rotation else "center",
                           fontsize=8, color=MPL_TEXT)
        if len(x_labels) > 30:
            ax.xaxis.set_major_locator(MultipleLocator(30))
            ax.xaxis.set_minor_locator(MultipleLocator(1) if len(x_labels) <90 else NullLocator())

        #annotate x labels on hover over markers
        cursor = mplcursors.cursor(points, hover=2)
        @cursor.connect("add")
        def on_add(sel):
            idx = int(sel.index)
            sel.annotation.set_text(x_labels[idx])
            sel.annotation.get_bbox_patch().set(fc=BG_MAIN, alpha=0.5)

        ax.tick_params(axis="y", colors=MPL_TEXT, labelsize=10)
        ax.yaxis.set_ticks(np.arange(0,max(y_values)+5,1))

        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0,right=x_pos[-1])
        ax.yaxis.label.set_visible(False)
        ax.xaxis.label.set_visible(False)

        ax.yaxis.grid(True, color=MPL_GRID,
                      linestyle="-", linewidth=0.5, alpha=0.7)

        fig.tight_layout(pad=1)
        self._embed(parent, fig)


    def _draw_bar_h(self, parent, rows, title):
        """Horizontal bar chart (light theme)."""
        labels = [str(r[0])[:30] for r in rows]
        values = [r[1] for r in rows]
        n      = len(rows)
        height = max(2.2, n * 0.46)

        fig, ax = plt.subplots(figsize=(8, height), facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)

        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.left.set_linewidth(0.5)
        ax.spines.bottom.set_linewidth(0.5)
        ax.spines.bottom.set_color(BG_DARK)
        ax.spines.left.set_color(BG_DARK)

        colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(n)]
        ax.barh(labels[::-1], values[::-1],
                         color=colors[::-1], height=0.6)

        ax.yaxis.label.set_visible(False)
        ax.xaxis.label.set_visible(False)

        ax.tick_params(colors=MPL_TEXT, labelsize=9)
        ax.xaxis.set_ticks(np.arange(0, max(values) + 2, 1))
        ax.xaxis.grid(True, color=MPL_GRID,
                      linestyle="-", linewidth=0.5, alpha=0.7)

        ax.set_title(title, fontsize=11, color=MPL_TEXT,
                     fontweight="bold", loc='center', pad=10)
        fig.tight_layout(pad=1.4)
        self._embed(parent, fig)
        
    def _draw_donut(self, parent, rows):
        """Donut chart (light theme)."""
        labels = [str(r[0]) for r in rows]
        values = [r[1]      for r in rows]
        n      = len(rows)
        colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(n)]

        fig, ax = plt.subplots(figsize=(8,4), facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)

        wedges, texts, autotexts = ax.pie(
            values,
            radius=1.5,
            labels=None,
            colors=colors,
            autopct=lambda pct: f"{pct:.1f}%" if pct > 8 else "",
            pctdistance=0.75,
            startangle=90,
            counterclock=False,
            wedgeprops={"width": 0.7,          # donut hole width
                        "edgecolor": MPL_BG,
                        "linewidth": 2},
            )

        for at in autotexts:
            at.set_fontsize(10)
            at.set_color(MPL_BG)
            at.set_fontweight("bold")


        # Centre label — total loans
        total = sum(values)
        ax.text(0, 0.1, str(total),
                ha="center", va="center",
                fontsize=18, fontweight="bold", color=MPL_TEXT)
        ax.text(0, -0.1, "δανεισμοί",
                ha="center", va="center",
                fontsize=12, color=FG_MUTED)

        # Legend on the right
        legend=ax.legend(
            wedges, [f"{l} ({val/total*100:.1f}%)" for l,val in zip(labels,values)],
            loc="center left",
            bbox_to_anchor=(1.2, 0.5),
            fontsize=10,
            labelcolor=MPL_TEXT,
        )

        self._embed(parent, fig)

    def _embed(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        widget = (canvas.get_tk_widget())
        widget.configure(bg=MPL_BG)
        widget.pack(fill="both", expand=True)
        plt.close(fig)

    # ================================================================
    # Widget factories
    # ================================================================

    # Stat Card function
    def card_create(self, parent, row, title):
        container = tk.Frame(
            parent,
            bd=0,
            bg=BG_CARD,
            padx=10,
            pady=10
        )
        container.grid(row=row, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # title button(toggle)
        title_lbl = tk.Label(
            container,
            anchor="center",
            bg=BG_CARD,
            fg=FG_MUTED,
            bd=0,
            font=FONT_SUBHEADER_BOLD,
            text=title,
            cursor="hand2"
        )
        title_lbl.grid(row=0, column=0, sticky='w', padx=15, pady=10)

        # frame for content
        content_frame = tk.Frame(container, bg=BG_CARD)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_remove()

        # toggle behavior
        title_lbl.bind("<Button-1>", lambda e: self.toggle_chart(content_frame))

        return container, content_frame

    def date_entry(self,parent,default=None):
        e = ttk.Entry(
            parent,
            font=FONT_MAIN,
            width=10,
            style="CustomEntry.TEntry",
            exportselection=False
            )
        e.insert(0, default if default is not None else TODAY)
        return e

    def _make_tree(self, parent, columns):
        container = tk.Frame(parent, bg=BG_CARD)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)

        tree = ttk.Treeview(container, columns=columns, show="headings",
                            selectmode="none",style="Custom.Treeview",
                            height=6)
        tree.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 5))

        for col in columns:
            tree.heading(col, text=col,anchor="w")
            tree.column(
                col,
                anchor="w",
                width=120,
                minwidth=120,
                stretch=True,
                )

        v_sb = ttk.Scrollbar(container, orient="vertical",
                             command=tree.yview,style="Vertical.TScrollbar")
        tree.configure(yscrollcommand=v_sb.set)
        v_sb.grid(row=0, column=1, sticky="ns")

        h_sb = ttk.Scrollbar(
            container,
            orient='horizontal',
            command=tree.xview,
            style="Horizontal.TScrollbar"
        )
        h_sb.set(0.2, 0.5)
        h_sb.grid(row=1, column=0, columnspan=2, sticky='we', padx=(15, 0))
        tree.config(xscrollcommand=h_sb.set)

        return container

    def make_btn(self,parent, text, command):
        btn = ttk.Button(
                parent,
                text=text,
                command=command,
                width=18,
                style="CustomButton.TButton",
                cursor='hand2'
                )
        return btn

    # ================================================================
    # Utility helpers
    # ================================================================

    @staticmethod
    def _clear(frame):
        for w in frame.winfo_children():
            w.destroy()

    def _no_data(self, frame, msg="Δεν βρέθηκαν δεδομένα."):
        tk.Label(frame, text=msg, bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(pady=16)

    @staticmethod
    def _valid_range(d_from, d_to):
        fmt = "%Y-%m-%d"
        try:
            if datetime.strptime(d_from, fmt) > datetime.strptime(d_to, fmt):
                messagebox.showwarning(
                    "Εύρος ημερομηνιών",
                    "Η ημερομηνία 'Από' δεν μπορεί να είναι "
                    "μεταγενέστερη της 'Έως'.")
                return False
            return True
        except ValueError:
            messagebox.showwarning(
                "Μορφή ημερομηνίας",
                "Χρησιμοποιήστε τη μορφή ΕΕΕΕ-ΜΜ-ΗΗ (π.χ. 2026-01-01).")
            return False

    def toggle_chart(self, frame):
        if frame.winfo_ismapped():
            frame.grid_remove()
        else:
            frame.grid()

    def reset_section(self,combo,from_entry,to_entry,result,content):
        getattr(self,combo).set("")
        if from_entry:
            getattr(self, from_entry).delete(0, "end")
            getattr(self, from_entry).insert(0, TODAY)

        if to_entry:
            getattr(self, to_entry).delete(0, "end")
            getattr(self, to_entry).insert(0, TODAY)

        self._clear(getattr(self, result))
        getattr(self, result).grid_remove()
        if hasattr(self, "toggle_chart") and getattr(self, content).winfo_ismapped():
            self.toggle_chart(getattr(self, content))

    def _on_mousewheel(self, e):
        start, end = self.cvs.yview()

        #if there is no scrollable area
        if start == 0.0 and end == 1.0:
            return

        self.cvs.yview_scroll(-1 * (e.delta // 120), "units")

    #clear changes
    def reset(self):
        """Called when the page becomes visible. Refresh member combos
        so newly added/removed members appear in the dropdowns."""
        try:
            self.on_show()
        except Exception:
            pass
        sections = [
            ("_s1_combo", "_s1_from", "_s1_to", "_s1_result", "_s1_content"),
            ("_s2_combo", "_s2_from", "_s2_to", "_s2_result", "_s2_content"),
            ("_s3_combo", None, None, "_s3_result", "_s3_content"),
            ("_s4_combo", "_s4_from", "_s4_to", "_s4_result", "_s4_content"),
        ]

        for args in sections:
            self.reset_section(*args)
