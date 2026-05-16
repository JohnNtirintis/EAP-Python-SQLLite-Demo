# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox

from gui.Styles import *
from gui.Loans_Page import Loans


class Rating(tk.Frame):
    def __init__(self, parent, app, service=None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        # Loan being returned. Populated in reset() from Loans page.
        self._loan_id = None
        # Book info string for display
        self._book_info = ""

        #make Rating expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.rating_frame = tk.Frame(
                            self,
                            bg=BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.rating_frame.grid(row=0, column=0, sticky='nswe')

        self.rating_frame.grid_propagate(False)
        self.rating_frame.grid_columnconfigure(0, weight=1)
        self.rating_frame.grid_rowconfigure(0, weight=0)
        self.rating_frame.grid_rowconfigure(1, weight=1)
        self.rating_frame.grid_rowconfigure(2, weight=1)
        self.rating_frame.grid_rowconfigure(3, weight=0)
        self.rating_frame.grid_rowconfigure(4, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file='gui/Assets/back_btn_icon.png')
        back_btn = tk.Button(
                            self.rating_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Δανεισμός Βιβλίων',
                            bd=0,
                            width=160,
                            padx=10,
                            bg=BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg=FG_MUTED,
                            font=FONT_MAIN,
                            command=lambda: self.app.change_page("Δανεισμός Βιβλίων"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0, column=0, padx=5, pady=(0, 10), sticky='w')

        #rating title - now shows the book being rated
        self.title_text = tk.StringVar(value='Βαθμολόγησε το Βιβλίο:')
        rating_label = tk.Label(
                            self.rating_frame,
                            anchor='center',
                            textvariable=self.title_text,
                            bd=0,
                            bg=BG_MAIN,
                            fg=FG_MUTED,
                            font=FONT_TITLE_BOLD
                            )
        rating_label.grid(row=1, column=0, pady=(30, 15))

        #submit button (returns the loan + saves rating)
        self.submit_button = ttk.Button(
                        self.rating_frame,
                        text="ΥΠΟΒΟΛΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.submit_rating,
                        )
        self.submit_button.grid(row=4, column=0, sticky='e', padx=15, pady=130)

        #skip-rating button (just returns without rating)
        self.skip_button = ttk.Button(
                        self.rating_frame,
                        text="ΕΠΙΣΤΡΟΦΗ ΧΩΡΙΣ ΒΑΘΜΟΛΟΓΙΑ",
                        width=32,
                        style="CustomButton.TButton",
                        cursor='hand2',
                        command=self.submit_no_rating,
                        )
        self.skip_button.grid(row=4, column=0, sticky='w', padx=15, pady=130)

        #rating entry
        self.rating_var = tk.DoubleVar()
        self.rating_entry = ttk.Entry(
                self.rating_frame,
                font=FONT_TITLE_BOLD,
                width=5,
                justify='center',
                style="CustomEntry.TEntry",
                textvariable=self.rating_var,
                exportselection=False,
                )
        self.rating_entry.grid(row=3, column=0, pady=20)
        self.rating_var.trace_add("write", lambda *args: self.star_update())

        #rating text
        max_label = tk.Label(
                        self.rating_frame,
                        text="/ 5",
                        anchor='e',
                        bd=0,
                        bg=BG_MAIN,
                        fg=FG_DARK,
                        font=FONT_TITLE_BOLD
                        )
        max_label.grid(row=3, column=0, padx=(140, 0), pady=20)

        #Stars Canvas
        self.star_empty = tk.PhotoImage(file="gui/Assets/star_empty.png")
        self.star_full  = tk.PhotoImage(file="gui/Assets/star_full.png")
        self.star_half  = tk.PhotoImage(file="gui/Assets/star_half.png")

        self.star_canvas = tk.Canvas(
                        self.rating_frame,
                        bd=0,
                        highlightthickness=0,
                        bg=BG_MAIN,
                        height=120,
                        width=700
                        )
        self.star_canvas.grid(row=2, column=0)

        self.stars = []
        x_pos = 100 // 2
        y_pos = 96 // 2
        for i in range(5):
            img = self.star_canvas.create_image(x_pos, y_pos,
                                                image=self.star_empty,
                                                anchor='center')
            self.stars.append(img)
            x_pos += 150

    # =========================================
    # Star helpers
    # =========================================
    def set_star(self, index, state):
        if state == "full":
            img = self.star_full
        elif state == "half":
            img = self.star_half
        else:
            img = self.star_empty
        self.star_canvas.itemconfig(self.stars[index], image=img)

    def star_update(self):
        try:
            rating = float(self.rating_var.get())
        except tk.TclError:
            rating = 0.0

        for i in range(5):
            self.set_star(i, "empty")

        rating = max(0.0, min(5.0, rating))
        full_stars = int(rating)
        has_half = (rating - full_stars) >= 0.5
        if not has_half:
            # treat any non-zero remainder under 0.5 as no half
            pass

        for i in range(full_stars):
            self.set_star(i, 'full')
        if has_half and full_stars < 5:
            self.set_star(full_stars, 'half')

    # =========================================
    # ΥΠΟΒΟΛΗ - return book with rating
    # =========================================
    def submit_rating(self):
        if not self.service or self._loan_id is None:
            messagebox.showwarning("Σφάλμα",
                                   "Δεν έχει επιλεγεί δανεισμός προς επιστροφή.")
            return
        try:
            rating = float(self.rating_var.get())
        except (tk.TclError, ValueError):
            messagebox.showwarning("Άκυρη τιμή",
                                   "Δώστε βαθμολογία μεταξύ 1 και 5.")
            return

        rating_int = int(round(rating))
        if rating_int < 1 or rating_int > 5:
            messagebox.showwarning("Άκυρη τιμή",
                                   "Η βαθμολογία πρέπει να είναι 1 έως 5.")
            return

        try:
            self.service.return_book(self._loan_id, rating=rating_int)
            messagebox.showinfo("Επιτυχία",
                                "Η επιστροφή και η βαθμολογία καταχωρήθηκαν.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return

        self._loan_id = None
        self.app.change_page("Δανεισμός Βιβλίων")

    # =========================================
    # Skip rating - just return the loan
    # =========================================
    def submit_no_rating(self):
        if not self.service or self._loan_id is None:
            return
        try:
            self.service.return_book(self._loan_id)
            messagebox.showinfo("Επιτυχία", "Η επιστροφή καταχωρήθηκε.")
        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
            return
        self._loan_id = None
        self.app.change_page("Δανεισμός Βιβλίων")

    # =========================================
    # Reset Entries on Page Change
    # =========================================
    def reset(self):
        self.rating_var.set(0.0)
        self.star_update()

        #pick up the loan from Loans page
        loans_page = self.app.pages.get(Loans) if hasattr(self.app, "pages") else None
        loan_id = getattr(loans_page, "pending_return_loan_id", None) if loans_page else None
        if loan_id is None:
            self._loan_id = None
            self.title_text.set("Επιλέξτε πρώτα δανεισμό προς επιστροφή.")
            self.submit_button.state(['disabled'])
            self.skip_button.state(['disabled'])
            return

        self._loan_id = loan_id
        # consume the pending loan id so navigating back-and-forth doesn't re-use it
        if loans_page is not None:
            loans_page.pending_return_loan_id = None

        # try to fetch the loan details for display
        try:
            loans = self.service.list_loans() if self.service else []
        except Exception:
            loans = []
        loan = next((l for l in loans if getattr(l, "id", None) == loan_id), None)
        if loan is not None:
            self.title_text.set(
                f"Βαθμολόγησε το βιβλίο: '{getattr(loan, 'book_title', '')}'"
            )
        else:
            self.title_text.set("Βαθμολόγησε το Βιβλίο:")

        self.submit_button.state(['!disabled'])
        self.skip_button.state(['!disabled'])
