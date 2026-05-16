# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox

from gui.Styles import *


class Categories(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        #map of display name -> category id, populated on every reload
        self._name_to_id = {}
        self._selected_category_id = None

        #make Categories expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.categories_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.categories_frame.grid(row=0, column=0, sticky='nswe')

        self.categories_frame.grid_propagate(False)
        self.categories_frame.grid_columnconfigure(0, weight=1)
        self.categories_frame.grid_columnconfigure(1, weight=0)
        self.categories_frame.grid_columnconfigure(2, weight=0)
        for r in range(4):
            self.categories_frame.grid_rowconfigure(r, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file='gui/Assets/back_btn_icon.png')
        back_btn = tk.Button(
                            self.categories_frame,
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

        #title
        category_label = tk.Label(
            self.categories_frame,
            anchor='w',
            text="Προσθήκη Κατηγορίας",
            bd=0,
            bg=BG_MAIN,
            fg=FG_MUTED,
            font=FONT_TITLE
            )
        category_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky='nsew')

        #container
        container = tk.Frame(
            self.categories_frame,
            bg=BG_CARD,
            height=200,
            padx=10,
            pady=10
            )
        container.grid(row=2, columnspan=3, column=0, padx=15, pady=30, sticky='nsew')
        container.grid_propagate(False)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=0)

        list_lbl = tk.Label(
                    container,
                    anchor="ne",
                    text="Κατηγορίες:",
                    bd=0,
                    bg=BG_CARD,
                    fg=FG_MUTED,
                    font=FONT_SUBHEADER_BOLD,
                    )
        list_lbl.grid(row=0, column=0, sticky='w', padx=(15, 0), pady=(15, 5))

        entry_lbl = tk.Label(
                    container,
                    anchor="ne",
                    text="Νέα Κατηγορία:",
                    bd=0,
                    bg=BG_CARD,
                    fg=FG_MUTED,
                    font=FONT_SUBHEADER_BOLD,
                    )
        entry_lbl.grid(row=0, column=1, sticky='w', padx=(15, 0), pady=(15, 5))

        #new category entry box
        self.new_category = ttk.Entry(
                    container,
                    font=FONT_MAIN,
                    style="CustomEntry.TEntry",
                    width=40,
                    exportselection=False,
                    )
        self.new_category.grid(row=1, column=1, sticky='w', padx=15, pady=5)

        #category list
        self.cat_list = ttk.Combobox(
                        container,
                        state="readonly",
                        font=FONT_MAIN,
                        width=40,
                        values=[],
                        style="CustomCombobox.TCombobox"
                        )
        self.cat_list.grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.cat_list.bind("<<ComboboxSelected>>", lambda e: self.selection_to_entry())

        #buttons
        self.edit_btn = ttk.Button(
                        self.categories_frame,
                        text="ΠΡΟΣΘΗΚΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.save_category,
                        )
        self.edit_btn.grid(row=3, column=0, sticky='e', padx=5, pady=5)

        self.delete_btn = ttk.Button(
                        self.categories_frame,
                        text="ΔΙΑΓΡΑΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.delete_category,
                        )
        self.delete_btn.grid(row=3, column=1, sticky='e', padx=5, pady=5)
        self.delete_btn.state(['disabled'])

        self.clear_btn = ttk.Button(
                        self.categories_frame,
                        text="ΚΑΘΑΡΙΣΜΟΣ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.clear_cb
                        )
        self.clear_btn.grid(row=3, column=2, sticky='e', padx=(5, 15), pady=5)

        self._load_categories()

    # =========================================
    # Combobox Selection to Entry
    # =========================================
    def selection_to_entry(self):
        selected = self.cat_list.get()
        self.new_category.delete(0, 'end')
        self.new_category.insert(0, selected)
        self._selected_category_id = self._name_to_id.get(selected)
        self.edit_btn.config(text="ΕΝΗΜΕΡΩΣΗ")
        if self._selected_category_id is not None:
            self.delete_btn.state(['!disabled'])
        else:
            self.delete_btn.state(['disabled'])

    # =========================================
    # Clear Combobox Selection
    # =========================================
    def clear_cb(self):
        self.cat_list.set('')
        try:
            self.cat_list.select_clear()
        except Exception:
            pass
        self.new_category.delete(0, 'end')
        self._selected_category_id = None
        self.edit_btn.config(text="ΠΡΟΣΘΗΚΗ")
        self.delete_btn.state(['disabled'])

    # =========================================
    # ΠΡΟΣΘΗΚΗ / ΕΝΗΜΕΡΩΣΗ
    # =========================================
    def save_category(self):
        if not self.service:
            return

        name = self.new_category.get().strip()
        if not name:
            messagebox.showwarning("Άκυρη καταχώρηση",
                                   "Το όνομα της κατηγορίας είναι υποχρεωτικό.")
            return

        try:
            if self._selected_category_id is None:
                self.service.add_category(name, "")
                messagebox.showinfo("Επιτυχία",
                                    f"Η κατηγορία '{name}' προστέθηκε.")
            else:
                self.service.update_category(self._selected_category_id, name, "")
                messagebox.showinfo("Επιτυχία",
                                    f"Η κατηγορία ενημερώθηκε σε '{name}'.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        self._load_categories()
        self.clear_cb()

    # =========================================
    # ΔΙΑΓΡΑΦΗ
    # =========================================
    def delete_category(self):
        if not self.service or self._selected_category_id is None:
            return
        name = self.cat_list.get()
        if not messagebox.askyesno("Επιβεβαίωση",
                                   f"Διαγραφή της κατηγορίας '{name}';"):
            return
        try:
            self.service.delete_category(self._selected_category_id)
            messagebox.showinfo("Επιτυχία", "Η κατηγορία διαγράφηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return
        self._load_categories()
        self.clear_cb()

    # =========================================
    # Reset on navigation
    # =========================================
    def reset(self):
        self._load_categories()
        self.clear_cb()

    # =========================================
    # Load combobox from service
    # =========================================
    def _load_categories(self):
        self._name_to_id = {}
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
                self._name_to_id[name] = cat_id
                labels.append(name)
        self.cat_list["values"] = labels
        # Don't auto-select - let the user click
