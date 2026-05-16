# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox

from gui.Styles import *


class BookEdit(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        #currently edited book id (None for create mode)
        self.selected_book_id = None
        #map of display category name -> id, populated on every reload
        self._cat_name_to_id = {}

        #make BookEdit expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.book_edit_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.book_edit_frame.grid(row=0, column=0, sticky='nswe')

        self.book_edit_frame.grid_propagate(False)
        self.book_edit_frame.grid_columnconfigure(0, weight=1)
        self.book_edit_frame.grid_columnconfigure(1, weight=0)
        for r in range(4):
            self.book_edit_frame.grid_rowconfigure(r, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file='gui/Assets/back_btn_icon.png')
        back_btn = tk.Button(
                            self.book_edit_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Κατάλογος Βιβλίων',
                            bd=0,
                            width=160,
                            padx=10,
                            bg=BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg=FG_MUTED,
                            font=FONT_MAIN,
                            command=lambda: self.app.change_page("Κατάλογος Βιβλίων"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0, column=0, padx=5, pady=(0, 10), sticky='w')

        #page title
        self.title_var = tk.StringVar(value='Προσθήκη Βιβλίου')
        book_edit_label = tk.Label(
                            self.book_edit_frame,
                            anchor='w',
                            textvariable=self.title_var,
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE
                            )
        book_edit_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky='nsew')

        #add/edit button
        self.edit_button = ttk.Button(
                        self.book_edit_frame,
                        text="ΠΡΟΣΘΗΚΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.save_book,
                        )
        self.edit_button.grid(row=3, column=0, sticky='e', padx=5, pady=5)

        #delete button
        self.delete_button = ttk.Button(
                        self.book_edit_frame,
                        text="ΔΙΑΓΡΑΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.delete_book,
                        )
        self.delete_button.grid(row=3, column=1, sticky='e', padx=(5, 15), pady=5)
        self.delete_button.state(['disabled'])

        #container for book data
        container = tk.Frame(
                    self.book_edit_frame,
                    bd=0,
                    bg=BG_CARD,
                    height=400,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        for r in range(6):
            container.grid_rowconfigure(r, weight=1 if r > 0 else 0)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)

        self.entries = {}

        def create_label(row, text):
            tk.Label(
                container,
                anchor="ne",
                text=text,
                bd=0,
                bg=BG_CARD,
                fg=FG_MUTED,
                font=FONT_BOLD,
            ).grid(row=row, column=0, sticky='w', padx=(15, 0), pady=5)

        def create_entry(row):
            entry = ttk.Entry(
                container,
                font=FONT_MAIN,
                width=50,
                style="CustomEntry.TEntry",
                exportselection=False,
            )
            entry.grid(row=row, column=1, sticky='w', padx=20, pady=5)
            return entry

        # rows 0..3 are entry-driven
        labels = ["Τίτλος:", "Συγγραφέας:", "Έτος έκδοσης:", "ISBN:",
                  "Κατηγορία:", "Απόθεμα:"]
        keys   = ["title",  "author",      "year",            "isbn"]

        for i, text in enumerate(labels):
            create_label(i, text)

        for i, key in enumerate(keys):
            entry = create_entry(i)
            self.entries[key] = entry

        # row 4: category combobox
        self.category_var = tk.StringVar()
        self.cat_list = ttk.Combobox(
                        container,
                        state="readonly",
                        font=FONT_MAIN,
                        width=40,
                        values=[],
                        textvariable=self.category_var,
                        style="CustomCombobox.TCombobox"
                        )
        self.cat_list.grid(row=4, column=1, sticky="w", padx=20, pady=5)

        # row 5: copies spinbox
        self.copies_var = tk.IntVar(value=1)
        self.stock = tk.Spinbox(
            container,
            from_=0,
            to=999,
            width=8,
            justify='center',
            font=FONT_MAIN,
            textvariable=self.copies_var,
            bg='white',
            fg=FG_DARK,
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground=FG_DARK,
            highlightcolor=ACCENT,
            buttonbackground='white',
            buttondownrelief='flat',
            buttonuprelief='flat',
            exportselection=False,
            insertbackground=ACCENT_DARK,
            repeatdelay=150,
            repeatinterval=50
            )
        self.stock.grid(row=5, column=1, sticky="w", padx=20, pady=5, ipady=2)

        self._load_categories()

    # =========================================
    # Reset/clear
    # =========================================
    def reset(self):
        #clear entries
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.category_var.set("")
        self.copies_var.set(1)
        self.selected_book_id = None
        self.title_var.set("Προσθήκη Βιβλίου")
        self.edit_button.config(text="ΠΡΟΣΘΗΚΗ")
        self.delete_button.state(['disabled'])

        # Always refresh category list when this page becomes visible
        self._load_categories()

    # =========================================
    # Prefill the form when called from Books page in "edit" mode
    # =========================================
    def prefill(self, book):
        """`book` is a dict with the same shape as `Books._books_to_dicts` items."""
        self._load_categories()
        self.reset_form_only()
        self.selected_book_id = book.get("id")
        self.entries["title"].insert(0, book.get("title", "") or "")
        self.entries["author"].insert(0, book.get("author", "") or "")
        self.entries["year"].insert(0, str(book.get("published_year") or ""))
        self.entries["isbn"].insert(0, book.get("isbn", "") or "")
        self.category_var.set(book.get("category_name", "") or "")
        try:
            self.copies_var.set(int(book.get("total_copies", 1) or 1))
        except (TypeError, ValueError):
            self.copies_var.set(1)
        self.title_var.set("Ενημέρωση Βιβλίου")
        self.edit_button.config(text="ΕΝΗΜΕΡΩΣΗ")
        self.delete_button.state(['!disabled'])

    def reset_form_only(self):
        """Like reset() but does not clear self.selected_book_id."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.category_var.set("")
        self.copies_var.set(1)

    # =========================================
    # ΠΡΟΣΘΗΚΗ / ΕΝΗΜΕΡΩΣΗ
    # =========================================
    def save_book(self):
        if not self.service:
            return

        title  = self.entries["title"].get().strip()
        author = self.entries["author"].get().strip()
        year_raw = self.entries["year"].get().strip()
        isbn   = self.entries["isbn"].get().strip()
        cat_name = self.category_var.get().strip()

        if not title:
            messagebox.showwarning("Άκυρη καταχώρηση", "Ο τίτλος είναι υποχρεωτικός.")
            return
        if not author:
            messagebox.showwarning("Άκυρη καταχώρηση", "Ο συγγραφέας είναι υποχρεωτικός.")
            return
        if not isbn:
            messagebox.showwarning("Άκυρη καταχώρηση", "Το ISBN είναι υποχρεωτικό.")
            return
        if not cat_name:
            messagebox.showwarning("Άκυρη καταχώρηση", "Επιλέξτε κατηγορία.")
            return

        category_id = self._cat_name_to_id.get(cat_name)
        if category_id is None:
            messagebox.showerror("Σφάλμα", "Άγνωστη κατηγορία.")
            return

        year = None
        if year_raw:
            try:
                year = int(year_raw)
            except ValueError:
                messagebox.showwarning("Άκυρη τιμή",
                                       "Το έτος πρέπει να είναι αριθμός.")
                return

        try:
            total_copies = int(self.copies_var.get())
        except (TypeError, ValueError, tk.TclError):
            messagebox.showwarning("Άκυρη τιμή",
                                   "Το απόθεμα πρέπει να είναι ακέραιος.")
            return

        if total_copies <= 0:
            messagebox.showwarning("Άκυρη τιμή",
                                   "Το απόθεμα πρέπει να είναι θετικός ακέραιος.")
            return

        kwargs = dict(
            title=title,
            author=author,
            isbn=isbn,
            category_id=category_id,
            total_copies=total_copies,
            published_year=year,
        )

        try:
            if self.selected_book_id is None:
                self.service.add_book(**kwargs)
                messagebox.showinfo("Επιτυχία", "Το βιβλίο προστέθηκε.")
            else:
                self.service.update_book(self.selected_book_id, **kwargs)
                messagebox.showinfo("Επιτυχία", "Το βιβλίο ενημερώθηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        self.reset()
        self.app.change_page("Κατάλογος Βιβλίων")

    # =========================================
    # ΔΙΑΓΡΑΦΗ
    # =========================================
    def delete_book(self):
        if not self.service or self.selected_book_id is None:
            return
        title = self.entries["title"].get().strip() or "(χωρίς τίτλο)"
        if not messagebox.askyesno("Επιβεβαίωση",
                                   f"Διαγραφή του βιβλίου '{title}';"):
            return
        try:
            self.service.delete_book(self.selected_book_id)
            messagebox.showinfo("Επιτυχία", "Το βιβλίο διαγράφηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return
        self.reset()
        self.app.change_page("Κατάλογος Βιβλίων")

    # =========================================
    # Load category list from service
    # =========================================
    def _load_categories(self):
        self._cat_name_to_id = {}
        if not self.service:
            self.cat_list["values"] = []
            return
        cats = self.service.list_categories() or []
        labels = []
        for c in cats:
            if isinstance(c, dict):
                name = c.get("name")
                cat_id = c.get("id")
            else:
                name = getattr(c, "name", None)
                cat_id = getattr(c, "id", None)
            if name and cat_id is not None:
                self._cat_name_to_id[name] = cat_id
                labels.append(name)
        self.cat_list["values"] = labels
