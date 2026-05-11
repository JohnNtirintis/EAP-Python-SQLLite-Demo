#import GUI package
import tkinter as tk
from tkinter import ttk
from Styles import *
from Members_Page import Members
from Dashboard_Page import autosize_content


class Recommend(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=BG_MAIN)
        self.app = app

        #make Recommend expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.recommend_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.recommend_frame.grid(row=0,column=0, sticky='nswe')

        self.recommend_frame.grid_propagate(False)
        self.recommend_frame.grid_columnconfigure(0, weight=1)
        self.recommend_frame.grid_rowconfigure(0, weight=0)
        self.recommend_frame.grid_rowconfigure(1, weight=0)
        self.recommend_frame.grid_rowconfigure(2, weight=0)
        self.recommend_frame.grid_rowconfigure(3, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file= 'back_btn_icon.png')
        #back button
        back_btn = tk.Button(
                            self.recommend_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Μέλη',
                            bd=0,
                            width=60,
                            padx=10,
                            bg= BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg= FG_MUTED,
                            font= FONT_MAIN,
                            command= lambda: self.app.change_page("Μέλη"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0,column=0,padx=5,pady=(0,10),sticky='w')

        self.loan_button = ttk.Button(
                        self.recommend_frame,
                        text = "ΔΑΝΕΙΣΜΟΣ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.loan_button.grid(row=3, column=0, sticky='e',padx=(5,15),pady=5)

        #recommend title 
        recommend_label = tk.Label(
                            self.recommend_frame,
                            anchor='w',
                            text='Πρόταση Επόμενου Βιβλίου',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        recommend_label.grid(row=1,column=0,padx=15, pady=(0,15), sticky='nsew')

        #container
        container = tk.Frame(
            self.recommend_frame,
            bg = BG_CARD,
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


        self.title_text = tk.StringVar()
        
        #table title
        table_title = tk.Label(
                        container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_SUBHEADER_BOLD,
                        textvariable = self.title_text
                        )
        table_title.grid(row=0, column=0, sticky='w',padx=(15,0),pady=(10,15))

        #table
        columns=("Τίτλος","Συγγραφέας","Έτος έκδοσης","ISBN","Κατηγρία","Βαθμολογία")
        self.recommend_table = ttk.Treeview(
                    container,
                    columns=columns,
                    show="headings",
                    selectmode='browse',
                    style="Custom.Treeview"
                    )
        self.recommend_table.grid(row=1, column=0, sticky='nsew',padx=15,pady=(0,5))

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.recommend_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.grid(row=2, column=0, sticky='we',padx=(15,0))
        self.recommend_table.config(xscrollcommand=h_scrollbar.set)

        #headers & columns
        for col in columns:
            self.recommend_table.heading(col, text=col, anchor='w')
            self.recommend_table.column(col, 
                                anchor="w", 
                                width=200, 
                                minwidth=200,
                                stretch=True)
        
        #populate data
        for r in datarecommend:
            self.recommend_table.insert("","end", values=r)

        #call autosizing function
        autosize_content(self.recommend_table)
        

    #clear changes
    def reset(self):
        self.member = self.app.pages[Members].selected_values
        self.title_text.set(f"Για το μέλος {self.member[1]} {self.member[2]} προτείνουμε:")

#dummy data
datarecommend=[
    ("Η Σκιά του Ανέμου", "Κάρλος Ρουίθ Θαφόν", "2001", "9789604530476", "Μυθιστόρημα", "4.8"),
    ("Το Όνομα του Ρόδου", "Ουμπέρτο Έκο", "1980", "9789604065435", "Ιστορικό", "4.7"),
    ("Ο Γέρος και η Θάλασσα", "Έρνεστ Χέμινγουεϊ", "1952", "9789602081239", "Κλασική Λογοτεχνία", "4.5"),
    ("1984", "Τζορτζ Όργουελ", "1949", "9789605171235", "Δυστοπία", "4.9"),
    ("Η Φάρμα των Ζώων", "Τζορτζ Όργουελ", "1945", "9789605171242", "Αλληγορία", "4.6")
]
