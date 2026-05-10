# gui/Categories_Page.py
# Embedded full-page panel — Προσθήκη / Διαχείριση Κατηγοριών.
# Αντικαθιστά τον κατάλογο (full-page swap) όταν ανοίγει.
#
# Callbacks:
#   on_change() → μετά από add / update / delete
#   on_back()   → κλικ στο breadcrumb "← Κατάλογος Βιβλίων"

import tkinter as tk
from tkinter import ttk, messagebox

from gui.styles import (
    BG_MAIN, BG_CARD, BG_FILTER, BG_DARK, BG_DARKER,
    ACCENT, FG_LIGHT, FG_DARK, FG_MUTED,
    FONT_MAIN, FONT_BOLD, FONT_TITLE, FONT_SEC, FONT_SMALL,
    FONT_TREE, FONT_THEAD, FONT_CRUMB,
    CHART_COLORS, MPL_BG, MPL_GRID, MPL_TEXT,
)


class CategoriesPanel(tk.Frame):

    def __init__(self, parent, service, on_change=None, on_back=None):
        super().__init__(parent, bg=BG_MAIN)
        self.service   = service
        self.on_change = on_change
        self.on_back   = on_back
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
        tk.Label(outer, text="Προσθήκη Κατηγορίας",
                 bg=BG_MAIN, fg=FG_DARK, font=FONT_TITLE,
                 anchor="w").grid(row=1, column=0, sticky="w", pady=(0, 16))

        # Card
        card = tk.Frame(outer, bg=BG_CARD, padx=22, pady=20)
        card.grid(row=2, column=0, sticky="new")
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=2)

        # Αριστερά: Combobox
        tk.Label(card, text="Κατηγορίες:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN,
                 anchor="w").grid(row=0, column=0, sticky="w",
                                  padx=(0, 20), pady=(0, 6))
        self._sel_var = tk.StringVar()
        self._combo   = ttk.Combobox(card, textvariable=self._sel_var,
                                     state="readonly", font=FONT_MAIN)
        self._combo.grid(row=1, column=0, sticky="ew", padx=(0, 20), ipady=5)
        self._combo.bind("<<ComboboxSelected>>", self._on_combo_select)

        # Δεξιά: Entry
        tk.Label(card, text="Νέα Κατηγορία:", bg=BG_CARD,
                 fg=FG_MUTED, font=FONT_MAIN,
                 anchor="w").grid(row=0, column=1, sticky="w", pady=(0, 6))
        self._name_var = tk.StringVar()
        tk.Entry(card, textvariable=self._name_var,
                 font=FONT_MAIN, relief="flat", bd=2,
                 bg="#FFFFFF", fg=FG_DARK,
                 insertbackground=FG_DARK).grid(
            row=1, column=1, sticky="ew", ipady=6)

        # Κουμπιά (bottom-right)
        btn_frame = tk.Frame(card, bg=BG_CARD)
        btn_frame.grid(row=2, column=0, columnspan=2,
                       sticky="e", pady=(20, 0))
        self._make_btn(btn_frame, "ΠΡΟΣΘΗΚΗ / ΕΝΗΜΕΡΩΣΗ",
                       self._save, bg=ACCENT, fg=FG_DARK).pack(
            side="left", padx=(0, 10))
        self._make_btn(btn_frame, "ΔΙΑΓΡΑΦΗ",
                       self._delete, bg=ACCENT, fg=FG_DARK).pack(side="left")

        self._reload()

    def _reload(self):
        self._cats = self.service.list_categories()
        cat_names  = [c["name"] for c in self._cats]
        self._combo["values"] = cat_names
        if self._sel_var.get() not in cat_names:
            self._sel_var.set("")

    def _on_combo_select(self, _=None):
        self._name_var.set(self._sel_var.get())

    def _save(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showwarning("Έλλειψη", "Πληκτρολογήστε όνομα κατηγορίας.")
            return
        sel_name = self._sel_var.get()
        cat_ids  = {c["name"]: c["id"] for c in self._cats}
        try:
            if sel_name and sel_name in cat_ids:
                self.service.update_category(cat_ids[sel_name], name)
            else:
                self.service.add_category(name)
            self._name_var.set("")
            self._sel_var.set("")
            self._reload()
            if self.on_change:
                self.on_change()
        except Exception as ex:
            messagebox.showerror("Σφάλμα", str(ex))

    def _delete(self):
        sel = self._sel_var.get()
        if not sel:
            messagebox.showwarning("Επιλογή", "Επιλέξτε κατηγορία για διαγραφή.")
            return
        cat_ids = {c["name"]: c["id"] for c in self._cats}
        if not messagebox.askyesno("Διαγραφή", f"Να διαγραφεί η κατηγορία «{sel}»;"):
            return
        try:
            self.service.delete_category(cat_ids[sel])
            self._name_var.set("")
            self._sel_var.set("")
            self._reload()
            if self.on_change:
                self.on_change()
        except Exception as ex:
            messagebox.showerror("Σφάλμα", str(ex))

    def refresh(self):
        self._reload()

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
