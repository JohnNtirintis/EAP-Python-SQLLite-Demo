import tkinter as tk
from tkinter import ttk, messagebox


class MembersView(ttk.Frame):
    """
    Members tab — now fully compatible with DTO-based DAL/BusinessLogic.
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # SECTION: Member profile
        # ---------------------------------------------------------
        profile_frame = ttk.LabelFrame(self, text="Member profile")
        profile_frame.pack(fill="x", padx=10, pady=10)

        # Row 0
        ttk.Label(profile_frame, text="Full name:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.entry_full_name = ttk.Entry(profile_frame, width=40)
        self.entry_full_name.grid(row=0, column=1, sticky="w")

        ttk.Label(profile_frame, text="Registration number:").grid(row=0, column=2, sticky="e", padx=5)
        self.entry_registration_number = ttk.Entry(profile_frame, width=20)
        self.entry_registration_number.grid(row=0, column=3, sticky="w")

        # Row 1
        ttk.Label(profile_frame, text="Address:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.entry_address = ttk.Entry(profile_frame, width=40)
        self.entry_address.grid(row=1, column=1, sticky="w")

        ttk.Label(profile_frame, text="Phone:").grid(row=1, column=2, sticky="e", padx=5)
        self.entry_phone = ttk.Entry(profile_frame, width=20)
        self.entry_phone.grid(row=1, column=3, sticky="w")

        # Row 2
        ttk.Label(profile_frame, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.entry_email = ttk.Entry(profile_frame, width=40)
        self.entry_email.grid(row=2, column=1, sticky="w")

        ttk.Label(profile_frame, text="Age:").grid(row=2, column=2, sticky="e", padx=5)
        self.entry_age = ttk.Entry(profile_frame, width=20)
        self.entry_age.grid(row=2, column=3, sticky="w")

        # Row 3
        ttk.Label(profile_frame, text="Profession:").grid(row=3, column=0, sticky="e", padx=5, pady=3)
        self.entry_profession = ttk.Entry(profile_frame, width=40)
        self.entry_profession.grid(row=3, column=1, sticky="w")

        ttk.Label(profile_frame, text="Gender:").grid(row=3, column=2, sticky="e", padx=5)
        self.entry_gender = ttk.Combobox(
            profile_frame,
            values=["Male", "Female", "Other"],
            width=18,
            state="readonly"
        )
        self.entry_gender.grid(row=3, column=3, sticky="w")
        self.entry_gender.set("Other")

        # Row 4
        ttk.Label(profile_frame, text="Notes:").grid(row=4, column=0, sticky="ne", padx=5, pady=3)
        self.entry_notes = tk.Text(profile_frame, width=60, height=3)
        self.entry_notes.grid(row=4, column=1, columnspan=3, sticky="w")

        # ---------------------------------------------------------
        # SECTION: Buttons
        # ---------------------------------------------------------
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Create", command=self.create_member).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Update selected", command=self.update_member).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete selected", command=self.delete_member).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Reset Form", command=self.reset_form).pack(side="left", padx=5)

        # ---------------------------------------------------------
        # SECTION: Members table
        # ---------------------------------------------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "full_name", "registration_number", "age", "profession", "gender", "status", "email", "phone")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())

        self.tree.column("id", width=40)
        self.tree.column("full_name", width=180)
        self.tree.column("registration_number", width=120)
        self.tree.column("age", width=50)
        self.tree.column("profession", width=120)
        self.tree.column("gender", width=80)
        self.tree.column("status", width=80)
        self.tree.column("email", width=180)
        self.tree.column("phone", width=120)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_member)

        self.refresh()

    # ---------------------------------------------------------
    # CRUD operations
    # ---------------------------------------------------------
    def refresh(self):
        self.tree.delete(*self.tree.get_children())

        for m in self.logic.list_members():  # m is MemberResponseDTO
            self.tree.insert("", "end", values=(
                m.id,
                m.full_name,
                m.registration_number,
                m.age,
                m.profession,
                m.gender,
                m.status,
                m.email,
                m.phone,
            ))

    def create_member(self):
        try:
            self.logic.add_member(
                full_name=self.entry_full_name.get(),
                registration_number=self.entry_registration_number.get(),
                address=self.entry_address.get(),
                phone=self.entry_phone.get(),
                email=self.entry_email.get(),
                age=int(self.entry_age.get()) if self.entry_age.get() else None,
                profession=self.entry_profession.get(),
                gender=self.entry_gender.get(),
                notes=self.entry_notes.get("1.0", "end").strip(),
            )
            messagebox.showinfo("Success", "Member created.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_member(self):
        try:
            selected = self.tree.selection()
            if not selected:
                raise ValueError("No member selected.")

            member_id = self.tree.item(selected[0])["values"][0]

            self.logic.update_member(
                member_id=member_id,
                full_name=self.entry_full_name.get(),
                address=self.entry_address.get(),
                phone=self.entry_phone.get(),
                email=self.entry_email.get(),
                age=int(self.entry_age.get()) if self.entry_age.get() else None,
                profession=self.entry_profession.get(),
                gender=self.entry_gender.get(),
                notes=self.entry_notes.get("1.0", "end").strip(),
            )
            messagebox.showinfo("Success", "Member updated.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_member(self):
        try:
            selected = self.tree.selection()
            if not selected:
                raise ValueError("No member selected.")

            member_id = self.tree.item(selected[0])["values"][0]
            self.logic.delete_member(member_id)
            messagebox.showinfo("Success", "Member deleted.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_form(self):
        self.entry_full_name.delete(0, "end")
        self.entry_registration_number.delete(0, "end")
        self.entry_address.delete(0, "end")
        self.entry_phone.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_age.delete(0, "end")
        self.entry_profession.delete(0, "end")
        self.entry_gender.set("Other")
        self.entry_notes.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection())

    # ---------------------------------------------------------
    # AUTO-FILL HANDLER
    # ---------------------------------------------------------
    def on_select_member(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        member_id = self.tree.item(selected[0])["values"][0]
        m = self.logic.get_member(member_id)  # m is MemberResponseDTO

        if not m:
            return

        self.entry_full_name.delete(0, "end")
        self.entry_full_name.insert(0, m.full_name)

        self.entry_registration_number.delete(0, "end")
        self.entry_registration_number.insert(0, m.registration_number)

        self.entry_address.delete(0, "end")
        self.entry_address.insert(0, m.address)

        self.entry_phone.delete(0, "end")
        self.entry_phone.insert(0, m.phone)

        self.entry_email.delete(0, "end")
        self.entry_email.insert(0, m.email)

        self.entry_age.delete(0, "end")
        self.entry_age.insert(0, m.age if m.age else "")

        self.entry_profession.delete(0, "end")
        self.entry_profession.insert(0, m.profession)

        self.entry_gender.set(m.gender)

        self.entry_notes.delete("1.0", "end")
        self.entry_notes.insert("1.0", "")  # notes removed from DTO
