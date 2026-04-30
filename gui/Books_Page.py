# gui/Books_Page.py
# Σελίδα Καταλόγου Βιβλίων 
# Views (full-page swap, grid_remove/grid):
#   _catalog_frame  → default
#   _edit_panel     → BookEditPanel
#   _cat_panel      → CategoriesPanel

import tkinter as tk
from tkinter import ttk, messagebox

from datetime import date, datetime
from gui.Categories_Page import CategoriesPanel
from gui.Book_Edit_Page  import BookEditPanel

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.dto import DateRangeDTO

from gui.styles import (
    BG_MAIN, BG_CARD, BG_FILTER, BG_DARK, BG_DARKER,
    ACCENT, FG_LIGHT, FG_DARK, FG_MUTED,
    FONT_MAIN, FONT_BOLD, FONT_TITLE, FONT_SEC, FONT_SMALL,
    FONT_TREE, FONT_THEAD, FONT_CRUMB,
    CHART_COLORS, MPL_BG, MPL_GRID, MPL_TEXT,
)

# ── Colour & font tokens ──────────────────────────────────────────────
FONT_FILT  = ("Segoe UI", 11)
FILTER_W   = 190   # fixed width of left filter panel

# ── Treeview column definitions ───────────────────────────────────────
BOOK_COLS  = ("id", "title", "author", "year", "isbn",
              "category", "copies", "rating")
BOOK_HEADS = [
    ("id",       "ID",            46),
    ("title",    "Τίτλος",       210),
    ("author",   "Συγγραφέας",   160),
    ("year",     "Έτος έκδοσης",  95),
    ("isbn",     "ISBN",          130),
    ("category", "Κατηγορία",    120),
    ("copies",   "Απόθεμα",       90),
    ("rating",   "Βαθμολογία",    85),
]

SORT_OPTIONS = ["Αύξουσα σειρά", "Φθίνουσα σειρά"]


