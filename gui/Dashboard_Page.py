#import GUI package
import tkinter as tk
from tkinter import ttk


import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as datetime
import pandas as pd


# ─── colour & font constants (match all other pages) ─────────────────────────
BG_MAIN = "#D9D9D9"
BG_CARD = "#EAEAEA"
SIDEBAR_BG_DARK = "#353535"
SIDEBAR_BG_DARKER = "#242424"
SIDEBAR_BG_HIGHLIGHT = "#282828"
SIDEBAR_FG_HIGHLIGHT = "#00D5E4"
SIDEBAR_FG = "#CCCCCC"
FG_DARK_BODY = "#1E1E1E"
FG_MUTED_HEADERS = "#5E5E5E"
BUTTON_BG = "#059CA7"
FONT_MAIN  = ("Segoe UI", 12)
FONT_BOLD  = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 18)
FONT_SMALL = ("Segoe UI", 10)
plt.rcParams["font.family"] = "Segoe UI"

class Dashboard(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg= BG_MAIN)
        
        # make Dashboard expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.controller = controller

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
        self.dashboardData_frame.grid_rowconfigure(1, weight=1,minsize=300)
        self.dashboardData_frame.grid_rowconfigure(2, weight=1,minsize=200)

        #images
        self.books_icon = tk.PhotoImage(file= 'books_icon.png')
        self.loaned_books_icon = tk.PhotoImage(file= 'loaned_books_icon.png')
        self.members_icon = tk.PhotoImage(file= 'members_icon.png')
        
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

    #create  dashboard data function
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
                    fg= FG_MUTED_HEADERS,
                    font= ("Segoe UI", 14)
                    )
        data_lbl.grid(row=0, column=1, sticky='e', padx=(0,20), pady=(10,0))

        #create value label
        data_value = tk.Label(
                    container,
                    anchor = "ne",
                    text= data["value"],
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_DARK_BODY,
                    font= ("Segoe UI", 20)
                    )
        data_value.grid(row=1, column=1, sticky='e', padx=(0,20), pady=(0,10))

    def create_overdue_table(self):
        #container
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg = BG_CARD,
                    height=200,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=3, padx=15, pady=(10,0), sticky='nsew')
        container.grid_propagate(False)

        #table title
        table_title = tk.Label(
                            container,
                            anchor = "center",
                            bg=BG_CARD,
                            fg=FG_MUTED_HEADERS,
                            bd=0,
                            font = ("Segoe UI", 18),
                            text = "Οφειλές"
                            )
        table_title.pack(side='top',anchor='w',padx=15, pady=5)


        #table
        columns=("ID","Μέλος","Βιβλίο","ISBN","Καθυστέρηση","Ημ/νία Επιστροφής")
        overdue_table = ttk.Treeview(container,
                                columns=columns,
                                show="headings",
                                selectmode='browse',
                                style="Custom.Treeview"
                                )
        
        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=overdue_table.yview,
                        style="Dashboard.Vertical.TScrollbar"
                        )
        v_scrollbar.set(0.2,0.5)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(35,0))
        overdue_table.config(yscrollcommand=v_scrollbar.set)


        #headings & column width & alignment
        for col in columns:
            overdue_table.heading(col, text=col, anchor='w')
            overdue_table.column(col, 
                                anchor="w", 
                                width=150 if col != "ID" else 80, 
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
            overdue_table.insert("", "end", values=r)


        overdue_table.pack(fill='both', expand=True)


    def create_figure(self):  
        
        #dummy data
        data = {'dates': ["04-27","04-28","04-29","04-30","05-1","05-2","05-3"],
                'y': [6,8,3,6,9,8,4]
                }   

        dataframe = pd.DataFrame(data)
        
        #container
        container = tk.Frame(
                    self.dashboardData_frame,
                    bg = BG_CARD,
                    height=350
                    )
        container.grid(row=1, columnspan=3, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)

        #figure creation
        figure = plt.Figure(figsize=(5,1), dpi=100,frameon=False)
        figure_plot = figure.add_subplot(1,1,1)
        
        #config spines (colour, width, visibility)
        figure_plot.spines.right.set_visible(False)
        figure_plot.spines.top.set_visible(False)
        figure_plot.spines.left.set_linewidth(0.5)
        figure_plot.spines.bottom.set_linewidth(0.5)
        figure_plot.spines.bottom.set_color(SIDEBAR_BG_DARK)
        figure_plot.spines.left.set_color(SIDEBAR_BG_DARK)

        
        figure_plot.axes.grid(axis='y',color = FG_MUTED_HEADERS, linewidth = 0.5)
        #adjust padding
        figure.subplots_adjust(top=0.75, bottom=0.15, left=0.08, right=0.95)
        
        #title
        figure_plot.set_title('Δανεισμοί',
                            x=-0.06,
                            y=1.1,
                            fontdict={'fontsize': 18,
                                    'color': FG_MUTED_HEADERS,
                                    'verticalalignment': 'center',
                                    "horizontalalignment" : 'left' },
                            loc='left',
                            pad=10
                            )

        #plot bg color        
        figure_plot.set_facecolor(BG_CARD)
        
        #figure to widget
        line_graph = FigureCanvasTkAgg(figure,container)
        widget = line_graph.get_tk_widget()
        widget.configure(bg=BG_CARD)
        widget.pack(fill='both', expand=True)

        dataframe.plot(kind='line',legend=False, ax=figure_plot, linewidth = 2, linestyle = '-',color= SIDEBAR_FG_HIGHLIGHT)

