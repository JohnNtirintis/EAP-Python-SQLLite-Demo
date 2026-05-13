# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from gui.Styles import *


class BookEdit(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=BG_MAIN)
        self.app = app

        #make BookEdit expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.book_edit_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.book_edit_frame.grid(row=0,column=0, sticky='nswe')

        self.book_edit_frame.grid_propagate(False)
        self.book_edit_frame.grid_columnconfigure(0, weight=1)
        self.book_edit_frame.grid_columnconfigure(1, weight=0)
        self.book_edit_frame.grid_rowconfigure(0, weight=0)
        self.book_edit_frame.grid_rowconfigure(1, weight=0)
        self.book_edit_frame.grid_rowconfigure(2, weight=0)
        self.book_edit_frame.grid_rowconfigure(3, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file= 'gui/Assets/back_btn_icon.png')
        #back button
        back_btn = tk.Button(
                            self.book_edit_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Κατάλογος Βιβλίων',
                            bd=0,
                            width=160,
                            padx=10,
                            bg= BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg= FG_MUTED,
                            font= FONT_MAIN,
                            command= lambda: self.app.change_page("Κατάλογος Βιβλίων"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0,column=0,padx=5,pady=(0,10),sticky='w')

        #page title 
        book_edit_label = tk.Label(
                            self.book_edit_frame,
                            anchor='w',
                            text='Προσθήκη Βιβλίου',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        book_edit_label.grid(row=1,column=0,padx=15, pady=(0,15), sticky='nsew')

        #add/edit button
        self.edit_button = ttk.Button(
                        self.book_edit_frame,
                        text = "ΠΡΟΣΘΗΚΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.edit_button.grid(row=3, column=0, sticky='e',padx=5,pady=5)

        #delete button
        self.delete_button = ttk.Button(
                        self.book_edit_frame,
                        text = "ΔΙΑΓΡΑΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.delete_button.grid(row=3, column=1, sticky='e',padx=(5,15),pady=5)

        #container for book data
        container = tk.Frame(
                    self.book_edit_frame,
                    bd=0,
                    bg= BG_CARD,
                    height=400,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_rowconfigure(3, weight=1)
        container.grid_rowconfigure(4, weight=1)
        container.grid_rowconfigure(4, weight=1)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)

        self.entries = {}

        # =========================================
        # Labels function
        # =========================================
        def create_labels(row,text):
            field_lbl = tk.Label(
                    container,
                    anchor = "ne",
                    text= text,
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_MUTED,
                    font= FONT_BOLD
                    )
            field_lbl.grid(row=row, column=0, sticky='w',padx=(15,0),pady=5)
        
        # =========================================
        # Entries function
        # =========================================
        def create_entries(row):
            entry_box = ttk.Entry(
                    container,
                    font = FONT_MAIN,
                    width=50,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    validate='focusout'
                    )
            entry_box.grid(row=row, column=1, sticky='w',padx=20,pady=5)
            
            return entry_box

        #entry labels
        entry_labels = ["Τίτλος:","Συγγραφέας:","Έτος έκδοσης:","ISBN:",
                        "Κατηγορία:","Απόθεμα"]
        
        keys = ["title","author","year","isbn","category_name","copies"]
        #loop for entry labels with corresponding text
        for i,text in enumerate(entry_labels):
            row = i
            create_labels(row,text)
        for i in range(4):
            row=i
            current_key = keys[i]
            entry = create_entries(row)
            self.entries[current_key] = entry
        
        self.category_var = tk.StringVar()
        #category list
        self.cat_list = ttk.Combobox(
                        container,
                        state="readonly",
                        font=FONT_MAIN,
                        width=40,
                        values=categoriesdata,
                        textvariable=self.category_var,
                        style="CustomCombobox.TCombobox"
                        )
        self.cat_list.grid(row=4, column=1, sticky="w", padx=20, pady=5)

        self.copies_var = tk.IntVar(value=0)
        #stock spinbox
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
            buttondownrelief = 'flat',
            buttonuprelief = 'flat',
            exportselection=False,
            insertbackground=ACCENT_DARK,
            repeatdelay=150,
            repeatinterval=50
            )
        self.stock.grid(row=5, column=1, sticky="w",padx=20, pady=5,ipady=2)

    def reset(self):
        #clear entries
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        #clear combobox & spinbox
        self.category_var.set("")
        self.copies_var.set(0)

    # =========================================
    # Prefill Fields function
    # =========================================
    def prefill(self,b):

        self.entries["title"].delete(0, tk.END)
        self.entries["title"].insert(0, b.get("title", ""))

        self.entries["author"].delete(0, tk.END)
        self.entries["author"].insert(0, b.get("author", ""))

        self.entries["year"].delete(0, tk.END)
        self.entries["year"].insert(0, str(b.get("published_year") or ""))

        self.entries["isbn"].delete(0, tk.END)
        self.entries["isbn"].insert(0, b.get("isbn", ""))

        # category
        self.category_var.set(b["category_name"])
        # stock
        self.copies_var.set(b["total_copies"])




# Dummy categories
categoriesdata = [
    "Μυθιστόρημα",
    "Φαντασία",
    "Αστυνομικό",
    "Δράμα",
    "Περιπέτεια",
    "Παιδικό",
]