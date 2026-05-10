# gui/Book_Edit_Page.py
# Embedded full-page panel — Προσθήκη / Ενημέρωση Βιβλίου.
# Αντικαθιστά τον κατάλογο (full-page swap) όταν ανοίγει.
#
# Callbacks:
#   on_save()  → μετά από επιτυχή αποθήκευση
#   on_back()  → κλικ στο breadcrumb "← Κατάλογος Βιβλίων"

import tkinter as tk
from tkinter import ttk, messagebox

from app.dto import CreateBookDTO, UpdateBookDTO

from gui.styles import (
    BG_MAIN, BG_CARD, BG_FILTER, BG_DARK, BG_DARKER,
    ACCENT, FG_LIGHT, FG_DARK, FG_MUTED,
    FONT_MAIN, FONT_BOLD, FONT_TITLE, FONT_SEC, FONT_SMALL,
    FONT_TREE, FONT_THEAD, FONT_CRUMB,
    CHART_COLORS, MPL_BG, MPL_GRID, MPL_TEXT,
)


class BookEditPanel(tk.Frame):


    def __init__(self, parent, service,
                 book: dict | None = None,
                 on_save=None, on_back=None):
        super().__init__(parent, bg=BG_MAIN)
        self.service = service
        self.book    = book
        self.on_save = on_save
        self.on_back = on_back
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG_MAIN, padx=30, pady=22)
        outer.pack(fill="both", expand=True)
        outer.grid_columnconfigure(0, weight=1)

        # Breadcrumb
        crumb = tk.Label(outer, text="← Κατάλογος Βιβλίων",
                         bg=BG_MAIN, fg=FG_MUTED,
                         font=FONT_CRUMB, cursor="hand2", anchor="w")
        crumb.grid(row=0, column=0, sticky="w", pady=(0, 4))
        crumb.bind("<Button-1>", lambda e: self._go_back())
        crumb.bind("<Enter>",    lambda e: crumb.config(fg=FG_DARK))
        crumb.bind("<Leave>",    lambda e: crumb.config(fg=FG_MUTED))

        # Page title
        tk.Label(outer, text="Προσθήκη / Ενημέρωση Βιβλίου",
                 bg=BG_MAIN, fg=FG_DARK, font=FONT_TITLE,
                 anchor="w").grid(row=1, column=0, sticky="w", pady=(0, 16))

        # Card
        card = tk.Frame(outer, bg=BG_CARD, padx=26, pady=22)
        card.grid(row=2, column=0, sticky="new")
        card.grid_columnconfigure(1, weight=1)

        # Text fields
        field_defs = [
            ("Τίτλος:",       "title"),
            ("Συγγραφέας:",   "author"),
            ("Έτος έκδοσης:", "year"),
            ("ISBN:",         "isbn"),
        ]
        self._entries: dict[str, tk.Entry] = {}
        for r, (lbl, key) in enumerate(field_defs):
            tk.Label(card, text=lbl, bg=BG_CARD, fg=FG_DARK,
                     font=FONT_MAIN, anchor="w", width=14).grid(
                row=r, column=0, sticky="w", pady=8, padx=(0, 16))
            e = tk.Entry(card, font=FONT_MAIN, relief="flat", bd=1,
                         bg="#FFFFFF", fg=FG_DARK,
                         insertbackground=FG_DARK,
                         highlightthickness=1,
                         highlightbackground="#CCCCCC",
                         highlightcolor=ACCENT)
            e.grid(row=r, column=1, sticky="ew", ipady=6, pady=8)
            self._entries[key] = e

        # Κατηγορία
        cat_row = len(field_defs)
        tk.Label(card, text="Κατηγορία:", bg=BG_CARD, fg=FG_DARK,
                 font=FONT_MAIN, anchor="w", width=14).grid(
            row=cat_row, column=0, sticky="w", pady=8, padx=(0, 16))
        self._cat_var = tk.StringVar()
        self._cat_cb  = ttk.Combobox(card, textvariable=self._cat_var,
                                     state="readonly", font=FONT_MAIN)
        self._cat_cb.grid(row=cat_row, column=1, sticky="ew", ipady=5, pady=8)

        # Απόθεμα
        sp_row = cat_row + 1
        tk.Label(card, text="Απόθεμα:", bg=BG_CARD, fg=FG_DARK,
                 font=FONT_MAIN, anchor="w", width=14).grid(
            row=sp_row, column=0, sticky="w", pady=8, padx=(0, 16))
        self._copies_var = tk.IntVar(value=1)
        tk.Spinbox(card, from_=1, to=999, textvariable=self._copies_var,
                   font=FONT_MAIN, relief="flat", bd=1,
                   bg="#FFFFFF", fg=FG_DARK,
                   insertbackground=FG_DARK, width=8,
                   buttonbackground=BG_CARD).grid(
            row=sp_row, column=1, sticky="w", ipady=5, pady=8)

        # Κουμπί (bottom-right)
        btn_frame = tk.Frame(card, bg=BG_CARD)
        btn_frame.grid(row=sp_row + 1, column=0, columnspan=2,
                       sticky="e", pady=(18, 0))
        self._make_btn(btn_frame, "ΠΡΟΣΘΗΚΗ / ΕΝΗΜΕΡΩΣΗ",
                       self._save, bg=ACCENT, fg=FG_DARK).pack(side="right")

        self._reload_categories()
        if self.book:
            self._prefill()

    def _reload_categories(self):
        cats            = self.service.list_categories()
        self._cat_names = [c["name"] for c in cats]
        self._cat_ids   = [c["id"]   for c in cats]
        self._cat_cb["values"] = self._cat_names

    def _prefill(self):
        b = self.book
        self._entries["title"].insert(0,  b.get("title", ""))
        self._entries["author"].insert(0, b.get("author", ""))
        self._entries["year"].insert(0,   str(b.get("published_year") or ""))
        self._entries["isbn"].insert(0,   b.get("isbn", ""))
        self._copies_var.set(b.get("total_copies", 1))
        try:
            cat_id = b.get("category_id")
            if cat_id and cat_id in self._cat_ids:
                self._cat_var.set(self._cat_names[self._cat_ids.index(cat_id)])
            elif b.get("category_name") in self._cat_names:
                self._cat_var.set(b["category_name"])
        except (ValueError, IndexError):
            pass

    def _clear_form(self):
        for e in self._entries.values():
            e.delete(0, "end")
        self._cat_var.set("")
        self._copies_var.set(1)
        self.book = None

    def _save(self):
        try:
            title  = self._entries["title"].get().strip()
            author = self._entries["author"].get().strip()
            yr_str = self._entries["year"].get().strip()
            isbn   = self._entries["isbn"].get().strip()
            cat_n  = self._cat_var.get()
            copies = int(self._copies_var.get())

            if not title or not author or not cat_n:
                messagebox.showwarning(
                    "Έλλειψη",
                    "Τίτλος, Συγγραφέας και Κατηγορία είναι υποχρεωτικά.")
                return

            year   = int(yr_str) if yr_str else None
            cat_id = self._cat_ids[self._cat_names.index(cat_n)]

            if self.book:
                self.service.update_book(UpdateBookDTO(
                    id=self.book["id"], title=title, author=author,
                    isbn=isbn, category_id=cat_id,
                    total_copies=copies, published_year=year,
                ))
                messagebox.showinfo("Επιτυχία", f"Το βιβλίο «{title}» ενημερώθηκε.")
            else:
                self.service.add_book(CreateBookDTO(
                    title=title, author=author, isbn=isbn,
                    category_id=cat_id, total_copies=copies,
                    available_copies=copies, published_year=year,
                ))
                messagebox.showinfo("Επιτυχία", f"Το βιβλίο «{title}» προστέθηκε.")
                self._clear_form()

            if self.on_save:
                self.on_save()

        except Exception as ex:
            messagebox.showerror("Σφάλμα", str(ex))

    def load_book(self, book: dict | None):
        """Φορτώνει βιβλίο για edit ή καθαρίζει για add. Καλείται από Books_Page."""
        self._clear_form()
        self.book = book
        self._reload_categories()
        if book:
            self._prefill()

    def refresh_categories(self):
        self._reload_categories()

    def _go_back(self):
        if self.on_back:
            self.on_back()

    @staticmethod
    def _make_btn(parent, text, command, bg=BG_DARK, fg=FG_LIGHT):
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg,
                        activebackground=BG_DARKER, activeforeground=FG_DARK,
                        relief="flat", font=("Segoe UI", 11),
                        padx=16, pady=7, cursor="hand2",
                        bd=0, highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=BG_DARKER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn
