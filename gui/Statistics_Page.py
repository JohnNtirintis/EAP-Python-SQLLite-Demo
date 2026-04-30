# gui/Statistics_Page.py
# Statistics page 
#
# ALL database access goes through self.service (LibraryBusinessLogic).
# No sqlite3 imports, no direct SQL, no placeholders.
#
# Sections:
#   1. Πλήθος βιβλίων ανά μέλος σε χρονική περίοδο  (area chart)
#   2. Κατανομή προτιμήσεων δανεισμού ανά μέλος      (horizontal bar)
#   3. Κατανομή προτιμήσεων όλων μελών ανά κατηγορία (horizontal bar)
#   4. Ιστορικό δανεισμού ανά μέλος                  (table)
#   5. Πλήθος δανεισμών ανά φίλτρο                   (author/age/gender bar)

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.dto import DateRangeDTO

from gui.styles import (
    BG_MAIN, BG_CARD, BG_DARK, BG_DARKER,
    ACCENT, FG_LIGHT, FG_DARK, FG_MUTED,
    FONT_MAIN, FONT_BOLD, FONT_SMALL,
)

# ── Tokens not present in styles.py — defined locally ────────────────
FONT_TITLE = ("Segoe UI", 16, "bold")   # styles.py has (18,) without bold
FONT_SEC   = ("Segoe UI", 13, "bold")   # section card headers

# ── Chart palette & matplotlib surfaces ──────────────────────────────
CHART_COLORS = [
    "#01696f", "#00D5E4", "#da7101", "#437a22",
    "#006494", "#7a39bb", "#a12c7b", "#a13544",
    "#d19900", "#0c4e54", "#2e5c10", "#275f8e",
]
MPL_BG   = "#EAEAEA"
MPL_GRID = "#C8C8C8"
MPL_TEXT = "#1E1E1E"

TODAY = date.today().isoformat()
DATE_MIN  = "2000-01-01"   # default "from" for Section 5 (all-time)


# =====================================================================
class Statistics(tk.Frame):
    """Statistics page with 5 scrollable sections."""

    def __init__(self, parent, controller, service):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.service    = service

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()

    # ================================================================
    # Navigation hook
    # ================================================================

    def on_show(self, **kwargs):
        """Called by MainTkWindow.show_frame() — refresh member combos."""
        self._s1_refresh_members("")
        self._s2_refresh_members("")
        self._s4_refresh_members("")

    # ================================================================
    # UI skeleton
    # ================================================================

    def _build_ui(self):
        outer = tk.Frame(self, bg=BG_MAIN, padx=28, pady=20)
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(1, weight=1)

        tk.Label(outer, text="Στατιστικά",
                 bg=BG_MAIN, fg=FG_DARK, font=FONT_TITLE,
                 anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 14))

        # Scrollable canvas
        host = tk.Frame(outer, bg=BG_MAIN)
        host.grid(row=1, column=0, sticky="nsew")
        host.grid_rowconfigure(0, weight=1)
        host.grid_columnconfigure(0, weight=1)

        self._cvs = tk.Canvas(host, bg=BG_MAIN, highlightthickness=0)
        vsb = ttk.Scrollbar(host, orient="vertical", command=self._cvs.yview)
        self._cvs.configure(yscrollcommand=vsb.set)
        self._cvs.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.content = tk.Frame(self._cvs, bg=BG_MAIN)
        self.content.grid_columnconfigure(0, weight=1)

        win_id = self._cvs.create_window(
            (0, 0), window=self.content, anchor="nw")

        self.content.bind(
            "<Configure>",
            lambda e: self._cvs.configure(
                scrollregion=self._cvs.bbox("all")))
        self._cvs.bind(
            "<Configure>",
            lambda e: self._cvs.itemconfig(win_id, width=e.width))
        self._cvs.bind_all(
            "<MouseWheel>",
            lambda e: self._cvs.yview_scroll(
                -1 * (e.delta // 120), "units"))

        self._build_s1()
        self._build_s2()
        self._build_s3()
        self._build_s4()
        self._build_s5()

    # ================================================================
    # SECTION 1 — Daily loan summary per member in a time period
    # ================================================================

    def _build_s1(self):
        card = self._make_card(
            self.content, row=0,
            title="1.  Πλήθος βιβλίων ανά μέλος σε χρονική περίοδο",
            accent=CHART_COLORS[0])

        row1 = tk.Frame(card, bg=BG_CARD)
        row1.pack(fill="x", pady=(0, 8))
        tk.Label(row1, text="Από:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s1_from = self._date_entry(row1)
        self._s1_from.pack(side="left", padx=(4, 16))
        tk.Label(row1, text="Έως:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s1_to = self._date_entry(row1)
        self._s1_to.pack(side="left", padx=(4, 0))

        row2 = tk.Frame(card, bg=BG_CARD)
        row2.pack(fill="x", pady=(0, 10))
        tk.Label(row2, text="Μέλος:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s1_sv = tk.StringVar()
        se = tk.Entry(row2, textvariable=self._s1_sv,
                      font=FONT_MAIN, relief="flat", bd=2,
                      bg="#FFFFFF", fg=FG_DARK,
                      insertbackground=FG_DARK, width=20)
        se.pack(side="left", padx=(4, 6), ipady=4)
        se.bind("<KeyRelease>",
                lambda e: self._s1_refresh_members(
                    self._s1_sv.get().strip()))

        self._s1_combo = ttk.Combobox(
            row2, state="readonly", font=FONT_MAIN, width=28)
        self._s1_combo.pack(side="left", padx=(0, 16), ipady=3)
        self._s1_member_map: dict = {}

        self._make_btn(row2, "🔍  Αναζήτηση", self._run_s1,
                       bg=ACCENT, fg=FG_DARK).pack(side="left")

        self._s1_result = tk.Frame(card, bg=BG_CARD)
        self._s1_result.pack(fill="x")

    def _s1_refresh_members(self, term=""):
        members = (self.service.search_members(term) if term
                   else self.service.list_members())
        self._s1_member_map = {
            f"[{m['id']}] {m['full_name']}": m["id"]
            for m in members
        }
        self._s1_combo["values"] = list(self._s1_member_map.keys())
        if self._s1_combo["values"]:
            self._s1_combo.current(0)

    def _run_s1(self):
        d_from = self._s1_from.get().strip()
        d_to   = self._s1_to.get().strip()
        sel    = self._s1_combo.get()

        if not self._valid_range(d_from, d_to):
            return
        if not sel:
            messagebox.showwarning("Επιλογή", "Παρακαλώ επιλέξτε μέλος.")
            return

        member_id  = self._s1_member_map[sel]
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

        # Table
        cols  = ("loan_date", "book_count", "titles")
        heads = [("Ημερομηνία", 110),
                 ("Πλήθος Βιβλίων", 130),
                 ("Τίτλοι", 500)]
        frame = self._make_tree(self._s1_result, cols, heads,
                                height=min(len(rows), 7))
        tree = frame.winfo_children()[0]
        for r in rows:
            tree.insert("", "end",
                        values=(r["loan_date"],
                                r["total_books"],
                                r["titles"]))
        frame.pack(fill="x", pady=(6, 10))

        # Area chart
        dates  = [r["loan_date"]   for r in rows]
        counts = [r["total_books"] for r in rows]
        self._draw_area(self._s1_result, dates, counts,
                        title=f"Δανεισμοί ανά ημέρα — {sel}",
                        ylabel="Βιβλία")

    # ================================================================
    # SECTION 2 — Category preferences per member (bar chart)
    # ================================================================

    def _build_s2(self):
        card = self._make_card(
            self.content, row=1,
            title="2.  Κατανομή προτιμήσεων δανεισμού ανά μέλος",
            accent=CHART_COLORS[2])

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text="Από:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s2_from = self._date_entry(top)
        self._s2_from.pack(side="left", padx=(4, 16))
        tk.Label(top, text="Έως:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s2_to = self._date_entry(top)
        self._s2_to.pack(side="left", padx=(4, 20))
        tk.Label(top, text="Μέλος:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s2_sv = tk.StringVar()
        se = tk.Entry(top, textvariable=self._s2_sv,
                      font=FONT_MAIN, relief="flat", bd=2,
                      bg="#FFFFFF", fg=FG_DARK,
                      insertbackground=FG_DARK, width=20)
        se.pack(side="left", padx=(4, 6), ipady=4)
        se.bind("<KeyRelease>",
                lambda e: self._s2_refresh_members(
                    self._s2_sv.get().strip()))
        self._s2_combo = ttk.Combobox(
            top, state="readonly", font=FONT_MAIN, width=28)
        self._s2_combo.pack(side="left", padx=(0, 16), ipady=3)
        self._s2_member_map: dict = {}
        self._make_btn(top, "📊  Γράφημα", self._run_s2,
                       bg=CHART_COLORS[2], fg="#FFFFFF").pack(side="left")

        self._s2_result = tk.Frame(card, bg=BG_CARD)
        self._s2_result.pack(fill="x")

    def _s2_refresh_members(self, term=""):
        members = (self.service.search_members(term) if term
                   else self.service.list_members())
        self._s2_member_map = {
            f"[{m['id']}] {m['full_name']}": m["id"]
            for m in members
        }
        self._s2_combo["values"] = list(self._s2_member_map.keys())
        if self._s2_combo["values"]:
            self._s2_combo.current(0)

    def _run_s2(self):
        d_from = self._s2_from.get().strip()
        d_to   = self._s2_to.get().strip()
        sel    = self._s2_combo.get()
        if not self._valid_range(d_from, d_to):
            return
        if not sel:
            messagebox.showwarning("Επιλογή", "Παρακαλώ επιλέξτε μέλος.")
            return

        member_id  = self._s2_member_map[sel]
        date_range = DateRangeDTO(date_from=d_from, date_to=d_to)
        self._clear(self._s2_result)

        try:
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
            [(r["category"], r["total"]) for r in rows],
            f"Κατηγορίες δανεισμού — {sel}")

    # ================================================================
    # SECTION 3 — Category distribution all members (bar chart)
    # ================================================================

    def _build_s3(self):
        card = self._make_card(
            self.content, row=2,
            title="3.  Κατανομή προτιμήσεων όλων μελών ανά κατηγορία",
            accent=CHART_COLORS[3])

        dr = tk.Frame(card, bg=BG_CARD)
        dr.pack(fill="x", pady=(0, 10))
        tk.Label(dr, text="Από:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s3_from = self._date_entry(dr)
        self._s3_from.pack(side="left", padx=(4, 16))
        tk.Label(dr, text="Έως:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s3_to = self._date_entry(dr)
        self._s3_to.pack(side="left", padx=(4, 16))
        self._make_btn(dr, "📊  Γράφημα", self._run_s3,
                       bg=CHART_COLORS[3], fg="#FFFFFF").pack(side="left")

        self._s3_result = tk.Frame(card, bg=BG_CARD)
        self._s3_result.pack(fill="x")

    def _run_s3(self):
        d_from = self._s3_from.get().strip()
        d_to   = self._s3_to.get().strip()
        if not self._valid_range(d_from, d_to):
            return

        date_range = DateRangeDTO(date_from=d_from, date_to=d_to)
        self._clear(self._s3_result)

        try:
            rows = self.service.get_all_category_stats(date_range)
        except Exception as ex:
            self._no_data(self._s3_result, str(ex))
            return

        if not rows:
            self._no_data(self._s3_result, "Δεν βρέθηκαν δεδομένα.")
            return

        self._draw_bar_h(
            self._s3_result,
            [(r["category"], r["total"]) for r in rows],
            "Συνολικοί δανεισμοί ανά κατηγορία")

    # ================================================================
    # SECTION 4 — Full loan history per member (table)
    # ================================================================

    def _build_s4(self):
        card = self._make_card(
            self.content, row=3,
            title="4.  Ιστορικό δανεισμού ανά μέλος",
            accent=CHART_COLORS[4])

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text="Αναζήτηση μέλους:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s4_sv = tk.StringVar()
        se4 = tk.Entry(top, textvariable=self._s4_sv,
                       font=FONT_MAIN, relief="flat", bd=2,
                       bg="#FFFFFF", fg=FG_DARK,
                       insertbackground=FG_DARK, width=22)
        se4.pack(side="left", padx=(6, 6), ipady=4)
        se4.bind("<KeyRelease>",
                 lambda e: self._s4_refresh_members(
                     self._s4_sv.get().strip()))
        self._s4_combo = ttk.Combobox(
            top, state="readonly", font=FONT_MAIN, width=30)
        self._s4_combo.pack(side="left", padx=(0, 14), ipady=3)
        self._s4_member_map: dict = {}
        self._make_btn(top, "📋  Εμφάνιση Ιστορικού", self._run_s4,
                       bg=BG_DARK, fg=FG_LIGHT).pack(side="left")

        self._s4_result = tk.Frame(card, bg=BG_CARD)
        self._s4_result.pack(fill="x")

    def _s4_refresh_members(self, term=""):
        members = (self.service.search_members(term) if term
                   else self.service.list_members())
        self._s4_member_map = {
            f"[{m['id']}] {m['full_name']}": m["id"]
            for m in members
        }
        self._s4_combo["values"] = list(self._s4_member_map.keys())
        if self._s4_combo["values"]:
            self._s4_combo.current(0)

    def _run_s4(self):
        sel = self._s4_combo.get()
        if not sel:
            return
        member_id = self._s4_member_map[sel]
        self._clear(self._s4_result)

        # Member profile card
        try:
            m = self.service.get_member(member_id)
        except Exception:
            m = None

        if m:
            prof = tk.Frame(self._s4_result, bg=BG_CARD, padx=14, pady=8)
            prof.pack(fill="x", pady=(0, 8))
            fields = [
                ("ID",              m.get("id", "")),
                ("Ονοματεπώνυμο",   m.get("full_name", "")),
                ("Αρ. Μητρώου",     m.get("registration_number", "")),
                ("Email",           m.get("email", "")),
                ("Τηλέφωνο",        m.get("phone", "")),
                ("Ηλικία",          m.get("age", "")),
                ("Επάγγελμα",       m.get("profession", "")),
                ("Εγγραφή",         str(m.get("created_at", ""))[:10]),
            ]
            for i, (lbl, val) in enumerate(fields):
                tk.Label(prof, text=f"{lbl}:", bg=BG_CARD,
                         fg=FG_MUTED, font=FONT_SMALL,
                         width=14, anchor="e").grid(
                    row=i // 4, column=(i % 4) * 2,
                    sticky="e", padx=(8, 2), pady=2)
                tk.Label(prof, text=str(val or "—"), bg=BG_CARD,
                         fg=FG_DARK, font=FONT_SMALL,
                         anchor="w").grid(
                    row=i // 4, column=(i % 4) * 2 + 1,
                    sticky="w", padx=(0, 16), pady=2)

        # Loan history table — uses get_member_loan_history()
        # Columns returned: id, book_title, book_author, category,
        #                   loan_date, due_date, return_date, status
        try:
            loans = self.service.get_member_loan_history(member_id)
        except Exception as ex:
            self._no_data(self._s4_result, str(ex))
            return

        if not loans:
            self._no_data(self._s4_result, "Δεν υπάρχουν δανεισμοί.")
            return

        cols  = ("book_title", "book_author", "category",
                 "loan_date", "due_date", "return_date", "status")
        heads = [("Τίτλος", 200), ("Συγγραφέας", 150),
                 ("Κατηγορία", 120), ("Δανεισμός", 100),
                 ("Λήξη", 90), ("Επιστροφή", 110),
                 ("Κατάσταση", 100)]
        frame = self._make_tree(self._s4_result, cols, heads,
                                height=min(len(loans), 10))
        tree = frame.winfo_children()[0]
        tree.tag_configure("active",   background="#FFF9E6",
                           foreground="#6B4F00")
        tree.tag_configure("returned", background="#EAF4EA")
        tree.tag_configure("overdue",  background="#FDECEA")

        today = date.today().isoformat()
        for ln in loans:
            ret  = ln.get("return_date") or ""
            due  = ln.get("due_date", "")
            stat = ln.get("status", "")
            tag  = ("returned" if stat == "returned"
                    else "overdue"
                    if due and due < today and stat != "returned"
                    else "active")
            tree.insert("", "end", tags=(tag,),
                        values=(
                            ln.get("book_title", ""),
                            ln.get("book_author", ""),
                            ln.get("category", ""),    # ← DAL returns "category"
                            ln.get("loan_date", ""),
                            due,
                            ret or "⏳ Ενεργός",
                            stat,
                        ))
        frame.pack(fill="x", pady=(4, 0))

    # ================================================================
    # SECTION 5 — Loans per filter (author / age / gender)
    # ================================================================

    def _build_s5(self):
        card = self._make_card(
            self.content, row=4,
            title="5.  Πλήθος δανεισμών ανά φίλτρο",
            accent=CHART_COLORS[5])

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x", pady=(0, 10))

        # Date range (required by all three DAL methods)
        tk.Label(top, text="Από:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s5_from = self._date_entry(top, default=DATE_MIN)
        self._s5_from.pack(side="left", padx=(4, 16))
        tk.Label(top, text="Έως:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s5_to = self._date_entry(top)
        self._s5_to.pack(side="left", padx=(4, 20))

        tk.Label(top, text="Εμφάνιση κατά:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN).pack(side="left")
        self._s5_filter = tk.StringVar(value="Συγγραφέας")
        ttk.Combobox(top, textvariable=self._s5_filter,
                     values=["Συγγραφέας", "Ηλικία", "Φύλο"],
                     state="readonly", font=FONT_MAIN,
                     width=16).pack(side="left", padx=(6, 16), ipady=3)
        self._make_btn(top, "📊  Γράφημα", self._run_s5,
                       bg=CHART_COLORS[5], fg="#FFFFFF").pack(side="left")

        self._s5_result = tk.Frame(card, bg=BG_CARD)
        self._s5_result.pack(fill="x", pady=(0, 10))

    def _run_s5(self):
        d_from = self._s5_from.get().strip()
        d_to   = self._s5_to.get().strip()
        if not self._valid_range(d_from, d_to):
            return

        date_range = DateRangeDTO(date_from=d_from, date_to=d_to)
        flt        = self._s5_filter.get()
        self._clear(self._s5_result)

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
            self._no_data(self._s5_result, str(ex))
            return

        if not pairs:
            self._no_data(self._s5_result, "Δεν βρέθηκαν δεδομένα.")
            return

        self._draw_bar_h(self._s5_result, pairs, title)

    # ================================================================
    # Matplotlib helpers
    # ================================================================

    def _draw_area(self, parent, x_labels, y_values, title, ylabel=""):
        """Straight-line filled area chart (light theme)."""
        x_pos = list(range(len(x_labels)))
        fig, ax = plt.subplots(figsize=(8, 3), facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)
        for sp in ax.spines.values():
            sp.set_visible(False)

        ax.plot(x_pos, y_values,
                color=CHART_COLORS[0], linewidth=2,
                marker="o", markersize=5,
                markerfacecolor=CHART_COLORS[0], linestyle="-")
        ax.fill_between(x_pos, y_values, alpha=0.20,
                        color=CHART_COLORS[0])

        rotation = 45 if len(x_labels) > 6 else 0
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels, rotation=rotation,
                           ha="right" if rotation else "center",
                           fontsize=8, color=MPL_TEXT)
        ax.tick_params(axis="y", colors=MPL_TEXT, labelsize=8)
        ax.set_ylabel(ylabel, fontsize=9, color=FG_MUTED)
        ax.yaxis.grid(True, color=MPL_GRID,
                      linestyle="--", linewidth=0.5, alpha=0.7)
        for xi, yi in zip(x_pos, y_values):
            ax.text(xi, yi + 0.05, str(yi),
                    ha="center", va="bottom",
                    fontsize=8, color=MPL_TEXT, fontweight="bold")
        ax.set_title(title, fontsize=11, color=MPL_TEXT,
                     fontweight="bold", pad=10)
        fig.tight_layout(pad=1.4)
        self._embed(parent, fig)

    def _draw_bar_h(self, parent, rows, title):
        """Horizontal bar chart (light theme)."""
        labels = [str(r[0])[:30] for r in rows]
        values = [r[1] for r in rows]
        n      = len(rows)
        height = max(2.2, n * 0.46)

        fig, ax = plt.subplots(figsize=(8, height), facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)
        for sp in ax.spines.values():
            sp.set_visible(False)

        colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(n)]
        bars   = ax.barh(labels[::-1], values[::-1],
                         color=colors[::-1], height=0.6)

        ax.set_xlabel("Δανεισμοί", fontsize=9, color=FG_MUTED)
        ax.tick_params(colors=MPL_TEXT, labelsize=9)
        ax.xaxis.grid(True, color=MPL_GRID,
                      linestyle="--", linewidth=0.5, alpha=0.7)
        for bar, val in zip(bars, values[::-1]):
            ax.text(bar.get_width() + 0.05,
                    bar.get_y() + bar.get_height() / 2,
                    str(val), va="center", ha="left",
                    fontsize=9, color=MPL_TEXT, fontweight="bold")
        ax.set_title(title, fontsize=11, color=MPL_TEXT,
                     fontweight="bold", pad=10)
        fig.tight_layout(pad=1.4)
        self._embed(parent, fig)
        
    def _draw_donut(self, parent, rows, title):
        """Donut chart (light theme)."""
        labels = [str(r[0]) for r in rows]
        values = [r[1]      for r in rows]
        n      = len(rows)
        colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(n)]

        fig, ax = plt.subplots(figsize=(7, 4), facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)

        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            colors=colors,
            autopct=lambda pct: f"{pct:.1f}%" if pct > 4 else "",
            pctdistance=0.78,
            startangle=90,
            wedgeprops={"width": 0.52,          # donut hole width
                        "edgecolor": MPL_BG,
                        "linewidth": 2},
        )

        for at in autotexts:
            at.set_fontsize(8)
            at.set_color(MPL_BG)
            at.set_fontweight("bold")

        # Centre label — total loans
        total = sum(values)
        ax.text(0, 0.08, str(total),
                ha="center", va="center",
                fontsize=18, fontweight="bold", color=MPL_TEXT)
        ax.text(0, -0.22, "δανεισμοί",
                ha="center", va="center",
                fontsize=8, color=FG_MUTED)

        # Legend on the right
        ax.legend(
            wedges, [f"{l}  ({v})" for l, v in zip(labels, values)],
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=9,
            frameon=False,
            labelcolor=MPL_TEXT,
        )

        ax.set_title(title, fontsize=11, color=MPL_TEXT,
                     fontweight="bold", pad=14)
        fig.tight_layout(pad=1.4)
        self._embed(parent, fig)

    def _embed(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", pady=(6, 0))
        plt.close(fig)

    # ================================================================
    # Widget factories
    # ================================================================

    def _make_card(self, parent, row, title, accent=ACCENT):
        outer = tk.Frame(parent, bg=BG_MAIN)
        outer.grid(row=row, column=0, sticky="ew", pady=(0, 18))
        outer.grid_columnconfigure(1, weight=1)

        # Coloured left accent bar
        tk.Frame(outer, bg=accent, width=5).grid(
            row=0, column=0, rowspan=2, sticky="ns")

        hdr = tk.Frame(outer, bg=BG_DARK, padx=14, pady=10)
        hdr.grid(row=0, column=1, sticky="ew")
        tk.Label(hdr, text=title, bg=BG_DARK, fg=FG_LIGHT,
                 font=FONT_SEC, anchor="w").pack(fill="x")

        body = tk.Frame(outer, bg=BG_CARD, padx=16, pady=14)
        body.grid(row=1, column=1, sticky="ew")
        body.grid_columnconfigure(0, weight=1)
        return body

    def _date_entry(self, parent, default=None):
        e = tk.Entry(parent, font=FONT_MAIN, relief="flat", bd=2,
                     bg="#FFFFFF", fg=FG_DARK,
                     insertbackground=FG_DARK, width=11)
        e.insert(0, default if default is not None else TODAY)
        return e

    def _make_tree(self, parent, cols, heads, height=6):
        sname = f"S{abs(id(parent)) % 99999}.Treeview"
        sty   = ttk.Style()
        sty.configure(sname,
                      background=BG_CARD, fieldbackground=BG_CARD,
                      foreground=FG_DARK, font=FONT_SMALL,
                      rowheight=28, borderwidth=0)
        sty.configure(f"{sname}.Heading",
                      background=BG_DARK, foreground=FG_LIGHT,
                      font=FONT_BOLD, relief="flat")
        sty.map(sname,
                background=[("selected", BG_DARKER)],
                foreground=[("selected", ACCENT)])

        frame = tk.Frame(parent, bg=BG_CARD)
        frame.grid_columnconfigure(0, weight=1)

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                             style=sname, height=height)
        for col, (h, w) in zip(cols, heads):
            tree.heading(col, text=h)
            tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(frame, orient="v", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.grid(row=0, column=0, sticky="ew")
        sb.grid(row=0, column=1, sticky="ns")
        return frame

    @staticmethod
    def _make_btn(parent, text, command, bg=BG_DARK, fg=FG_LIGHT):
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg,
                        activebackground=BG_DARKER,
                        activeforeground=ACCENT,
                        relief="flat", font=("Segoe UI", 11),
                        padx=14, pady=5,
                        cursor="hand2",
                        bd=0, highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=BG_DARKER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
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
