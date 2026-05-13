# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from gui.Styles import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as datetime
import pandas as pd


class Dashboard(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg= BG_MAIN)
        self.app = app

        #make Dashboard expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #frame creation and grid config 
        self.dashboardData_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx = 30,
                            pady = 20
                            )
        self.dashboardData_frame.grid(row=0, column=0, sticky='nsew')
        
        self.dashboardData_frame.grid_columnconfigure(0, weight=1)
        self.dashboardData_frame.grid_columnconfigure(1, weight=1)
        self.dashboardData_frame.grid_columnconfigure(2, weight=1)
        self.dashboardData_frame.grid_rowconfigure(0, weight=0)
        self.dashboardData_frame.grid_rowconfigure(1, weight=1,minsize=200)
        self.dashboardData_frame.grid_rowconfigure(2, weight=1,minsize=200)

        #images
        self.books_icon = tk.PhotoImage(file= 'gui/Assets/books_icon.png')
        self.loaned_books_icon = tk.PhotoImage(file= 'gui/Assets/loaned_books_icon.png')
        self.members_icon = tk.PhotoImage(file= 'gui/Assets/members_icon.png')
        
        #data info list
        dashboard_data_info = [
                        {"icon": self.books_icon, "label": "Συνολικά Βιβλία", "value": 235},
                        {"icon": self.members_icon, "label": "Συνολικά Μέλη", "value": 75},
                        {"icon": self.loaned_books_icon, "label": "Δανεισμένα Βιβλία", "value": 17}
                        ]
        
        #create loop of data info with corresponding img/text/value
        for col, item in enumerate(dashboard_data_info):
            self.create_dashboard_card(col,item)
        
        self.create_figure()
        
        self.create_overdue_table()

    #=========================================
    #Dashboard Data function
    #=========================================
    def create_dashboard_card(self,col,data):
        
        #container
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg = BG_CARD
                    )
        container.grid(row=0, column=col, padx=15, pady=(5,10), sticky='nsew')
        
        #container grid config
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)

        
        #create icon
        data_icon = tk.Label(
                    container,
                    anchor = "w",
                    image= data["icon"],
                    bg = BG_CARD
                    )
        
        data_icon.grid(rowspan=2, column=0, sticky='w', padx=(20,5))

        #create text label
        data_lbl = tk.Label(
                    container,
                    anchor = "ne",
                    text= data["label"],
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_MUTED,
                    font= FONT_SUBHEADER
                    )
        data_lbl.grid(row=0, column=1, sticky='e', padx=(0,20), pady=(10,0))

        #create value label
        data_value = tk.Label(
                    container,
                    anchor = "ne",
                    text= data["value"],
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_DARK,
                    font= ("Segoe UI", 20)
                    )
        data_value.grid(row=1, column=1, sticky='e', padx=(0,20), pady=(0,10))

    #=========================================
    #Overdue Table function
    #=========================================
    def create_overdue_table(self):
        #container
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg = BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=3, padx=15, pady=(10,0), sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        #table title
        table_title = tk.Label(
                        container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_TITLE,
                        text = "Οφειλές"
                        )
        table_title.grid(row=0, column=0, sticky='w',padx=(15,0),pady=10)
        
        self.return_btn = ttk.Button(
                        container,
                        text = "ΕΠΙΣΤΡΟΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2',
                        command= lambda: self.app.change_page("Βαθμολογία")
                        )
        self.return_btn.grid(row=0, column=1, sticky='e',padx=(0,15),pady=10)
        self.return_btn.state(['disabled'])

        #table
        columns=("ID","Μέλος","Βιβλίο","ISBN","Καθυστέρηση","Ημ/νία Επιστροφής")
        self.overdue_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.overdue_table.grid(row=1, column=0,columnspan=2, sticky='nsew',padx=(15,), pady=(0,5))
        self.overdue_table.bind("<<TreeviewSelect>>", lambda e: self.selection_btn())

        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=self.overdue_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=1, column=3, sticky='ns')
        self.overdue_table.config(yscrollcommand=v_scrollbar.set)

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.overdue_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2,0.5)
        h_scrollbar.grid(row=2, column=0, columnspan=2, sticky='we',padx=(15,0))
        self.overdue_table.config(xscrollcommand=h_scrollbar.set)


        #headings & column width & alignment
        for col in columns:
            self.overdue_table.heading(col, text=col, anchor='w')
            self.overdue_table.column(col, 
                                anchor="w", 
                                width=120 if col != "ID" else 80, 
                                minwidth=150 if col != "ID" else 80,
                                stretch=True if col != "ID" else False)

        #dummy data
        rows = [
            ("0001", "Γιώργος Ανδρέου", "Άμλετ", "965-322-12-6668-1", "3 ημέρες", "19/03/2026"),
            ("0002", "Άννα Γεωργίου", "Ιλιάδα", "975-452-02-5556-7", "7 ημέρες", "15/03/2026"),
            ("0003", "Μαρία Παπαδοπούλου", "Οδύσσεια", "978-123-45-6789-0", "1 ημέρα", "27/04/2026"),
            ("0004", "Γιώργος Ανδρέου", "Άμλετ", "965-322-12-6668-1", "3 ημέρες", "19/03/2026"),
            ("0005", "Άννα Γεωργίου", "Ιλιάδα", "975-452-02-5556-7", "7 ημέρες", "15/03/2026"),
            ("0006", "Μαρία Παπαδοπούλου", "Οδύσσεια", "978-123-45-6789-0", "1 ημέρα", "27/04/2026")
            ]
        for r in rows:
            self.overdue_table.insert("", "end", values=r)

        autosize_content(self.overdue_table)

    #=========================================
    #Figure function
    #=========================================
    def create_figure(self):  
        
        #dummy data
        data = {'dates': ["04-27","04-28","04-29","04-30","05-1","05-2","05-3"],
                'y': [6,8,3,6,9,8,4]
                }   

        dataframe = pd.DataFrame(data)
        
        #container
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg = BG_CARD
                    )
        container.grid(row=1, columnspan=3, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)

        #figure creation
        figure = plt.Figure(figsize=(5,1), dpi=100,frameon=False)
        figure_plot = figure.add_subplot(1,1,1)
        
        #config spines (colour, width, visibility) & ticks' color
        figure_plot.spines.right.set_visible(False)
        figure_plot.spines.top.set_visible(False)
        figure_plot.spines.left.set_linewidth(0.5)
        figure_plot.spines.bottom.set_linewidth(0.5)
        figure_plot.spines.bottom.set_color(BG_DARK)
        figure_plot.spines.left.set_color(BG_DARK)
        figure_plot.tick_params('both',colors=BG_DARK)

        #grid
        figure_plot.axes.grid(axis='y',color = MPL_GRID, linewidth = 0.5)
        
        #adjust padding
        figure.subplots_adjust(top=0.75, bottom=0.15, left=0.08, right=0.95)
        
        #title
        figure_plot.set_title('Δανεισμοί',
                            x=-0.06,
                            y=1.1,
                            fontdict={'fontsize': 18,
                                    'color': MPL_TEXT,
                                    'verticalalignment': 'center',
                                    "horizontalalignment" : 'left' },
                            loc='left',
                            pad=10
                            )

        #plot bg color        
        figure_plot.set_facecolor(MPL_BG)
        
        #figure to widget
        line_graph = FigureCanvasTkAgg(figure,container)
        widget = line_graph.get_tk_widget()
        widget.configure(bg=MPL_BG)
        widget.pack(fill='both', expand=True)

        dataframe.plot(kind='line',legend=False, ax=figure_plot, linewidth = 2, linestyle = '-',color= ACCENT)

    #=========================================
    #Table Selection to Button State function
    #=========================================
    def selection_btn(self):
        overdue_table = self.overdue_table

        #get selection
        selected = overdue_table.selection() 
        if not selected:
            self.return_btn.state(['disabled'])   
        else:
            self.return_btn.state(['!disabled'])

    #=========================================
    #Reset selection function
    #=========================================
    def reset(self):
        self.overdue_table.selection_set(())
    
#=========================================
#Autosize Table Column Width Based On Content function
#=========================================
def autosize_content(treeview):
    tree_font = tk.font.Font(font=FONT_BOLD)
            
    for col in treeview["columns"]:
        max_width = tree_font.measure(col) + 30

        for item in treeview.get_children():
            cell_text = treeview.set(item,col)
            cell_width = tree_font.measure(str(cell_text)) +30
            if cell_width > max_width:
                max_width = cell_width

        treeview.column(col, width = max_width, minwidth=max_width)