class Books(tk.Frame):
    """
    Κύρια σελίδα καταλόγου βιβλίων — full-page swap.

    _catalog_frame : πίνακας με φίλτρα (default)
    _edit_panel    : BookEditPanel
    _cat_panel     : CategoriesPanel
    """

    def __init__(self, parent, controller, service):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        self.service    = service

        self._cat_vars: dict[str, tk.BooleanVar] = {}
        self._sort_var = tk.StringVar(value=SORT_OPTIONS[0])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_ui()
        self.refresh()

    # ──────────────────────────────────────────────────────────────────
    # Top-level view skeleton
    # ──────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # View 0: κατάλογος
        self._catalog_frame = tk.Frame(self, bg=BG_MAIN)
        self._catalog_frame.grid(row=0, column=0, sticky="nsew")
        self._catalog_frame.grid_rowconfigure(0, weight=1)
        self._catalog_frame.grid_columnconfigure(0, weight=1)
        self._build_catalog(self._catalog_frame)

        # View 1: BookEditPanel
        self._edit_panel = BookEditPanel(
            self, service=self.service,
            on_save=self._on_panel_save,
            on_back=self._show_catalog,
        )
        self._edit_panel.grid(row=0, column=0, sticky="nsew")
        self._edit_panel.grid_remove()

        # View 2: CategoriesPanel
        self._cat_panel = CategoriesPanel(
            self, service=self.service,
            on_change=self._on_panel_save,
            on_back=self._show_catalog,
        )
        self._cat_panel.grid(row=0, column=0, sticky="nsew")
        self._cat_panel.grid_remove()

    # ──────────────────────────────────────────────────────────────────
    # Catalog view
    # ──────────────────────────────────────────────────────────────────

    def _build_catalog(self, parent):
        outer = tk.Frame(parent, bg=BG_MAIN, padx=24, pady=20)
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_rowconfigure(2, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        # ── Row 0: Τίτλος + κουμπιά ───────────────────────────────────
        top = tk.Frame(outer, bg=BG_MAIN)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        top.grid_columnconfigure(0, weight=1)

        tk.Label(top, text="Κατάλογος Βιβλίων",
                 bg=BG_MAIN, fg=FG_DARK, font=FONT_TITLE,
                 anchor="w").grid(row=0, column=0, sticky="w")

        btn_box = tk.Frame(top, bg=BG_MAIN)
        btn_box.grid(row=0, column=1, sticky="e")

        self._make_btn(btn_box,
                       "ΠΡΟΣΘΗΚΗ ΚΑΤΗΓΟΡΙΑΣ",
                       self._open_categories,
                       bg=ACCENT, fg=FG_DARK).pack(side="left", padx=(0, 8))
        self._make_btn(btn_box,
                       "ΠΡΟΣΘΗΚΗ / ΕΝΗΜΕΡΩΣΗ ΒΙΒΛΙΟΥ",
                       lambda: self._open_book_edit(None),
                       bg=ACCENT, fg=FG_DARK).pack(side="left")

        # ── Row 1: Search bar ─────────────────────────────────────────
        search_wrap = tk.Frame(outer, bg="#FFFFFF",
                               highlightthickness=1,
                               highlightbackground="#BBBBBB",
                               highlightcolor=ACCENT)
        search_wrap.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        search_wrap.grid_columnconfigure(1, weight=1)

        tk.Label(search_wrap, text="🔍", bg="#FFFFFF",
                 fg=FG_MUTED, font=("Segoe UI", 13)).grid(
            row=0, column=0, padx=(10, 4), pady=4)

        self._sv = tk.StringVar()
        tk.Entry(search_wrap, textvariable=self._sv,
                 font=FONT_MAIN, relief="flat", bd=0,
                 bg="#FFFFFF", fg=FG_DARK,
                 insertbackground=FG_DARK).grid(
            row=0, column=1, sticky="ew",
            ipady=7, padx=(0, 10), pady=4)
        self._sv.trace_add("write", lambda *_: self._apply_filters())

        # ── Row 2: Filter panel + Treeview ────────────────────────────
        body = tk.Frame(outer, bg=BG_MAIN)
        body.grid(row=2, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        # Left filter panel
        self._filter_panel = tk.Frame(body, bg=BG_FILTER, width=FILTER_W)
        self._filter_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._filter_panel.grid_propagate(False)
        self._filter_panel.grid_columnconfigure(0, weight=1)
        self._build_filter_panel(self._filter_panel)

        # Right treeview
        tree_card = tk.Frame(body, bg=BG_CARD)
        tree_card.grid(row=0, column=1, sticky="nsew")
        tree_card.grid_rowconfigure(0, weight=1)
        tree_card.grid_columnconfigure(0, weight=1)
        self._build_treeview(tree_card)

    # ── Filter panel ──────────────────────────────────────────────────

    def _build_filter_panel(self, parent):
        pad = tk.Frame(parent, bg=BG_FILTER, padx=14, pady=14)
        pad.pack(fill="both", expand=True)
        pad.grid_columnconfigure(0, weight=1)

        tk.Label(pad, text="Φίλτρα Αναζήτησης",
                 bg=BG_FILTER, fg=FG_DARK,
                 font=("Segoe UI", 11, "bold"),
                 anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 14))

#        # ── Ταξινόμηση ────────────────────────────────────────────────
#       tk.Label(pad, text="Ταξινόμηση κατά",
#                bg=BG_FILTER, fg=FG_MUTED, font=FONT_SMALL,
#                anchor="w").grid(row=1, column=0, sticky="w", pady=(0, 4))
#       sort_cb = ttk.Combobox(pad, textvariable=self._sort_var,
#                              values=SORT_OPTIONS,
#                              state="readonly", font=FONT_SMALL, width=18)
#       sort_cb.grid(row=2, column=0, sticky="ew", ipady=3, pady=(0, 16))
#       sort_cb.bind("<<ComboboxSelected>>", lambda _: self._apply_filters())

        # ── Κατηγορία ─────────────────────────────────────────────────
        cat_hdr = tk.Frame(pad, bg=BG_FILTER)
        cat_hdr.grid(row=3, column=0, sticky="ew", pady=(0, 6))
        cat_hdr.grid_columnconfigure(0, weight=1)

        tk.Label(cat_hdr, text="Κατηγορία",
                 bg=BG_FILTER, fg=FG_DARK,
                 font=("Segoe UI", 11, "bold"),
                 anchor="w").grid(row=0, column=0, sticky="w")

        self._cat_expanded = True
        self._cat_arrow = tk.Label(cat_hdr, text="∧",
                                    bg=BG_FILTER, fg=FG_DARK,
                                    font=FONT_SMALL, cursor="hand2")
        self._cat_arrow.grid(row=0, column=1, sticky="e")
        self._cat_arrow.bind("<Button-1>", self._toggle_cat_section)

        self._cat_cb_frame = tk.Frame(pad, bg=BG_FILTER)
        self._cat_cb_frame.grid(row=4, column=0, sticky="ew")
        self._refresh_category_checkboxes()

    def _refresh_category_checkboxes(self):
        """Ξαναχτίζει τα checkboxes κατηγοριών από το service."""
        for w in self._cat_cb_frame.winfo_children():
            w.destroy()

        cats = self.service.list_categories()
        old  = {k: v.get() for k, v in self._cat_vars.items()}
        self._cat_vars = {}

        for c in cats:
            name = c["name"]
            var  = tk.BooleanVar(value=old.get(name, False))
            self._cat_vars[name] = var
            tk.Checkbutton(
                self._cat_cb_frame, text=name,
                variable=var,
                bg=BG_FILTER, fg=FG_DARK,
                activebackground=BG_FILTER,
                selectcolor="#FFFFFF",
                font=FONT_SMALL, anchor="w",
                command=self._apply_filters
            ).pack(fill="x", pady=1)

    def _toggle_cat_section(self, _=None):
        if self._cat_expanded:
            self._cat_cb_frame.grid_remove()
            self._cat_arrow.config(text="∨")
        else:
            self._cat_cb_frame.grid()
            self._cat_arrow.config(text="∧")
        self._cat_expanded = not self._cat_expanded

    # ── Treeview ──────────────────────────────────────────────────────

    def _build_treeview(self, parent):
        sty = ttk.Style()
        sty.theme_use("clam")
        sty.configure("Books.Treeview",
                       background=BG_CARD,
                       fieldbackground=BG_CARD,
                       foreground=FG_DARK,
                       font=FONT_TREE,
                       rowheight=34,
                       borderwidth=0)
        sty.configure("Books.Treeview.Heading",
                       background=BG_DARK,
                       foreground=FG_LIGHT,
                       font=FONT_THEAD,
                       relief="flat",
                       borderwidth=0,
                       padding=(6, 6))
        sty.map("Books.Treeview",
                background=[("selected", BG_DARKER)],
                foreground=[("selected", ACCENT)])
        sty.map("Books.Treeview.Heading",
                background=[("active", BG_DARKER)])

        self.tree = ttk.Treeview(parent, columns=BOOK_COLS,
                                  show="headings",
                                  style="Books.Treeview",
                                  selectmode="browse")
        for col, head, width in BOOK_HEADS:
            self.tree.heading(col, text=head)
            self.tree.column(col, width=width, minwidth=width, anchor="w")

        sb = ttk.Scrollbar(parent, orient="v", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self.tree.tag_configure("odd",     background="#F0F0F0", foreground=FG_DARK)
        self.tree.tag_configure("even",    background=BG_CARD,   foreground=FG_DARK)
        self.tree.tag_configure("unavail", foreground="#9E9E9E")

        self.tree.bind("<Double-1>", lambda e: self._edit_selected())

        ctx = tk.Menu(self, tearoff=0, bg=BG_DARK, fg=FG_LIGHT,
                      activebackground=BG_DARKER, activeforeground=ACCENT,
                      font=FONT_SMALL)
        ctx.add_command(label="Επεξεργασία", command=self._edit_selected)
        ctx.add_command(label="Διαγραφή",    command=self._delete_selected)
        self.tree.bind("<Button-3>", lambda e: (
            self.tree.selection_set(self.tree.identify_row(e.y)),
            ctx.post(e.x_root, e.y_root)
        ))

    # ──────────────────────────────────────────────────────────────────
    # View switching
    # ──────────────────────────────────────────────────────────────────

    def _show_catalog(self):
        self._edit_panel.grid_remove()
        self._cat_panel.grid_remove()
        self._catalog_frame.grid()

    def _open_categories(self):
        self._catalog_frame.grid_remove()
        self._edit_panel.grid_remove()
        self._cat_panel.refresh()
        self._cat_panel.grid()

    def _open_book_edit(self, book: dict | None):
        self._catalog_frame.grid_remove()
        self._cat_panel.grid_remove()
        self._edit_panel.load_book(book)
        self._edit_panel.grid()

    def _on_panel_save(self):
        self._refresh_category_checkboxes()
        self.refresh()
        self._edit_panel.refresh_categories()

    # ──────────────────────────────────────────────────────────────────
    # Treeview actions
    # ──────────────────────────────────────────────────────────────────

    def _edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        book = self.service.get_book(int(sel[0]))
        if book:
            self._open_book_edit(book)

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        if messagebox.askyesno("Διαγραφή",
                               "Να διαγραφεί το επιλεγμένο βιβλίο;"):
            try:
                self.service.delete_book(int(sel[0]))
                self.refresh()
            except Exception as ex:
                messagebox.showerror("Σφάλμα", str(ex))

    # ──────────────────────────────────────────────────────────────────
    # Data & filtering
    # ──────────────────────────────────────────────────────────────────

    def _populate(self, books):
        self.tree.delete(*self.tree.get_children())

        rev   = self._sort_var.get() == SORT_OPTIONS[1]
        books = sorted(books,
                       key=lambda b: (b.get("title") or "").lower(),
                       reverse=rev)

        for i, b in enumerate(books):
            avail      = int(b.get("available_copies", 0))
            total      = int(b.get("total_copies", 0))
            copies_str = f"{avail}/{total} τμχ"
            rat        = b.get("avg_rating") or b.get("rating")
            rat_str    = f"{rat}/5" if rat else "—"

            tags = ("odd" if i % 2 else "even",)
            if avail == 0:
                tags = tags + ("unavail",)

            self.tree.insert("", "end", iid=str(b["id"]), tags=tags,
                             values=(
                                 f"{b['id']:04d}",
                                 b.get("title", ""),
                                 b.get("author", ""),
                                 b.get("published_year", ""),
                                 b.get("isbn", ""),
                                 b.get("category_name", ""),
                                 copies_str,
                                 rat_str,
                             ))

    def _apply_filters(self, *_):
        kw = self._sv.get().strip()
        try:
            books = (self.service.search_books(kw) if kw
                     else self.service.list_books())
        except Exception:
            books = []

        active_cats = {n for n, v in self._cat_vars.items() if v.get()}
        if active_cats:
            books = [b for b in books
                     if b.get("category_name") in active_cats]

        self._populate(books)

    def on_show(self, **kwargs):
        self._show_catalog()
        self._refresh_category_checkboxes()
        self.refresh()

    def refresh(self):
        self._apply_filters()

    # ──────────────────────────────────────────────────────────────────
    # Widget factory
    # ──────────────────────────────────────────────────────────────────

    @staticmethod
    def _make_btn(parent, text, command, bg=BG_DARK, fg=FG_LIGHT):
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg,
                        activebackground=BG_DARKER,
                        activeforeground=ACCENT,
                        relief="flat",
                        font=("Segoe UI", 11, "bold"),
                        padx=16, pady=8,
                        cursor="hand2", bd=0, highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=BG_DARKER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn
