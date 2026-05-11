#import GUI package
import tkinter as tk
from tkinter import ttk, font
from Styles import *
from Dashboard_Page import autosize_content
from datetime import *


class Loans(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=BG_MAIN)

        #make Loans expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        self.app = app

        #frame creation and grid config
        self.loans_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.loans_frame.grid(row=0,column=0, sticky='nswe')

        self.loans_frame.grid_columnconfigure(0, weight=1)
        self.loans_frame.grid_columnconfigure(1, weight=1)
        self.loans_frame.grid_rowconfigure(0, weight=0)
        self.loans_frame.grid_rowconfigure(1, weight=1,minsize=200)
        self.loans_frame.grid_rowconfigure(2, weight=1,minsize=200)
        self.loans_frame.grid_rowconfigure(3, weight=0)
        self.loans_frame.grid_rowconfigure(4, weight=1,minsize=200)

        #loans title 
        loans_label = tk.Label(
                            self.loans_frame,
                            anchor='w',
                            text='Δανεισμός Βιβλίων',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        loans_label.grid(row=0,column=0,padx=15, pady=(5,10), sticky='nsew')
        
        #loans button
        self.loan_button = ttk.Button(
                        self.loans_frame,
                        text = "ΔΑΝΕΙΣΜΟΣ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.loan_button.grid(row=0, column=1, sticky='e',padx=(0,15),pady=10)
        self.loan_button.state(['disabled'])

        #table title
        loans_table_title = tk.Label(
                            self.loans_frame,
                            anchor='w',
                            text='Δανεισμένα Βιβλία',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        loans_table_title.grid(row=3,column=0,padx=15, pady=(5,10), sticky='nsew')

        #return button
        self.return_button = ttk.Button(
                        self.loans_frame,
                        text = "ΕΠΙΣΤΡΟΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.return_button.grid(row=3, column=1, sticky='e',padx=(0,15),pady=10)
        self.return_button.state(['disabled'])

        ####################################
        
        self.selectbook_loan()
        self.selectmember_loan()
        self.return_table()

    def update_loan_btn(self):
        #make selection True/False
        has_book = bool(self.searchbooks_table.selection())
        has_member = bool(self.searchmember_table.selection())

        #check if both tables have selection to activate button
        if has_book and has_member:
            self.loan_button.state(['!disabled'])
        else:
            self.loan_button.state(['disabled'])

    #activate button on selection
    def update_return_btn(self,button,table):     
        selected = table.selection()
        if not selected:
            button.state(['disabled'])   
        else:
            button.state(['!disabled'])

    #select book
    def selectbook_loan(self):
        #container
        container = tk.Frame(
                    self.loans_frame,
                    bd=0,
                    bg= BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=1, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        #title
        title_lbl = tk.Label(
                        container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_SUBHEADER_BOLD,
                        text = "Επιλογή Βιβλίου:"
                        )
        title_lbl.grid(row=0,column=0,sticky='w',padx=(15,0),pady=10)

        #searchbar
        self.searchbar_book_var = tk.StringVar()
        self.searchbar_book = ttk.Entry(
                    container,
                    font = FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    textvariable=self.searchbar_book_var
                    )
        self.searchbar_book.grid(row=0, column=1, sticky='ew',padx=15,pady=10)
        #default text change on focus in/out
        self.searchbar_book_var.set("Αναζήτηση...")
        self.searchbar_book.bind("<FocusIn>", lambda e: self.remove_placeholder_var(self.searchbar_book_var))
        self.searchbar_book.bind("<FocusOut>", lambda e: self.add_placeholder_var(self.searchbar_book_var))
        #show filtered results based on query
        self.searchbar_book.bind("<Return>", lambda e: search_results(databook,self.searchbar_book_var,
                                                                    self.searchbooks_table))


        #table
        columns=("ID","Τίτλος βιβλίου","Συγγραφέας","Έτος έκδοσης","ISBN")
        self.searchbooks_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.searchbooks_table.grid(row=1, column=0, columnspan=2, sticky='nsew',padx=(15,5),pady=(0,5))
        #update loan_button check
        self.searchbooks_table.bind("<<TreeviewSelect>>", lambda e: self.update_loan_btn())
        #callback for table visibility
        self.searchbar_book_var.trace_add("write", lambda *args: self.table_visible(
            self.searchbar_book_var,self.searchbooks_table,v_scrollbar,h_scrollbar))

        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=self.searchbooks_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=1, column=3, sticky='ns')
        self.searchbooks_table.config(yscrollcommand=v_scrollbar.set)

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.searchbooks_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2,0.5)
        h_scrollbar.grid(row=2, column=0, columnspan=2, sticky='we',padx=(15,0))
        self.searchbooks_table.config(xscrollcommand=h_scrollbar.set)
        #headers & columns
        for col in columns:
            self.searchbooks_table.heading(col, text=col, anchor='w')
            self.searchbooks_table.column(col, 
                                anchor="w", 
                                width=120 if col != "ID" else 80, 
                                minwidth=150 if col != "ID" else 80,
                                stretch=True if col != "ID" else False)

        #call autosizing function
        autosize_content(self.searchbooks_table)

        #visible toggle
        self.table_visible(self.searchbar_book_var,self.searchbooks_table,v_scrollbar,h_scrollbar)

    def selectmember_loan(self):
        #container
        container = tk.Frame(
                    self.loans_frame,
                    bd=0,
                    bg= BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        #title
        title_lbl = tk.Label(
                        container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_SUBHEADER_BOLD,
                        text = "Επιλογή Mέλους:"
                        )
        title_lbl.grid(row=0,column=0,sticky='w',padx=(15,0),pady=10)

        #searchbar
        self.searchbar_member_var = tk.StringVar()
        self.searchbar_member = ttk.Entry(
                    container,
                    font = FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    textvariable=self.searchbar_member_var
                    )
        self.searchbar_member.grid(row=0, column=1, sticky='ew',padx=15,pady=10)
        #default text
        self.searchbar_member_var.set("Αναζήτηση...")
        #default change on focus in/out
        self.searchbar_member.bind("<FocusIn>", lambda e: self.remove_placeholder_var(self.searchbar_member_var))
        self.searchbar_member.bind("<FocusOut>", lambda e: self.add_placeholder_var(self.searchbar_member_var))
        #show filtered results based on query
        self.searchbar_member.bind("<Return>", lambda e: search_results(datamember,self.searchbar_member_var,
                                                                    self.searchmember_table))


        #table
        columns=("ID","Όνομα","Επώνυμο","Ημ/νία Γέννησης","Email","Τηλέφωνο")
        self.searchmember_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.searchmember_table.grid(row=1, column=0, columnspan=2, sticky='nsew',padx=(15,5),pady=(0,5))
        #update loan_button check
        self.searchmember_table.bind("<<TreeviewSelect>>", lambda e: self.update_loan_btn())
        #callback to searchbar for table visibility
        self.searchbar_member_var.trace_add("write", lambda *args: self.table_visible(
            self.searchbar_member_var,self.searchmember_table,v_scrollbar,h_scrollbar))
        
        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=self.searchmember_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=1, column=3, sticky='ns')
        self.searchmember_table.config(yscrollcommand=v_scrollbar.set)

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.searchmember_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2,0.5)
        h_scrollbar.grid(row=2, column=0, columnspan=2, sticky='we',padx=(15,0))
        self.searchmember_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.searchmember_table.heading(col, text=col, anchor='w')
            self.searchmember_table.column(col, 
                                anchor="w", 
                                width=120 if col != "ID" else 80, 
                                minwidth=150 if col != "ID" else 80,
                                stretch=True if col != "ID" else False)


        #call autosizing function
        autosize_content(self.searchmember_table)

        #visible toggle
        self.table_visible(self.searchbar_member_var,self.searchmember_table,v_scrollbar,h_scrollbar)

    def return_table(self):
        #container
        container = tk.Frame(
                    self.loans_frame,
                    bd=0,
                    bg= BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=4, columnspan=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)


        #table
        columns=("ID","Μέλος","Βιβλίο","ISBN","Ημ/νία Δανεισμού","Προθεσμία Επιστροφής","Κατάσταση")
        self.loans_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.loans_table.grid(row=0, column=0, sticky='nsew',padx=(15,5),pady=(0,5))
        #button status change based on selection
        self.loans_table.bind("<<TreeviewSelect>>", lambda e: self.update_return_btn(self.return_button,self.loans_table))
        self.loans_table.bind("<FocusOut>", lambda e: self.loans_table.selection_set(()))
        
        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=self.loans_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.loans_table.config(yscrollcommand=v_scrollbar.set)

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.loans_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2,0.5)
        h_scrollbar.grid(row=1, column=0, sticky='we',padx=(15,0))
        self.loans_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.loans_table.heading(col, text=col, anchor='w')
            self.loans_table.column(col, 
                                anchor="w", 
                                width=120 if col != "ID" else 80, 
                                minwidth=150 if col != "ID" else 80,
                                stretch=True if col != "ID" else False)
        #populate data
        for r in dataloans:
            self.loans_table.insert("","end", values=r)

        #call autosizing function
        autosize_content(self.loans_table)

    #placeholder for searchbar
    def add_placeholder_var(self,searchbar_var):
        if searchbar_var.get() == "":
            searchbar_var.set("Αναζήτηση...")
    def remove_placeholder_var(self,searchbar_var):
        if searchbar_var.get() == "Αναζήτηση...":    
            searchbar_var.set("")
    
    #table visbility toggle
    def table_visible(self,searchbar_var,table,scrollv,scroll_h):
        if searchbar_var.get() == "Αναζήτηση...":
            table.grid_remove()
            scrollv.grid_remove()
            scroll_h.grid_remove()
        else:
            table.grid()
            scrollv.grid()
            scroll_h.grid()


    #clear changes
    def reset(self):
        self.loans_table.selection_set(())
        self.searchbooks_table.selection_set(())
        self.searchmember_table.selection_set(())
        self.searchbar_member_var.set("Αναζήτηση...")
        self.searchbar_book_var.set("Αναζήτηση...")

def filter_books(all_books, query): #<-ειναι bussiness logic αλλα το εβαλα προσωρινα για να φαινεται το searchbar code
    query = query.lower().strip()
    return [
        row for row in all_books
        if any(query in str(cell).lower() for cell in row)
    ]

def search_results(data,searchbar_var,table):
    query = searchbar_var.get()
    results = filter_books(data, query)

    # καθαρισμός πίνακα
    for item in table.get_children():
        table.delete(item)

    # εμφάνιση νέων αποτελεσμάτων
    for row in results:
        table.insert("", "end", values=row)

#dummy data
databook = [
    ("0001", "Το Κεφάλαιο", "Καρλ Μαρξ", "1867", "978-960-348-123-4"),
    ("0002", "Η Φόνισσα", "Αλέξανδρος Παπαδιαμάντης", "1903", "978-960-03-1234-5"),
    ("0003", "Ο Μικρός Πρίγκιπας", "Antoine de Saint‑Exupéry", "1943", "978-960-567-882-1"),
    ("0004", "Ζορμπάς", "Νίκος Καζαντζάκης", "1946", "978-960-452-778-9"),
    ("0005", "Το Όνομα του Ρόδου", "Umberto Eco", "1980", "978-960-321-556-3"),
    ("0006", "1984", "George Orwell", "1949", "978-960-453-987-0"),
    ("0007", "Ο Γέρος και η Θάλασσα", "Ernest Hemingway", "1952", "978-960-221-345-2"),
    ("0008", "Η Δίκη", "Franz Kafka", "1925", "978-960-455-112-8"),
    ("0009", "Ο Άρχοντας των Δαχτυλιδιών", "J.R.R. Tolkien", "1954", "978-960-620-441-1"),
    ("0010", "Το Κορίτσι με το Τατουάζ", "Stieg Larsson", "2005", "978-960-453-778-2")
        ]

datamember = [
    ("2001", "Γιάννης", "Παπαδόπουλος", "1998-04-12", "g.papadopoulos@example.com", "6982457812"),
    ("2002", "Μαρία", "Κωνσταντίνου", "2001-11-03", "m.konstantinou@example.com", "6978823411"),
    ("2003", "Αντώνης", "Σταθάκης", "1995-02-27", "a.stathakis@example.com", "6945527810"),
    ("2004", "Ελένη", "Μανωλά", "1989-09-15", "e.manola@example.com", "6993341287"),
    ("2005", "Νίκος", "Θεοδωρίδης", "1992-06-08", "n.theodoridis@example.com", "6937812245"),
    ("2006", "Αγγελική", "Ράπτη", "2000-12-21", "a.rapti@example.com", "6981124578"),
    ("2007", "Παναγιώτης", "Λάμπρου", "1987-03-30", "p.lamprou@example.com", "6974412890"),
    ("2008", "Σοφία", "Μητροπούλου", "1999-07-19", "s.mitropoulou@example.com", "6948891234"),
    ("2009", "Κώστας", "Βασιλείου", "1990-01-05", "k.vasileiou@example.com", "6990023411"),
    ("2010", "Αναστασία", "Χατζηδάκη", "1997-10-11", "a.chatzidaki@example.com", "6957748821")
]

dataloans = [
    ("1001", "Γιάννης Παπαδόπουλος", "Ο Μικρός Πρίγκιπας", "978-960-567-882-1",
     "2025-11-12", "2025-11-26", "Ενεργό"),
    ("1002", "Μαρία Κωνσταντίνου", "Το Όνομα του Ρόδου", "978-960-321-556-3",
     "2025-10-03", "2025-10-17", "Καθυστερημένο"),
    ("1003", "Αντώνης Σταθάκης", "1984", "978-960-453-987-0",
     "2025-11-01", "2025-11-15", "Ενεργό"),
    ("1004", "Ελένη Μανωλά", "Η Φόνισσα", "978-960-03-1234-5",
     "2025-09-20", "2025-10-04", "Επιστράφηκε"),
    ("1005", "Νίκος Θεοδωρίδης", "Ζορμπάς", "978-960-452-778-9",
     "2025-11-05", "2025-11-19", "Ενεργό"),
    ("1006", "Αγγελική Ράπτη", "Ο Άρχοντας των Δαχτυλιδιών", "978-960-620-441-1",
     "2025-10-28", "2025-11-11", "Καθυστερημένο"),
    ("1007", "Παναγιώτης Λάμπρου", "Η Δίκη", "978-960-455-112-8",
     "2025-11-10", "2025-11-24", "Ενεργό"),
    ("1008", "Σοφία Μητροπούλου", "Το Κεφάλαιο", "978-960-348-123-4",
     "2025-08-14", "2025-08-28", "Επιστράφηκε"),
    ("1009", "Κώστας Βασιλείου", "Ο Γέρος και η Θάλασσα", "978-960-221-345-2",
     "2025-11-03", "2025-11-17", "Ενεργό"),
    ("1010", "Αναστασία Χατζηδάκη", "Το Κορίτσι με το Τατουάζ", "978-960-453-778-2",
      "2025-10-15", "2025-10-29", "Καθυστερημένο")
    ]   
