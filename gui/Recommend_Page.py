# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox

from gui.Styles import *
from gui.Members_Page import Members
from gui.Dashboard_Page import autosize_content


class Recommend(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service
        self.member = None  # populated in reset()

        #make Recommend expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.recommend_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.recommend_frame.grid(row=0, column=0, sticky='nswe')

        self.recommend_frame.grid_propagate(False)
        self.recommend_frame.grid_columnconfigure(0, weight=1)
        self.recommend_frame.grid_rowconfigure(0, weight=0)
        self.recommend_frame.grid_rowconfigure(1, weight=0)
        self.recommend_frame.grid_rowconfigure(2, weight=0)
        self.recommend_frame.grid_rowconfigure(3, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file='gui/Assets/back_btn_icon.png')
        back_btn = tk.Button(
                            self.recommend_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Μέλη',
                            bd=0,
                            width=60,
                            padx=10,
                            bg=BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg=FG_MUTED,
                            font=FONT_MAIN,
                            command=lambda: self.app.change_page("Μέλη"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0, column=0, padx=5, pady=(0, 10), sticky='w')

        self.loan_button = ttk.Button(
                        self.recommend_frame,
                        text="ΔΑΝΕΙΣΜΟΣ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.loan_recommended,
                        )
        self.loan_button.grid(row=3, column=0, sticky='e', padx=(5, 15), pady=5)
        self.loan_button.state(['disabled'])

        recommend_label = tk.Label(
                            self.recommend_frame,
                            anchor='w',
                            text='Πρόταση Επόμενου Βιβλίου',
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE
                            )
        recommend_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky='nsew')

        #container
        container = tk.Frame(
                    self.recommend_frame,
                    bg=BG_CARD,
                    height=300,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, column=0, padx=15, pady=30, sticky='nsew')
        container.grid_propagate(False)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)

        self.title_text = tk.StringVar(value="Επιλέξτε πρώτα ένα μέλος από τη σελίδα 'Μέλη'.")

        #table title
        table_title = tk.Label(
                        container,
                        anchor="center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font=FONT_SUBHEADER_BOLD,
                        textvariable=self.title_text,
                        )
        table_title.grid(row=0, column=0, sticky='w', padx=(15, 0), pady=(10, 15))

        #table
        columns = ("ID", "Τίτλος", "Συγγραφέας", "Έτος έκδοσης",
                   "ISBN", "Κατηγορία", "Score")
        self.recommend_table = ttk.Treeview(
                    container,
                    columns=columns,
                    show="headings",
                    selectmode='browse',
                    style="Custom.Treeview"
                    )
        self.recommend_table.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 5))
        self.recommend_table.bind("<<TreeviewSelect>>",
                                  lambda e: self._update_loan_btn())

        h_scrollbar = ttk.Scrollbar(
                        container,
                        orient='horizontal',
                        command=self.recommend_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.grid(row=2, column=0, sticky='we', padx=(15, 0))
        self.recommend_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.recommend_table.heading(col, text=col, anchor='w')
            self.recommend_table.column(col,
                                anchor="w",
                                width=200,
                                minwidth=120,
                                stretch=True)

    # =========================================
    # Loan button activation
    # =========================================
    def _update_loan_btn(self):
        if self.recommend_table.selection() and self.member is not None:
            self.loan_button.state(['!disabled'])
        else:
            self.loan_button.state(['disabled'])

    # =========================================
    # Borrow the selected recommended book
    # =========================================
    def loan_recommended(self):
        if not self.service or self.member is None:
            return
        sel = self.recommend_table.selection()
        if not sel:
            return
        book_id = int(sel[0])
        try:
            self.service.borrow_book(self.member["id"], book_id)
            messagebox.showinfo("Επιτυχία", "Ο δανεισμός καταχωρήθηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return
        # refresh recommendations - the borrowed book should no longer appear
        self._populate_recommendations()

    # =========================================
    # Fetch & populate recommendations
    # =========================================
    def _populate_recommendations(self):
        #clear current rows
        for item in self.recommend_table.get_children():
            self.recommend_table.delete(item)

        if not self.service or self.member is None:
            return

        try:
            recs = self.service.recommend_books(self.member["id"], limit=10)
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        for r in recs:
            book = r.book
            self.recommend_table.insert(
                "", "end",
                iid=str(book.id),
                values=(
                    f"{book.id:04d}",
                    book.title,
                    book.author,
                    book.published_year or "",
                    book.isbn,
                    book.category_name,
                    f"{r.score:.2f}",
                ),
            )
        autosize_content(self.recommend_table)

    # =========================================
    # Reset Content on Page Change
    # =========================================
    def reset(self):
        #safely pull the currently-selected member from the Members page
        members_page = self.app.pages.get(Members) if hasattr(self.app, "pages") else None
        member_id = getattr(members_page, "selected_member_id", None) if members_page else None

        if not self.service or member_id is None:
            self.member = None
            self.title_text.set("Επιλέξτε πρώτα ένα μέλος από τη σελίδα 'Μέλη'.")
            for item in self.recommend_table.get_children():
                self.recommend_table.delete(item)
            self.loan_button.state(['disabled'])
            return

        self.member = self.service.get_member(member_id)
        if not self.member:
            self.title_text.set("Το μέλος δεν βρέθηκε.")
            return

        self.title_text.set(
            f"Για το μέλος '{self.member['full_name']}' προτείνουμε:")
        self._populate_recommendations()
        self.loan_button.state(['disabled'])
