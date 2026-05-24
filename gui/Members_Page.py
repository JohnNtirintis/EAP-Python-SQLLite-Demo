# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, font, messagebox

from gui.Styles import *
from gui.Dashboard_Page import autosize_content
from gui.Loans_Page import remove_placeholder_var,add_placeholder_var


# Display labels used in the Φύλο combobox <-> the DB values understood by the schema.
GENDER_DISPLAY_TO_DB = {
    "Άνδρας":  "Male",
    "Γυναίκα": "Female",
    "Άλλο":    "Other",
    "":        None,
}
GENDER_DB_TO_DISPLAY = {v: k for k, v in GENDER_DISPLAY_TO_DB.items() if v is not None}


class Members(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        #currently selected member id (or None). Exposed for Recommend page.
        self.selected_member_id = None

        #make Members expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.member_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.member_frame.grid(row=0, column=0, sticky='nswe')

        self.member_frame.grid_columnconfigure(0, weight=1)
        self.member_frame.grid_rowconfigure(0, weight=0)
        self.member_frame.grid_rowconfigure(1, weight=1, minsize=200)
        self.member_frame.grid_rowconfigure(2, weight=0)
        self.member_frame.grid_rowconfigure(3, weight=1, minsize=200)

        #profile title
        profile_label = tk.Label(
                            self.member_frame,
                            anchor='w',
                            text='Μέλη',
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE
                            )
        profile_label.grid(row=0, column=0, padx=15, pady=(5, 10), sticky='nsew')

        #table title
        table_title = tk.Label(
                            self.member_frame,
                            anchor='w',
                            text='Λίστα Μελών',
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE
                            )
        table_title.grid(row=2, column=0, padx=15, pady=(5, 10), sticky='nsew')

        #searchbar
        self.searchbar_member_var = tk.StringVar()
        self.searchbar_member = ttk.Entry(
                    self.member_frame,
                    font=FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    textvariable=self.searchbar_member_var
                    )
        self.searchbar_member.grid(row=2, column=0, sticky='e', padx=15, pady=10)
        self.searchbar_member_var.set("Αναζήτηση...")
        self.searchbar_member.bind("<FocusIn>",
                                   lambda e: remove_placeholder_var(self.searchbar_member_var))
        self.searchbar_member.bind("<FocusOut>",
                                   lambda e: add_placeholder_var(self.searchbar_member_var))
        self.searchbar_member.bind("<Return>", lambda e: self.run_search())
        self.searchbar_member_var.trace_add("write", lambda *a: self.run_search())


        self.entries = {}
        self.create_members_profile()
        self.create_members_table()
        self.refresh_members_table()

    # =========================================
    # Members' Profile function
    # =========================================
    def create_members_profile(self):
        container = tk.Frame(
                    self.member_frame,
                    bd=0,
                    bg=BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=1, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        for r in range(5):
            container.grid_rowconfigure(r, weight=1 if r > 0 else 0)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)
        container.grid_columnconfigure(3, weight=1)
        container.grid_columnconfigure(4, weight=1)

        #title
        title_lbl = tk.Label(
                        container,
                        anchor="center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font=FONT_SUBHEADER_BOLD,
                        text="Προφίλ μέλους:"
                        )
        title_lbl.grid(row=0, column=0, sticky='w', padx=(15, 0), pady=10)

        #---- helpers ----
        def create_entry(row, col, label_text):
            lbl = tk.Label(
                    container,
                    anchor="ne",
                    text=label_text,
                    bd=0,
                    bg=BG_CARD,
                    fg=FG_MUTED,
                    font=FONT_BOLD,
                    )
            lbl.grid(row=row, column=col * 2, sticky='w', padx=(15, 0), pady=5)
            entry = ttk.Entry(
                    container,
                    font=FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    )
            entry.grid(row=row, column=col * 2 + 1, sticky='ew', padx=5, pady=5)
            return entry

        def create_combo(row, col, label_text, values):
            lbl = tk.Label(
                    container,
                    anchor="ne",
                    text=label_text,
                    bd=0,
                    bg=BG_CARD,
                    fg=FG_MUTED,
                    font=FONT_BOLD,
                    )
            lbl.grid(row=row, column=col * 2, sticky='w', padx=(15, 0), pady=5)
            combo = ttk.Combobox(
                    container,
                    state="readonly",
                    font=FONT_MAIN,
                    values=values,
                    style="CustomCombobox.TCombobox",
                    )
            combo.grid(row=row, column=col * 2 + 1, sticky='ew', padx=5, pady=5)
            return combo

        def create_button(row, text):
            btn = ttk.Button(
                        container,
                        text=text,
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2'
                        )
            btn.grid(row=row + 1, column=4, sticky='e', padx=(5, 15), pady=5)
            return btn

        # Form fields. Column 0 = left, column 1 = right.
        # Row 1..4 are the entries.
        self.entries["full_name"] = create_entry(1, 0, "Ονοματεπώνυμο:")
        self.entries["age"]       = create_entry(2, 0, "Ηλικία:")
        self.entries["email"]     = create_entry(3, 0, "Email:")
        self.entries["phone"]     = create_entry(4, 0, "Τηλέφωνο:")

        self.entries["address"]            = create_entry(1, 1, "Διεύθυνση:")
        self.entries["profession"]         = create_entry(2, 1, "Επάγγελμα:")
        self.entries["registration_number"]= create_entry(3, 1, "Αρ. Μητρώου:")
        self.gender_combo = create_combo(4, 1, "Φύλο:",
                                         list(GENDER_DISPLAY_TO_DB.keys()))

        # Buttons
        self.save_button = create_button(0, "ΔΗΜΙΟΥΡΓΙΑ")
        self.save_button.config(command=self.save_member)

        self.status_button = create_button(1, "ΑΝΑΝΕΩΣΗ")
        self.status_button.config(command=self.toggle_status)
        self.status_button.state(['disabled'])

        self.suggestion_button = create_button(2, "ΠΡΟΤΑΣΗ ΒΙΒΛΙΟΥ")
        self.suggestion_button.config(command=self.go_to_recommend)
        self.suggestion_button.state(['disabled'])

        self.clear_button = create_button(3, "ΚΑΘΑΡΙΣΜΟΣ")
        self.clear_button.config(command=self.reset)
        self.clear_button.state(['disabled'])

    # =========================================
    # Members' Table function
    # =========================================
    def create_members_table(self):
        container = tk.Frame(
                    self.member_frame,
                    bd=0,
                    bg=BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=3, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)

        #table
        # Columns reflect what's actually stored in the DB schema.
        columns = ("ID", "Ονοματεπώνυμο", "Αρ. Μητρώου", "Φύλο", "Ηλικία",
                   "Email", "Τηλέφωνο", "Διεύθυνση", "Επάγγελμα", "Κατάσταση")
        self.members_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.members_table.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=(0, 5))

        #scrollbars
        v_scrollbar = ttk.Scrollbar(
                        container,
                        orient='vertical',
                        command=self.members_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.members_table.config(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(
                        container,
                        orient='horizontal',
                        command=self.members_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2, 0.5)
        h_scrollbar.grid(row=1, column=0, sticky='we')
        self.members_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.members_table.heading(col, text=col, anchor='w')
            self.members_table.column(
                col,
                anchor="w",
                stretch=False,
                minwidth=80 if col in ("ID", "Φύλο", "Ηλικία", "Κατάσταση") else 150,
                width=100 if col in ("ID", "Φύλο", "Ηλικία", "Κατάσταση") else 180,
                )

        self.members_table.bind("<<TreeviewSelect>>",
                                lambda e: self.selection_to_entry())

    # =========================================
    # Load data from service into the table
    # =========================================
    def refresh_members_table(self):
        for item in self.members_table.get_children():
            self.members_table.delete(item)

        if not self.service:
            return

        try:
            members = self.service.list_members()
        except Exception as e:
            messagebox.showerror("Σφάλμα φόρτωσης",
                                 f"Αδυναμία ανάκτησης μελών: {e}")
            return

        for m in members:
            gender_display = GENDER_DB_TO_DISPLAY.get(m.get("gender"),
                                                      m.get("gender") or "")
            status_display = "Ενεργό" if m.get("status") == "active" else "Ανενεργό"
            age_display = "" if m.get("age") in (None, "") else str(m.get("age"))
            self.members_table.insert(
                "", "end",
                iid=str(m["id"]),
                values=(
                    f"{m['id']:04d}",
                    m.get("full_name", ""),
                    m.get("registration_number", ""),
                    gender_display,
                    age_display,
                    m.get("email", "") or "",
                    m.get("phone", "") or "",
                    m.get("address", "") or "",
                    m.get("profession", "") or "",
                    status_display,
                ),
            )

        autosize_content(self.members_table)

    # =========================================
    # Selection -> form
    # =========================================
    def selection_to_entry(self):
        selected = self.members_table.selection()

        if not selected:
            self.selected_member_id = None
            self.save_button.config(text="ΔΗΜΙΟΥΡΓΙΑ")
            self.status_button.config(text="ΑΝΑΝΕΩΣΗ")
            self.status_button.state(['disabled'])
            self.suggestion_button.state(['disabled'])
            self.clear_button.state(['disabled'])
            return

        self.selected_member_id = int(selected[0])
        member = self.service.get_member(self.selected_member_id) if self.service else None
        if not member:
            messagebox.showerror("Σφάλμα",
                                 "Το μέλος δεν βρέθηκε.")
            return

        # Fill form
        self.clear_entries()
        self.entries["full_name"].insert(0, member.get("full_name", ""))
        self.entries["age"].insert(0, "" if member.get("age") is None
                                        else str(member.get("age")))
        self.entries["email"].insert(0, member.get("email", "") or "")
        self.entries["phone"].insert(0, member.get("phone", "") or "")
        self.entries["address"].insert(0, member.get("address", "") or "")
        self.entries["profession"].insert(0, member.get("profession", "") or "")
        self.entries["registration_number"].insert(
            0, member.get("registration_number", "") or "")
        self.gender_combo.set(
            GENDER_DB_TO_DISPLAY.get(member.get("gender"), ""))

        # Buttons
        self.save_button.config(text="ΕΝΗΜΕΡΩΣΗ")
        if member.get("status") == "active":
            self.status_button.config(text="ΤΕΡΜΑΤΙΣΜΟΣ")
        else:
            self.status_button.config(text="ΑΝΑΝΕΩΣΗ")
        self.status_button.state(['!disabled'])
        self.suggestion_button.state(['!disabled'])
        self.clear_button.state(['!disabled'])

    # =========================================
    # Read form values into a kwargs dict for the service
    # =========================================
    def _form_to_kwargs(self):
        """Pull values from the form. Raises ValueError on bad numeric input."""
        full_name = self.entries["full_name"].get().strip()
        age_raw   = self.entries["age"].get().strip()
        email     = self.entries["email"].get().strip()
        phone     = self.entries["phone"].get().strip()
        address   = self.entries["address"].get().strip()
        profession= self.entries["profession"].get().strip()
        reg_no    = self.entries["registration_number"].get().strip()
        gender    = GENDER_DISPLAY_TO_DB.get(self.gender_combo.get(), None)

        age = None
        if age_raw:
            try:
                age = int(age_raw)
            except ValueError:
                raise ValueError("Η ηλικία πρέπει να είναι ακέραιος αριθμός.")

        return {
            "full_name": full_name,
            "registration_number": reg_no,
            "address": address,
            "phone": phone,
            "email": email,
            "age": age,
            "profession": profession,
            "gender": gender,
            "notes": "",
        }

    def _auto_registration_number(self):
        """Generate a registration number like M-1011 based on highest existing one."""
        if not self.service:
            return "M-1001"
        existing = self.service.list_members()
        max_n = 1000
        for m in existing:
            rn = (m.get("registration_number") or "").strip()
            if rn.startswith("M-"):
                try:
                    n = int(rn[2:])
                    if n > max_n:
                        max_n = n
                except ValueError:
                    pass
        return f"M-{max_n + 1}"

    # =========================================
    # ΔΗΜΙΟΥΡΓΙΑ / ΕΝΗΜΕΡΩΣΗ
    # =========================================
    def save_member(self):
        if not self.service:
            return

        try:
            kwargs = self._form_to_kwargs()
        except ValueError as e:
            messagebox.showwarning("Άκυρη τιμή", str(e))
            return

        if not kwargs["full_name"]:
            messagebox.showwarning("Άκυρη καταχώρηση",
                                   "Το ονοματεπώνυμο είναι υποχρεωτικό.")
            return

        try:
            if self.selected_member_id is None:
                # CREATE
                if not kwargs["registration_number"]:
                    kwargs["registration_number"] = self._auto_registration_number()
                self.service.add_member(**kwargs)
                messagebox.showinfo("Επιτυχία", "Το μέλος δημιουργήθηκε.")
            else:
                # UPDATE - registration_number is not updatable
                update_kwargs = {k: v for k, v in kwargs.items()
                                 if k != "registration_number"}
                self.service.update_member(self.selected_member_id, **update_kwargs)
                messagebox.showinfo("Επιτυχία", "Το μέλος ενημερώθηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        self.refresh_members_table()
        self.reset()

    # =========================================
    # ΑΝΑΝΕΩΣΗ / ΤΕΡΜΑΤΙΣΜΟΣ
    # =========================================
    def toggle_status(self):
        if not self.service or self.selected_member_id is None:
            return

        member = self.service.get_member(self.selected_member_id)
        if not member:
            return

        try:
            if member.get("status") == "active":
                self.service.deactivate_member(self.selected_member_id)
                messagebox.showinfo("Επιτυχία",
                                    "Η εγγραφή του μέλους διεκόπη.")
            else:
                self.service.renew_membership(self.selected_member_id)
                messagebox.showinfo("Επιτυχία",
                                    "Η εγγραφή του μέλους ανανεώθηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        self.refresh_members_table()
        self.reset()

    #=========================================
    # search members
    #=========================================
    def run_search(self):
        if not self.service:
            return
        term = self.searchbar_member_var.get().strip()
        if term == "Αναζήτηση...":
            term = ""
        term_l = term.lower()

        self.members_table.delete(*self.members_table.get_children())

        for m in self.service.list_members():
            name = m.get("full_name", "") or ""
            reg = m.get("registration_number", "") or ""
            email = m.get("email", "") or ""
            phone = m.get("phone", "") or ""
            if term_l:
                hay = " ".join([name, reg, email,phone]).lower()
                if term_l not in hay:
                    continue

            gender_display = GENDER_DB_TO_DISPLAY.get(m.get("gender"),
                                                      m.get("gender") or "")
            status_display = "Ενεργό" if m.get("status") == "active" else "Ανενεργό"
            age_display = "" if m.get("age") in (None, "") else str(m.get("age"))

            self.members_table.insert(
                "",
                "end",
                iid=str(m["id"]),
                values=(
                    f"{m['id']:04d}",
                    name,
                    reg,
                    gender_display,
                    age_display,
                    email,
                    phone,
                    m.get("address", "") or "",
                    m.get("profession", "") or "",
                    status_display,
                ),
            )
        autosize_content(self.members_table)

    # =========================================
    # navigate to Recommend
    # =========================================
    def go_to_recommend(self):
        if self.selected_member_id is None:
            messagebox.showwarning("Επιλογή",
                                   "Παρακαλώ επιλέξτε πρώτα ένα μέλος.")
            return
        self.app.change_page("Πρόταση Βιβλίου")

    # =========================================
    # Clear form
    # =========================================
    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')
        self.gender_combo.set("")

    # =========================================
    # Reset state on navigation
    # =========================================
    def reset(self):
        self.clear_entries()
        try:
            self.members_table.selection_set(())
        except Exception:
            pass
        self.selected_member_id = None
        self.save_button.config(text="ΔΗΜΙΟΥΡΓΙΑ")
        self.status_button.config(text="ΑΝΑΝΕΩΣΗ")
        self.status_button.state(['disabled'])
        self.suggestion_button.state(['disabled'])
        self.clear_button.state(['disabled'])
        # also refresh data on every navigation so new members appear
        self.refresh_members_table()
