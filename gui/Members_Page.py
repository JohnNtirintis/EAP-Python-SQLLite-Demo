# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk, font
from gui.Styles import *
from gui.Dashboard_Page import autosize_content
from datetime import *


class Members(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=BG_MAIN)
        self.app = app

        #make Members expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        

        #frame creation and grid config
        self.member_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.member_frame.grid(row=0,column=0, sticky='nswe')

        self.member_frame.grid_columnconfigure(0, weight=1)
        self.member_frame.grid_rowconfigure(0, weight=0)
        self.member_frame.grid_rowconfigure(1, weight=1,minsize=200)
        self.member_frame.grid_rowconfigure(2, weight=0)
        self.member_frame.grid_rowconfigure(3, weight=1,minsize=200)

        #profile title 
        profile_label = tk.Label(
                            self.member_frame,
                            anchor='w',
                            text='Μέλη',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        profile_label.grid(row=0,column=0,padx=15, pady=(5,10), sticky='nsew')

        #table title
        table_title = tk.Label(
                            self.member_frame,
                            anchor='w',
                            text='Λίστα Μελών',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        table_title.grid(row=2,column=0,padx=15, pady=(5,10), sticky='nsew')
        
        self.entries = {}
        self.create_members_profile()
        self.create_members_table()

    #=========================================
    #Members' Profile function
    #=========================================
    def create_members_profile(self):

        container = tk.Frame(
                    self.member_frame,
                    bd=0,
                    bg= BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=1, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_rowconfigure(3, weight=1)
        container.grid_rowconfigure(4, weight=1)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)
        container.grid_columnconfigure(3, weight=1)
        container.grid_columnconfigure(4, weight=1)

        #title
        title_lbl = tk.Label(
                        container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_SUBHEADER_BOLD,
                        text = "Προφίλ μέλους:"
                        )
        title_lbl.grid(row=0,column=0,sticky='w',padx=(15,0),pady=10)

        #=========================================
        #Entries function
        #=========================================
        def create_entries(row,col,text):
            entry_lbl = tk.Label(
                    container,
                    anchor = "ne",
                    text= text,
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_MUTED,
                    font= FONT_BOLD
                    )
            entry_lbl.grid(row=row, column=col*2, sticky='w',padx=(15,0),pady=5)

            entry_box = ttk.Entry(
                    container,
                    font = FONT_MAIN,
                    style="CustomEntry.TEntry",
                    exportselection=False,
                    validate='focusout'
                    )
            entry_box.grid(row=row, column=col*2+1, sticky='ew',padx=5,pady=5)
            
            return entry_box

        # =========================================
        # Buttons function
        # =========================================
        def create_buttons(row,text):
            profile_btn = ttk.Button(
                        container,
                        text = text,
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
            profile_btn.grid(row=row+1, column=4, sticky='e',padx=(5,15),pady=5)
            return profile_btn


        #entry labels
        entry_labels = ["Όνομα:","Επώνυμο:","Φύλλο:","Ημ/νία Γέννησης:",
                        "Email:","Τηλέφωνο:","Διεύθυνση:"]
        
        #loop for entry labels with corresponding text
        for i,text in enumerate(entry_labels):
            col = i // 4
            row = i % 4 +1

            key = text.replace(":","").lower()
            entry = create_entries(row,col,text)
            self.entries[key] = entry

        btn_labels = ("ΔΗΜΙΟΥΡΓΙΑ","ΑΝΑΝΕΩΣΗ","ΠΡΟΤΑΣΗ ΒΙΒΛΙΟΥ","ΚΑΘΑΡΙΣΜΟΣ")

        for row,text in enumerate(btn_labels):
            btn = create_buttons(row,text)
            if text == "ΔΗΜΙΟΥΡΓΙΑ":
                self.save_button = btn
            elif text == "ΑΝΑΝΕΩΣΗ":
                self.status_button = btn
                self.status_button.state(['disabled'])
            elif text == "ΠΡΟΤΑΣΗ ΒΙΒΛΙΟΥ":
                self.suggestion_button = btn
                self.suggestion_button.config(command= lambda: self.app.change_page("Πρόταση Βιβλίου"))
                self.suggestion_button.state(['disabled'])
            if text == "ΚΑΘΑΡΙΣΜΟΣ":
                self.clear_button = btn
                self.clear_button.state(['disabled'])
                self.clear_button.config(command= self.reset)


    #=========================================
    #Members' Table function
    #=========================================
    def create_members_table(self):
        #container
        container = tk.Frame(
                    self.member_frame,
                    bd=0,
                    bg= BG_CARD,
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
        columns=("ID","Όνομα","Επώνυμο","Φύλλο","Ημ/νία Γέννησης","Email",
                 "Τηλέφωνο","Διεύθυνση","Ημ/νία Εγγραφής","Λήξη Εγγραφής","Κατάσταση")
        self.members_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.members_table.grid(row=0, column=0, sticky='nsew',padx=(0,5),pady=(0,5))
        
        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=self.members_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.members_table.config(yscrollcommand=v_scrollbar.set)

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.members_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2,0.5)
        h_scrollbar.grid(row=1, column=0, sticky='we')
        self.members_table.config(xscrollcommand=h_scrollbar.set)


        #headings & column width & alignment
        for col in columns:
            self.members_table.heading(col, text=col, anchor='w')
            self.members_table.column(col, 
                                anchor="w", 
                                stretch=False,
                                minwidth=80 if col in ("ID","Φύλλο","Κατάσταση") else 150,
                                )


        #dummy data
        members = [
            ("0001", "Γιώργος", "Ανδρέου", "Άνδρας", "14/03/1992",
            "g.andreou92@example.com", "6945123456", "Αθηνάς 12, Αθήνα",
            "10/01/2025", "10/01/2026", "Ενεργό"),

            ("0002", "Μαρία", "Παπαδοπούλου", "Γυναίκα", "22/07/1988",
            "m.papadopoulou88@example.com", "6978456123", "Σόλωνος 45, Αθήνα",
            "03/11/2024", "03/11/2025", "Ενεργό"),

            ("0003", "Αντώνης", "Κυριακίδης", "Άνδρας", "05/12/1995",
            "antonis.kyr@example.com", "6982234511", "Ερμού 78, Πειραιάς",
            "18/02/2025", "18/02/2026", "Ενεργό"),

            ("0004", "Ελένη", "Γεωργίου", "Γυναίκα", "30/09/1999",
            "eleni.geo99@example.com", "6947788991", "Κηφισίας 102, Μαρούσι",
            "01/03/2025", "01/03/2026", "Ενεργό"),

            ("0005", "Νίκος", "Σταματίου", "Άνδρας", "17/01/1985",
            "nikos.stam@example.com", "6933344556", "Θησέως 5, Καλλιθέα",
            "20/05/2024", "20/05/2025", "Ανενεργό"),

            ("0006", "Άννα", "Λαμπροπούλου", "Γυναίκα", "11/04/1993",
            "anna.lam93@example.com", "6971122334", "Πατησίων 210, Αθήνα",
            "10/04/2025", "10/04/2026", "Ενεργό"),

            ("0007", "Πέτρος", "Μανιάτης", "Άνδρας", "08/06/1990",
            "petros.maniatis@example.com", "6956677889", "Αγίου Κωνσταντίνου 9, Πειραιάς",
            "14/09/2024", "14/09/2025", "Ανενεργό"),

            ("0008", "Σοφία", "Καραμήτρου", "Γυναίκα", "27/02/2000",
            "sofia.karam@example.com", "6989001122", "Μεσογείων 150, Χολαργός",
            "25/01/2025", "25/01/2026", "Ενεργό"),

            ("0009", "Χρήστος", "Δημητρίου", "Άνδρας", "19/10/1987",
            "x.dimitriou87@example.com", "6945566778", "Αχαρνών 33, Αθήνα",
            "01/12/2024", "01/12/2025", "Ενεργό"),

            ("0010", "Ιωάννα", "Στεργίου", "Γυναίκα", "03/08/1996",
            "ioanna.sterg@example.com", "6977008899", "Φιλελλήνων 20, Αθήνα",
            "12/03/2025", "12/03/2026", "Ενεργό")
            ]
        
        for m in members:
            self.members_table.insert("", "end", values=m)

        #call autosizing function
        autosize_content(self.members_table)

        #call selection-to-entry-table function
        self.members_table.bind("<<TreeviewSelect>>", lambda e: self.selection_to_entry())
        self.selection_to_entry()

    #=========================================
    #Table Selection to Entry function
    #=========================================
    def selection_to_entry(self):
        entries = self.entries
        members_table = self.members_table

        #get selection items
        selected = members_table.selection()
        
        if not selected:
            self.save_button.config(text="ΔΗΜΙΟΥΡΓΙΑ")
            self.clear_button.state(['disabled'])
            self.status_button.config(text="ΑΝΑΝΕΩΣΗ")
            self.status_button.state(['disabled'])
            self.suggestion_button.state(['disabled'])
            return
        
        #clear entry boxes
        self.clear_entries()

        values = members_table.item(selected, 'values')
        self.selected_values = values

        #change btn text
        self.save_button.config(text="ΕΝΗΜΕΡΩΣΗ")
        if values[10] == "Ενεργό":
            self.status_button.config(text='ΤΕΡΜΑΤΙΣΜΟΣ')
        else:
            self.status_button.config(text='ΑΝΑΝΕΩΣΗ')

        #output to entry boxes
        mapping = [
            "όνομα",
            "επώνυμο",
            "φύλλο",
            "ημ/νία γέννησης",
            "email",
            "τηλέφωνο",
            "διεύθυνση"]
        
        for i,key in enumerate(mapping, start=1):
            entries[key].insert(0,values[i])

        #change btn status
        self.clear_button.state(['!disabled'])
        self.status_button.state(['!disabled'])
        self.suggestion_button.state(['!disabled'])
        
        return values

    #=========================================
    #Clear Entry Text function
    #=========================================
    def clear_entries(self):
        entries = self.entries

        for entry in entries.values():
            entry.delete(0,'end')

    #=========================================
    #Reset Entries & Selection on Page Change
    #=========================================    
    def reset(self):
        self.clear_entries()
        self.members_table.selection_set(())





